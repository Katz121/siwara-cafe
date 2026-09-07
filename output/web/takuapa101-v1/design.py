"""Presentation layer for the 2026-09-07 editorial redesign."""
from html import escape as e
import re

GROUPS = [('temple','วัดและเจดีย์',['wat-boromthat','wat-khuha','wat-pathum','wat-kongkha','wat-nikorn','wat-sena']),('shrine','ศาลเจ้าและโรงเจ',['guan-yu','pun-thao','kue-chai','rong-jae']),('heritage','ตึกเก่าและร่องรอยเมือง',['iron-bridge','governor-wall','khun-in','tao-ming']),('park','สวนและพื้นที่สาธารณะ',['phra-narai','thung-phra']),('market','ตลาดและของกิน',['riverwalk','culture-street','food-center']),('museum','พิพิธภัณฑ์',['museum'])]
MAP_NOTE = 'แผนที่ประชาสัมพันธ์ของเทศบาลเมืองตะกั่วป่า ระยะและสัดส่วนไม่ตรงตามพื้นที่จริง'

def cta(href, label):
    return f'<a class="button" href="{href}">{label}<span aria-hidden="true">↗</span></a>'

def heading(no, title, detail=''):
    return f'<div class="section-heading"><div><span class="chapter">{no} / เปิดอ่านเมือง</span><h2>{title}</h2></div><p>{detail}</p></div>'

def card(id, ctx):
    r=ctx['byid'][id]; key,label=next((k,l) for k,l,ids in GROUPS if id in ids)
    return f'<article class="place-card" data-place-card data-category="{key}" data-name="{e(r["name_th"])}"><a class="place-image" href="{ctx["url"](r)}">{ctx["pic"](id)}<span class="card-index">{ctx["places"].index(r)+1:02d}</span><span class="image-arrow" aria-hidden="true">↗</span></a><div class="card-copy"><span class="eyebrow">{label}</span><h3>{ctx["a"](r)}</h3><p>{e(ctx["copy"][id]["kicker"])}</p></div></article>'

def explorer(ctx, search=False):
    tabs='<button type="button" data-filter="all" aria-pressed="true">ทั้งหมด <sup>20</sup></button>'+''.join(f'<button type="button" data-filter="{key}" aria-pressed="false">{label} <sup>{len(ids)}</sup></button>' for key,label,ids in GROUPS)
    field='<label class="search-label">ค้นหาสถานที่<input type="search" data-place-search placeholder="ชื่อวัด ศาลเจ้า หรือจุดที่อยากไป" autocomplete="off"></label>' if search else ''
    return f'<div class="explorer" data-explorer><div class="explorer-tools">{field}<div class="filter-tabs" role="group" aria-label="หมวดสถานที่">{tabs}</div></div><div class="explorer-status"><span data-place-count role="status" aria-live="polite">20 สถานที่ให้ค่อย ๆ รู้จัก</span><span>เลือกภาพเพื่อเปิดอ่าน ↗</span></div><div class="places-grid">'+''.join(card(id,ctx) for _,_,ids in GROUPS for id in ids)+'</div><div class="empty-state" data-place-empty hidden><h3>ยังไม่เจอจุดหมายนี้</h3><p>ลองคำค้นอื่น หรือเลือกดูสถานที่ทั้งหมด</p><button type="button" data-clear-places>ล้างตัวกรอง</button></div></div>'

def route_cards(ctx):
    arts=['wat-boromthat','guan-yu','tao-ming']; angles=['อ่านเมืองผ่านศรัทธา','มองเรื่องราวของชุมชนจีน','ตามรอยอาคาร การค้า และผู้คน']
    return '<div class="route-cards">'+''.join(f'<a class="route-card" href="/routes/#route-{i}"><div class="route-art">{ctx["pic"](arts[i-1])}<span class="route-no">0{i}</span></div><div class="route-copy"><span class="eyebrow">{angles[i-1]}</span><h3>{name}</h3><span class="route-footer">{len(ids)} จุดหมาย <span aria-hidden="true">↗</span></span></div></a>' for i,(name,ids) in enumerate(ctx['routes'],1))+'</div>'

def map_teaser():
    return f'<section class="map-teaser"><div class="map-teaser-copy"><span class="chapter">กางแผนที่ / แล้วออกไปรู้จักเมือง</span><h2>ตรอกไหน ถนนไหน<br><em>มีเรื่องรออยู่</em></h2><p>จากย่านยาวถึงเมืองเก่า เปิดแผนที่เทศบาลแล้วค่อย ๆ มองหาจุดหมายถัดไป</p>{cta("/map/","กางแผนที่เมือง")}<span class="map-caption">ใช้ภาพแผนที่เทศบาลฉบับต้นทาง</span></div><a class="map-paper" href="/map/" aria-label="เปิดแผนที่เทศบาล"><img src="/assets/municipal-map.png" width="1358" height="1938" alt="แผนที่ท่องเที่ยวเมืองตะกั่วป่าจากเทศบาล" loading="lazy"><span class="paper-tag">TAKUA PA · TOWN MAP ↗</span></a><span class="map-compass" aria-hidden="true">✳</span></section>'

def traditions(ctx):
    order=['new-year-alms','ruler-ceremony','relic-procession','narai-ceremony','vegetarian','chak-phra','loy-krathong']; rows=[]
    for i,id in enumerate(order,1):
        r=ctx['byid'][id]; related=ctx['links'].get(id,[])
        content='<p>สถานที่ที่เกี่ยวข้อง: '+' · '.join(ctx['a'](ctx['byid'][x]) for x in related)+'</p>' if related else '<p>กิจกรรมในหมวดประเพณีของเอกสารเทศบาลเมืองตะกั่วป่า</p>'
        rows.append(f'<details class="tradition"><summary><span class="event-no">0{i}</span><span class="event-name">{e(r["name_th"])}</span><span class="event-period">{ctx["period"](r)}</span><span class="expand-icon" aria-hidden="true">+</span></summary><div class="event-body">{content}<a class="text-link" href="{ctx["url"](r)}">อ่านรายละเอียดจากเอกสาร ↗</a></div></details>')
    return '<div class="traditions-list">'+''.join(rows)+'</div>'

def transform(path,body,ctx,record):
    import place_pages
    if record and record['type']=='place': return place_pages.render(record,ctx,GROUPS)
    if path=='/stories/kuapapoh/': return body+place_pages.story_gallery()
    pic=ctx['pic']; intro=ctx['intro']; source=ctx['source']; byid=ctx['byid']
    if path=='/':
        hero=f'''<section class="hero"><div class="hero-topline"><span>PHANG NGA, THAILAND</span><span>เรื่องของเมือง / ฉบับที่ ๑</span></div><div class="hero-layout"><div class="hero-copy"><span class="hero-eyebrow"><i></i> คู่มือเมืองเก่าที่ชวนคุณค่อย ๆ เดิน</span><h1>ตะกั่วป่า<span class="hero-title-bottom">เมืองเล่าเรื่อง<em>101</em></span></h1><p>ผ่านประตูศาลเจ้า มองหน้าต่างบ้านเก่า<br>แล้วรู้จักเมืองอีกนิด ในทุกจุดที่แวะ</p><div class="hero-actions">{cta('#places','เลือกจุดหมายของคุณ')}<a class="text-link" href="/map/">เปิดแผนที่ ↗</a></div><div class="hero-footnote"><span class="tiny-star" aria-hidden="true">✳</span><span>20 สถานที่ · 7 ประเพณี · 59 ร้าน<br>รวบรวมจากแผ่นพับเทศบาลเมืองตะกั่วป่า</span></div></div><div class="hero-collage"><div class="collage-ring" aria-hidden="true"></div><span class="stamp">TAKUA PA<br><strong>ตะกั่วป่า</strong><br>OLD TOWN</span><a class="postcard postcard-main" href="/places/tao-ming/">{pic('tao-ming',True)}<span><b>01 / ตึกเก่า</b> โรงเรียนเต้าหมิง ↗</span></a><a class="postcard postcard-left" href="/places/guan-yu/">{pic('guan-yu',True)}<span>ศรัทธาของชุมชน ↗</span></a><a class="postcard postcard-right" href="/places/khun-in/">{pic('khun-in',True)}<span>หน้าต่างสู่วันวาน ↗</span></a><span class="collage-note">เก็บเรื่องราวระหว่างทาง</span><span class="collage-spark" aria-hidden="true">✳</span></div></div><div class="hero-bottom"><span>วัดและเจดีย์</span><i>✳</i><span>ศาลเจ้า</span><i>✳</i><span>บ้านเก่า</span><i>✳</i><span>ตลาดริมน้ำ</span><a href="#start">เริ่มเปิดอ่าน ↓</a></div></section>'''
        body=hero+quick_start()
        body+='<section id="start" class="section">'+heading('01','เริ่มจากเรื่องที่คุณสนใจ','สามเส้นทางอ่านเมือง · เลือกจุดแวะในแบบของคุณ')+route_cards(ctx)+'</section>'
        body+=city_feed(ctx)+map_teaser()
        body+='<section id="places" class="section">'+heading('03','เมืองเดียว หลายมุมให้รู้จัก','สถานที่ทั้ง 20 แห่ง จากหน้ากระดาษสู่เรื่องเล่าของเมือง')+explorer(ctx)+'<a class="text-link index-link" href="/places/">เปิดดัชนีและค้นหาสถานที่ ↗</a></section>'
        body+='<section class="section traditions-section">'+heading('04','เมื่อเมืองมีนัดหมาย','ประเพณีตลอดปี · ช่วงเวลาตามเอกสารต้นทาง')+traditions(ctx)+'<p class="small">ตรวจสอบกำหนดการของแต่ละปีก่อนเดินทาง</p></section>'
        body+=f'<section class="food-feature"><div class="food-feature-image">{pic("food-center")}<span class="food-stamp">LOCAL<br>FLAVOURS</span></div><div class="food-feature-copy"><span class="chapter">05 / กินและซื้อของฝากในย่าน</span><h2>รู้จักเมือง<br>ผ่านอีกรสชาติ</h2><p>เปิดรายชื่อร้านอาหาร เครื่องดื่ม และของฝาก<br>59 ร้านจากแผ่นพับเทศบาล</p><div class="food-counts"><span><b>32</b>อาหาร</span><span><b>20</b>เครื่องดื่ม</span><span><b>08</b>ของฝาก</span></div>{cta("/eat/","หาร้านในย่าน")}</div></section>'
        return body+'<section class="about-strip"><span class="chapter">บันทึกจากบ้านศิวรา</span><h2>เรื่องของเมือง<br>ที่อยากชวนคุณรู้จัก</h2><div><p>ตะกั่วป่า 101 รวบรวมข้อมูลจากแผ่นพับเทศบาลเมืองตะกั่วป่า พร้อมที่มาและขอบเขตข้อมูลให้คุณอ่านต่อได้</p><a class="text-link" href="/about/">รู้จักคู่มือเล่มนี้ ↗</a></div></section>'
    if path=='/places/':
        return intro('เลือกเปิดเรื่องของเมือง','20 จุดหมาย · วัด ศาลเจ้า ตึกเก่า และชีวิตริมทาง')+explorer(ctx,True)+source()
    if path=='/map/':
        import seo
        import json
        records = list(seo.ENRICHED.values())
        map_data = []
        for r in records:
            g = r.get('geo') or {}
            coords = [g['lng'], g['lat']] if isinstance(g.get('lat'), (int,float)) and isinstance(g.get('lng'), (int,float)) else None
            photos = r.get('photos', {}).get('usable', [])
            hero_photo = next((p for p in photos if p.get('era') in ('current','now')), photos[0] if photos else None)
            if hero_photo:
                photo_src = hero_photo.get('file') or hero_photo.get('local_path') or hero_photo.get('url')
            else:
                import os as _os
                _cand = r['id']
                if not _os.path.exists(f"site/assets/{_cand}.webp"):
                    _linked = (ctx.get('links') or {}).get(r['id']) or []
                    _cand = next((x for x in _linked if _os.path.exists(f"site/assets/{x}.webp")), 'culture-street')
                photo_src = f"/assets/{_cand}.webp"
            kicker = ctx['copy'][r['id']]['kicker'] if r['id'] in ctx['copy'] else (ctx['period'](r) if r['type']=='event' else '')
            a = r.get('address') or {}
            address_th = ' · '.join(filter(None, [a.get('line_th'), a.get('district')])) if a else ''
            from seo_config import BASE_PATH as _BP
            _abs = lambda u: (_BP + u) if isinstance(u, str) and u.startswith('/') and not u.startswith(_BP + '/') else u
            map_data.append({'id': r['id'], 'name': r['name_th'], 'category': r.get('category'), 'coords': coords, 'photo': _abs(photo_src), 'kicker': kicker, 'url': _abs(ctx['url'](r)), 'address': address_th})
        map_json = json.dumps(map_data, ensure_ascii=False)
        body=intro('กางแผนที่ แล้วค่อย ๆ ไป','จากย่านยาวถึงเมืองเก่า · ภาพแผนที่จริงพร้อมภาพเทศบาลซ้อนทับ')
        body+=f'<div id="interactive-map-app" data-map-data="{e(map_json)}"></div>'
        body+='<noscript>'
        body+='''<section class="map-workspace" data-map-viewer><div class="map-toolbar"><div class="map-zones" role="group" aria-label="เลือกบริเวณแผนที่"><button type="button" data-map-zone="full" aria-pressed="true">เต็มภาพ</button><button type="button" data-map-zone="north" aria-pressed="false">ย่านยาว</button><button type="button" data-map-zone="old" aria-pressed="false">เมืองเก่า</button></div><div class="map-zoom"><button type="button" data-map-action="out" aria-label="ย่อแผนที่">−</button><output data-map-level aria-live="polite" aria-label="ระดับการขยาย">100%</output><button type="button" data-map-action="in" aria-label="ขยายแผนที่">+</button><button type="button" data-map-action="reset" aria-label="คืนขนาดแผนที่">↺</button></div></div><div class="map-stage" tabindex="0" role="region" aria-label="ภาพแผนที่ เลื่อนด้วยปุ่มลูกศร ขยายด้วยเครื่องหมายบวก ย่อด้วยเครื่องหมายลบ"><img class="map-image" src="/assets/municipal-map.png" width="1358" height="1938" alt="แผนที่ท่องเที่ยวตะกั่วป่าจากเทศบาล แสดงย่านยาว เมืองเก่า ถนน สถานที่ และหมายเลขร้าน" draggable="false" loading="eager"></div><div class="map-help"><span>ลากเพื่อเลื่อน · ใช้ปุ่ม + / − เพื่อขยาย</span><a href="/assets/municipal-map.png" target="_blank" rel="noopener">เปิดภาพเต็มในแท็บใหม่ ↗</a></div></section>'''
        body+=f'<p class="small map-source-caption">{MAP_NOTE} · หมายเลขและสัญลักษณ์บนภาพคงตามเอกสารต้นทาง</p><section class="section">'+heading('อ่านต่อ','พบจุดหมายแล้ว เปิดเรื่องของที่นี่','รายชื่อสถานที่ในคู่มือ · เลือกชื่อเพื่ออ่านต่อ')
        body+='<div class="map-place-index">'+''.join(f'<section><h3>{label}</h3><ul>'+''.join(f'<li>{ctx["a"](byid[id])}</li>' for id in ids)+'</ul></section>' for _,label,ids in GROUPS)+'</div></section>'
        body+='</noscript>'
        return body+source()
    if path=='/traditions/':
        return intro('เมื่อเมืองมีนัดหมาย','เรื่องราวของศรัทธาและประเพณีที่อยู่ในปฏิทินของเมือง')+'<p class="calendar-note">ช่วงเวลาตามเอกสารต้นทาง · ยังไม่ใช่กำหนดการยืนยันของปีปัจจุบัน</p>'+traditions(ctx)+source()
    if path=='/routes/':
        result=intro('เลือกจังหวะเดินของคุณ','สามชุดจุดหมาย ที่ชวนมองตะกั่วป่าผ่านคนละเรื่อง')+'<p class="route-notice">จัดกลุ่มตามความสนใจ ไม่กำหนดระยะทางหรือเวลาเดิน ตรวจสอบการเข้าชมและใช้แผนที่ประกอบก่อนเดินทาง</p><div class="route-jumps">'+''.join(f'<a href="#route-{i}">0{i} / {name}</a>' for i,(name,_) in enumerate(ctx['routes'],1))+'</div>'
        for i,(name,ids) in enumerate(ctx['routes'],1):
            result+=f'<section class="route-chapter" id="route-{i}"><div class="route-chapter-visual"><span class="giant-number">0{i}</span>{pic(ids[0])}<span class="chapter">TAKUA PA / WALK & READ</span></div><div class="route-chapter-copy"><h2>{name}</h2><ol class="stops">'+''.join(f'<li><span>{j:02d}</span><div><h3>{ctx["a"](byid[x])}</h3><p>{e(ctx["copy"][x]["kicker"])}</p></div></li>' for j,x in enumerate(ids,1))+'</ol><a class="text-link" href="/map/">เปิดแผนที่ประกอบ ↗</a></div></section>'
        return result+source()
    if path=='/eat/':
        body=body.replace('59 รายชื่อ','60 รายชื่อ').replace('59 รายชื่อและลำดับ','60 รายชื่อและลำดับ')
        start=body.index('<div class="filters">')
        # First-party listing: Siwara Cafe belongs in the drinks section, not restaurants.
        siwara_li='<li id="siwara-cafe" data-shop="ศิวรา คาเฟ่ Siwara Cafe"><span class="shop-number">—</span><span><a href="https://siwaracafe.com/" rel="noopener">ศิวรา คาเฟ่ · Siwara Cafe</a></span></li>'
        drinks_at=body.index('<ol class="shop-list">', body.index('<h2>เครื่องดื่ม'))
        cut=drinks_at+len('<ol class="shop-list">')
        body=body[:cut]+siwara_li+body[cut:]
        body=body.replace('59 รายชื่อ','60 รายชื่อ').replace('แสดง 59 ร้าน','แสดง 60 ร้าน').replace('<h2>เครื่องดื่ม <span class="count">19</span></h2>','<h2>เครื่องดื่ม <span class="count">20</span></h2>')
        tools=body[start:].replace('</select></label></div>','</select></label><button class="button button-outline" id="clear-shops" type="button">ล้างตัวกรอง</button></div>',1)
        return f'<header class="eat-intro"><div>{intro("อีกรสชาติของตะกั่วป่า","กิน ดื่ม และเลือกของฝากจากย่านเมืองเก่า")}<p>59 รายชื่อและลำดับตามแผ่นพับเทศบาล<br>ยังไม่ได้ยืนยันสถานะการเปิดร้านในปัจจุบัน</p></div><div class="eat-intro-art">{pic("food-center",True)}<span class="food-stamp">EAT<br>LOCAL</span></div></header>'+tools
    if record and record['type']=='place':
        id=record['id']; idx=ctx['places'].index(record); _,label=next((k,l) for k,l,ids in GROUPS if id in ids)
        hero=f'<div class="breadcrumbs"><a href="/">หน้าแรก</a><span>/</span><a href="/places/">สถานที่</a><span>/</span><span>{label}</span></div><header class="place-hero"><div class="place-hero-copy"><span class="chapter">FIELD NOTE {idx+1:02d} / {label}</span><h1>{e(record["name_th"])}</h1><p class="english">{e(record.get("name_en",""))}</p><p class="place-lead">{e(ctx["copy"][id]["kicker"])}</p><a class="text-link" href="#story">เปิดอ่านเรื่องของที่นี่ ↓</a></div><figure class="place-hero-art">{pic(id,True)}<figcaption><span>TAKUA PA / {idx+1:02d}</span><span>สถานที่ในเมืองตะกั่วป่า</span></figcaption></figure></header>'
        text=body[body.index('<h2>เรื่องของที่นี่</h2>'):body.index('<h2>อยู่ตรงไหนในย่าน</h2>')]
        text=text.replace('<h2>เรื่องของที่นี่</h2>',f'<span class="chapter">เรื่องของที่นี่</span><h2>{e(ctx["copy"][id]["kicker"])}</h2>',1)
        text=text.replace('<h2>รายละเอียดจากเอกสาร</h2>','<h2 id="details">รายละเอียดจากเอกสาร</h2>')
        # Facts already paraphrased in the lead remain available in a collapsible source excerpt.
        facts=''.join(f'<p>{e(f)}</p>' for f in record.get('facts_paraphrased',[]))
        if facts in text: text=text.replace(facts,f'<details class="document-excerpt"><summary>อ่านสาระจากเอกสารต้นทาง</summary>{facts}</details>',1)
        mini=f'<a class="mini-map-link" href="/map/"><img src="/assets/municipal-map.png" alt="แผนที่เทศบาลเมืองตะกั่วป่า" width="1358" height="1938" loading="lazy"><span><b>กางแผนที่ แล้วอ่านเมืองต่อ</b><small>เปิดภาพต้นทางจากเทศบาล ↗</small></span></a>'
        aside='<aside class="story-aside"><span class="chapter">ในบันทึกหน้านี้</span><a href="#story">เรื่องของที่นี่</a>'+('<a href="#details">รายละเอียดจากเอกสาร</a>' if 'id="details"' in text else '')+'<a href="#related">เกี่ยวข้องกัน</a><a href="/map/">กางแผนที่เมือง ↗</a></aside>'
        ids=next(ids for _,_,ids in GROUPS if id in ids)
        related=list(dict.fromkeys([x for x in ids if x!=id][:3]+ctx['links'].get(id,[])+[key for key,values in ctx['links'].items() if id in values]))
        rel_places=[x for x in related if byid[x]['type']=='place'][:3]; rel_events=[x for x in related if byid[x]['type']=='event']
        result=hero+'<div class="story-layout">'+aside+'<article class="story" id="story">'+text+mini+source()+'</article></div><section id="related" class="section related-section">'+heading('อ่านต่อ','อีกมุมของเมือง')+'<div class="related-grid">'+''.join(card(x,ctx) for x in rel_places)+'</div>'
        if rel_events: result+='<div class="related-events"><span class="eyebrow">ประเพณีที่เกี่ยวข้อง</span>'+''.join(ctx['a'](byid[x]) for x in rel_events)+'</div>'
        if not related: result+='<a class="text-link" href="/places/">กลับไปเลือกจากสถานที่ทั้ง 20 แห่ง ↗</a>'
        prev,nxt=ctx['places'][(idx-1)%20],ctx['places'][(idx+1)%20]
        return result+f'</section><nav class="page-turn" aria-label="เปิดสถานที่ก่อนหน้าหรือถัดไป"><a href="{ctx["url"](prev)}"><span>← บันทึกก่อนหน้า</span><b>{e(prev["name_th"])}</b></a><a href="{ctx["url"](nxt)}"><span>บันทึกถัดไป →</span><b>{e(nxt["name_th"])}</b></a></nav>'
    if record and record['type']=='event':
        related=ctx['links'].get(record['id'],[])
        result=intro(e(record['name_th']),ctx['period'](record))+'<div class="event-note"><span class="calendar-symbol" aria-hidden="true">✳</span><article><span class="chapter">ช่วงเวลาจากเอกสาร</span><h2>'+ctx['period'](record)+'</h2><p>รายการนี้ปรากฏในหมวดกิจกรรมและประเพณีของแผ่นพับเทศบาลเมืองตะกั่วป่า ช่วงเวลาข้างต้นยังไม่ใช่กำหนดการยืนยันของปีปัจจุบัน</p><a class="text-link" href="/traditions/">ดูประเพณีตลอดปี ↗</a></article></div>'
        if related: result+='<section class="section">'+heading('อ่านต่อ','สถานที่ที่เกี่ยวข้อง')+'<div class="related-grid">'+''.join(card(x,ctx) for x in related)+'</div></section>'
        return result+source()
    if path=='/about/':
        text=body[body.index('<h2>คู่มือจากบ้านศิวรา</h2>'):body.index('<h2>อ่านผังอย่างไร</h2>')]
        return intro('เมืองหนึ่งเมือง<br>เล่าได้อีกหลายหน้า','ที่มาของตะกั่วป่า 101 และเรื่องที่เราเลือกนำมาเล่า')+f'<div class="about-layout"><div class="about-illustration">{pic("culture-street",True)}<span class="chapter">TAKUA PA / PEOPLE & PLACES</span></div><article class="prose">{text}<h2>แผนที่ที่คุณเห็น</h2><p>{MAP_NOTE} เว็บไซต์ใช้ภาพแผนที่ต้นทางโดยตรง และให้ขยายหรือเลื่อนอ่านได้</p></article></div>'+source()
    if path=='/trip/':
        return intro('ทริปของคุณ','เลือกจุดหมายในเมืองเก่าตะกั่วป่า แล้วจัดเป็นเส้นทางเดินของคุณเอง')+'<div id="trip-app"></div><noscript><p>กรุณาเปิด JavaScript เพื่อจัดทริป หรือเลือกดู<a href="/places/">สถานที่ทั้งหมด</a>และ<a href="/map/">แผนที่</a></p></noscript>'
    return body

# ---- Phase 8: tourist-facing homepage blocks ----
def _load_json(rel, default):
    import json, os
    fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), rel)
    if not os.path.exists(fp):
        return default
    try:
        return json.load(open(fp, encoding='utf-8'))
    except Exception:
        return default


def quick_start():
    """Four large entry points so a first-time visitor never has to hunt."""
    items = [
        ('/map/', 'กางแผนที่', 'ดูว่าอะไรอยู่ตรงไหน', 'map'),
        ('/places/', 'เที่ยวไหนดี', '20 สถานที่ในเมืองเก่า', 'places'),
        ('/eat/', 'กินอะไรดี', '60 ร้านในย่าน', 'eat'),
        ('/trip/', 'จัดทริปของฉัน', 'เลือกเก็บไว้ แล้วเดินตามลำดับ', 'trip'),
    ]
    cards = ''
    for href, title, sub, key in items:
        badge = '<span class="qs-badge" data-trip-count hidden>0</span>' if key == 'trip' else ''
        cards += f'<a class="quick-card" href="{href}" data-qs="{key}"><span class="qs-icon" aria-hidden="true"></span><span class="qs-text"><b>{title}</b><small>{sub}</small></span>{badge}</a>'
    return f'<nav class="quick-start" aria-label="เริ่มต้นใช้งาน"><h2 class="visually-hidden">เริ่มที่นี่</h2>{cards}</nav>'


def city_feed(ctx, limit_news=8):
    """Stories + real city news, rendered server side so it works without JS."""
    import os, glob, json
    root = os.path.dirname(os.path.abspath(__file__))
    stories = []
    for fp in sorted(glob.glob(os.path.join(root, 'data', 'stories', '*.json'))):
        try:
            sd = json.load(open(fp, encoding='utf-8'))
        except Exception:
            continue
        if sd.get('id') and sd.get('sections'):
            stories.append(sd)
    if not stories:
        try:
            import stories as st
            stories = [{'id': x['id'], 'group': x['group'], 'title': x['title'], 'dek': x['dek']} for x in st.STORIES + [st.KUAPAPOH]]
        except Exception:
            stories = []
    _order = ['city', 'architecture', 'water-trade', 'food-people', 'kuapapoh']
    stories.sort(key=lambda x: _order.index(x['id']) if x.get('id') in _order else 99)
    news = _load_json('data/news-feed.json', [])[:limit_news]

    used = set()

    def story_card(sd, big=False):
        # A tile image must be specific to this story: reuse of one generic photo
        # across every card reads as a mistake, so fall back to the illustration
        # of the first place the story actually links to.
        import os as _os
        # Tiles use the commissioned illustrations: they are on-brand and each one
        # is distinct. Photographs stay inside the article where captions and
        # credits give them context.
        src = None
        for pid in (sd.get('places') or []):
            cand = f'/assets/{pid}.webp'
            if _os.path.exists('site' + cand) and cand not in used:
                src = cand
                break
        if not src:
            src = (sd.get('hero_photo') or {}).get('file')
        if src:
            used.add(src)
        img = f'<span class="sc-img"><img src="{e(src)}" alt="" loading="lazy"></span>' if src else ''
        mins = sd.get('reading_minutes')
        meta = f'<small>{mins} นาที</small>' if mins else ''
        return (f'<a class="story-tile{" story-tile-lead" if big else ""}" href="/stories/{e(sd["id"])}/">{img}'
                f'<span class="sc-body"><span class="chapter">{e(sd.get("group",""))}</span>'
                f'<b>{e(sd.get("title",""))}</b><p>{e(sd.get("dek",""))}</p>{meta}</span></a>')

    def news_item(n):
        d = n.get('date') or ''
        if d:
            try:
                y, m, dd = d.split('-')
                d = f'{int(dd)}/{int(m)}/{int(y)+543-2000+2500 if False else int(y)+543}'
            except Exception:
                pass
        place = f'<a href="{e(n["place_url"])}">{e(n["place_name"])}</a>' if n.get('place_url') else ''
        out = e(n.get('outlet') or '')
        link = f'<a class="news-out" href="{e(n["url"])}" target="_blank" rel="noopener">อ่านข่าวต้นทาง ↗</a>' if n.get('url') else ''
        return (f'<li class="news-row"><span class="news-date">{e(d)}</span>'
                f'<span class="news-main"><b>{e(n.get("title_th",""))}</b>'
                f'<span class="news-meta">{place}{" · " + out if out else ""}</span>{link}</span></li>')

    left = ''.join(story_card(sd, i == 0) for i, sd in enumerate(stories[:5]))
    right = ''.join(news_item(n) for n in news)
    return (
        '<section class="section city-feed" id="city-feed">'
        + heading('02', 'กระทู้และข่าวสารของเมือง', 'เรื่องเล่าที่เรียบเรียงไว้ และความเคลื่อนไหวล่าสุดในตะกั่วป่า')
        + '<div class="city-feed-grid">'
        + f'<div class="cf-stories"><h3 class="cf-title">เรื่องเล่าของเมือง</h3><div class="story-tiles">{left}</div>'
          '<a class="text-link" href="/stories/">อ่านเรื่องเล่าทั้งหมด ↗</a></div>'
        + f'<div class="cf-news"><h3 class="cf-title">ความเคลื่อนไหวล่าสุด</h3><ol class="news-list">{right}</ol>'
          '<a class="text-link" href="/news/">ดูความเคลื่อนไหวทั้งหมด ↗</a>'
          '<p class="small">รวบรวมจากข่าวสาธารณะ · ตรวจกำหนดการกับผู้จัดก่อนเดินทาง</p></div>'
        + '</div></section>')


def shell(path, html):
    html=html.replace('/assets/site.css','/assets/design.css').replace('/assets/site.js','/assets/design.js')
    html=html.replace('<body>',f'<body class="{"home" if path=="/" else "inner-page"}">')
    html=re.sub(r'<header class="nav">.*?</header>',lambda m:m.group().replace('class="nav"','class="site-header"').replace('<a class="brand" href="/">ตะกั่วป่า <span>101</span></a>','<a class="brand" href="/" aria-label="ตะกั่วป่า 101 หน้าแรก"><span class="brand-mark">๑๐๑</span><span>ตะกั่วป่า<small>TAKUA PA FIELD NOTES</small></span></a>').replace('</nav>','</nav><a class="header-map" href="/map/">เปิดแผนที่ ↗</a>'),html,count=1)
    footer='<footer class="site-footer"><div class="footer-top"><a href="/" class="footer-name">ตะกั่วป่า <em>101</em></a><p>เมืองหนึ่งเมือง<br>มีเรื่องให้ค่อย ๆ รู้จัก</p><a class="round-link" href="#main" aria-label="กลับขึ้นด้านบน">↑</a></div><div class="footer-bottom"><a href="https://siwaracafe.com/">จัดทำโดยบ้านศิวรา ตะกั่วป่า</a><span>คู่มือเมืองเก่า · จังหวัดพังงา</span><a href="https://www.takuapacity.go.th/pdf/travel-preview.pdf">แผ่นพับต้นทาง ↗</a></div></footer>'
    html=re.sub(r'<footer>.*?</footer>',lambda m:footer,html,count=1)
    if path == '/map/':
        html=html.replace('</head>', '<style>@import url("https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/5.6.1/maplibre-gl.css");</style>\n<script src="https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/5.6.1/maplibre-gl.js"></script>\n</head>')
    html=html.replace('</head>','<meta name="theme-color" content="#203f39"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"></head>')
    return html
