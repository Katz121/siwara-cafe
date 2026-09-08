# English prose fixes

แก้ที่ไฟล์คำแปลใน `data/i18n/en/` และสร้างใหม่ด้วย `python build_en.py` · ไม่ได้แก้ HTML ใน `site/` โดยตรง

| # | ก่อน | หลัง |
|---:|---|---|
| 1 | Through shrine doors, looking at old house windows / And know the city a bit more at every stop | Step through shrine doors and peer into old-house windows / Get to know a little more of the city at every stop |
| 2 | Short walk from wooden house | A short walk from the wooden house |
| 3 | 20 places to slowly get to know | 20 places to discover at your own pace |
| 4 | Look at the story of the Chinese community | Explore the story of the Chinese community |
| 5 | the school formally declared its intention to be established in 1920 | the school submitted a formal request to establish itself in 1920 |
| 6 | the bridge became a mining town trace | the bridge became a trace of the town's mining past |
| 7 | The bridge thus stands between functioning infrastructure and a landmark for walking, views, and photography | The bridge is both functioning infrastructure and a landmark for walks, views, and photography |
| 8 | with a Hidden Gem style | with a hidden-gem feel |
| 9 | turning it into a beautiful orange | making it glow beautifully |

ตรวจผลใน `site/en/` แล้ว: ข้อความใหม่ปรากฏจริง และข้อความเก่าทั้ง 9 จุดไม่เหลืออยู่ในหน้า HTML ที่ build ใหม่ (จุดที่ 6 ตรวจหลังแก้ไฟล์ข้อมูลหลักและ build ซ้ำ)
