import asyncio,functools,http.server,os,socketserver,sys,threading
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright
SITE=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'site')
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=SITE)
class S(socketserver.TCPServer): allow_reuse_address=True
srv=S(("127.0.0.1",8788),H); threading.Thread(target=srv.serve_forever,daemon=True).start()
async def main():
    async with async_playwright() as pw:
        br=await pw.chromium.launch(); pg=await br.new_page(viewport={"width":1200,"height":900})
        await pg.goto("http://127.0.0.1:8788/eat/index.html",wait_until="networkidle")
        for term in ["ศิวรา","บอร์ดเกม","เค้ก","บ้านไม้","Siwara"]:
            await pg.fill("#shop-search",term); await pg.wait_for_timeout(300)
            names=await pg.eval_on_selector_all("[data-shop]",
              "e=>e.filter(x=>x.offsetParent!==null).map(x=>x.querySelector('a')?.textContent||'').slice(0,3)")
            print('ค้น %-10s เจอ %d · %s'%(term,len(names),' , '.join(n[:24] for n in names)))
        await br.close()
asyncio.run(main()); srv.shutdown()
