"""End-to-end local QA for the completed redesign; no external browsing."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import argparse, hashlib, json, sys
from seo_config import BASE_PATH
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
SITE=ROOT/'site'
QA=ROOT/'qa'/'2026-09-07-redesign'
QA.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser()
parser.add_argument('--base',default='http://127.0.0.1:8091'+BASE_PATH)
args=parser.parse_args()
BASE=args.base.rstrip('/')
class Document(HTMLParser):
    def __init__(self):
        super().__init__();self.refs=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag in ['a','img','script','link']:
            ref=attrs.get('href',attrs.get('src',''))
            if ref:self.refs.append(ref)
files=list(SITE.rglob('index.html'))
assert len(files)==40
parsed={}
for file in files:
    raw=file.read_text(encoding='utf-8');doc=Document();doc.feed(raw);parsed[file]=doc
    assert len(doc.ids)==len(set(doc.ids)),f'Duplicate IDs: {file}'
    assert 'index,follow,max-image-preview:large' in raw
    assert '\ufffd' not in raw
    assert 'street-map' not in raw and '<svg' not in raw, f'Obsolete traced map: {file}'
    for banned in ['ภาพวาดประกอบ','ภาพวาดจากภาพถ่ายบ้านศิวรา','ไม่ใช่แผนที่นำทาง','Paint','Lab.เล่าหุ้น']:
        assert banned not in raw,(file,banned)
for file,doc in parsed.items():
    for ref in doc.refs:
        part=urlparse(ref)
        if part.scheme or part.netloc:continue
        target=SITE/unquote(part.path.removeprefix(BASE_PATH)).lstrip('/') if part.path.startswith('/') else file.parent/unquote(part.path)
        if not part.path:target=file
        elif part.path.endswith('/'):target=target/'index.html'
        assert target.exists(),(file,ref)
        if part.fragment and target in parsed:assert unquote(part.fragment) in parsed[target].ids,(file,ref,'missing anchor')
source=ROOT.parents[1]/'library/2026-09-06_takuapa-siwara-v1/source/maps.png'
assert hashlib.sha256(source.read_bytes()).digest()==hashlib.sha256((SITE/'assets/municipal-map.png').read_bytes()).digest()
report={'pages':40,'map_matches_user_source':True,'checked_routes':[],'screenshots':[],'errors':[],'failed_responses':[],'checks':[]}
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
    page.on('pageerror',lambda error:report['errors'].append(str(error)))
    page.on('response',lambda r:report['failed_responses'].append(r.url) if r.status>=400 and r.url.startswith(BASE) else None)
    for width in [1440,390]:
        page.set_viewport_size({'width':width,'height':1000 if width==1440 else 844})
        for file in files:
            route='/'+file.parent.relative_to(SITE).as_posix().strip('.')+'/'
            route=route.replace('//','/')
            response=page.goto(BASE+route)
            assert response.status==200,route
            page.evaluate('document.fonts.ready')
            assert page.locator('h1').count()==1,route
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,route,'overflow')
            assert page.locator('link[rel=stylesheet]').get_attribute('href')==BASE_PATH+'/assets/design.css'
            for block in page.locator('script[type="application/ld+json"]').all():json.loads(block.text_content())
            report['checked_routes'].append([width,route])
        for route,name in [('/','home'),('/places/','places'),('/places/wat-boromthat/','place'),('/map/','map'),('/eat/','eat'),('/routes/','routes'),('/traditions/','traditions'),('/traditions/vegetarian/','event'),('/about/','about'),('/stories/','stories'),('/stories/city/','story-city'),('/stories/architecture/','story-architecture'),('/stories/water-trade/','story-water'),('/stories/food-people/','story-food'),('/stories/kuapapoh/','story-kuapapoh')]:
            page.goto(BASE+route);page.evaluate('document.fonts.ready');page.wait_for_timeout(450)
            filename=f'{name}-{width}.png';page.screenshot(path=str(QA/filename),full_page=True);report['screenshots'].append(filename)
            if name in ['home','map']:
                page.screenshot(path=str(QA/f'{name}-{width}-viewport.png'))
    page.goto(BASE+'/places/')
    for cat,count in [('temple',6),('shrine',4),('heritage',4),('park',2),('market',3),('museum',1),('all',20)]:
        page.locator(f'[data-filter="{cat}"]').click()
        assert page.locator('[data-place-card]:visible').count()==count,cat
    page.locator('[data-place-search]').fill('ปุนเถ่ากง')
    assert page.locator('[data-place-card]:visible').count()==1
    assert 'pun-thao' in page.locator('[data-place-card]:visible img').get_attribute('src')
    page.locator('[data-filter="temple"]').click();assert page.locator('[data-place-empty]').is_visible()
    page.locator('[data-clear-places]').click();assert page.locator('[data-place-card]:visible').count()==20
    report['checks'].append('All six place filters, Thai search, combined empty state and reset')
    page.goto(BASE+'/eat/')
    for cat,count in [('restaurant',33),('drink_shop',19),('souvenir_shop',8),('all',60)]:
        page.locator('#shop-category').select_option(cat);assert page.locator('[data-shop]:visible').count()==count
    page.locator('#shop-search').fill('ฮกกี่เหลา');assert page.locator('[data-shop]:visible').count()==1
    page.locator('#shop-search').fill('no-result-123');assert page.locator('#empty').is_visible()
    page.locator('#clear-shops').click();assert page.locator('[data-shop]:visible').count()==60
    assert page.locator('#siwara-cafe a').get_attribute('href')=='https://siwaracafe.com/'
    report['checks'].append('60 businesses including first-party Siwara Cafe, each category, Thai search, empty state and reset')
    page.goto(BASE+'/traditions/')
    assert page.locator('.tradition').count()==7
    page.locator('.tradition summary').first.click();assert page.locator('.tradition').first.get_attribute('open') is not None
    page.locator('.tradition .event-body a').last.is_enabled()
    report['checks'].append('Seven accessible native tradition disclosures')
    for width in [1440,390]:
        page.set_viewport_size({'width':width,'height':900})
        page.goto(BASE+'/map/');page.locator('.map-stage.ready').wait_for()
        assert page.locator('[data-map-level]').text_content()=='100%'
        page.locator('[data-map-action="in"]').click();assert int(page.locator('[data-map-level]').text_content().strip('%'))>100
        page.locator('[data-map-action="reset"]').click();assert page.locator('[data-map-level]').text_content()=='100%'
        for zone in ['north','old']:
            page.locator(f'[data-map-zone="{zone}"]').click();assert page.locator(f'[data-map-zone="{zone}"]').get_attribute('aria-pressed')=='true'
            assert int(page.locator('[data-map-level]').text_content().strip('%'))>100
        page.locator('[data-map-action="in"]').click()
        stage=page.locator('.map-stage');stage.scroll_into_view_if_needed();box=stage.bounding_box()
        before=page.locator('.map-image').get_attribute('style')
        page.mouse.move(box['x']+box['width']*.55,box['y']+box['height']*.55)
        page.mouse.down();page.mouse.move(box['x']+box['width']*.55+60,box['y']+box['height']*.55+60,steps=8);page.mouse.up()
        assert page.locator('.map-image').get_attribute('style')!=before
        stage.focus();page.keyboard.press('Home');assert page.locator('[data-map-level]').text_content()=='100%'
        page.keyboard.press('+');assert page.locator('[data-map-level]').text_content()=='140%'
        if width==1440:page.screenshot(path=str(QA/'map-zoomed-desktop.png'))
    report['checks'].append('Original image map: zone framing, zoom, reset, mouse drag and keyboard controls at both widths')
    touch=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
    mobile=touch.new_page();mobile.goto(BASE+'/map/');mobile.locator('.map-stage.ready').scroll_into_view_if_needed()
    box=mobile.locator('.map-stage').bounding_box();cx=box['x']+box['width']/2;cy=max(180,box['y']+150)
    cdp=touch.new_cdp_session(mobile)
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':cx-35,'y':cy,'id':1},{'x':cx+35,'y':cy,'id':2}]})
    cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':cx-70,'y':cy,'id':1},{'x':cx+70,'y':cy,'id':2}]})
    cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    assert mobile.locator('[data-map-level]').text_content()=='200%'
    mobile.screenshot(path=str(QA/'map-pinch-mobile.png'));touch.close()
    report['checks'].append('Mobile two-finger pinch doubles scale from 100% to 200%')
    page.set_viewport_size({'width':1280,'height':900})
    for route in ['/','/places/','/map/','/eat/','/places/wat-boromthat/','/routes/','/traditions/','/about/','/stories/','/stories/city/']:
        page.goto(BASE+route);page.evaluate("document.documentElement.style.fontSize='200%'");page.evaluate('document.fonts.ready')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(route,'200% text overflow')
    report['checks'].append('200% text enlargement across all primary page types at 1280px')
    nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
    fallback=nojs.new_page();fallback.goto(BASE+'/places/');assert fallback.locator('[data-place-card]:visible').count()==20
    fallback.goto(BASE+'/map/');assert fallback.locator('.map-image').is_visible();assert fallback.locator('.map-place-index a').count()==20
    fallback.goto(BASE+'/stories/');assert fallback.locator('.story-card').count()==5
    nojs.close();report['checks'].append('No-JS place index and original map fallback')
    page.emulate_media(reduced_motion='reduce');page.goto(BASE+'/');assert page.locator('.hero-copy').evaluate('(e)=>getComputedStyle(e).animationName')=='none'
    report['checks'].append('Reduced-motion setting respected')
    browser.close()
assert not report['errors'],report['errors']
assert not report['failed_responses'],report['failed_responses']
(QA/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pages':40,'responsive_route_checks':len(report['checked_routes']),'screenshots':len(report['screenshots']),'errors':report['errors'],'checks':report['checks']},ensure_ascii=False))
