/* takuapa101-news · Cloudflare Worker
   cron  -> harvest, rule-filter, AI re-check, store in KV
   fetch -> serve the reviewed feed to the site as JSON */
import { GOOGLE_NEWS_QUERIES, DIRECT_SOURCES, FIRST_PARTY } from './sources.js';
import { ruleFilter, fingerprint, normalise } from './filter.js';
import { recheck, bucketOf } from './recheck.js';

const UA = 'takuapa101-news/1.0 (+https://siwaracafe.com/takuapa/)';
const KEY_LIVE = 'feed:live';
const KEY_HELD = 'feed:held';
const KEY_SEEN = 'seen:index';
const KEY_RUN = 'run:last';

function cors(env, request) {
  const origin = request.headers.get('Origin') || '';
  const allowed = (env.ALLOWED_ORIGINS || '').split(',').map((s) => s.trim()).filter(Boolean);
  const ok = allowed.some((a) => origin === a || origin.startsWith(a));
  return {
    'Access-Control-Allow-Origin': ok ? origin : (allowed[0] || '*'),
    'Access-Control-Allow-Methods': 'GET,OPTIONS',
    'Access-Control-Allow-Headers': 'content-type',
    'Cache-Control': 'public, max-age=600',
  };
}

function tag(xml, name) {
  const m = xml.match(new RegExp('<' + name + '[^>]*>([\\s\\S]*?)</' + name + '>'));
  return m ? normalise(m[1].replace(/<!\[CDATA\[|\]\]>/g, '')) : '';
}

function toISO(d) {
  const t = Date.parse(d);
  return Number.isNaN(t) ? '' : new Date(t).toISOString().slice(0, 10);
}

async function fetchText(url) {
  const r = await fetch(url, { headers: { 'User-Agent': UA, 'Accept-Language': 'th,en' }, cf: { cacheTtl: 300 } });
  if (!r.ok) throw new Error(url.slice(0, 60) + ' -> ' + r.status);
  return r.text();
}

async function harvestGoogleNews() {
  const out = [];
  for (const q of GOOGLE_NEWS_QUERIES) {
    const url = 'https://news.google.com/rss/search?q=' + encodeURIComponent(q) + '&hl=th&gl=TH&ceid=TH:th';
    let xml;
    try {
      xml = await fetchText(url);
    } catch (e) {
      continue;
    }
    for (const raw of xml.split('<item>').slice(1)) {
      const block = raw.split('</item>')[0];
      const title = tag(block, 'title');
      const link = tag(block, 'link');
      if (!title || !link) continue;
      out.push({
        title,
        link,
        date: toISO(tag(block, 'pubDate')),
        outlet: tag(block, 'source'),
        summary: normalise(tag(block, 'description')).slice(0, 400),
        source: 'google-news',
        query: q,
      });
    }
  }
  return out;
}

async function harvestDirect() {
  const out = [];
  for (const s of DIRECT_SOURCES.concat(FIRST_PARTY)) {
    try {
      if (s.kind === 'json') {
        const d = JSON.parse(await fetchText(s.url));
        const events = Array.isArray(d) ? d : (d.events || []);
        for (const e of events) {
          if (!e.title) continue;
          out.push({
            title: e.title,
            link: e.url || s.url,
            date: (e.date || '').slice(0, 10),
            outlet: s.name,
            summary: e.summary || '',
            source: s.id,
            authority: s.authority,
          });
        }
      } else {
        const html = await fetchText(s.url);
        const seen = new Set();
        const re = /<a[^>]+href="([^"]+)"[^>]*>([\s\S]{6,160}?)<\/a>/gi;
        let m;
        while ((m = re.exec(html))) {
          const text = normalise(m[2]);
          if (text.length < 14 || seen.has(text)) continue;
          if (!/ตะกั่วป่า|ตะโกลา/.test(text)) continue;
          seen.add(text);
          let href = m[1];
          if (href.startsWith('/')) href = new URL(s.url).origin + href;
          if (!/^https?:/.test(href)) continue;
          out.push({ title: text, link: href, date: '', outlet: s.name, summary: '', source: s.id, authority: s.authority });
          if (seen.size >= 20) break;
        }
      }
    } catch (e) {
      // one bad source must not stop the run
    }
  }
  return out;
}

async function readJSON(env, key, fallback) {
  const v = await env.NEWS.get(key, 'json');
  return (v === null || v === undefined) ? fallback : v;
}

export async function runHarvest(env) {
  const started = new Date().toISOString();
  const minConf = Number(env.MIN_CONFIDENCE || 75);
  const maxItems = Number(env.MAX_ITEMS || 60);
  const maxReviews = Number(env.MAX_REVIEWS_PER_RUN || 20);

  const fromGoogle = await harvestGoogleNews();
  const fromDirect = await harvestDirect();
  const raw = fromGoogle.concat(fromDirect);

  const seen = new Set(await readJSON(env, KEY_SEEN, []));
  const stats = { fetched: raw.length, rule_rejected: 0, already_seen: 0, reviewed: 0, live: 0, held: 0, dropped: 0 };

  const candidates = [];
  for (const item of raw) {
    const fp = await fingerprint(item);
    if (seen.has(fp)) { stats.already_seen++; continue; }
    const verdict = ruleFilter(item);
    if (!verdict.ok) { stats.rule_rejected++; seen.add(fp); continue; }
    candidates.push({ ...item, id: fp, place_id: verdict.place_id, rule_score: verdict.score });
  }
  candidates.sort((a, b) => b.rule_score - a.rule_score);

  const live = await readJSON(env, KEY_LIVE, []);
  const held = await readJSON(env, KEY_HELD, []);

  for (const c of candidates.slice(0, maxReviews)) {
    const reviewed = await recheck(env, c);
    stats.reviewed++;
    const bucket = bucketOf(reviewed, minConf);
    seen.add(c.id);
    const record = {
      id: reviewed.id,
      date: reviewed.date,
      title_th: reviewed.title,
      summary_th: reviewed.summary,
      outlet: reviewed.outlet,
      url: reviewed.link,
      place_id: reviewed.place_id,
      confidence: reviewed.confidence,
      reason_th: reviewed.review_reason_th || '',
      source: reviewed.source,
      auto: true,
      checked_at: started,
    };
    if (bucket === 'live') { live.unshift(record); stats.live++; }
    else if (bucket === 'held') { held.unshift({ ...record, verdict: reviewed.verdict, review_error: reviewed.review_error || '' }); stats.held++; }
    else { stats.dropped++; }
  }

  const byDate = (a, b) => String(b.date || '').localeCompare(String(a.date || ''));
  const trimmedLive = live.sort(byDate).slice(0, maxItems);
  const trimmedHeld = held.sort(byDate).slice(0, 80);

  await env.NEWS.put(KEY_LIVE, JSON.stringify(trimmedLive));
  await env.NEWS.put(KEY_HELD, JSON.stringify(trimmedHeld));
  await env.NEWS.put(KEY_SEEN, JSON.stringify([...seen].slice(-4000)));
  await env.NEWS.put(KEY_RUN, JSON.stringify({ started, finished: new Date().toISOString(), stats }));
  return stats;
}

export default {
  async scheduled(event, env, ctx) {
    ctx.waitUntil(runHarvest(env));
  },

  async fetch(request, env) {
    const url = new URL(request.url);
    const headers = { ...cors(env, request), 'content-type': 'application/json; charset=utf-8' };
    if (request.method === 'OPTIONS') return new Response(null, { headers });

    if (url.pathname === '/api/news') {
      const live = await readJSON(env, KEY_LIVE, []);
      const run = await readJSON(env, KEY_RUN, {});
      const limit = Math.min(Number(url.searchParams.get('limit') || 20), 60);
      return new Response(JSON.stringify({ items: live.slice(0, limit), updated: run.finished || null }), { headers });
    }
    if (url.pathname === '/api/held') {
      // Items the reviewer was not confident about. Inspectable, never rendered as news.
      const heldItems = await readJSON(env, KEY_HELD, []);
      return new Response(JSON.stringify({ items: heldItems }), { headers });
    }
    if (url.pathname === '/api/status') {
      const run = await readJSON(env, KEY_RUN, { note: 'ยังไม่เคยรัน' });
      return new Response(JSON.stringify(run), { headers });
    }
    if (url.pathname === '/api/run') {
      const key = url.searchParams.get('key');
      if (key && env.RUN_KEY && key === env.RUN_KEY) {
        const stats = await runHarvest(env);
        return new Response(JSON.stringify(stats), { headers });
      }
      return new Response(JSON.stringify({ error: 'ต้องมี key ที่ถูกต้อง' }), { status: 403, headers });
    }
    return new Response(JSON.stringify({ endpoints: ['/api/news', '/api/held', '/api/status'] }), { headers });
  },
};
