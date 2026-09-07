"""Browser acceptance checks for Phase 3, including static fallback."""
import sys,json
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).parent
QA=ROOT/'qa/2026-09-07-phase3';QA.mkdir(parents=True,exist_ok=True)
BASE='http://127.0.0.1:8095/takuapa'
data=json.loads((ROOT/'data/places-enriched.json').read_text(encoding='utf-8'))
report={'screenshots':[],'checks':[],'console_errors':[],'failed_responses':[]}
with sync_playwright() as p:
    browser=p.chromium.launch()
    for enabled in [True,False]:
        for width in [1440,390]:
            context=browser.new_context(java_script_enabled=enabled,viewport={'width':width,'height':1000 if width==1440 else 844})
            page=context.new_page()
            page.on('pageerror',lambda e:report['console_errors'].append(str(e)))
            page.on('console',lambda m:report['console_errors'].append(m.text) if m.type=='error' else None)
            page.on('response',lambda r:report['failed_responses'].append(r.url) if r.status>=400 else None)
            for rid in ['tao-ming','wat-boromthat','culture-street']:
                r=next(r for r in data if r['id']==rid)
                page.goto(BASE+'/places/'+rid+'/');page.evaluate('document.fonts.ready')
                assert page.locator('[data-era]').count()==3
                assert page.locator('h1').count()==1
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
                assert page.locator('#faq details').count()==len(__import__('seo').faq(r))
                assert page.locator('#sources .unknowns li').count()==len(r['unknowns'])
                images=page.locator('img').evaluate_all('(els)=>els.map(e=>e.getAttribute("src"))')
                forbidden={p.get('url') or p.get('file') for p in r['photos']['needs_permission']}
                assert not forbidden.intersection(images)
                for img in page.locator('img').all():
                    img.scroll_into_view_if_needed();img.evaluate('(e)=>e.decode()')
                card=page.locator('.visit-card').bounding_box();body=page.locator('.research-body').bounding_box()
                assert card['x']>=body['x']+body['width']-1 if width==1440 else card['y']+card['height']<=body['y']
                if enabled and r['photos']['usable']:
                    page.locator('[data-tab="archive"]').click()
                    assert page.locator('[data-panel="archive"]').is_visible()
                    page.locator('[data-tab="today"]').focus();page.keyboard.press('Home')
                    page.locator('[data-lightbox]:visible').first.click()
                    assert page.locator('dialog').is_visible()
                    page.keyboard.press('Escape');assert not page.locator('dialog').is_visible()
                if not enabled and r['photos']['usable']:
                    assert page.locator('[data-panel]:visible').count()==2
                    assert page.locator('[data-lightbox]').count()==len(r['photos']['usable'])
                if enabled:
                    page.locator('#sources').scroll_into_view_if_needed();page.wait_for_timeout(100)
                    assert page.locator('.research-rail a[aria-current]').get_attribute('href')=='#sources'
                    page.evaluate('scrollTo(0,0)');page.wait_for_timeout(100)
                    name=f'{rid}-{width}.png';page.screenshot(path=str(QA/name),full_page=True);report['screenshots'].append(name)
                report['checks'].append(f'{rid} · {width}px · JS {enabled}: eras, FAQ, unknowns, photo permissions, layout, images OK')
            page.goto(BASE+'/stories/kuapapoh/')
            assert page.locator('#project-gallery [data-lightbox]').count()==6
            context.close()
    browser.close()
assert not report['console_errors'],report['console_errors']
assert not report['failed_responses'],report['failed_responses']
(QA/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
