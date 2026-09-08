import asyncio,functools,http.server,os,socketserver,sys,threading
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright
SITE=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'site')
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=SITE)
class S(socketserver.TCPServer): allow_reuse_address=True
srv=S(("127.0.0.1",8790),H); threading.Thread(target=srv.serve_forever,daemon=True).start()
async def main():
    async with async_playwright() as pw:
        br=await pw.chromium.launch()
        for w in (390,1100):
            pg=await br.new_page(viewport={"width":w,"height":900})
            bad=[]; pg.on("response",lambda r: bad.append(r.status) if r.status>=400 else None)
            await pg.goto("http://127.0.0.1:8790/stories/apaporn/index.html",wait_until="networkidle")
            await pg.evaluate("()=>window.scrollTo(0,document.body.scrollHeight)")
            await pg.wait_for_timeout(2500)
            res=await pg.eval_on_selector_all("main img",
              "e=>e.map(x=>({s:x.getAttribute('src').split('/').pop(),ok:x.naturalWidth>0}))")
            over=await pg.evaluate("()=>document.documentElement.scrollWidth-document.documentElement.clientWidth")
            miss=[r['s'] for r in res if not r['ok']]
            print(f"{w}px · รูป {len(res)} ใบ · โหลดไม่ขึ้น {miss or 'ไม่มี'} · ล้น {over}px · 4xx/5xx {bad or 'ไม่มี'}")
            await pg.close()
        await br.close()
asyncio.run(main()); srv.shutdown()
