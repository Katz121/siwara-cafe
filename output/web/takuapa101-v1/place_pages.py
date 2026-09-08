"""Phase 3 place pages, rendered solely from enriched research."""
import json
from html import escape
from pathlib import Path
import seo
from dead_sources import source_link
ROOT = Path(__file__).parent
_PHOTO_REGISTRY = None

def text(v):
    return escape(seo.clean(v)) if v is not None else ''

def badge(status):
    status = status if status in ('CONFIRMED','UNVERIFIED','DISPUTED') else 'UNKNOWN'
    return f'<span class="fact-status {status.lower()}">{dict(CONFIRMED="ยืนยันแล้ว", UNVERIFIED="ยังไม่ยืนยัน", DISPUTED="ข้อมูลขัดแย้ง", UNKNOWN="ยังไม่ยืนยัน")[status]}</span>'

def link(url, label='อ่านแหล่งอ้างอิง ↗'):
    if not url or not str(url).startswith(('https://','http://','/')): return ''
    return source_link(url, text(label))

def paragraphs(value):
    values=value if isinstance(value,list) else (value or '').split('\n\n')
    return ''.join(f'<p>{text(p)}</p>' for p in values if p)

def photo(p, eager=False, zoom=False):
    global _PHOTO_REGISTRY
    src=p.get('file') or p.get('local_path') or p.get('url')
    if _PHOTO_REGISTRY is None:
        registry = json.loads((ROOT/'data/photo-registry.json').read_text(encoding='utf-8'))
        _PHOTO_REGISTRY = {x.get('file'): x for x in registry.get('photos', [])}
    registered = _PHOTO_REGISTRY.get(src)
    caption=(registered or {}).get('caption_th') if registered else None
    caption=caption or 'ภาพจากคลังโครงการ'
    img=f'<img src="{escape(src, quote=True)}" alt="{text(caption)}" loading="{"eager" if eager else "lazy"}">'
    if zoom: img=f'<a data-lightbox href="{escape(src, quote=True)}" aria-label="ขยายภาพ · {text(caption)}">{img}</a>'
    return '<figure class="research-photo">'+img+'<figcaption>'+text(caption)+'<small>เครดิต · '+text(p.get('credit') or p.get('attribution_th') or 'ยังไม่ยืนยัน')+'</small><small>สัญญาอนุญาต · '+text(p.get('license_note_th') or p.get('license') or 'ยังไม่ยืนยัน')+'</small>'+link(p.get('page_url'),'ที่มาของภาพ ↗')+'</figcaption></figure>'

def gallery(photos):
    if not photos: return '<p class="missing-photo">ยังไม่มีภาพที่ได้รับอนุญาตให้เผยแพร่</p>'
    out='<div data-gallery><div class="gallery-tabs" hidden><button type="button" data-tab="today">ภาพวันนี้</button><button type="button" data-tab="archive">ภาพเก่า</button></div>'
    for key,label in [('today','ภาพวันนี้'),('archive','ภาพเก่า')]:
        items=[p for p in photos if (p.get('era') in ('archive','then','before'))==(key=='archive')]
        out+=f'<div id="gallery-{key}" data-panel="{key}"><h3>{label}</h3><div class="photo-grid">'+(''.join(photo(p,zoom=True) for p in items) or '<p class="muted">ยังไม่มีภาพที่ได้รับอนุญาตให้เผยแพร่ในหมวดนี้</p>')+'</div></div>'
    return out+'</div>'

def render(record,ctx,groups):
    r=seo.ENRICHED[record['id']]; rid=r['id']; photos=r.get('photos',{}).get('usable',[])
    _,category,ids=next(g for g in groups if rid in g[2])
    hero_photo=next((p for p in photos if p.get('era') in ('current','now')),photos[0] if photos else None)
    hero='<div class="breadcrumbs"><a href="/">หน้าแรก</a> / <a href="/places/">สถานที่</a> / '+text(category)+'</div><header class="place-hero full-place-hero"><div><span class="chapter">บันทึกสถานที่ · '+text(category)+'</span><h1>'+text(r['name_th'])+'</h1><p class="english">'+text(r.get('name_en'))+'</p><span class="fact-status confirmed">ยืนยันแล้ว '+str(r.get('counts',{}).get('confirmed',0))+' ข้อ</span><p><a class="text-link" href="#eras">ตอนนั้น · ก่อนหน้า · ตอนนี้ ↓</a></p><p class="place-hero-actions"><button class="button" type="button" data-trip-add="'+text(rid)+'">เพิ่มลงทริป</button><a class="text-link" href="/trip/">ดูทริปของคุณ</a></p></div><div class="place-hero-art">'+(photo(hero_photo,True) if hero_photo else ctx['pic'](rid,True))+'</div></header>'
    v=r.get('visit') or {}; c=r.get('contact') or {}; g=r.get('geo') or {}
    def field(label,value,status=None,href=None):
        content=(link(href,value) if href else text(value)) if value is not None and value!='' else '<span class="muted">ยังไม่ยืนยัน</span>'
        return '<div><dt>'+label+'</dt><dd>'+content+(' '+badge(status) if value is not None and value!='' else '')+'</dd></div>'
    facts=''
    coords=isinstance(g.get('lat'),(int,float)) and isinstance(g.get('lng'),(int,float))
    facts+=field('พิกัด',f'{g["lat"]}, {g["lng"]}' if coords else None,g.get('status'))
    if coords: facts+='<div class="directions">'+link(f'https://www.google.com/maps/search/?api=1&query={g["lat"]},{g["lng"]}','นำทางด้วย Google Maps ↗')+link(g.get('source_url'),'แหล่งพิกัด ↗')+'</div>'
    for key,label,status in [('opening_hours_th','เวลาเปิด','opening_hours_status'),('admission_fee_th','ค่าเข้า','admission_status'),('parking_th','ที่จอดรถ','parking_status'),('restroom','ห้องน้ำ','restroom_status'),('wheelchair_th','รถเข็น','wheelchair_status'),('dress_code_th','การแต่งกาย','dress_code_status')]:
        value=v.get(key)
        if isinstance(value,bool): value='มี' if value else 'ไม่มี'
        facts+=field(label,value,v.get(status))
    for key,label in [('phone','โทรศัพท์'),('facebook','เพจ'),('website','เว็บไซต์'),('line','ไลน์')]: facts+=field(label,c.get(key),c.get(key+'_status',c.get('status')),c.get(key) if key in ('facebook','website') else None)
    facts+='<div>'+''.join(link(u,'แหล่งข้อมูลการเข้าชม ↗') for u in v.get('source_urls',[]))+link(c.get('source_url'),'แหล่งข้อมูลติดต่อ ↗')+'</div>'
    practical='<aside class="visit-card" id="visit"><h2>ข้อมูลใช้จริง</h2><dl>'+facts+'</dl></aside>'
    sections=[]
    def section(key,title,content):
        sections.append((key,title,f'<section class="research-section" id="{key}"><h2>{title}</h2>{content}</section>'))
    eras='<div class="era-axis">'
    for key,label in [('then','ตอนนั้น'),('before','ก่อนหน้า'),('now','ตอนนี้')]:
        era=r.get('eras',{}).get(key) or {}
        matching=[p for p in photos if p.get('era') in (('current','now') if key=='now' else ('archive',key))]
        eras+=f'<article class="era-card" data-era="{key}"><span class="chapter">{label}</span><h3>{text(era.get("headline_th") or label)}</h3><p class="era-years">{text(era.get("years_th"))}</p>'+badge(era.get('status'))+paragraphs(era.get('body_th'))+(photo(matching[0]) if matching else '')+'<div class="era-sources">แหล่งอ้างอิง · '+ ' · '.join(link(s.get('url'),s.get('name') or 'แหล่งข้อมูล') for s in era.get('sources',[]))+'</div></article>'
    section('eras','ตอนนั้น · ก่อนหน้า · ตอนนี้',eras+'</div>')
    def year(t):
        return t.get('year_ce') if isinstance(t.get('year_ce'),(int,float)) else t['year_be']-543 if isinstance(t.get('year_be'),(int,float)) else 99999
    points=''
    for t in sorted(r.get('timeline',[]),key=year):
        date=t.get('date_th') or ('พ.ศ. '+str(t['year_be']) if t.get('year_be') else 'ค.ศ. '+str(t['year_ce']) if t.get('year_ce') else 'ไม่ระบุปี')
        points+='<li>'+badge(t.get('status'))+'<p class="era-years">'+text(date)+'</p><h3>'+text(t.get('title_th'))+'</h3>'+paragraphs(t.get('detail_th'))+link(t.get('source_url'))+'</li>'
    section('timeline','เส้นเวลาแบบจุด','<ol class="point-timeline" tabindex="0" aria-label="เส้นเวลา เลื่อนเพื่ออ่านเหตุการณ์">'+points+'</ol>')
    if photos: section('gallery','แกลเลอรี',gallery(photos))
    else: sections.append(('', '',gallery([])))
    for key,title,bodykey in [('highlights','จุดเด่นที่ควรดู','detail_th'),('news','ข่าวและความเคลื่อนไหว','summary_th'),('did_you_know','รู้หรือไม่','fact_th'),('getting_there','วิธีเดินทาง','text_th')]:
        items=r.get(key,[])
        if not items: continue
        if key=='news':items=sorted(items,key=lambda i:i.get('date') or '',reverse=True)
        cards=''
        for item in items:
            cards+='<article class="research-note">'
            if key=='news': cards+='<p class="muted">'+text(item.get('date'))+' · '+text(item.get('outlet'))+'</p>'
            titletext=item.get('title_th') or item.get('from')
            if titletext: cards+='<h3>'+text(titletext)+'</h3>'
            if key!='news' or item.get('status'):cards+=badge(item.get('status'))
            cards+=paragraphs(item.get(bodykey))+link(item.get('source_url') or item.get('url'))+'</article>'
        section(key,title,'<div class="research-cards">'+cards+'</div>')
    nearby=[]
    nearby_rows=[]
    for item in r.get('nearby',[]):
        if isinstance(item,str): nid=item
        else: nid=item.get('place_id') or item.get('id')
        if not nid and isinstance(item,dict):
            name=item.get('name_th','')
            nid=next((p['id'] for p in seo.ENRICHED.values() if name and (name==p.get('name_th') or name in (p.get('aliases_th') or []))),None)
        if nid in ctx['byid'] and nid!=rid:
            nearby.append(nid)
            nearby_rows.append('<li>'+ctx['a'](ctx['byid'][nid])+(' '+badge(item.get('status')) if isinstance(item,dict) else '')+'</li>')
        elif isinstance(item,dict):
            nearby_rows.append('<li>'+text(item.get('name_th'))+' '+badge(item.get('status'))+' '+link(item.get('source_url'))+'</li>')
    nearby=list(dict.fromkeys(nearby+[i for i in ids if i!=rid]))
    section('nearby','ที่ใกล้เคียงและสถานที่ในหมวดเดียวกัน','<ul class="nearby-links">'+''.join(nearby_rows)+''.join('<li>'+ctx['a'](ctx['byid'][i])+'</li>' for i in nearby if i not in [p for p in []] and not any(ctx['url'](ctx['byid'][i]) in row for row in nearby_rows))+'</ul>')
    import design as _d
    _note = _d.siwara_note(rid)
    if _note:
        sections.append(('nearby-note', '', _note))
    section('faq','คำถามที่พบบ่อย','<!--PLACE_FAQ-->')
    types={'official':'หน่วยงานทางการ','news':'ข่าว','blog':'บล็อก','social':'สื่อสังคม','community':'ชุมชน','project':'โครงการ','reference':'เอกสารอ้างอิง'}
    rows=''.join('<tr><th scope="row">'+text(s.get('name'))+'</th><td>'+text(types.get(s.get('type'),'แหล่งข้อมูลอื่น'))+'</td><td>'+text(s.get('accessed') or 'ยังไม่ยืนยัน')+'</td><td>'+link(s.get('url'),'เปิดแหล่ง ↗')+'</td></tr>' for s in r.get('sources',[]))
    section('sources','ที่มาของข้อมูล','<div class="source-table"><table><thead><tr><th>ชื่อ</th><th>ประเภท</th><th>วันที่เข้าถึง</th><th>ลิงก์</th></tr></thead><tbody>'+rows+'</tbody></table></div><details class="unknowns"><summary>ข้อมูลที่ยังหาไม่เจอ</summary><ul>'+''.join('<li>'+text(u)+'</li>' for u in r.get('unknowns',[]))+'</ul></details>')
    rail='<nav class="research-rail" aria-label="สารบัญหน้านี้"><span class="chapter">ในบันทึกหน้านี้</span><a href="#visit">ข้อมูลใช้จริง</a>'+''.join(f'<a href="#{k}">{title}</a>' for k,title,_ in sections if k)+'</nav>'
    return hero+'<div class="research-layout">'+practical+rail+'<div class="research-body">'+''.join(s for _,_,s in sections)+'</div></div>'

def story_gallery():
    photos=json.loads((ROOT/'data/photos-local.json').read_text(encoding='utf-8'))
    return '<section class="research-section" id="project-gallery"><h2>ภาพจากคลังโครงการกั่วป่าโพ้</h2>'+gallery([p for p in photos if p.get('place_id')=='kuapapoh' or 'kuapapoh-pattern' in p.get('file','')])+'</section>'
