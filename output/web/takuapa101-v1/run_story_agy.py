import subprocess, sys, os, shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.stdout.reconfigure(encoding='utf-8')
AGY = r"C:\Users\siwat\AppData\Local\agy\bin\agy.cmd"
if not os.path.exists(AGY): AGY = shutil.which("agy") or r"C:\Users\siwat\AppData\Local\agy\bin\agy"
HERE = os.path.dirname(os.path.abspath(__file__))
IDS = sys.argv[1:] or ["city", "architecture", "water-trade", "food-people", "kuapapoh"]
TMPL = open(os.path.join(HERE, "briefs", "_story_prompt.txt"), encoding="utf-8").read()

def run(sid):
    out = os.path.join(HERE, "data", "stories", sid + ".json")
    if os.path.exists(out) and os.path.getsize(out) > 2000:
        return sid, "skip(exists)"
    p = subprocess.run([AGY, "--dangerously-skip-permissions", "--model", "gemini-3.1-pro-high",
                        "-p", TMPL.replace("{ID}", sid)],
                       cwd=HERE, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=3000)
    open(os.path.join(HERE, "data", "stories", sid + ".log"), "w", encoding="utf-8").write((p.stdout or "") + "\n--ERR--\n" + (p.stderr or ""))
    ok = os.path.exists(out) and os.path.getsize(out) > 2000
    return sid, ("OK " + str(os.path.getsize(out)) + "B" if ok else "FAIL")

with ThreadPoolExecutor(max_workers=3) as ex:
    for f in as_completed({ex.submit(run, i): i for i in IDS}):
        print("  %s: %s" % f.result(), flush=True)
print("done")
