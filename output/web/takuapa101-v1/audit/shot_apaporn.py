import asyncio,functools,http.server,os,socketserver,sys,threading
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright
SITE=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'site')
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=SITE)
class S(socketserver.TCPServer): allow_reuse_address=True
srv=S(("127.0.0.1",8792),H); threading.Thread(target=srv.serve_forever,daemon=True).start()
OUT=sys.argv[1]
async def main():
    async with async_playwright() as pw:
        br=await pw.chromium.launch(); pg=await br.new_page(viewport={"width":1100,"height":1000})
        await pg.goto("http://127.0.0.1:8792/stories/apaporn/index.html",wait_until="networkidle")
        await pg.evaluate("()=>new Promise(r=>{let y=0;const t=setInterval(()=>{window.scrollTo(0,y);y+=600;if(y>document.body.scrollHeight){clearInterval(t);window.scrollTo(0,0);r()}},60)})")
        await pg.wait_for_timeout(1200)
        await pg.screenshot(path=OUT,full_page=True)
        n=await pg.eval_on_selector_all("main img","e=>e.length")
        print("รูปในหน้า",n)
        await br.close()
asyncio.run(main()); srv.shutdown()
