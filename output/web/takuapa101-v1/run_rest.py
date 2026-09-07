import subprocess, sys, os, shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.stdout.reconfigure(encoding='utf-8')
AGY = r"C:\Users\siwat\AppData\Local\agy\bin\agy.cmd"
if not os.path.exists(AGY): AGY = shutil.which("agy") or "agy"
HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = {
 "kuapapoh": open(os.path.join(HERE,"briefs","_story_prompt.txt"),encoding="utf-8").read().replace("{ID}","kuapapoh")
   + "\n\nเพิ่มเติมสำหรับบทความนี้: อ่าน D:\Takuapa\content.json และ D:\Takuapa\PROJECT_MEMORY.md เป็นแหล่งข้อมูลโครงการกั่วป่าโพ้ · ภาพที่ใช้ได้คือ /assets/photos/kuapapoh-*.webp และ kuapapoh-*.jpg ตามที่ระบุใน data/photos-local.json เท่านั้น",
 "render": open(os.path.join(HERE,"briefs","_render_prompt.txt"),encoding="utf-8").read(),
}
def run(k):
    p = subprocess.run([AGY,"--dangerously-skip-permissions","--model","gemini-3.1-pro-high","-p",JOBS[k]],
        cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3000)
    open(os.path.join(HERE,f"_agy_{k}.log"),"w",encoding="utf-8").write((p.stdout or "")+"\n--ERR--\n"+(p.stderr or ""))
    return k, "rc=%d" % p.returncode
with ThreadPoolExecutor(max_workers=2) as ex:
    for f in as_completed({ex.submit(run,k):k for k in JOBS}):
        print("  %s: %s" % f.result(), flush=True)
print("done")
