import re

with open('build_site.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add 'rest' to nav
code = code.replace(
    "nav.insert(1, ('news', 'ความเคลื่อนไหว'))",
    "nav.insert(1, ('news', 'ความเคลื่อนไหว'))\nnav.insert(5, ('rest', 'พักเบรก'))"
)

# 2. Add route 4
code = code.replace(
    "routes = [('เส้นวัดและเจดีย์',groups[0][1]),('เส้นศาลเจ้าและโรงเจ',groups[1][1]),('เส้นตึกเก่าและตลาดริมน้ำ',['tao-ming','khun-in','governor-wall','culture-street','riverwalk','food-center'])]",
    "routes = [('เส้นวัดและเจดีย์',groups[0][1]),('เส้นศาลเจ้าและโรงเจ',groups[1][1]),('เส้นตึกเก่าและตลาดริมน้ำ',['tao-ming','khun-in','governor-wall','culture-street','riverwalk','food-center']), ('เดินสั้นจากบ้านไม้',['khun-in','tao-ming','guan-yu','iron-bridge'])]"
)

# 3. Update route_list
old_route_list = """def route_list(): return '<div class="route-list">'+''.join(f'<article id="route-{i}"><span class="number">0{i}</span><div><h3><a href="/routes/#route-{i}">{name} ↗</a></h3><p>'+ ' · '.join(a(byid[id]) for id in ids)+'</p></div></article>' for i,(name,ids) in enumerate(routes,1))+'</div>'"""

new_route_list = """def route_list(is_route_page=False):
 out = '<div class="route-list">'
 for i,(name,ids) in enumerate(routes,1):
  desc = '<p>เหมาะกับคนมีเวลาครึ่งวัน</p>' if i == 4 and is_route_page else ''
  out += f'<article id="route-{i}"><span class="number">0{i}</span><div><h3><a href="/routes/#route-{i}">{name} ↗</a></h3>{desc}<p>'+ ' · '.join(a(byid[id]) for id in ids)+'</p></div></article>'
 out += '</div>'
 return out"""
code = code.replace(old_route_list, new_route_list)

code = code.replace("route_list()+'</section>'", "route_list(False)+'</section>'")
code = code.replace("route_list()+map_preview()", "route_list(True)+map_preview()")

# 4. Update about page
old_about = """page('/about/','ข้อมูลนี้มาจากไหน','ที่มาของคู่มือเมืองเก่าตะกั่วป่า ความสัมพันธ์กับบ้านศิวรา และขอบเขตข้อมูลจากแผ่นพับเทศบาล',intro('ข้อมูลนี้มาจากไหน','รู้จักเมือง พร้อมรู้ที่มาของเรื่องที่อ่าน')+'<div class="detail"><h2>คู่มือจากบ้านศิวรา</h2><p>ตะกั่วป่า 101 จัดทำโดย <a href="https://siwaracafe.com/">บ้านศิวรา</a> ในตะกั่วป่า เพื่อรวบรวมเรื่องสถานที่ ประเพณี และร้านค้าในเมืองให้อ่านต่อกันได้</p><h2>ข้อมูลที่นำมาใช้</h2><p>แผ่นพับเทศบาลเมืองตะกั่วป่าเป็นต้นทางของข้อมูลสถานที่ 20 แห่ง ประเพณี 7 รายการ และรายชื่อร้าน 59 แห่ง รวม 86 รายการ สกัดเมื่อ 6 กันยายน 2569</p><h2>ก่อนออกเดินทาง</h2><p>เอกสารต้นทางไม่ระบุวันที่เผยแพร่ เว็บไซต์จึงยังไม่ยืนยันเวลาเปิด ค่าเข้า สถานะร้าน หรือกำหนดการจัดงานปัจจุบัน ควรติดต่อสถานที่หรือเทศบาลเพื่อยืนยันรายละเอียดก่อนเดินทาง</p><h2>อ่านผังอย่างไร</h2><p>'+caption+'</p><p>จับคู่สถานที่ได้ 14 แห่ง ส่วนอีก 6 แห่งแสดงในรายชื่อโดยไม่เติมตำแหน่งขึ้นเอง</p>'+source()+'</div>')"""

new_about = """about_jsonld = [
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "ศิวรา คาเฟ่",
    "sameAs": ["https://siwaracafe.com/"]
  }
]
about_html = intro('ข้อมูลนี้มาจากไหน','รู้จักเมือง พร้อมรู้ที่มาของเรื่องที่อ่าน') + f'<div class="detail"><h2>คู่มือจากบ้านศิวรา</h2><p>ตะกั่วป่า 101 จัดทำโดย <a href="https://siwaracafe.com/">บ้านศิวรา</a> ในตะกั่วป่า เพื่อรวบรวมเรื่องสถานที่ ประเพณี และร้านค้าในเมืองให้อ่านต่อกันได้</p><p>ศิวรา คาเฟ่ เป็นบ้านไม้สักหลังหนึ่งในย่านตลาดเก่า สังเกตได้จากจั่วไม้ กระจกสี และบานประตูไม้เก่าแบบดั้งเดิม ตั้งอยู่ที่ 53 ถนนราษฎร์บำรุง โดยเราตั้งใจให้บ้านไม้หลังนี้พาผู้คนไปรู้จักเมืองให้ลึกซึ้งขึ้น</p><h2>ข้อมูลที่นำมาใช้</h2><p>แผ่นพับเทศบาลเมืองตะกั่วป่าเป็นต้นทางของข้อมูลสถานที่ 20 แห่ง ประเพณี 7 รายการ และรายชื่อร้าน 59 แห่ง รวม 86 รายการ สกัดเมื่อ 6 กันยายน 2569</p><h2>ก่อนออกเดินทาง</h2><p>เอกสารต้นทางไม่ระบุวันที่เผยแพร่ เว็บไซต์จึงยังไม่ยืนยันเวลาเปิด ค่าเข้า สถานะร้าน หรือกำหนดการจัดงานปัจจุบัน ควรติดต่อสถานที่หรือเทศบาลเพื่อยืนยันรายละเอียดก่อนเดินทาง</p><h2>อ่านผังอย่างไร</h2><p>'+caption+'</p><p>จับคู่สถานที่ได้ 14 แห่ง ส่วนอีก 6 แห่งแสดงในรายชื่อโดยไม่เติมตำแหน่งขึ้นเอง</p>'+source()+'</div>'
about_html += f'<script type="application/ld+json">{json.dumps(about_jsonld, ensure_ascii=False).replace("</", "<\\\\/")}</script>'
page('/about/','ข้อมูลนี้มาจากไหน','ที่มาของคู่มือเมืองเก่าตะกั่วป่า ความสัมพันธ์กับบ้านศิวรา และขอบเขตข้อมูลจากแผ่นพับเทศบาล', about_html)"""
code = code.replace(old_about, new_about)

# 5. Place pages modification for 4 specific pages
place_page_block = """  body=intro(r['name_th'],copy[id]['kicker'])+f'<div class="detail"><p class="english">{esc(r.get("name_en",""))}</p><figure>{pic(id,True)}</figure><h2>เรื่องของที่นี่</h2><p>{copy[id]["body"]}</p>'+''.join(f'<p>{esc(f)}</p>' for f in r.get('facts_paraphrased',[]) if f!=copy[id]['body'])+(f'<h2>รายละเอียดจากเอกสาร</h2><dl>{dl}</dl>' if dl else '')+'<h2>อยู่ตรงไหนในย่าน</h2>'+(f'<div class="detail-map">{map_svg(id)}</div><p class="small">{caption}</p>' if mapped else '<p>ไม่ปรากฏตำแหน่งในแผนที่ต้นทาง</p>')+'<a class="text-link" href="/map/">เปิดแผนที่และรายชื่อทั้งหมด ↗</a>'+('<h2>เกี่ยวข้องกัน</h2><ul>'+''.join(f'<li>{a(byid[x])}</li>' for x in related)+'</ul>' if related else '')+source()+'</div>'"""

new_place_page_block = """  rel_html = '<h2>เกี่ยวข้องกัน</h2><ul>'+''.join(f'<li>{a(byid[x])}</li>' for x in related)+'</ul>' if related else ''
  if id in ['khun-in', 'tao-ming', 'guan-yu', 'iron-bridge']:
      rel_html += '<h2>ที่ใกล้เคียง</h2><p>มี<a href="/rest/">จุดพักในย่าน</a></p>'
  
  body=intro(r['name_th'],copy[id]['kicker'])+f'<div class="detail"><p class="english">{esc(r.get("name_en",""))}</p><figure>{pic(id,True)}</figure><h2>เรื่องของที่นี่</h2><p>{copy[id]["body"]}</p>'+''.join(f'<p>{esc(f)}</p>' for f in r.get('facts_paraphrased',[]) if f!=copy[id]['body'])+(f'<h2>รายละเอียดจากเอกสาร</h2><dl>{dl}</dl>' if dl else '')+'<h2>อยู่ตรงไหนในย่าน</h2>'+(f'<div class="detail-map">{map_svg(id)}</div><p class="small">{caption}</p>' if mapped else '<p>ไม่ปรากฏตำแหน่งในแผนที่ต้นทาง</p>')+'<a class="text-link" href="/map/">เปิดแผนที่และรายชื่อทั้งหมด ↗</a>'+rel_html+source()+'</div>'"""

code = code.replace(place_page_block, new_place_page_block)

# 6. Add /rest/ page rendering logic before (OUT/'sitemap.xml').write_text
rest_logic = """def render_rest():
    extra_shops = json.loads((DATA/'shops-extra.json').read_text(encoding='utf-8'))
    all_shops = shops + extra_shops
    rest_stops = [r for r in all_shops if r['category'] == 'drink_shop' and (r.get('near_old_town') == True or r.get('subdistrict') == 'ตะกั่วป่า')]
    rest_stops.sort(key=lambda x: x['name_th'])
    
    html = intro('พักเบรกระหว่างเดินเมืองเก่า', 'จุดนั่งพัก ห้องน้ำ และร้านเครื่องดื่มระหว่างเดินเมืองเก่าตะกั่วป่า')
    html += '<p>เมืองเก่าเดินได้ทั้งย่านแต่ร่มน้อย ช่วงบ่ายแดดแรง การมีจุดพักช่วยให้เดินได้ครบ</p>'
    
    html += '<h2>จุดพักในย่าน</h2><div class="rest-stops">'
    json_ld_list = []
    for i, r in enumerate(rest_stops):
        gmap = f'<a href="{esc(r["maps_search_url"])}" target="_blank" rel="noopener">หาบน Google Maps</a>' if r.get('maps_search_url') else ''
        hours = f'<p>เวลาเปิด: {esc(r["hours_th"])}</p>' if r.get('hours_th') else 'ตรวจสอบจากช่องทางร้านก่อนมา'
        desc = f'<p>{esc(r.get("one_liner_th") or "")}</p>'
        html += f'<article class="rest-stop"><h3>{esc(r["name_th"])}</h3>{desc}{hours}{gmap}</article>'
        item_type = "Place" if r['id'] == 'siwara-cafe' else "LocalBusiness"
        if r['id'] != 'siwara-cafe': # Rule: ห้ามใส่ schema Restaurant หรือ LocalBusiness ของศิวราในหน้านี้ ให้ใช้ sameAs ในหน้า /about/ แทน
            json_ld_list.append({
                "@type": "ListItem",
                "position": len(json_ld_list) + 1,
                "item": {
                    "@type": item_type,
                    "name": r["name_th"],
                    "url": r.get("website") or r.get("maps_search_url") or f"{BASE}/rest/"
                }
            })
    html += '</div>'
    
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
    html += f'<script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False).replace("</", "<\\\\/")}</script>'
    return html

page('/rest/', 'พักเบรกระหว่างเดินเมืองเก่า', 'จุดนั่งพัก ห้องน้ำ และร้านเครื่องดื่มระหว่างเดินเมืองเก่าตะกั่วป่า', render_rest())

"""

code = code.replace("(OUT/'sitemap.xml').write_text('<?xml", rest_logic + "(OUT/'sitemap.xml').write_text('<?xml")

with open('build_site.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patch applied")
