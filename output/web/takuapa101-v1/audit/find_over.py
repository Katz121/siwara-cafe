import asyncio,functools,http.server,os,socketserver,sys,threading
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright
SITE=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'site')
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=SITE)
class S(socketserver.TCPServer): allow_reuse_address=True
srv=S(("127.0.0.1",8789),H); threading.Thread(target=srv.serve_forever,daemon=True).start()
async def main():
    async with async_playwright() as pw:
        br=await pw.chromium.launch(); pg=await br.new_page(viewport={"width":390,"height":900})
        for r in ["/en/","/en/eat/"]:
            await pg.goto("http://127.0.0.1:8789"+r+"index.html",wait_until="networkidle")
            out=await pg.evaluate("""()=>{const W=document.documentElement.clientWidth;
              return [...document.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>W+1)
                .slice(0,6).map(e=>{const b=e.getBoundingClientRect();
                  return e.tagName+'.'+(e.className||'').toString().split(' ')[0]+' w='+Math.round(b.width)+' right='+Math.round(b.right)+' txt='+(e.textContent||'').trim().slice(0,28)})}""")
            print(r); [print('   ',x) for x in out]
        await br.close()
asyncio.run(main()); srv.shutdown()
