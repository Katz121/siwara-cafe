// Serverless proxy ดึงรูปจาก Google Places (New) · key อยู่ฝั่ง server เท่านั้น (process.env.SS_GMAPS_KEY)
// เบราว์เซอร์เรียก /api/photo?name=places/XXX/photos/YYY → ไม่เห็น key เลย
export default async function handler(req, res) {
  const name = String((req.query && req.query.name) || '');
  // รับเฉพาะ resource ชื่อรูปของ Places เท่านั้น (กัน SSRF/abuse)
  if (!/^places\/[A-Za-z0-9_-]+\/photos\/[A-Za-z0-9_-]+$/.test(name)) {
    res.status(400).json({ error: 'bad name' }); return;
  }
  // อนุญาตเฉพาะ request ที่มาจากเว็บเราเอง (soft guard)
  const ref = String(req.headers.referer || req.headers.origin || '');
  if (ref && !/(^|\/\/)([a-z0-9-]+\.)?siwara\.cafe(\/|$)/i.test(ref)) {
    res.status(403).json({ error: 'forbidden' }); return;
  }
  const key = process.env.SS_GMAPS_KEY;
  if (!key) { res.status(503).json({ error: 'no key' }); return; }
  const w = Math.min(parseInt(req.query.w, 10) || 900, 1200);
  const url = `https://places.googleapis.com/v1/${name}/media?maxWidthPx=${w}&key=${key}`;
  try {
    const r = await fetch(url); // ตาม redirect ไปไฟล์รูปอัตโนมัติ
    if (!r.ok) { res.status(502).json({ error: 'upstream ' + r.status }); return; }
    const buf = Buffer.from(await r.arrayBuffer());
    res.setHeader('Content-Type', r.headers.get('content-type') || 'image/jpeg');
    res.setHeader('Cache-Control', 'public, max-age=604800, s-maxage=604800, immutable'); // cache 7 วัน ลดการเรียกซ้ำ
    res.status(200).send(buf);
  } catch (e) {
    res.status(500).json({ error: 'fetch failed' });
  }
}
