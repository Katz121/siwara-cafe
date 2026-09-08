import asyncio,http.server,socketserver,threading,functools,os,sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site')
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=os.path.abspath(ROOT))
class S(socketserver.TCPServer): allow_reuse_address=True
srv=S(("127.0.0.1",8795),H); threading.Thread(target=srv.serve_forever,daemon=True).start()
async def main():
    async with async_playwright() as pw:
        br=await pw.chromium.launch(); pg=await br.new_page(viewport={"width":390,"height":844})
        await pg.goto("http://127.0.0.1:8795/en/eat/index.html",wait_until="networkidle")
        total=await pg.eval_on_selector_all("[data-shop]","e=>e.length")
        maps=await pg.eval_on_selector_all("a[href*='google.com/maps']","e=>e.length")
        print("ร้านทั้งหมด",total,"· ลิงก์แผนที่",maps)
        for term in ["Hokkilao","Chicken","Coffee","Khanom Jeen","Satay"]:
            await pg.fill("#shop-search",term); await pg.wait_for_timeout(320)
            n=await pg.eval_on_selector_all("[data-shop]","e=>e.filter(x=>x.offsetParent!==null).length")
            print(f"  ค้น {term:14} เจอ {n}")
        await pg.fill("#shop-search","")
        await br.close()
asyncio.run(main()); srv.shutdown()
