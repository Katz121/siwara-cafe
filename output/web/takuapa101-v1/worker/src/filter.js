/* Stage 1: rule filter. Cheap, deterministic, runs on every fetched item. */
import { REQUIRE_ANY, BLOCK_PATTERNS, OUTLET_ALLOWLIST, PLACE_KEYWORDS } from './sources.js';

const ENTITIES = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ' };

export function decodeEntities(s) {
  return String(s || '').replace(/&(#x?[0-9a-f]+|[a-z]+);/gi, function (m, code) {
    if (code[0] === '#') {
      const n = code[1] === 'x' || code[1] === 'X'
        ? parseInt(code.slice(2), 16)
        : parseInt(code.slice(1), 10);
      return Number.isFinite(n) ? String.fromCodePoint(n) : m;
    }
    const hit = ENTITIES[code.toLowerCase()];
    return hit === undefined ? m : hit;
  });
}

export function normalise(s) {
  return decodeEntities((s || '').replace(/<[^>]*>/g, ' ')).replace(/\s+/g, ' ').trim();
}

/* Bing hands back a click tracker, not the article. The real address sits in
   the url= parameter, percent encoded. */
export function unwrapLink(link) {
  const raw = decodeEntities(String(link || '')).trim();
  const m = raw.match(/[?&]url=([^&\s]+)/i);
  if (m) {
    try {
      const inner = decodeURIComponent(m[1]);
      if (/^https?:\/\//i.test(inner)) return inner;
    } catch (e) {
      // fall through to the raw link
    }
  }
  return raw;
}

/* Same article from two outlets, or the same outlet twice, is one story. */
export function urlKey(u) {
  try {
    const parsed = new URL(unwrapLink(u));
    return (parsed.hostname.replace(/^www\./, '') + parsed.pathname.replace(/\/+$/, '')).toLowerCase();
  } catch (e) {
    return String(u || '').slice(0, 90).toLowerCase();
  }
}

export function outletAllowed(outlet, link) {
  const hay = ((outlet || '') + ' ' + (link || '')).toLowerCase();
  return OUTLET_ALLOWLIST.some((o) => hay.includes(o.toLowerCase()));
}

export function guessPlace(text) {
  for (const [id, words] of Object.entries(PLACE_KEYWORDS)) {
    if (words.some((w) => text.includes(w))) return id;
  }
  return null;
}

/* Returns {ok, reason, place_id, score}. score 0-100 is a rough relevance hint,
   not a truth claim: stage 2 decides whether the item is publishable. */
export function ruleFilter(item) {
  const text = normalise(item.title + ' ' + (item.summary || ''));
  if (!text) return { ok: false, reason: 'ไม่มีข้อความ' };
  if (!REQUIRE_ANY.some((w) => text.includes(w))) {
    return { ok: false, reason: 'ไม่พบชื่อเมืองในข่าว' };
  }
  const blocked = BLOCK_PATTERNS.find((re) => re.test(text));
  if (blocked) return { ok: false, reason: 'อยู่ในหมวดที่ไม่รับ: ' + blocked.source.slice(0, 28) };
  if (!outletAllowed(item.outlet, item.link)) {
    return { ok: false, reason: 'สำนักข่าวไม่อยู่ในรายการที่รับ: ' + (item.outlet || '?') };
  }
  const place_id = guessPlace(text);
  let score = 40;
  if (text.includes('เมืองเก่า')) score += 20;
  if (place_id) score += 20;
  if (/เทศกาล|ประเพณี|งาน|จัดขึ้น|เปิดตัว|บูรณะ|ขึ้นทะเบียน|นิทรรศการ|เดินเมือง/.test(text)) score += 15;
  if (/เทศบาล|ททท\.|กรมศิลปากร|จังหวัดพังงา/.test(text)) score += 10;
  return { ok: true, reason: 'ผ่านกฎ', place_id, score: Math.min(score, 100) };
}

/* Stable id so the same story is never published twice. */
export async function fingerprint(item) {
  const base = urlKey(item.link || '') + '|' + normalise(item.title).slice(0, 90);
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(base));
  return [...new Uint8Array(buf)].slice(0, 10).map((b) => b.toString(16).padStart(2, '0')).join('');
}


/* Two outlets carrying the same story should appear once. Compare on a stripped
   title rather than the link, since each outlet has its own URL. */
export function titleKey(title) {
  return normalise(title)
    .replace(/[\s฀-๿]*(สยามรัฐ|มติชน|ข่าวสด|ไทยรัฐ|แนวหน้า|ผู้จัดการ|NBT|MGR).*/i, '')
    .replace(/[^0-9a-zA-Z฀-๿]/g, '')
    .slice(0, 48)
    .toLowerCase();
}
