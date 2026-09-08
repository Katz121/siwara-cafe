import asyncio,http.server,socketserver,threading,functools,os,sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site')
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=os.path.abspath(ROOT))
class S(socketserver.TCPServer): allow_reuse_address=True
srv=S(("127.0.0.1",8793),H); threading.Thread(target=srv.serve_forever,daemon=True).start()
async def main():
    async with async_playwright() as pw:
        br=await pw.chromium.launch(); pg=await br.new_page(viewport={"width":390,"height":844})
        for p in ["/","/places/","/eat/","/places/tao-ming/"]:
            await pg.goto("http://127.0.0.1:8793"+p+"index.html",wait_until="networkidle")
            small=await pg.evaluate("""()=>[...document.querySelectorAll('a,button,[role=button],input,select')]
              .filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&(r.width<44||r.height<44)})
              .map(e=>{const r=e.getBoundingClientRect();return (e.tagName+'.'+(e.className||'').toString().split(' ')[0])+' '+Math.round(r.width)+'x'+Math.round(r.height)})""")
            from collections import Counter
            c=Counter(small)
            print(p, len(small),'จุด')
            for k,v in c.most_common(6): print('    ',v,'x',k)
        await br.close()
asyncio.run(main()); srv.shutdown()
