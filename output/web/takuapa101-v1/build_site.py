"""Build the local Takuapa101 editorial prototype from the approved library."""
from pathlib import Path
from html import escape as esc
import json, os, sys
from datetime import date
from seo_config import SITE_BASE_URL, BASE_PATH, NEWS_API, ROBOTS
import seo
sys.stdout.reconfigure(encoding="utf-8")
import design
import stories
from PIL import Image
from fontTools import subset

ROOT = Path(__file__).parent
OUT = ROOT / 'site'
DATA = ROOT / 'data'
library = json.loads((DATA/'library.json').read_text(encoding='utf-8'))
copy = json.loads((DATA/'card-copy.json').read_text(encoding='utf-8'))
records = library['records']
byid = {r['id']: r for r in records}
places = [r for r in records if r['type']=='place']
events = [r for r in records if r['type']=='event']
shops = [r for r in records if r['type']=='business_directory']
BASE = SITE_BASE_URL
SOURCE = library['source_url']
PAGES = []
groups = [('วัด',[r['id'] for r in places if r['category']=='temple']),('ศาลเจ้าและโรงเจ',['guan-yu','pun-thao','kue-chai','rong-jae']),('ตึกเก่าและร่องรอยเมือง',['iron-bridge','governor-wall','khun-in','tao-ming']),('สวนและพื้นที่สาธารณะ',['phra-narai','thung-phra']),('ตลาด ถนน และของกิน',['riverwalk','culture-street','food-center']),('พิพิธภัณฑ์',['museum'])]
routes = [('เส้นวัดและเจดีย์',groups[0][1]),('เส้นศาลเจ้าและโรงเจ',groups[1][1]),('เส้นตึกเก่าและตลาดริมน้ำ',['tao-ming','khun-in','governor-wall','culture-street','riverwalk','food-center']), ('เดินสั้นจากบ้านไม้',['khun-in','tao-ming','guan-yu','iron-bridge'])]
links = {'narai-ceremony':['phra-narai'],'vegetarian':groups[1][1],'relic-procession':['wat-boromthat'],'chak-phra':groups[0][1],'loy-krathong':['riverwalk'],'ruler-ceremony':['governor-wall'],'culture-street':['tao-ming','khun-in','iron-bridge','food-center']}
if not (DATA/'links.json').exists(): (DATA/'links.json').write_text(json.dumps(links,ensure_ascii=False,indent=2),encoding='utf-8')
links = json.loads((DATA/'links.json').read_text(encoding='utf-8'))
# Coordinates traced from the supplied 1312 x 1872 municipal artwork, scaled to 1000 x 1400.
positions={'phra-narai':(413,261),'food-center':(493,283),'iron-bridge':(519,480),'tao-ming':(597,552),'wat-kongkha':(472,609),'pun-thao':(838,637),'khun-in':(503,766),'governor-wall':(692,775),'thung-phra':(838,786),'wat-sena':(411,898),'guan-yu':(556,930),'kue-chai':(553,1002),'wat-boromthat':(280,1027),'wat-pathum':(742,1027)}
if not (DATA/'map-points.json').exists():
 (DATA/'map-points.json').write_text(json.dumps([{'id':r['id'],'x':positions.get(r['id'],(None,None))[0],'y':positions.get(r['id'],(None,None))[1],'confidence':'from_source_map' if r['id'] in positions else 'not_on_source_map'} for r in places],ensure_ascii=False,indent=2),encoding='utf-8')
points=json.loads((DATA/'map-points.json').read_text(encoding='utf-8'))
periods={'January 1':'1 มกราคม','March-April':'มีนาคม · เมษายน','February':'กุมภาพันธ์','Chinese lunar month 9, days 1-9; usually September-October':'วันที่ 1 ถึง 9 เดือน 9 ตามปฏิทินจีน · โดยมากกันยายนถึงตุลาคม','Full moon of Thai lunar month 12; brochure mentions November':'ขึ้น 15 ค่ำ เดือน 12 · เอกสารระบุพฤศจิกายน','Day after Buddhist Lent ends':'วันถัดจากวันออกพรรษา','Makha Bucha Day':'วันมาฆบูชา'}
def period(r): return periods.get(r.get('source_period'), 'เอกสารไม่ระบุช่วงเวลา')
def url(r): return ('/places/' if r['type']=='place' else '/traditions/')+r['id']+'/'
def a(r): return f'<a href="{url(r)}">{esc(r["name_th"])}</a>'
def pic(id, eager=False):
 w,h=Image.open(OUT/f'assets/{id}.webp').size
 return f'<img src="/assets/{id}.webp" alt="{esc(byid[id]["name_th"])}" width="{w}" height="{h}" loading="{"eager" if eager else "lazy"}">'
def source(): return f'<aside class="source"><h2>ที่มาของข้อมูล</h2><p>เรียบเรียงจาก<a href="{SOURCE}">แผ่นพับเทศบาลเมืองตะกั่วป่า</a> · สกัดข้อมูล 6 กันยายน 2569 เอกสารไม่ระบุวันที่เผยแพร่ เวลาเปิด สถานะร้าน และกำหนดงานปัจจุบันยังไม่ได้ยืนยัน ควรตรวจสอบกับสถานที่ก่อนเดินทาง</p></aside>'
# Ten top level links plus four header buttons will not sit on one row, and a
# wrapped menu reads as a mistake. Six carry the site; the rest stay one tap away
# in the menu drawer and remain in the footer, so nothing becomes unreachable.
NAV_PRIMARY=[('places','สถานที่'),('stories','เรื่องเล่า'),('map','แผนที่'),('rest','กินเที่ยว'),('news','ความเคลื่อนไหว'),('trip','ทริปของคุณ')]
NAV_MORE=[('traditions','ประเพณี'),('eat','กินและของฝาก'),('routes','เส้นทางเดิน'),('leaflet','แผ่นพับ'),('about','เกี่ยวกับ')]
nav=NAV_PRIMARY+NAV_MORE
def page(path,title,desc,body,record=None):
 body = design.transform(path, body, globals(), record)
 if path == '/map/':
  title = 'แผนที่เมืองตะกั่วป่า'
  desc = 'เปิดภาพแผนที่เทศบาลเมืองตะกั่วป่า ขยายและเลื่อนดูย่านยาวกับเมืองเก่า พร้อมรายชื่อสถานที่สำหรับอ่านต่อ'
 canonical=BASE+path
 schema, body = seo.schemas(path, title, record, body)
 og_image=BASE+"/assets/og/"+(record["id"] if record else "default")+".png"
 meta={"og:title":title,"og:description":desc,"og:url":canonical,"og:type":"website","og:image":og_image,"og:locale":"th_TH","og:site_name":"ตะกั่วป่า 101","twitter:card":"summary_large_image","twitter:image":og_image}
 social="".join(f'<meta {"property" if k.startswith("og:") else "name"}="{k}" content="{esc(v)}">' for k,v in meta.items())
 def _link(slug, label, extra=''):
  cur = ' aria-current="page"' if path.startswith('/' + slug + '/') else ''
  return f'<a href="/{slug}/"{cur}{extra}>{label}</a>'
 menu = ''.join(_link(s2, l) for s2, l in NAV_PRIMARY)
 menu += ''.join(_link(s2, l, ' class="nav-more"') for s2, l in NAV_MORE)
 html=f'''<!doctype html><html lang="th" data-base="{BASE_PATH}" data-news-api="{NEWS_API}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)} · ตะกั่วป่า 101</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="{ROBOTS}">{social}<meta name="generator" content="ตะกั่วป่า 101"><link rel="canonical" href="{esc(canonical)}"><link rel="preload" href="/assets/NotoSerifThai.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/IBMPlexSansThaiLooped-Regular.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/assets/site.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('</','<\\/')}</script><script src="/assets/site.js" defer></script><script src="/assets/trip.js" defer></script>{'<script src="/assets/trip-page.js" defer></script>' if path == '/trip/' else ''}</head><body><a class="skip" href="#main">ข้ามไปเนื้อหา</a><header class="nav"><a class="brand" href="/">ตะกั่วป่า <span>101</span></a><nav id="main-nav" aria-label="เมนูหลัก">{menu}</nav></header><main id="main">{body}</main><footer><a class="brand" href="/">ตะกั่วป่า <span>101</span></a><p>เมืองเก่า เรื่องเล่า และผู้คน</p><div><a href="https://siwaracafe.com/">จัดทำโดยบ้านศิวรา ตะกั่วป่า</a><a href="{SOURCE}">แผ่นพับต้นทาง ↗</a></div></footer></body></html>'''
 html = seo.prefix_links(design.shell(path, html))
 dest=OUT/path.strip('/')/'index.html'; dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(html,encoding='utf-8');PAGES.append(path)
def intro(title,desc): return f'<div class="intro"><a class="eyebrow" href="/">ตะกั่วป่า 101 / คู่มือเมืองเก่า</a><h1>{title}</h1><p class="lead">{desc}</p></div>'
def cards(ids): return '<div class="places-grid">'+''.join(f'<article class="place"><a class="art" href="{url(byid[id])}">{pic(id)}</a><div><span class="eyebrow">{places.index(byid[id])+1:02d} / TAKUA PA</span><h3>{a(byid[id])}</h3><p>{copy[id]["kicker"]}</p></div></article>' for id in ids)+'</div>'
def directory(): return ''.join(f'<section class="category" id="category-{i}"><div class="section-heading"><h2>{label}</h2><span>{len(ids):02d} แห่ง</span></div>{cards(ids)}</section>' for i,(label,ids) in enumerate(groups))
def route_list(is_route_page=False):
 out = '<div class="route-list">'
 for i,(name,ids) in enumerate(routes,1):
  desc = '<p>เหมาะกับคนมีเวลาครึ่งวัน</p>' if i == 4 and is_route_page else ''
  out += f'<article id="route-{i}"><span class="number">0{i}</span><div><h3><a href="/routes/#route-{i}">{name} ↗</a></h3>{desc}<p>'+ ' · '.join(a(byid[id]) for id in ids)+'</p></div></article>'
 out += '</div>'
 return out
roads=[('ถนนเพชรเกษม','M 413,90 L 450,120 L 450,477 L 400,565 Q 390,655 480,680 L 600,717'),('ถนนเสนารัฐ','M 407,250 L 636,230 L 907,211'),('ถนนศรีเมือง','M 449,373 Q 600,400 781,382'),('ถนนศรีมนตรี','M 625,30 L 633,230 L 643,384'),('ถนนมนตรี 2','M 633,310 L 679,300 L 774,320'),('ถนนเสนานุชิต','M 180,891 Q 420,1020 480,930 Q 475,893 516,908'),('ถนนศรีตะกั่วป่า','M 785,400 L 789,520 L 735,709 Q 749,755 701,828 L 590,900 L 584,1210'),('ถนนอุดมธารา','M 521,908 L 700,828'),('ถนนบรมธาตุ','M 350,980 L 380,1040 Q 420,1055 514,1037'),('ถนนหน้าเมือง','M 584,1150 Q 716,1117 764,1045'),('ถนนเกี่ยวข้าว','M 277,510 L 400,565'),('ซอยศรีมนตรี','M 679,300 L 674,384'),('ซอยหิรัณย์','M 741,310 L 739,384'),('ซอยรวงผึ้ง','M 470,684 Q 453,793 401,855')]
linework=''.join(f'<path id="road-{i}" d="{d}"/>' for i,(_,d) in enumerate(roads))
labels=''.join(f'<text><textPath href="#road-{i}" startOffset="12%">{name}</textPath></text>' for i,(name,_) in enumerate(roads))
mapbase=f'<path class="river" d="M 951,35 Q 776,161 817,510"/>{linework}'
def map_svg(active=None,decorative=False):
 pins=''.join(f'<a href="/places/{p["id"]}/" aria-label="{esc(byid[p["id"]]["name_th"])}"><title>{esc(byid[p["id"]]["name_th"])}</title><circle class="pin {"active" if active==p["id"] else ""}" cx="{p["x"]}" cy="{p["y"]}" r="17"/><text class="pin-label" x="{p["x"]}" y="{p["y"]+5}">{places.index(byid[p["id"]])+1}</text></a>' for p in points if p['x'] is not None)
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="150 0 850 1250" class="street-map" '+('aria-hidden="true"' if decorative else 'role="img" aria-label="ผังย่านเก่า อ้างอิงแผนที่เทศบาล"')+f'>{mapbase}{"" if decorative else labels+pins}</svg>'
caption='ผังนี้อ้างอิงตำแหน่งจากแผนที่ประชาสัมพันธ์ของเทศบาลเมืองตะกั่วป่า ระยะและสัดส่วนไม่ตรงตามพื้นที่จริง'
def map_preview(): return f'<div class="map-preview"><div>{map_svg()}</div><div><span class="eyebrow">READ THE OLD TOWN</span><h2>แผนที่ย่านเก่า</h2><p>มองถนน สายน้ำ และจุดหมายของเมืองไว้ในภาพเดียว เลือกหมายเลขเพื่ออ่านเรื่องของสถานที่</p><a class="text-link" href="/map/">เปิดแผนที่เต็มและรายชื่อจุด ↗</a><p class="small">{caption}</p></div></div>'
def timeline(): return '<div class="timeline">'+''.join(f'<article><span class="eyebrow">{period(r)}</span><h3>{a(r)}</h3></article>' for r in sorted(events,key=lambda r:['new-year-alms','ruler-ceremony','relic-procession','narai-ceremony','vegetarian','chak-phra','loy-krathong'].index(r['id'])))+'</div>'
hero=f'<section class="masthead"><div class="hero-lines">{map_svg(decorative=True)}</div><div class="edition"><span>TAKUA PA · PHANG NGA</span><span>คู่มือเมืองเก่า / 01</span></div><div class="hero-title"><div><span class="eyebrow">ค่อย ๆ รู้จักเมือง ผ่านเรื่องราวระหว่างทาง</span><h1>ตะกั่วป่า <em>101</em></h1><p class="subtitle">วัด ศาลเจ้า ตึกเก่า<br>และย่านตลาดริมน้ำ</p><p>รวมสถานที่และเรื่องราวจากแผ่นพับเทศบาลเมืองตะกั่วป่า<br>ชวนเลือกจุดแวะ แล้วเปิดอ่านเมืองในแบบของคุณ</p><div class="hero-links"><a href="/map/">เปิดแผนที่ย่านเก่า ↗</a><a href="/places/">ดูสถานที่ทั้ง 20 แห่ง ↗</a></div></div><a class="hero-art" href="/places/tao-ming/">{pic("tao-ming",True)}<span>โรงเรียนเต้าหมิง · อาคารที่ส่งต่อภาษาและวัฒนธรรม ↗</span></a></div><div class="hero-bottom"><span>20 สถานที่</span><span>7 ประเพณี</span><span>59 ร้านจากเอกสารเทศบาล</span></div></section>'
page('/','คู่มือเมืองเก่าตะกั่วป่า','รู้จักตะกั่วป่าผ่าน 20 สถานที่ แผนที่ย่านเก่า ประเพณี และรายชื่อร้านจากเอกสารเทศบาล',hero+'<section><div class="section-heading"><h2>เริ่มจากตรงนี้</h2><span>เลือกเรื่องที่อยากรู้จัก</span></div>'+route_list()+'</section><section>'+map_preview()+'</section><section><div class="section-heading"><h2>สถานที่ 20 แห่ง</h2><span>เรื่องของเมือง ผ่านแต่ละจุดหมาย</span></div>'+directory()+'</section><section><h2>ประเพณีตลอดปี</h2><p>ช่วงเวลาตามเอกสารต้นทาง · ตรวจสอบกำหนดการของแต่ละปีก่อนเดินทาง</p>'+timeline()+'</section><section class="eat-callout"><span class="number">59</span><div><h2>กินและซื้อของฝากในย่าน</h2><p>รายชื่อร้านอาหาร 32 แห่ง · เครื่องดื่ม 19 แห่ง · ของฝาก 8 แห่ง จากแผ่นพับ</p><a class="text-link" href="/eat/">เปิดรายชื่อร้านในย่าน ↗</a></div></section><section><h2>ข้อมูลนี้มาจากไหน</h2><p class="measure">ข้อมูลเรียบเรียงจากแผ่นพับประชาสัมพันธ์เทศบาลเมืองตะกั่วป่า สกัดเมื่อ 6 กันยายน 2569 รายละเอียดการเข้าชมและสถานะร้านปัจจุบันยังไม่ได้ยืนยัน</p><a class="text-link" href="/about/">อ่านที่มาและข้อจำกัดข้อมูล ↗</a></section>')
page('/places/','สถานที่ 20 แห่ง','ดัชนีวัด ศาลเจ้า ตึกเก่า สวน ตลาด และพิพิธภัณฑ์ในตะกั่วป่า',intro('สถานที่ 20 แห่ง','เลือกหนึ่งจุดหมาย แล้วค่อย ๆ ต่อเรื่องราวของเมืองเข้าด้วยกัน')+'<div class="jump-links">'+''.join(f'<a href="#category-{i}">{name} · {len(ids)}</a>' for i,(name,ids) in enumerate(groups))+'</div>'+directory())
for r in places:
 id=r['id']; related=next(ids for _,ids in groups if id in ids); related=[x for x in related if x!=id][:3]+links.get(id,[])+[key for key,ids in links.items() if id in ids];related=list(dict.fromkeys(related))
 details=r.get('source_details',{});dl=''
 for key,label in [('built_be','สร้างเมื่อ พ.ศ.'),('historical_event_be','เหตุการณ์ที่เอกสารกล่าวถึง พ.ศ.'),('founder_as_printed','ผู้ก่อตั้งตามเอกสาร')]:
  if key in details: dl+=f'<dt>{label}</dt><dd>{esc(str(details[key]))}</dd>'
 if 'source_superlative' in details: dl+='<dt>ข้อสังเกตจากต้นทาง</dt><dd>เอกสารเทศบาลระบุว่าเป็นอุโบสถขนาดเล็กที่สุดในไทย ยังไม่ได้ตรวจเทียบกับแหล่งอื่น</dd>'
 mapped=id in positions
 body=intro(r['name_th'],copy[id]['kicker'])+f'<div class="detail"><p class="english">{esc(r.get("name_en",""))}</p><figure>{pic(id,True)}</figure><h2>เรื่องของที่นี่</h2><p>{copy[id]["body"]}</p>'+''.join(f'<p>{esc(f)}</p>' for f in r.get('facts_paraphrased',[]) if f!=copy[id]['body'])+(f'<h2>รายละเอียดจากเอกสาร</h2><dl>{dl}</dl>' if dl else '')+'<h2>อยู่ตรงไหนในย่าน</h2>'+(f'<div class="detail-map">{map_svg(id)}</div><p class="small">{caption}</p>' if mapped else '<p>ไม่ปรากฏตำแหน่งในแผนที่ต้นทาง</p>')+'<a class="text-link" href="/map/">เปิดแผนที่และรายชื่อทั้งหมด ↗</a>'+('<h2>เกี่ยวข้องกัน</h2><ul>'+''.join(f'<li>{a(byid[x])}</li>' for x in related)+'</ul>' if related else '')+source()+'</div>'
 page(url(r),r['name_th'],copy[id]['kicker']+' · '+copy[id]['body'],body,r)
page('/traditions/','ประเพณีตลอดปี','กิจกรรมและประเพณีตะกั่วป่า 7 รายการ พร้อมช่วงเวลาตามแผ่นพับเทศบาล',intro('ประเพณีตลอดปี','จังหวะของเมือง ผ่านความเชื่อและการพบกันของผู้คน')+timeline()+source())
for r in events:
 body=intro(r['name_th'],period(r))+'<div class="detail"><h2>ช่วงเวลาจากเอกสาร</h2><p>'+period(r)+'</p><p>รายการนี้ปรากฏในหมวดกิจกรรมและประเพณีของแผ่นพับเทศบาลเมืองตะกั่วป่า ช่วงเวลาข้างต้นเป็นข้อมูลจากเอกสาร ยังไม่ใช่กำหนดการยืนยันของปีปัจจุบัน</p>'+('<h2>สถานที่ที่เกี่ยวข้อง</h2><ul>'+''.join(f'<li>{a(byid[id])}</li>' for id in links.get(r['id'],[]))+'</ul>' if links.get(r['id']) else '')+source()+'</div>'
 page(url(r),r['name_th'],r['name_th']+' · '+period(r)+' ตามเอกสารเทศบาลเมืองตะกั่วป่า',body,r)
page('/routes/','เส้นทางเดินอ่านเมือง','เลือกจุดแวะตามเรื่องวัดและเจดีย์ ศาลเจ้า หรือตึกเก่าและตลาดริมน้ำ',intro('เส้นทางเดินอ่านเมือง','สามชุดจุดหมายให้เลือกตามความสนใจ')+'<p class="measure">รายการนี้จัดกลุ่มสถานที่ตามเรื่องราว ไม่กำหนดเวลาเดินหรือระยะทาง ใช้แผนที่ประกอบการเลือกจุดแวะ และตรวจสอบการเข้าชมก่อนออกเดินทาง</p>'+route_list(True)+map_preview()+source())
shopgroups=[('restaurant','ร้านอาหาร'),('drink_shop','เครื่องดื่ม'),('souvenir_shop','ของฝาก')]
shophtml=''.join(f'<section class="shop-group" data-category="{cat}"><h2>{label} <span class="count">{sum(r["category"]==cat for r in shops)}</span></h2><ol class="shop-list">'+''.join(f'<li id="{r["id"]}" data-shop="{esc(r["name_th"])}"><span class="shop-number">{r["source_list_number"]:02d}</span><span>{esc(r["name_th"])}</span></li>' for r in shops if r['category']==cat)+'</ol></section>' for cat,label in shopgroups)
page('/eat/','กินและของฝาก','ค้นหารายชื่อร้านอาหาร เครื่องดื่ม และของฝาก 59 ร้าน ตามแผ่นพับเทศบาลเมืองตะกั่วป่า',intro('กินและของฝากในย่าน','59 รายชื่อจากแผ่นพับเทศบาลเมืองตะกั่วป่า')+'<p>รายชื่อและลำดับตามเอกสารต้นทาง ยังไม่ได้ยืนยันสถานะการเปิดร้านในปัจจุบัน</p><div class="filters"><label>ค้นหาชื่อร้าน<input id="shop-search" type="search" placeholder="พิมพ์ชื่อร้านที่ต้องการ"></label><label>หมวดหมู่<select id="shop-category"><option value="all">ทุกร้าน</option>'+''.join(f'<option value="{cat}">{label}</option>' for cat,label in shopgroups)+'</select></label></div><p id="results" role="status" aria-live="polite">แสดง 59 ร้าน</p><p id="empty" hidden>ไม่พบรายชื่อ ลองเปลี่ยนคำค้นหรือเลือกหมวดอื่น</p>'+shophtml+source())
table='<table><caption>รายชื่อจุดบนผัง</caption><thead><tr><th>หมายเลข</th><th>สถานที่</th><th>ตำแหน่งในต้นทาง</th></tr></thead><tbody>'+''.join(f'<tr><td>{places.index(byid[p["id"]])+1:02d}</td><td>{a(byid[p["id"]])}</td><td>{"ปรากฏในแผนที่" if p["x"] is not None else "ไม่ปรากฏตำแหน่ง"}</td></tr>' for p in points)+'</tbody></table>'
page('/map/','แผนที่ย่านเก่า','ผังถนนและสถานที่จากแผนที่เทศบาลเมืองตะกั่วป่า พร้อมรายชื่อจุดและแผนที่ต้นทาง',intro('แผนที่ย่านเก่า','ถนน สายน้ำ และจุดหมายที่เชื่อมเรื่องราวของเมือง')+f'<p class="measure">{caption}</p><details class="map-panel"><summary>ดูเป็นผังแผนที่ · 14 จุดจากต้นทาง</summary><div class="map-scroll">{map_svg()}</div></details>'+table+'<h2>เทียบกับแผนที่ต้นทาง</h2><p>แสดงเฉพาะหมุดสถานที่ที่จับคู่ได้ชัดเจน หมายเลขร้านบนภาพต้นทางยังไม่ได้จับคู่เป็นหมุดในผังนี้</p><a class="text-link" href="/assets/municipal-map.png">เปิดภาพแผนที่เทศบาลฉบับเต็ม ↗</a>'+source())
about_jsonld = [
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "ศิวรา คาเฟ่",
    "sameAs": ["https://siwaracafe.com/"]
  }
]
about_html = intro('ข้อมูลนี้มาจากไหน','รู้จักเมือง พร้อมรู้ที่มาของเรื่องที่อ่าน') + f'<div class="detail"><h2>คู่มือจากบ้านศิวรา</h2><p>ตะกั่วป่า 101 จัดทำโดย <a href="https://siwaracafe.com/">บ้านศิวรา</a> ในตะกั่วป่า เพื่อรวบรวมเรื่องสถานที่ ประเพณี และร้านค้าในเมืองให้อ่านต่อกันได้</p><p>ศิวรา คาเฟ่ เป็นบ้านไม้สักหลังหนึ่งในย่านตลาดเก่า สังเกตได้จากจั่วไม้ กระจกสี และบานประตูไม้เก่าแบบดั้งเดิม ตั้งอยู่ที่ 53 ถนนราษฎร์บำรุง โดยเราตั้งใจให้บ้านไม้หลังนี้พาผู้คนไปรู้จักเมืองให้ลึกซึ้งขึ้น</p><h2>ข้อมูลที่นำมาใช้</h2><p>แผ่นพับเทศบาลเมืองตะกั่วป่าเป็นต้นทางของข้อมูลสถานที่ 20 แห่ง ประเพณี 7 รายการ และรายชื่อร้าน 59 แห่ง รวม 86 รายการ สกัดเมื่อ 6 กันยายน 2569</p><h2>ก่อนออกเดินทาง</h2><p>เอกสารต้นทางไม่ระบุวันที่เผยแพร่ เว็บไซต์จึงยังไม่ยืนยันเวลาเปิด ค่าเข้า สถานะร้าน หรือกำหนดการจัดงานปัจจุบัน ควรติดต่อสถานที่หรือเทศบาลเพื่อยืนยันรายละเอียดก่อนเดินทาง</p><h2>อ่านผังอย่างไร</h2><p>'+caption+'</p><p>จับคู่สถานที่ได้ 14 แห่ง ส่วนอีก 6 แห่งแสดงในรายชื่อโดยไม่เติมตำแหน่งขึ้นเอง</p>'+source()+'</div>'
about_html += f'<script type="application/ld+json">{json.dumps(about_jsonld, ensure_ascii=False).replace("</", "<\\/")}</script>'
page('/about/','ข้อมูลนี้มาจากไหน','ที่มาของคู่มือเมืองเก่าตะกั่วป่า ความสัมพันธ์กับบ้านศิวรา และขอบเขตข้อมูลจากแผ่นพับเทศบาล', about_html)
page('/trip/','ทริปของคุณ','เลือกจุดหมายในเมืองเก่าตะกั่วป่า แล้วจัดเป็นเส้นทางเดินของคุณเอง','<div id="trip-app"></div><noscript><p>ต้องเปิด JavaScript เพื่อใช้งานจัดทริป หรือเลือกดู<a href="/places/">สถานที่ทั้งหมด</a>และ<a href="/map/">แผนที่</a></p></noscript>')
def render_rest():
    extra_shops = json.loads((DATA/'shops-extra.json').read_text(encoding='utf-8'))
    all_shops = shops + extra_shops
    picks = json.loads((DATA/'guide-picks.json').read_text(encoding='utf-8'))

    html = intro('พักเบรกและกินเที่ยวตะกั่วป่า', 'ร้านและจุดแวะที่คนทำคู่มือเล่มนี้ไปมาเองแล้ว พร้อมเวลาเปิดและพิกัดนำทาง')
    html += ('<p>เมืองเก่าเดินได้ทั้งย่านแต่ร่มน้อย ช่วงบ่ายแดดแรง การมีจุดแวะช่วยให้เดินได้ครบ</p>'
             '<p class="small">รายการข้างล่างคัดมาจาก'
             '<a href="https://siwaracafe.com/guide" target="_blank" rel="noopener">คู่มือกินเที่ยวตะกั่วป่าของศิวรา คาเฟ่</a>'
             ' ซึ่งเป็นคนจัดทำเว็บนี้ · ต่างจากรายชื่อร้านใน<a href="/eat/">หน้ากินและของฝาก</a> ตรงที่ทุกร้านตรงนี้มีคนไปมาเองแล้ว '
             'จึงมีเวลาเปิดและพิกัดที่ใช้ได้จริง · ถึงอย่างนั้นร้านเล็กเปลี่ยนเวลาได้เสมอ ควรโทรถามก่อนเดินทางไกล</p>')

    GROUPS = [('dining', 'ร้านอาหารและของกิน'), ('attraction', 'จุดแวะและที่เที่ยว'), ('souvenir', 'ของฝาก')]
    json_ld_list = []
    for key, label in GROUPS:
        rows = [r for r in picks if r.get('guide_group') == key]
        if not rows:
            continue
        rows.sort(key=lambda x: x['name_th'])
        html += f'<h2>{esc(label)}</h2><div class="rest-stops">'
        for r in rows:
            art = f'<a class="pick-art" href="{esc(r["google_maps_url"])}" target="_blank" rel="noopener"><img src="{esc(r["image"])}" alt="{esc(r["name_th"])}" loading="lazy"></a>' if r.get('image') else ''
            meta = []
            if r.get('hours_th'):
                meta.append('เวลาเปิด ' + esc(r['hours_th']))
            if r.get('distance_th'):
                meta.append(esc(r['distance_th']))
            metaline = f'<p class="pick-meta">{" · ".join(meta)}</p>' if meta else ''
            tip = f'<p class="pick-tip">{esc(r["tip_th"])}</p>' if r.get('tip_th') else ''
            gmap = f'<a class="shop-nav" href="{esc(r["google_maps_url"])}" target="_blank" rel="noopener">นำทาง ↗</a>' if r.get('google_maps_url') else ''
            html += (f'<article class="rest-stop pick">{art}<div class="pick-body">'
                     f'<h3>{esc(r["name_th"])}</h3>'
                     f'<p>{esc(r.get("one_liner_th") or "")}</p>{metaline}{tip}{gmap}'
                     f'</div></article>')
            json_ld_list.append({
                "@type": "ListItem",
                "position": len(json_ld_list) + 1,
                "item": {"@type": "Place", "name": r["name_th"],
                         "url": r.get("google_maps_url") or f"{BASE}/rest/"}
            })
        html += '</div>'

    html += ('<h2>แผ่นพับพกไปเดิน</h2>'
             '<div class="leaflet-block">'
             '<a class="leaflet-art" href="/assets/leaflet/takuapa-walk-leaflet.pdf" target="_blank" rel="noopener">'
             '<img src="/assets/leaflet/leaflet-page-1.webp" alt="แผ่นพับเดินเมืองเก่าตะกั่วป่า หน้าแรก" loading="lazy"></a>'
             '<div class="leaflet-copy">'
             '<p>แผ่นพับสองหน้า เล่าเรื่องบ้านไม้และสี่จุดในเส้นทางข้างบน '
             'พิมพ์ใส่กระดาษ A4 แล้วพับครึ่งพกไปเดินได้เลย ไม่ต้องเปิดมือถือกลางแดด</p>'
             '<div class="leaflet-actions">'
             '<a class="button" href="/assets/leaflet/takuapa-walk-leaflet.pdf" target="_blank" rel="noopener">โหลดแผ่นพับ PDF</a>'
             '<a class="text-link" href="/leaflet/">อ่านบนเว็บแทน ↗</a>'
             '</div>'
             '<p class="small">จัดทำโดย'
             '<a href="https://siwaracafe.com/" target="_blank" rel="noopener">ศิวรา คาเฟ่</a>'
             ' ผู้จัดทำคู่มือเล่มนี้ · แจกฟรี นำไปพิมพ์ต่อได้</p>'
             '</div></div>')

    html += '''
    <h2>บ้านไม้ที่ทำคู่มือเล่มนี้</h2>
    <div class="siwara-card">
        <p>เว็บไซต์นี้จัดทำโดยศิวรา คาเฟ่ บ้านไม้สัก จั่วไม้ กระจกสี ประตูบานเก่า ที่อยู่ 53 ถนนราษฎร์บำรุง ย่านตลาดเก่า</p>
        <a href="https://siwaracafe.com/" target="_blank" rel="noopener">รู้จักบ้านศิวราผู้จัดทำคู่มือ ↗</a>
    </div>
    '''
    
    html += '<h2>เส้นทางเดินสั้นจากบ้านไม้</h2>'
    walk_points = [
        ('khun-in', 'หลังคาระเบียงและช่องเปิด'),
        ('tao-ming', 'หน้าจั่วและระเบียงสีเหลือง'),
        ('guan-yu', 'ประตูและรายละเอียดสีแดง'),
        ('iron-bridge', 'โครงเหล็กและภูมิทัศน์ริมน้ำ')
    ]
    html += '<div class="short-walk">'
    for pid, focus in walk_points:
        html += f'<article class="walk-point"><a href="{url(byid[pid])}">{pic(pid)}</a><div><h3>{a(byid[pid])}</h3><p>ชวนมอง: {focus}</p><button data-trip-add="{pid}">เพิ่มลงทริป</button></div></article>'
    html += '</div>'
    
    html += '<p>วางแผนต่อ: <a href="/trip/">จัดทริปของคุณ ↗</a> · <a href="/map/">ดูแผนที่เมือง ↗</a></p>'
    html += source()
    
    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "หน้าแรก", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "พักเบรกระหว่างเดินเมืองเก่า", "item": BASE + "/rest/"}
            ]
        }
    ]
    if json_ld_list:
        json_ld.append({
            "@context": "https://schema.org",
            "@type": "ItemList",
            "itemListElement": json_ld_list
        })
    html += f'<script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False).replace("</", "<\\/")}</script>'
    return html

def render_leaflet():
    html = intro('แผ่นพับเดินเมืองเก่าตะกั่วป่า', 'สองหน้า พิมพ์ใส่ A4 พับครึ่ง พกไปเดินได้')
    html += ('<p>แผ่นพับนี้เล่าเรื่องบ้านไม้สักหลังหนึ่งในย่านตลาดเก่า แล้วชวนเดินต่อไปอีกสี่จุดในเมือง '
             'ทำไว้สำหรับคนที่อยากเดินโดยไม่ต้องก้มดูมือถือตลอดทาง</p>')
    html += ('<div class="leaflet-pages">'
             '<figure><img src="/assets/leaflet/leaflet-page-1.webp" alt="แผ่นพับหน้าแรก เล่าเรื่องบ้านไม้ศิวรา" loading="eager" width="1400"><figcaption>หน้าแรก</figcaption></figure>'
             '<figure><img src="/assets/leaflet/leaflet-page-2.webp" alt="แผ่นพับหน้าสอง สี่จุดในเส้นทางเดิน" loading="lazy" width="1400"><figcaption>หน้าสอง</figcaption></figure>'
             '</div>')
    html += ('<div class="leaflet-actions">'
             '<a class="button" href="/assets/leaflet/takuapa-walk-leaflet.pdf" target="_blank" rel="noopener">โหลด PDF สำหรับพิมพ์</a>'
             '<a class="text-link" href="/rest/">กลับไปหน้ากินเที่ยว ↗</a>'
             '</div>')
    html += ('<aside class="source"><h2>ที่มาของแผ่นพับ</h2>'
             '<p>ออกแบบและจัดทำโดย<a href="https://siwaracafe.com/" target="_blank" rel="noopener">ศิวรา คาเฟ่</a> '
             'บ้านไม้ในย่านตลาดเก่าที่เป็นผู้จัดทำคู่มือเล่มนี้ · แจกฟรี พิมพ์ต่อและแจกต่อได้ '
             'ข้อมูลสถานที่เรียบเรียงจากแหล่งเดียวกับหน้าสถานที่ในเว็บนี้</p></aside>')
    return html

page('/leaflet/', 'แผ่นพับเดินเมืองเก่าตะกั่วป่า', 'แผ่นพับสองหน้า พิมพ์ A4 พับครึ่ง พกไปเดินเมืองเก่าตะกั่วป่า โหลดฟรี', render_leaflet())
page('/rest/', 'พักเบรกและกินเที่ยวตะกั่วป่า', 'ร้านอร่อยและจุดแวะในตะกั่วป่าที่มีคนไปมาเองแล้ว พร้อมเวลาเปิดและพิกัดนำทาง แผ่นพับเดินเมืองเก่าโหลดฟรี', render_rest())

(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{esc(BASE+p)}</loc><lastmod>{date.today().isoformat()}</lastmod></url>' for p in PAGES)+'</urlset>',encoding='utf-8')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n',encoding='utf-8')

def render_news():
    news_data = json.loads((DATA/'news-feed.json').read_text(encoding='utf-8'))
    places = sorted(list(set(n['place_name'] for n in news_data if n.get('place_name'))))
    years = sorted(list(set(n.get('date','')[:4] for n in news_data if n.get('date'))), reverse=True)
    
    tabs = '<button type="button" data-news-filter="all" aria-pressed="true">ทั้งหมด</button>'
    for p in places: tabs += f'<button type="button" data-news-filter="{esc(p)}" aria-pressed="false">{esc(p)}</button>'
    for y in years: tabs += f'<button type="button" data-news-filter="{y}" aria-pressed="false">ปี {int(y)+543}</button>'
    
    items_html = ''
    jsonld_items = []
    
    for i, n in enumerate(news_data):
        d = n.get('date', '')
        d_th = ''
        y = d[:4] if d else ''
        if d:
            try:
                yx, m, dd = d.split('-')
                months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
                d_th = f'{int(dd)} {months[int(m)-1]} {int(yx)+543}'
            except:
                pass
                
        place_link = f'<a href="{esc(n["place_url"])}">{esc(n["place_name"])}</a>' if n.get("place_url") else ''
        title = esc(n.get("title_th", ""))
        summary = esc(n.get("summary_th", ""))
        outlet = esc(n.get("outlet", ""))
        url_link = esc(n.get("url", ""))
        link = f'<a class="news-out" href="{url_link}" target="_blank" rel="noopener">อ่านข่าวต้นทาง ↗</a>' if url_link else ''
        
        items_html += f'<article class="news-item" data-place="{esc(n.get("place_name",""))}" data-year="{y}"><time datetime="{d}">{d_th}</time><div class="news-content"><h2>{title}</h2><p>{summary}</p><div class="news-meta">{place_link}{" · " if place_link and outlet else ""}{outlet}</div>{link}</div></article>'
        
        jsonld_items.append({
            "@type": "ListItem",
            "position": i + 1,
            "item": {
                "@type": "NewsArticle",
                "headline": title,
                "datePublished": d,
                "url": url_link
            }
        })
        
    jsonld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": jsonld_items
    }
    
    html = f'<div class="news-page"><div class="intro"><a class="eyebrow" href="/">ตะกั่วป่า 101 / คู่มือเมืองเก่า</a><h1>ความเคลื่อนไหวของเมือง</h1><p class="lead">ข่าวสารและกิจกรรมที่เกิดขึ้นในเมืองเก่าตะกั่วป่า</p></div><div class="news-filters" role="group" aria-label="กรองข่าวสาร">{tabs}</div><div class="news-list-full">{items_html}</div></div><script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False).replace("</", "<\\\\/")}</script>'
    return html

page('/news/','ความเคลื่อนไหวของเมือง','ข่าวสารและกิจกรรมในเมืองเก่าตะกั่วป่า',render_news())

stories.write_audit()
page('/stories/','เรื่องเล่าตะกั่วป่า','บทความประวัติศาสตร์และวัฒนธรรมตะกั่วป่าจากแหล่งข้อมูลทางการ แยกระดับหลักฐานชัดเจน',stories.index({'byid': byid}))
for story in stories.get_all_stories():
 route = story.get('route') or f"/stories/{story['id']}/"
 page(route, story['title'], story['dek'], stories.article(story, {'byid': byid}))
page('/rest/', 'พักเบรกและกินเที่ยวตะกั่วป่า', 'ร้านอร่อยและจุดแวะในตะกั่วป่าที่มีคนไปมาเองแล้ว พร้อมเวลาเปิดและพิกัดนำทาง แผ่นพับเดินเมืองเก่าโหลดฟรี', render_rest())

(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{esc(BASE+p)}</loc><lastmod>{date.today().isoformat()}</lastmod></url>' for p in PAGES)+'</urlset>',encoding='utf-8')
for name in ['NotoSerifThai','IBMPlexSansThaiLooped-Regular','CormorantGaramond']:
 target=OUT/f'assets/{name}.woff2'
 if not target.exists():
  opts=subset.Options();opts.flavor='woff2';font=subset.load_font(str(OUT/f'assets/{name}.ttf'),opts); sub=subset.Subsetter(options=opts);sub.populate(unicodes=list(range(0x20,0x180))+list(range(0xE00,0xE80))+list(range(0x2000,0x2070))+[0x2197]);sub.subset(font);subset.save_font(font,str(target),opts)
print(f'Built {len(PAGES)} pages, 20 places, 7 traditions, 59 directory entries. Original municipal image map. Local preview: {BASE}/')
