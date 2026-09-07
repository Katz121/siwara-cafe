# schema ของ data/stories/<id>.json

{
 "id": "city",
 "group": "รู้จักเมือง",
 "title": "หัวเรื่องที่ชวนอ่าน ไม่ใช่ป้ายหมวด",
 "dek": "บรรทัดสรุป 1-2 ประโยค",
 "reading_minutes": 6,
 "hero_photo": {"file":"/assets/photos/...","caption_th":"","credit":"","license":""} หรือ null,
 "lede": ["ย่อหน้าเปิดเรื่อง 1", "ย่อหน้าเปิดเรื่อง 2", "ย่อหน้าเปิดเรื่อง 3"],
 "sections": [
   {
    "heading_th": "หัวข้อตอน",
    "paragraphs": ["ย่อหน้า 1", "ย่อหน้า 2", "ย่อหน้า 3"],
    "flags": [{"text_th":"ยังไม่มีข้อยุติ","kind":"unverified|disputed"}],
    "photo": {"file":"","caption_th":"","credit":"","license":""} หรือ null,
    "source_refs": ["b-onep-report"]
   }
 ],
 "pull_quotes": ["ประโยคคมจากเนื้อเรื่องเอง"],
 "evidence_box": {
   "heading_th": "หลักฐานอยู่ตรงไหน",
   "items": [{"claim_th":"","status":"UNVERIFIED|DISPUTED","explain_th":"","source_url":""}]
 },
 "unknowns": ["สิ่งที่ยังหาไม่เจอ"],
 "places": ["riverwalk","wat-kongkha"],
 "sources": [{"id":"b-onep-report","title":"","publisher":"","url":"","locator":"หน้า 55-58","accessed":"2026-09-07"}],
 "updated": "2026-09-07"
}

ทุก paragraph เป็นข้อความล้วน ไม่มี HTML tag
