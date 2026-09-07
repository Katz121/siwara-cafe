/* Stage 1: rule filter. Cheap, deterministic, runs on every fetched item. */
import { REQUIRE_ANY, BLOCK_PATTERNS, OUTLET_ALLOWLIST, PLACE_KEYWORDS } from './sources.js';

export function normalise(s) {
  return (s || '').replace(/<[^>]*>/g, ' ').replace(/&[a-z]+;|&#\d+;/gi, ' ').replace(/\s+/g, ' ').trim();
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
  const base = (item.link || '') + '|' + normalise(item.title).slice(0, 90);
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(base));
  return [...new Uint8Array(buf)].slice(0, 10).map((b) => b.toString(16).padStart(2, '0')).join('');
}
