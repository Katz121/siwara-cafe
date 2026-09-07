"""Operator runner: fan out one codex exec per target to research real place data."""
import json, subprocess, sys, time, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "out3"
LOGS = HERE / "logs"
OUT.mkdir(exist_ok=True); LOGS.mkdir(exist_ok=True)

TEMPLATE = (HERE / "PROMPT_PHOTOS.md").read_text(encoding="utf-8")

TARGETS = json.loads((HERE / "targets.json").read_text(encoding="utf-8"))

import shutil
CODEX = shutil.which("codex") or shutil.which("codex.cmd") or "codex"
MODEL = os.environ.get("RESEARCH_MODEL", "gpt-5.6-luna")
WORKERS = int(os.environ.get("RESEARCH_WORKERS", "5"))
ONLY = set(sys.argv[1:])


def run(t):
    tid = t["id"]
    outfile = OUT / f"{tid}.json"
    if outfile.exists() and outfile.stat().st_size > 200:
        return tid, "skip(exists)"
    p1 = HERE / "out" / f"{tid}.json"
    PASS1 = p1.read_text(encoding="utf-8")[:6000] if p1.exists() else "(ยังไม่มี)"
    prompt = (TEMPLATE
              .replace("{ID}", tid)
              .replace("{NAME_TH}", t["name_th"])
              .replace("{NAME_EN}", t.get("name_en") or "-")
              .replace("{CATEGORY}", t["category"])
              .replace("{FACTS}", "\n".join("- " + f for f in t.get("brochure_facts", [])) or "- (ไม่มี)")
              .replace("{OUTFILE}", str(outfile).replace("\\", "/"))
              .replace("{PASS1}", PASS1))
    t0 = time.time()
    p = subprocess.run(
        [CODEX, "exec", "-m", MODEL, "--skip-git-repo-check",
         "--dangerously-bypass-approvals-and-sandbox", "-"],
        input=prompt, capture_output=True, text=True, encoding="utf-8",
        errors="replace", cwd=str(HERE), timeout=1800)
    (LOGS / f"{tid}.log").write_text((p.stdout or "") + "\n--STDERR--\n" + (p.stderr or ""), encoding="utf-8")
    ok = outfile.exists() and outfile.stat().st_size > 200
    return tid, f"{'OK' if ok else 'FAIL'} {time.time()-t0:.0f}s"


targets = [t for t in TARGETS if not ONLY or t["id"] in ONLY]
print(f"targets={len(targets)} model={MODEL} workers={WORKERS}", flush=True)
with ThreadPoolExecutor(max_workers=WORKERS) as ex:
    futs = {ex.submit(run, t): t["id"] for t in targets}
    for f in as_completed(futs):
        try:
            tid, st = f.result()
        except Exception as e:
            tid, st = futs[f], f"ERR {e}"
        print(f"  {tid}: {st}", flush=True)
print("done")
