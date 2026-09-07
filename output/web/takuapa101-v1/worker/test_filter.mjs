/* Local dry run: fetch the real feeds and show what stage 1 keeps and drops. */
import { GOOGLE_NEWS_QUERIES } from './src/sources.js';
import { ruleFilter, normalise } from './src/filter.js';

function tag(xml, name) {
  const m = xml.match(new RegExp('<' + name + '[^>]*>([\\s\\S]*?)</' + name + '>'));
  return m ? normalise(m[1].replace(/<!\[CDATA\[|\]\]>/g, '')) : '';
}

const kept = [];
const dropped = {};
const seenLinks = new Set();

for (const q of GOOGLE_NEWS_QUERIES) {
  const url = 'https://news.google.com/rss/search?q=' + encodeURIComponent(q) + '&hl=th&gl=TH&ceid=TH:th';
  let xml;
  try {
    const r = await fetch(url, { headers: { 'User-Agent': 'takuapa101-news/1.0' } });
    xml = await r.text();
  } catch (e) {
    console.log('ERR', q, e.message);
    continue;
  }
  for (const raw of xml.split('<item>').slice(1)) {
    const block = raw.split('</item>')[0];
    const item = {
      title: tag(block, 'title'),
      link: tag(block, 'link'),
      date: tag(block, 'pubDate'),
      outlet: tag(block, 'source'),
      summary: normalise(tag(block, 'description')).slice(0, 400),
    };
    if (!item.title || !item.link || seenLinks.has(item.link)) continue;
    seenLinks.add(item.link);
    const v = ruleFilter(item);
    if (v.ok) kept.push({ ...item, ...v });
    else (dropped[v.reason.split(':')[0]] ||= []).push(item.title.slice(0, 62));
  }
}

kept.sort((a, b) => b.score - a.score);
console.log('ดึงมาทั้งหมด (ไม่ซ้ำลิงก์):', seenLinks.size);
console.log('ผ่านด่าน 1:', kept.length);
console.log('\n--- ผ่าน 12 อันดับแรก ---');
for (const k of kept.slice(0, 12)) {
  console.log(`  [${k.score}] ${(k.place_id || '-').padEnd(17)} ${k.outlet.slice(0, 14).padEnd(15)} ${k.title.slice(0, 62)}`);
}
console.log('\n--- ตัดออก แยกตามเหตุผล ---');
for (const [reason, list] of Object.entries(dropped).sort((a, b) => b[1].length - a[1].length)) {
  console.log(`  ${reason} · ${list.length} ข่าว`);
  for (const t of list.slice(0, 3)) console.log(`      ${t}`);
}
