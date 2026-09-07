/* Stage 2: an automatic second opinion. No human in the loop, but nothing is
   published on the rule filter alone. Uses the Claude API when a key is
   configured (best Thai), otherwise the Workers AI binding. */

const SYSTEM = `คุณคือบรรณาธิการข่าวท้องถิ่นของเว็บไกด์ "ตะกั่วป่า 101" (อำเภอตะกั่วป่า จังหวัดพังงา)
หน้าที่: ตรวจข่าวที่ผ่านตัวกรองอัตโนมัติมาแล้ว ว่าควรขึ้นเว็บหรือไม่

เกณฑ์ผ่าน (ต้องครบทุกข้อ):
1. เป็นข่าวเกี่ยวกับ "อำเภอตะกั่วป่า จังหวัดพังงา" จริง ไม่ใช่แค่เอ่ยชื่อผ่าน ๆ หรือเป็นข่าวระดับประเทศที่บังเอิญมีคำนี้
2. เป็นเรื่องที่นักท่องเที่ยวหรือคนสนใจเมืองอยากรู้ เช่น เทศกาล ประเพณี งานเมือง การบูรณะ สถานที่ เส้นทางเดินทาง วัฒนธรรม อาหาร
3. ไม่ใช่ข่าวอาชญากรรม อุบัติเหตุ การเมืองท้องถิ่นที่ขัดแย้ง โฆษณา ประกาศขาย หรือข่าวที่ทำให้เมืองเสียหาย
4. หัวข้อไม่ใช่ clickbait และเนื้อหาไม่ขัดกับตัวเอง

ตอบเป็น JSON อย่างเดียว ไม่ต้องมีข้อความอื่น:
{"verdict":"publish|hold|drop","confidence":0-100,"place_id":"<id หรือ null>","reason_th":"เหตุผลสั้น 1 ประโยค","clean_title_th":"หัวข้อที่เรียบเรียงให้อ่านง่ายขึ้น ไม่เกิน 90 ตัวอักษร ห้ามเติมข้อเท็จจริงใหม่","summary_th":"สรุป 1-2 ประโยคจากเนื้อที่ให้มาเท่านั้น ห้ามแต่งเพิ่ม"}

verdict:
- publish = มั่นใจว่าเข้าเกณฑ์ครบ
- hold = น่าจะเกี่ยว แต่ข้อมูลไม่พอตัดสิน
- drop = ไม่เข้าเกณฑ์

id สถานที่ที่เลือกได้: wat-boromthat, wat-khuha, wat-pathum, wat-kongkha, wat-nikorn, wat-sena, museum, guan-yu, pun-thao, kue-chai, rong-jae, phra-narai, thung-phra, riverwalk, culture-street, iron-bridge, governor-wall, khun-in, tao-ming, food-center, vegetarian, loy-krathong, chak-phra, new-year-alms, narai-ceremony, ruler-ceremony, relic-procession`;


function salvage(text) {
  const verdict = (text.match(/(publish|hold|drop)/i) || [])[1];
  if (!verdict) return null;
  const conf = (text.match(/confidence["'\s:]+(\d{1,3})/i) || [])[1];
  const place = (text.match(/place_id["'\s:]+["']([a-z0-9-]+)["']/i) || [])[1];
  const reason = (text.match(/reason_th["'\s:]+["']([^"']{2,120})["']/i) || [])[1];
  const title = (text.match(/clean_title_th["'\s:]+["']([^"']{2,120})["']/i) || [])[1];
  const summary = (text.match(/summary_th["'\s:]+["']([^"']{2,300})["']/i) || [])[1];
  return {
    verdict: verdict.toLowerCase(),
    confidence: conf ? Number(conf) : 60,
    place_id: place || null,
    reason_th: reason || '',
    clean_title_th: title || '',
    summary_th: summary || '',
  };
}

function parseVerdict(text) {
  try {
    // Small models wrap JSON in prose or code fences, and sometimes emit the
    // fields without braces at all. Try the strict read first, then salvage.
    const cleaned = String(text || '').replace(/```json|```/g, ' ');
    const m = cleaned.match(/\{[\s\S]*\}/);
    if (!m) return salvage(cleaned);
    let v;
    try {
      v = JSON.parse(m[0]);
    } catch (e) {
      v = salvage(cleaned);
      if (!v) return null;
    }
    if (!['publish', 'hold', 'drop'].includes(v.verdict)) return null;
    v.confidence = Math.max(0, Math.min(100, Number(v.confidence) || 0));
    return v;
  } catch (e) {
    return null;
  }
}

async function viaClaude(env, prompt) {
  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'x-api-key': env.ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model: env.RECHECK_MODEL || 'claude-haiku-4-5-20251001',
      max_tokens: 700,
      system: SYSTEM,
      messages: [{ role: 'user', content: prompt }],
    }),
  });
  if (!r.ok) throw new Error('claude ' + r.status);
  const d = await r.json();
  return (d.content || []).map((c) => c.text || '').join('');
}

async function viaWorkersAI(env, prompt) {
  const out = await env.AI.run(env.WORKERS_AI_MODEL || '@cf/meta/llama-3.3-70b-instruct-fp8-fast', {
    messages: [
      { role: 'system', content: SYSTEM },
      { role: 'user', content: prompt + '\n\nReply with JSON only, no other text.' },
    ],
    max_tokens: 700,
    temperature: 0.1,
  });
  // Workers AI answers in two shapes depending on the model: a bare
  // {response} or an OpenAI style {choices:[{message:{content}}]}.
  if (typeof out === 'string') return out;
  if (out && typeof out.response === 'string') return out.response;
  const choice = out && out.choices && out.choices[0];
  if (choice && choice.message && typeof choice.message.content === 'string') {
    return choice.message.content;
  }
  if (choice && typeof choice.text === 'string') return choice.text;
  return JSON.stringify(out);
}

/* Returns the item annotated with the review, or null when it should be dropped. */
export async function recheck(env, item) {
  const prompt = `หัวข้อ: ${item.title}\nสำนักข่าว: ${item.outlet || 'ไม่ทราบ'}\nวันที่: ${item.date || 'ไม่ทราบ'}\nลิงก์: ${item.link}\nเนื้อหาย่อ: ${item.summary || '(ไม่มี)'}\nสถานที่ที่ตัวกรองเดาไว้: ${item.place_id || 'ไม่ทราบ'}`;
  let text = '';
  try {
    text = env.ANTHROPIC_API_KEY ? await viaClaude(env, prompt) : await viaWorkersAI(env, prompt);
  } catch (e) {
    // A failed review must never publish an unreviewed item.
    return { ...item, verdict: 'hold', confidence: 0, review_error: String(e).slice(0, 120) };
  }
  const v = parseVerdict(text);
  if (!v) {
    return { ...item, verdict: 'hold', confidence: 0,
             review_error: 'อ่านคำตอบไม่ได้', raw_reply: String(text).slice(0, 400) };
  }
  return {
    ...item,
    verdict: v.verdict,
    confidence: v.confidence,
    place_id: v.place_id || item.place_id || null,
    review_reason_th: v.reason_th || '',
    title: v.clean_title_th || item.title,
    summary: v.summary_th || item.summary || '',
  };
}

/* Only a confident pass reaches the public feed. */
export function bucketOf(item, minConfidence) {
  if (item.verdict === 'publish' && item.confidence >= minConfidence) return 'live';
  if (item.verdict === 'drop') return 'dropped';
  return 'held';
}
