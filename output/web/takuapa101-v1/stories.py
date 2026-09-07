"""Evidence-led story pages for Takuapa 101.

The copy in this module is deliberately qualified: historical uncertainty is
shown to readers instead of being silently flattened into a definitive claim.
"""
from html import escape
from pathlib import Path
import json
import glob
import os

# ---- Photo registry guard ----
# Nothing renders a photograph unless the registry says that photo depicts this
# subject. A caption always comes from the registry, never from the page that is
# placing it, so a picture cannot be relabelled to fit a heading.
_PHOTO_REG = None


def photo_for(subject, file=None, era=None):
    """Return a renderable photo dict for this subject, or None."""
    global _PHOTO_REG
    import json as _j, os as _o
    if _PHOTO_REG is None:
        fp = _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), 'data', 'photo-registry.json')
        try:
            reg = _j.load(open(fp, encoding='utf-8'))
        except Exception:
            reg = {'photos': []}
        _PHOTO_REG = {p['file']: p for p in reg.get('photos', [])}
    if file:
        p = _PHOTO_REG.get(file)
        return p if p and subject in p.get('allowed_on', []) else None
    for p in _PHOTO_REG.values():
        if subject in p.get('allowed_on', []) and (era is None or p.get('era') == era):
            return p
    return None


ROOT = Path(__file__).parent
AUDIT_DIR = ROOT / "research" / "2026-09-07-history"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "onep-html": {"title": "เมืองเก่าตะกั่วป่า", "publisher": "สำนักงานนโยบายและแผนทรัพยากรธรรมชาติและสิ่งแวดล้อม (สผ.)", "url": "https://culturalenvi.onep.go.th/site/detail/4428", "locator": "หน้าเว็บหัวข้อเมืองเก่าตะกั่วป่า", "authority": "official"},
    "onep-pdf": {"title": "เอกสารเมืองเก่าตะกั่วป่า", "publisher": "สผ.", "url": "https://nced.onep.go.th/opendata/2568/oldtown36_announce/takuapa.pdf", "locator": "PDF หน้า 11–13, 55–56, 58", "authority": "official"},
    "finearts-thungtuk": {"title": "ทุ่งตึกเมืองท่าการค้าโบราณ", "publisher": "กรมศิลปากร", "url": "https://www.finearts.go.th/architecture/view/35708-ทุ่งตึกเมืองท่าการค้าโบราณ", "locator": "บทความแหล่งโบราณคดีทุ่งตึก", "authority": "official"},
    "sac-wall": {"title": "ฐานข้อมูลแหล่งโบราณคดี: เมืองตะกั่วป่า", "publisher": "ศูนย์มานุษยวิทยาสิรินธร", "url": "https://archaeology.sac.or.th/archaeology/874", "locator": "รายการแหล่งโบราณคดีและข้อสันนิษฐานกำแพง", "authority": "official"},
    "dcp-food": {"title": "มรดกภูมิปัญญาทางวัฒนธรรมของชาติ: อาหารบาบ๋า", "publisher": "กรมส่งเสริมวัฒนธรรม", "url": "https://book.culture.go.th/newbook/ich/ich2013.pdf", "locator": "หนังสือมรดกภูมิปัญญาฯ พ.ศ. 2556 หน้า 124 (ฉบับพิมพ์) / PDF หน้า 133", "authority": "official"},
    "fda-taosor": {"title": "ข่าวลงพื้นที่ผลิตภัณฑ์เต้าส้อจังหวัดพังงา", "publisher": "สำนักงานคณะกรรมการอาหารและยา", "url": "https://dis.fda.moph.go.th/detail-newsUpdate?id=3271", "locator": "ข่าวภาคสนามปี 2568 · เต้าส้อสองชั้น", "authority": "official"},
    "dit-market": {"title": "ถนนวัฒนธรรมเมืองเก่าตะกั่วป่า", "publisher": "กรมการค้าภายใน", "url": "https://www.dit.go.th/th/market/2383/ภาคใต/พ-งงา/ถนนว-ฒนธรรมเม-องเก-าตะก-วป-า/", "locator": "ระเบียนตลาด/ย่านการค้า", "authority": "official"},
    "kuapapoh-content": {"title": "กั่วป่าโพ้ · จดหมายเหตุโครงการ", "publisher": "โครงการกั่วป่าโพ้", "url": "https://kuapapoh.pages.dev/", "locator": "content.json · ส่วน origin, events, openings (เข้าถึง 7 ก.ย. 2569)", "authority": "project-published"},
}

STORIES = [
    {
        "id": "city", "group": "รู้จักเมือง", "title": "ตะกั่วป่า เมืองริมน้ำที่ชื่อยังมีคำถาม", "dek": "จากชุมชนโบราณบนเส้นทางข้ามคาบสมุทร สู่เมืองตลาดและเมืองเหมืองแร่ · เรื่องที่ยืนยันได้และเรื่องที่ควรอ่านอย่างระมัดระวัง", "route": "/stories/city/", "sources": ["onep-html", "onep-pdf"], "places": ["riverwalk", "wat-kongkha", "governor-wall"],
        "sections": [
            ("เมืองที่เติบโตกับสายน้ำ", "แหล่งข้อมูลของ สผ. อธิบายเมืองเก่าตะกั่วป่าว่าเป็นชุมชนโบราณริมแม่น้ำตะกั่วป่า และเป็นศูนย์กลางการค้าในเส้นทางเชื่อมฝั่งทะเล การอธิบายนี้เป็นกรอบจากเอกสารทางการ ไม่ได้แปลว่าสถานที่ทุกแห่งในเมืองปัจจุบันมีอายุเท่ากัน"),
            ("ชื่อเมืองยังไม่มีข้อยุติ", "เอกสารทางการเสนอที่มาของชื่อไว้สองแนวทาง · เชื่อมโยงกับชื่อโบราณ “ตะโกลา” หรือเชื่อมโยงกับคำว่า “ตะกั่ว” และ “ป่า” เอกสารเดียวกันระบุว่ายังไม่มีหลักฐานที่ยืนยันแนวทางใดได้เด็ดขาด"),
            ("ตลาดใหญ่และการย้ายเมือง", "รายงาน สผ. เล่าลำดับเมืองตลาดใหญ่ในสมัยรัชกาลที่ 3 และการย้ายเมืองไปยังย่านย่านยาวใน พ.ศ. 2456 โดยเชื่อมโยงกับตะกอนในลำน้ำและการเดินเรือที่ลดลง · วันที่และเหตุผลนี้ควรอ้างตามรายงานต้นทางเมื่อใช้ในงานวิชาการ"),
        ],
    },
    {
        "id": "architecture", "group": "บ้านเก่าและสถาปัตยกรรม", "title": "เรือนแถว ถนน และอาคารที่จำเมืองไว้", "dek": "อ่านเมืองผ่านอาคารการค้า โรงเรียน สะพาน และร่องรอยกำแพง · แต่ละชิ้นมีระดับหลักฐานไม่เท่ากัน", "route": "/stories/architecture/", "sources": ["onep-pdf", "sac-wall"], "places": ["tao-ming", "iron-bridge", "khun-in", "governor-wall", "culture-street"],
        "sections": [
            ("เรือนแถวของย่านการค้า", "เอกสาร สผ. ระบุอาคารเรือนแถวแบบชิโน–โปรตุกีสบนถนนอุดมธาราและศรีเมืองตะกั่วป่า และเชื่อมรูปแบบย่านกับการค้าและเหมืองแร่ · นี่เป็นคำอธิบายระดับย่าน ไม่ใช่การยืนยันอายุของบ้านแต่ละหลัง"),
            ("เต๋าหมิงและสะพานเหล็ก", "รายงานเดียวกันระบุว่าโรงเรียนเต๋าหมิงสร้าง พ.ศ. 2465 ด้วยเงินของพ่อค้าจีนจากหลายเมือง และสะพานเหล็กบุญสูงสร้าง พ.ศ. 2511 โดยบริษัทจุติบุญสูง พร้อมการนำเหล็กจากเรือขุดแร่ที่เลิกใช้มาใช้ซ้ำ"),
            ("สิ่งที่ต้องแยกคำว่า ‘สร้าง’ กับ ‘ซ่อม’", "ข้อมูลของขุนอินระบุการซ่อมแซมใน พ.ศ. 2524 ขณะที่ทะเบียนสถานที่ของโครงการใช้ปี พ.ศ. 2460 เป็นปีสร้าง · สองข้อมูลนี้อาจพูดถึงคนละเหตุการณ์ จึงไม่ควรรวมเป็นปีเดียวโดยไม่อธิบาย"),
            ("กำแพงที่เป็นข้อสันนิษฐาน", "ฐานข้อมูลโบราณคดีของศูนย์มานุษยวิทยาสิรินธรใช้ถ้อยคำเชิงข้อสันนิษฐานเกี่ยวกับช่วงสร้างกำแพงเมือง ส่วนรายงาน สผ. กล่าวถึงแนวกำแพงที่สูญหายบางส่วนจากการขยายถนน · เว็บไซต์จึงแสดงเรื่องนี้เป็นหลักฐานที่ต้องอ่านพร้อมคำกำกับ"),
        ],
    },
    {
        "id": "water-trade", "group": "สายน้ำและการค้า", "title": "จากทุ่งตึกถึงแม่น้ำตะกั่วป่า", "dek": "สายน้ำไม่ได้เป็นฉากหลังของเมือง · มันคือเส้นทาง ผู้เชื่อมคน และหลักฐานที่ต้องอ่านตามแหล่งต้นทาง", "route": "/stories/water-trade/", "sources": ["finearts-thungtuk", "onep-pdf"], "places": ["riverwalk", "iron-bridge", "wat-pathum", "thung-phra"],
        "sections": [
            ("ทุ่งตึกกับเครือข่ายการค้า", "กรมศิลปากรอธิบายทุ่งตึกว่าเป็นเมืองท่าการค้าโบราณบนเส้นทางข้ามคาบสมุทร และเชื่อมโยงกับเครือข่ายการค้าทางทะเลกว้างขวาง · บทความนี้ใช้คำว่า ‘อธิบาย’ และ ‘เชื่อมโยง’ ตามระดับหลักฐานของหน้าแหล่งข้อมูล"),
            ("หัวน้ำสองฝั่งคาบสมุทร", "รายงาน สผ. กล่าวถึงการใช้ลำน้ำตะกั่วป่าเป็นเส้นทางข้ามคาบสมุทร และระบุระยะระหว่างต้นน้ำสองฝั่งโดยประมาณ · ตัวเลขนี้เป็นข้อมูลในรายงาน ไม่ใช่ระยะที่เว็บไซต์คำนวณใหม่"),
            ("เมืองริมน้ำในวันนี้", "แผนที่ประชาสัมพันธ์ของเทศบาลที่ใช้ในเว็บไซต์ช่วยให้เห็นแม่น้ำ ถนน และจุดหมายร่วมกัน ส่วนการระบุอายุหรือหน้าที่เดิมของแต่ละจุดให้ยึดหน้าสถานที่และเอกสารอ้างอิงแยกกัน"),
        ],
    },
    {
        "id": "food-people", "group": "ผู้คนและรสชาติ", "title": "รสชาติของชุมชนบาบ๋าและตลาดเก่า", "dek": "อาหารเป็นทั้งความทรงจำของครัวเรือนและหลักฐานของการแลกเปลี่ยน · อ่านเมนูอย่างเคารพแหล่งที่มา", "route": "/stories/food-people/", "sources": ["dcp-food", "fda-taosor", "dit-market"], "places": ["food-center", "culture-street"],
        "sections": [
            ("ตะกั่วป่าในแผนที่อาหารบาบ๋า", "หนังสือมรดกภูมิปัญญาทางวัฒนธรรมของกรมส่งเสริมวัฒนธรรมระบุชื่อตะกั่วป่าไว้ในกลุ่มชุมชนอาหารบาบ๋า–เปอรานากัน · การอ้างนี้บอกถึงบริบททางวัฒนธรรม ไม่ได้ยืนยันว่าร้านหรือเมนูทุกรายการมีสูตรเดียวกัน"),
            ("เต้าส้อสองชั้น", "เอกสารภาคสนามของสำนักงานคณะกรรมการอาหารและยากล่าวถึงเต้าส้อสองชั้นของจังหวัดพังงาและการรับรองผลิตภัณฑ์บางรายการ · เว็บไซต์ไม่เติมชื่อผู้ผลิต ราคา หรือเวลาขายที่ไม่ได้อยู่ในเอกสาร"),
            ("ตลาดเป็นพื้นที่ของการพบกัน", "ระเบียนของกรมการค้าภายในใช้เป็นหลักฐานประกอบเรื่องย่านตลาดและการค้าบนถนนศรีเมืองตะกั่วป่าและอุดมธารา · รายชื่อร้านในเมนู ‘กินและของฝาก’ ยังคงเป็นรายชื่อจากเอกสารเทศบาล จึงควรตรวจสอบสถานะก่อนเดินทาง"),
            ("ศิวรา คาเฟ่ในระบบเรื่องเล่า", "ศิวรา คาเฟ่เป็นผู้จัดทำตะกั่วป่า 101 และอยู่ในหมวดเครื่องดื่มของเว็บไซต์เพื่อให้ผู้อ่านแยกบทบาทผู้จัดทำออกจากข้อมูลประวัติศาสตร์ได้ชัดเจน · ข้อมูลการเปิดบริการและเมนูให้ตรวจจากเว็บไซต์ของร้านโดยตรง"),
        ],
    },
]

KUAPAPOH = {"id": "kuapapoh", "group": "กระทู้เมือง", "title": "กั่วป่าโพ้ · เมืองที่กลับมาเล่าเรื่องตัวเอง", "dek": "ประวัติความเป็นมา แนวคิดพื้นที่สร้างสรรค์ และบันทึกการจัดงานที่ผ่านมา จากข้อมูลโครงการกั่วป่าโพ้", "route": "/stories/kuapapoh/", "sources": ["kuapapoh-content"], "places": ["tao-ming", "culture-street", "riverwalk"], "sections": [
    ("กั่วป่าโพ้คืออะไร", "ข้อมูลโครงการอธิบายกั่วป่าโพ้ในฐานะโครงการพื้นที่สร้างสรรค์ย่านเมืองเก่าตะกั่วป่า เชื่อมบ้านเลขที่ 78, 109 และ 305 กับนิทรรศการ งานออกแบบ และกิจกรรมของชุมชน · ข้อนี้เป็นคำอธิบายจากเจ้าของโครงการ ไม่ใช่การประกาศสถานะจากหน่วยงานรัฐ"),
    ("ที่มาของคำว่า ‘โพ้’", "content.json ของโครงการอธิบายคำว่า “กั่วป่าโพ้” ว่าใช้เรียกตะกั่วป่าในบริบทชุมชนจีนฮกเกี้ยน และเชื่อมความหมายกับตลาดหรือท่าเรือ · เรื่องที่มาของชื่อเมืองตะกั่วป่าในงานประวัติศาสตร์ยังมีหลายสมมติฐาน จึงไม่ควรใช้คำอธิบายโครงการแทนข้อยุติทางวิชาการ"),
    ("การจัดงานที่บันทึกไว้", "ข้อมูลกิจกรรมที่ตรวจได้ระบุการจัดนิทรรศการ “มนต์เสน่ห์เปอรานากัน · Still Becoming” ในเดือนกันยายน 2569 ที่ 78 สตูดิโอ ถนนวัฒนธรรมตะกั่วป่า โดยระบุศิลปิน Tinnapop Ngansathin และมีภาพนิทรรศการประกอบในโครงการ"),
    ("งานที่ผ่านมาและสิ่งที่ยังต้องตรวจซ้ำ", "หน้าโครงการบันทึกกิจกรรมเปิดพื้นที่ของบ้าน 78, 109 และ 305 รวมถึงเวิร์กช็อปและนิทรรศการ แต่ไม่ได้เป็นปฏิทินราชการย้อนหลังที่ยืนยันจำนวนผู้เข้าร่วมหรือผลกระทบทางเศรษฐกิจ · เว็บไซต์จึงไม่เติมตัวเลข วันเวลา หรือสถานะการจัดงานที่ไม่มีหลักฐาน"),
]}

def get_all_stories():
    stories_dict = {s['id']: s for s in STORIES + [KUAPAPOH]}
    for fp in glob.glob(os.path.join(ROOT, 'data', 'stories', '*.json')):
        try:
            sd = json.load(open(fp, encoding='utf-8'))
            if 'id' in sd:
                stories_dict[sd['id']] = sd
        except Exception:
            pass
    order = ['city', 'architecture', 'water-trade', 'food-people', 'kuapapoh']
    result = []
    for o in order:
        if o in stories_dict:
            result.append(stories_dict[o])
            del stories_dict[o]
    for _, v in stories_dict.items():
        result.append(v)
    return result

def _source_list(ids):
    return '<ol class="story-sources">' + ''.join(f'<li><a href="{escape(SOURCES[i]["url"])}" rel="noopener">{escape(SOURCES[i]["title"])}</a> · {escape(SOURCES[i]["publisher"])} · {escape(SOURCES[i]["locator"])}</li>' for i in ids) + '</ol>'

def _place_links(ids, ctx):
    return '<div class="story-place-links">' + ''.join(f'<a href="/places/{i}/">{escape(ctx["byid"][i]["name_th"])}</a>' for i in ids if i in ctx['byid']) + '</div>'


def illustration_for(story, ctx=None, skip=()):
    """The commissioned drawing of a place this story is actually about.

    Illustrations are drawn per place, so they are always on topic. They are the
    right fallback when no photograph in the registry depicts the subject.
    """
    import os as _o
    root = _o.path.dirname(_o.path.abspath(__file__))
    for pid in (story.get('places') or []):
        if pid in skip:
            continue
        rel = f'/assets/{pid}.webp'
        if _o.path.exists(_o.path.join(root, 'site', rel.lstrip('/'))):
            name = ''
            if ctx and pid in (ctx.get('byid') or {}):
                name = ctx['byid'][pid]['name_th']
            return {'file': rel, 'caption_th': name, 'pid': pid}
    return None

def article(story, ctx):
    is_new = 'lede' in story
    if not is_new:
        sections = ''.join(f'<section><span class="chapter">หลักฐานช่วงที่ {i:02d}</span><h2>{escape(h)}</h2><p>{escape(p)}</p></section>' for i, (h, p) in enumerate(story['sections'], 1))
        return f'<div class="story-article"><div class="breadcrumbs"><a href="/">หน้าแรก</a><span>/</span><a href="/stories/">เรื่องเล่าตะกั่วป่า</a><span>/</span><span>{escape(story["group"])}</span></div><header class="story-hero"><span class="eyebrow">เรื่องเล่าตะกั่วป่า · {escape(story["group"])}</span><h1>{escape(story["title"])}</h1><p class="lead">{escape(story["dek"])}</p><p class="story-meta">ปรับปรุง 7 กันยายน 2569 · เรียบเรียงจากเอกสารทางการ · ระดับหลักฐาน: มีทั้งข้อเท็จจริงและข้อสันนิษฐาน</p></header><article class="story-prose">{sections}<aside class="evidence-note"><strong>อ่านอย่างมีหลักฐาน</strong><p>ข้อความนี้สรุปจากแหล่งที่ระบุด้านล่าง หากเป็นคำว่า “เชื่อมโยง”, “สันนิษฐาน” หรือ “ยังไม่มีข้อยุติ” เว็บไซต์คงคำกำกับไว้เพื่อไม่ทำให้ข้อสันนิษฐานกลายเป็นข้อเท็จจริง</p></aside><h2>สถานที่ที่อ่านต่อได้</h2>{_place_links(story["places"], ctx)}<h2>แหล่งข้อมูลของบทความ</h2>{_source_list(story["sources"])}</article></div>'

    meta = f'<p class="story-meta">ปรับปรุงเมื่อ {escape(story.get("updated", ""))} · เวลาอ่าน {story.get("reading_minutes", 0)} นาที</p>'
    header = f'<header class="story-hero-v2"><div class="breadcrumbs"><a href="/">หน้าแรก</a><span>/</span><a href="/stories/">เรื่องเล่าตะกั่วป่า</a><span>/</span><span>{escape(story.get("group", ""))}</span></div><span class="eyebrow">เรื่องเล่าตะกั่วป่า · {escape(story.get("group", ""))}</span><h1>{escape(story.get("title", ""))}</h1><p class="lead">{escape(story.get("dek", ""))}</p>{meta}</header>'
    
    used_images = set()
    hero_html = ''
    hp = photo_for(story.get("id"), (story.get("hero_photo") or {}).get("file"))
    if hp:
        used_images.add(hp["file"])
    if hp:
        hero_html = f'<figure class="hero-photo-v2"><img src="{escape(hp["file"])}" alt="{escape(hp.get("caption_th",""))}" loading="eager"><figcaption><span>{escape(hp.get("caption_th",""))}</span><span class="credit">{escape(hp.get("credit",""))}</span></figcaption></figure>'
    else:
        ill = illustration_for(story, ctx)
        if ill:
            used_images.add(ill["file"])
            hero_html = (f'<figure class="hero-photo-v2 is-illustration"><img src="{escape(ill["file"])}" '
                         f'alt="{escape(ill["caption_th"])}" loading="eager"><figcaption>'
                         f'<span>{escape(ill["caption_th"])}</span>'
                         f'<span class="credit">ภาพวาดประกอบ · ยังไม่มีภาพถ่ายที่ได้รับอนุญาตของเรื่องนี้</span></figcaption></figure>')
    
    lede_html = '<div class="story-lede-v2">' + ''.join(f'<p>{escape(p)}</p>' for p in story.get("lede", [])) + '</div>'
    
    toc_links = []
    sections_html = ''
    pull_quotes = story.get("pull_quotes", [])
    
    for i, sec in enumerate(story.get("sections", [])):
        h_id = f'section-{i}'
        h2 = sec.get("heading_th", "")
        toc_links.append(f'<li><a href="#{h_id}">{escape(h2)}</a></li>')
        
        sec_content = f'<h2 id="{h_id}">{escape(h2)}</h2>'
        
        sp = photo_for(story.get("id"), (sec.get("photo") or {}).get("file"))
        if sp and sp["file"] in used_images:
            sp = None
        if sp is None:
            _alt = illustration_for(story, ctx, skip=tuple(
                f.rsplit('/', 1)[-1].rsplit('.', 1)[0] for f in used_images))
            sp = None
            if _alt and _alt["file"] not in used_images:
                sp = {'file': _alt['file'], 'caption_th': _alt['caption_th'],
                      'credit': 'ภาพวาดประกอบ'}
        if sp:
            used_images.add(sp["file"])
        if sp:
            sec_content += f'<figure class="section-photo-v2"><img src="{escape(sp["file"])}" alt="{escape(sp.get("caption_th",""))}" loading="lazy"><figcaption><span>{escape(sp.get("caption_th",""))}</span><span class="credit">{escape(sp.get("credit",""))}</span></figcaption></figure>'
        
        for p in sec.get("paragraphs", []):
            sec_content += f'<p>{escape(p)}</p>'
            
        flags_html = ''
        for flag in sec.get("flags", []):
            kind = flag.get("kind", "")
            cls = "flag-unverified" if kind == "unverified" else ("flag-disputed" if kind == "disputed" else "")
            flags_html += f'<span class="story-flag-v2 {cls}">{escape(flag.get("text_th",""))}</span>'
        if flags_html:
            sec_content += f'<div class="story-flags-v2">{flags_html}</div>'
            
        sections_html += f'<section class="story-section-v2">{sec_content}</section>'
        
        if i < len(pull_quotes):
            sections_html += f'<blockquote class="pull-quote-v2"><p>{escape(pull_quotes[i])}</p></blockquote>'

    toc_html = f'<nav class="story-toc-v2 scrollspy" id="story-toc"><h2>เนื้อหาในบทความ</h2><ul class="scrollspy-nav">{"".join(toc_links)}</ul></nav>'
    
    ev = story.get("evidence_box")
    ev_html = ''
    if ev:
        items = ''
        for it in ev.get("items", []):
            st = it.get("status", "")
            items += f'<li><div class="ev-claim">{escape(it.get("claim_th",""))}</div><div class="ev-status {escape(st.lower())}">{escape(st)}</div><div class="ev-explain">{escape(it.get("explain_th",""))} <a href="{escape(it.get("source_url",""))}" target="_blank" rel="noopener">อ้างอิง ↗</a></div></li>'
        ev_html = f'<aside class="evidence-box-v2"><h3>{escape(ev.get("heading_th",""))}</h3><ul class="ev-items-v2">{items}</ul></aside>'

    places_html = ''
    if story.get("places"):
        cards = ''
        for pid in story["places"]:
            if pid in ctx["byid"]:
                pr = ctx["byid"][pid]
                pic_html = ctx["pic"](pid) if "pic" in ctx else ""
                cards += f'<div class="place-card-mini">{pic_html}<div><h4>{escape(pr["name_th"])}</h4><button class="button button-outline" data-trip-add="{escape(pid)}">เพิ่มลงทริป</button></div></div>'
        places_html = f'<section class="story-places-v2"><h2>ไปดูของจริงได้ที่ไหน</h2><div class="mini-cards-v2">{cards}</div></section>'

    unknowns = story.get("unknowns", [])
    un_html = ''
    if unknowns:
        lis = ''.join(f'<li>{escape(u)}</li>' for u in unknowns)
        un_html = f'<details class="unknowns-box-v2"><summary>ข้อมูลที่ยังหาไม่เจอ</summary><ul>{lis}</ul></details>'

    sources = story.get("sources", [])
    src_lis = ''
    for s in sources:
        if isinstance(s, dict):
            src_lis += f'<li><cite>{escape(s.get("title",""))}</cite> · {escape(s.get("publisher",""))} · {escape(s.get("locator",""))} · <a href="{escape(s.get("url",""))}" target="_blank" rel="noopener">ดูแหล่งที่มา</a> (เข้าถึง {escape(s.get("accessed",""))})</li>'
        else:
            if s in SOURCES:
                src = SOURCES[s]
                src_lis += f'<li><cite>{escape(src["title"])}</cite> · {escape(src["publisher"])} · {escape(src["locator"])} · <a href="{escape(src["url"])}" target="_blank" rel="noopener">ดูแหล่งที่มา</a></li>'
    sources_html = f'<section class="story-sources-v2"><h2>แหล่งข้อมูล</h2><ol>{src_lis}</ol></section>'

    return f'<div class="story-article-v2">{header}{hero_html}<div class="story-layout-v2"><div class="story-main-v2">{lede_html}{sections_html}{places_html}{un_html}{sources_html}</div><div class="story-sidebar-v2">{ev_html}{toc_html}</div></div></div>'

def index(ctx):
    cards = ''
    used_art = set()
    for i, s in enumerate(get_all_stories()):
        is_new = 'reading_minutes' in s
        route = s.get('route', f'/stories/{s["id"]}/')
        mins = f'<span class="story-mins">{s["reading_minutes"]} นาที</span>' if is_new else ''
        # The index is a gallery, so every card gets the same treatment: the
        # commissioned illustration of a place the story is about. Photographs
        # stay inside the articles where a caption gives them context.
        photo = ''
        for pid in s.get("places", []):
            if pid not in used_art and os.path.exists(f"site/assets/{pid}.webp"):
                photo = f'<img src="/assets/{pid}.webp" alt="" loading="lazy">'
                used_art.add(pid)
                break
        if not photo:
            for pid in s.get("places", []):
                if os.path.exists(f"site/assets/{pid}.webp"):
                    photo = f'<img src="/assets/{pid}.webp" alt="" loading="lazy">'
                    break
        photo_html = f'<div class="card-art-v2">{photo}</div>' if photo else ''
        cls = "story-card-v2"
        if i == 0:
            cls += " story-card-v2-lead"
            
        cards += (
            f'<article class="{cls}">'
            f'{photo_html}'
            f'<div class="card-content-v2">'
            f'<span class="chapter">{escape(s["group"])}</span>'
            f'<h2><a href="{route}">{escape(s["title"])}</a></h2>'
            f'<p>{escape(s["dek"])}</p>'
            f'<div class="card-meta-v2">{mins}<span class="card-go" aria-hidden="true">เปิดเรื่องนี้ ↗</span></div>'
            f'</div></article>')
    return f'<div class="stories-index-v2"><div class="intro"><a class="eyebrow" href="/">ตะกั่วป่า 101 / คู่มือเมืองเก่า</a><h1>เรื่องเล่าตะกั่วป่า</h1><p class="lead">สี่มุมมองสำหรับอ่านเมืองผ่านแหล่งข้อมูล · รู้จักเมือง บ้านเก่าและสถาปัตยกรรม สายน้ำและการค้า ผู้คนและรสชาติ</p></div><div class="story-grid-v2">{cards}</div><aside class="source"><h2>วิธีอ่านหน้านี้</h2><p>บทความเรียบเรียงจากเอกสารราชการและฐานข้อมูลสถาบันการศึกษา พร้อมแยกระดับหลักฐานในแต่ละเรื่อง · ข้อมูลร้าน เวลาเปิด และกำหนดการควรตรวจสอบกับผู้ให้บริการก่อนเดินทาง</p></aside></div>'

def write_audit():
    claims = []
    for s in STORIES+[KUAPAPOH]:
        for n, (heading, text) in enumerate(s['sections'], 1):
            claims.append({"id": f"{s['id']}-{n}", "article_id": s['id'], "text_th": text, "status": "qualified", "source_ids": s['sources'], "notes": "ถ้อยคำคงระดับหลักฐานตามแหล่งต้นทาง"})
    audit = {"audit_date": "2026-09-07", "method": "ตรวจแหล่งราชการ/สถาบันก่อนเรียบเรียง; ไม่ใช้โพสต์สรุปเป็นแหล่งยืนยัน; แยก supported, qualified และ unverified", "sources": [{"id": k, **v, "accessed": "2026-09-07"} for k, v in SOURCES.items()], "claims": claims, "excluded_claims": ["เวลาเปิดร้าน ราคา รีวิว คะแนน และสถานะปัจจุบันที่ไม่มีแหล่งยืนยัน", "คำกล่าวเชิง superlative เช่น เล็กที่สุดหรือเก่าแก่ที่สุด", "การระบุที่ตั้งตะโกลาเป็นข้อยุติเดียว"]}
    (AUDIT_DIR/'audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
