import asyncio,http.server,socketserver,threading,functools,os,sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright
SITE=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'site')
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=SITE)
class S(socketserver.TCPServer): allow_reuse_address=True
srv=S(("127.0.0.1",8796),H); threading.Thread(target=srv.serve_forever,daemon=True).start()
async def main():
    async with async_playwright() as pw:
        br=await pw.chromium.launch(); pg=await br.new_page(viewport={"width":1280,"height":900})
        errs=[]; pg.on("console",lambda m: errs.append(m.text[:80]) if m.type=="error" else None)
        await pg.goto("http://127.0.0.1:8796/map/index.html",wait_until="networkidle")
        await pg.wait_for_timeout(1500)
        btns=await pg.eval_on_selector_all("#map-filters button","e=>e.map(x=>x.textContent.trim())")
        cnt=await pg.eval_on_selector("#map-count","e=>e.textContent.trim()")
        heads=await pg.eval_on_selector_all(".missing-coords-heading,.map-note,.full-map-link","e=>e.map(x=>x.textContent.trim())")
        pins=await pg.eval_on_selector_all(".maplibregl-marker","e=>e.length")
        popup=await pg.evaluate("()=>{const m=document.querySelector('.maplibregl-marker'); m&&m.click(); return 1}")
        await pg.wait_for_timeout(700)
        popup=await pg.eval_on_selector_all(".map-popup a","e=>e.map(x=>x.textContent.trim())")
        print("ปุ่มกรอง:",btns)
        print("ตัวนับ:",cnt,"· หมุด:",pins)
        print("ข้อความอื่น:",heads)
        print("ปุ่มในป๊อปอัพ:",popup)
        print("console error:",errs or "ไม่มี")
        await br.close()
asyncio.run(main()); srv.shutdown()
