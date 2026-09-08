import asyncio, http.server, socketserver, threading, functools, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site')
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=os.path.abspath(ROOT))
class S(socketserver.TCPServer): allow_reuse_address=True
srv=S(("127.0.0.1",8791),H); threading.Thread(target=srv.serve_forever,daemon=True).start()
B="http://127.0.0.1:8791"
PAGES=["/","/places/","/map/","/rest/","/eat/","/news/","/places/tao-ming/","/en/"]
async def main():
    async with async_playwright() as pw:
        br=await pw.chromium.launch()
        pg=await br.new_page(viewport={"width":390,"height":844})
        for p in PAGES:
            await pg.goto(B+p+("index.html" if p.endswith("/") else ""),wait_until="networkidle")
            over=await pg.evaluate("()=>document.documentElement.scrollWidth-document.documentElement.clientWidth")
            wide=await pg.evaluate("()=>[...document.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>document.documentElement.clientWidth+1).slice(0,3).map(e=>e.tagName+'.'+e.className)")
            print(f"{p:24} ล้น {over}px {wide if over>0 else ''}")
        # trip cart
        await pg.goto(B+"/places/tao-ming/index.html",wait_until="networkidle")
        n=await pg.eval_on_selector_all("[data-trip-add]","e=>e.length")
        before=await pg.evaluate("()=>window.TakuaTrip.count()")
        await pg.click("[data-trip-add]")
        after=await pg.evaluate("()=>window.TakuaTrip.count()")
        label=await pg.eval_on_selector("[data-trip-add]","e=>e.textContent")
        badge=await pg.eval_on_selector_all("[data-trip-count]","e=>e.map(x=>x.textContent+(x.hidden?' (ซ่อน)':''))")
        print(f"\nปุ่มในหน้าสถานที่: {n} · กดแล้ว {before} -> {after} · ป้ายปุ่ม: {label} · badge: {badge}")
        await pg.goto(B+"/trip/index.html",wait_until="networkidle")
        rows=await pg.eval_on_selector_all(".trip-item, [data-trip-row], li","e=>e.length")
        print(f"หน้า /trip/ หลังเพิ่ม: {rows} แถว · จำค่าข้ามหน้า: {await pg.evaluate('()=>window.TakuaTrip.count()')}")
        await br.close()
asyncio.run(main()); srv.shutdown()
