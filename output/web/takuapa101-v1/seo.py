"""ข้อมูล SEO จากระเบียนต้นทาง โดยไม่เติมข้อเท็จจริงที่ขาดหาย"""
import json, re
from html import escape
from seo_config import ROOT, SITE_BASE_URL, BASE_PATH
ENRICHED = {r['id']: r for r in json.loads((ROOT/'data/places-enriched.json').read_text(encoding='utf-8'))}

def clean(text):
    return str(text).replace('—', '·').replace('–', '·').strip()

def usable(text):
    return isinstance(text, str) and bool(text.strip()) and not any(x in text for x in ['ไม่พบ', 'ไม่ทราบ', 'ยังไม่พบ', 'ไม่ระบุ', 'ยังไม่ยืนยัน'])

def faq(record):
    result=[]
    def add(q, a, status=None):
        if usable(a):
            if status in ('UNKNOWN', 'DISPUTED'): return
            prefix='ข้อมูลยังไม่ยืนยัน · ' if status=='UNVERIFIED' else ''
            result.append((q, prefix+clean(a)))
    v=record.get('visit') or {}
    for key,q,status in [('opening_hours_th','เปิดให้เข้าชมเวลาใด','opening_hours_status'),('admission_fee_th','มีค่าเข้าชมหรือไม่','admission_status'),('parking_th','มีที่จอดรถไหม',None),('dress_code_th','ควรแต่งกายอย่างไร',None)]:
        add(q,v.get(key),v.get(status) if status else None)
    for route in record.get('getting_there',[]):
        if route.get('from'): add('เดินทางจาก'+route['from']+'อย่างไร',route.get('text_th'),route.get('status'))
        if len(result)>=4: break
    history=[h['claim_th'] for h in record.get('history',[]) if h.get('status')=='CONFIRMED' and usable(h.get('claim_th'))]
    if history: add('สถานที่นี้มีประวัติความเป็นมาอย่างไร',' '.join(history[:2]))
    highlights=[h['detail_th'] for h in record.get('highlights',[]) if usable(h.get('detail_th')) and h.get('status') not in ('UNVERIFIED','DISPUTED')]
    if highlights: add('มีจุดเด่นอะไรให้ชม',' '.join(highlights[:3]))
    if len(result)<3 and record.get('brochure_facts'): add('เอกสารเทศบาลกล่าวถึงที่นี่อย่างไร',' '.join(record['brochure_facts']))
    return result[:6]

def address(r):
    a=r.get('address') or {}
    fields={out:clean(a[key]) for key,out in [('line_th','streetAddress'),('district','addressLocality'),('province','addressRegion'),('postcode','postalCode')] if a.get(key)}
    return {'@type':'PostalAddress',**fields,'addressCountry':'TH'} if fields else None

def entity(r, canonical):
    event=r.get('category')=='tradition' or r['type']=='event'
    facts=r.get('brochure_facts') or [r.get('editorial_angle')]
    s={'@context':'https://schema.org','@type':'Event' if event else 'TouristAttraction','name':clean(r['name_th']),'url':canonical,'image':SITE_BASE_URL+'/assets/'+r['id']+'.webp'}
    if event:s['image']=SITE_BASE_URL+'/assets/og/'+r['id']+'.png'
    description=' '.join(clean(x) for x in facts if x)
    if description:s['description']=description
    a=address(r)
    if not event:
        if a:s['address']=a
        g=r.get('geo') or {}
        if isinstance(g.get('lat'),(int,float)) and isinstance(g.get('lng'),(int,float)):
            s['geo']={'@type':'GeoCoordinates','latitude':g['lat'],'longitude':g['lng']}
        c=r.get('contact') or {}
        if c.get('phone'):s['telephone']=c['phone']
        same=[c[k] for k in ('facebook','website') if c.get(k) and c[k].startswith(('https://','http://'))]
        if same:s['sameAs']=same
        v=r.get('visit') or {}
        # Only parse a complete, unambiguous weekly statement, never a historical/conflicting schedule.
        m=re.fullmatch(r'วันอาทิตย์ (\d{2})[.:](\d{2})[–-](\d{2})[.:](\d{2}) น\.',v.get('opening_hours_th') or '')
        if v.get('opening_hours_status')=='CONFIRMED' and m:
            s['openingHoursSpecification']=[{'@type':'OpeningHoursSpecification','dayOfWeek':'https://schema.org/Sunday','opens':m[1]+':'+m[2],'closes':m[3]+':'+m[4]}]
    else:
        f=r.get('festival') or {}
        if f.get('venue_th'):s['location']={'@type':'Place','name':clean(f['venue_th'])}
        if f.get('activities_th'):s['description']=' · '.join(clean(x) for x in f['activities_th'])
        # Exclude approximate lunar months and evidence limited to one past year.
        months=['มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม']
        value=(f.get('months_th') or '').strip()
        if value in months:s['eventSchedule']={'@type':'Schedule','repeatFrequency':'P1Y','byMonth':months.index(value)+1}
    return s

# บ้านศิวราเป็นผู้จัดทำเว็บนี้ · ประกาศเป็น Organization ในช่อง publisher
# ซึ่งเป็นช่องที่ถูกต้องสำหรับองค์กร · ช่อง author ไว้สำหรับคนที่เขียนจริง
# เนื้อหาบทความเรียบเรียงจากเอกสารราชการ จึงไม่อ้างว่าคาเฟ่เป็นผู้เขียน
PUBLISHER = {
    '@type': 'Organization',
    'name': 'บ้านศิวรา ตะกั่วป่า',
    'alternateName': ['ศิวรา คาเฟ่', 'Siwara Cafe', 'Baan Siwara Takua Pa'],
    'url': 'https://siwaracafe.com/',
    'sameAs': ['https://siwaracafe.com/',
               'https://www.facebook.com/siwaracafetakuapa/',
               'https://www.instagram.com/si.wara_cafe/'],
}


def article_schema(canonical, title, desc, story, og_image):
    """Article schema ให้หน้ากระทู้ · เดิมหน้าพวกนี้มีแค่ BreadcrumbList
    เสิร์ชเอนจินจึงไม่รู้ว่าเป็นบทความ ใครจัดทำ และอัปเดตเมื่อไร"""
    updated = (story.get('updated') or '').strip()
    d = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': title[:110],
        'description': desc,
        'mainEntityOfPage': {'@type': 'WebPage', '@id': canonical},
        'url': canonical,
        'inLanguage': 'th-TH',
        'publisher': PUBLISHER,
        'isPartOf': {'@type': 'WebSite', 'name': 'ตะกั่วป่า 101', 'url': SITE_BASE_URL + '/'},
        'about': {'@type': 'Place', 'name': 'เมืองเก่าตะกั่วป่า จังหวัดพังงา'},
    }
    if updated:
        d['datePublished'] = updated
        d['dateModified'] = updated
    if og_image:
        d['image'] = og_image
    return d


SHOP_TYPE = {'restaurant': 'Restaurant', 'drink_shop': 'CafeOrCoffeeShop',
             'souvenir_shop': 'Store'}


def shop_entity(r, canonical):
    """structured data ของร้านที่ค้นข้อมูลมาแล้ว · ใส่เฉพาะ field ที่มีข้อมูลจริง
    ห้ามเดา เพราะ schema ที่กรอกมั่วเสียหายกว่าไม่มี"""
    node = {'@type': SHOP_TYPE.get(r.get('category'), 'LocalBusiness'),
            'name': r.get('name_th'),
            'url': canonical + '#' + r['id']}
    # ร้านที่มีเว็บของตัวเอง ใช้ @id เดียวกับที่เว็บนั้นประกาศไว้
    # เสิร์ชเอนจินจะได้รู้ว่าเป็นกิจการเดียวกัน ไม่ใช่คนละแห่งที่ชื่อพ้องกัน
    if r.get('id') == 'siwara-cafe':
        node['@id'] = 'https://siwaracafe.com/#cafe'
        node['sameAs'] = ['https://siwaracafe.com/',
                          'https://www.facebook.com/siwaracafetakuapa/',
                          'https://www.instagram.com/si.wara_cafe/']
    if r.get('name_en'):
        node['alternateName'] = r['name_en']
    if r.get('one_liner_th'):
        node['description'] = r['one_liner_th']
    if r.get('address_th'):
        node['address'] = {'@type': 'PostalAddress', 'streetAddress': r['address_th'],
                           'addressLocality': 'ตะกั่วป่า', 'addressRegion': 'พังงา',
                           'addressCountry': 'TH'}
    g = r.get('geo') or {}
    if g.get('lat') and g.get('lng'):
        node['geo'] = {'@type': 'GeoCoordinates', 'latitude': g['lat'], 'longitude': g['lng']}
    if r.get('phone'):
        digits = ''.join(c for c in r['phone'] if c.isdigit())
        node['telephone'] = ('+66' + digits[1:]) if digits.startswith('0') else r['phone']
    if r.get('website'):
        node['url'] = r['website']
    if r.get('google_maps_url'):
        node['hasMap'] = r['google_maps_url']
    if r.get('price_range_symbol'):
        node['priceRange'] = r['price_range_symbol']
    if r.get('signature_th'):
        node['makesOffer'] = [{'@type': 'Offer', 'itemOffered':
                               {'@type': 'MenuItem' if r.get('category') != 'souvenir_shop' else 'Product',
                                'name': x}} for x in r['signature_th'][:5]]
    return node


def schemas(path,title,record,body,story=None,og_image=None):
    canonical=SITE_BASE_URL+path
    result=[{'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'หน้าแรก','item':SITE_BASE_URL+'/'}]+([{'@type':'ListItem','position':2,'name':title,'item':canonical}] if path!='/' else [])}]
    if story:
        result.append(article_schema(canonical, title, story.get('dek',''), story, og_image))
    if path=='/':result.append({'@context':'https://schema.org','@type':'WebSite','name':'ตะกั่วป่า 101','url':canonical,'potentialAction':{'@type':'SearchAction','target':{'@type':'EntryPoint','urlTemplate':SITE_BASE_URL+'/places/?q={search_term_string}'},'query-input':'required name=search_term_string'},'publisher':{'@type':'Organization','name':'บ้านศิวรา ตะกั่วป่า','alternateName':'Baan Siwara Takua Pa','url':'https://siwaracafe.com/','sameAs':['https://siwaracafe.com/','https://www.facebook.com/siwaracafetakuapa/']},'isPartOf':{'@type':'WebSite','url':'https://siwaracafe.com/'}})
    if record:
        r=ENRICHED[record['id']];result.append(entity(r,canonical))
        questions=faq(r) if r['type']=='place' else []
        if questions:
            result.append({'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in questions]})
            section='<section class="section"><h2>คำถามที่พบบ่อย</h2>'+''.join('<details><summary>'+escape(q)+'</summary><p>'+escape(a)+'</p></details>' for q,a in questions)+'</section>'
            if '<!--PLACE_FAQ-->' in body:
                body=body.replace('<!--PLACE_FAQ-->', ''.join('<details><summary>'+escape(q)+'</summary><p>'+escape(a)+'</p></details>' for q,a in questions))
            else: body+=section
    elif path in ('/','/places/','/traditions/','/map/','/routes/','/eat/','/stories/'):
        from html.parser import HTMLParser
        class Links(HTMLParser):
            def __init__(self):super().__init__();self.links=[]
            def handle_starttag(self,tag,attrs):
                href=dict(attrs).get('href','')
                if tag=='a' and href.startswith(('/places/','/traditions/','/stories/')) and href.count('/')>=3 and '#' not in href:self.links.append(href)
        p=Links();p.feed(body)
        items=list(dict.fromkeys(p.links))
        if path=='/eat/':
            library=json.loads((ROOT/'data/library.json').read_text(encoding='utf-8'))
            result.append({'@context':'https://schema.org','@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i,'name':r['name_th'],'url':canonical+'#'+r['id']} for i,r in enumerate([r for r in library['records'] if r['type']=='business_directory'],1)]})
        if path=='/eat/':
            try:
                extra=json.loads((ROOT/'data/shops-extra.json').read_text(encoding='utf-8'))
                extra=extra if isinstance(extra,list) else extra.get('shops',[])
            except Exception:
                extra=[]
            rich=[shop_entity(r,canonical) for r in extra if r.get('address_th') or r.get('website')]
            if rich:
                result.append({'@context':'https://schema.org','@type':'ItemList',
                               'name':'ร้านอาหาร คาเฟ่ และของฝากในอำเภอตะกั่วป่า',
                               'itemListElement':[{'@type':'ListItem','position':i,'item':n}
                                                  for i,n in enumerate(rich,1)]})
        if items:result.append({'@context':'https://schema.org','@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i,'url':SITE_BASE_URL+u} for i,u in enumerate(items,1)]})
    return result,body

def prefix_links(html):
    return re.sub(r'\b(href|src|action|poster)=( ["\']|["\'])(/(?!/)[^"\']*)',lambda m:m[1]+'='+m[2]+BASE_PATH+m[3],html)
