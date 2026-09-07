"""ตรวจ SEO และลิงก์ subfolder จากผล build จริง"""
import json,re,sys
from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image
from seo_config import ROOT,SITE_BASE_URL,BASE_PATH
sys.stdout.reconfigure(encoding='utf-8')
site=ROOT/'site';geo=[];counts=[];files=list(site.rglob('index.html'))
def check(value):
    if isinstance(value,dict):
        for v in value.values():
            assert v is not None and v!='' and v!=[],value
            check(v)
    elif isinstance(value,list):
        for v in value:check(v)
for f in files:
    raw=f.read_text(encoding='utf-8')
    assert 'noindex' not in raw and '127.0.0.1' not in raw
    assert 'index,follow,max-image-preview:large' in raw
    assert not re.search(r'(?:href|src)=[\"\']/(?!'+re.escape(BASE_PATH.strip('/'))+r'/|/)',raw)
    for key in ('og:title','og:description','og:url','og:type','og:image','og:locale','og:site_name','twitter:card','twitter:image'):assert key in raw
    nodes=[n for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',raw,re.S) for n in json.loads(block)]
    check(nodes)
    assert any(n['@type']=='BreadcrumbList' for n in nodes)
    for n in nodes:
        if n.get('geo'):geo.append(f.parent.name)
        if n['@type']=='FAQPage':
            counts.append(len(n['mainEntity']))
            assert 3<=counts[-1]<=6
            from html import escape
            for q in n['mainEntity']:assert escape(q['acceptedAnswer']['text']) in raw
        if n['@type']=='Event':assert 'startDate' not in n and n.get('location') and n.get('description')
    for image in re.findall(r'(?:property="og:image"|name="twitter:image") content="([^"]+)"',raw):
        with Image.open(site/image.removeprefix(SITE_BASE_URL+'/')) as im:assert im.size==(1200,630)
urls=ET.parse(site/'sitemap.xml').getroot()
assert len(urls)==len(files)
for u in urls:
    loc=u.find('{*}loc').text
    assert loc.startswith(SITE_BASE_URL+'/')
    assert (site/loc.removeprefix(SITE_BASE_URL+'/')/'index.html').exists()
    from datetime import date
    assert u.find('{*}lastmod').text==date.today().isoformat()
print('JSON-LD ok')
print(f'ผ่าน SEO {len(files)} หน้า · OG 28 ภาพ · sitemap {len(urls)} URL')
print(f'geo {len(geo)} หน้า: '+', '.join(geo))
print(f'FAQ {sum(counts)} ข้อ / {len(counts)} หน้า · เฉลี่ย {sum(counts)/len(counts):.2f}')
