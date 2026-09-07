#!/usr/bin/env bash
# Drive the English build to completion.
#
# Each round translates a slice of what is still missing, rebuilds, and
# recomputes the gap. Rebuilding between rounds matters: one repeated label can
# unlock several pages, which shrinks the next round's work.
cd "$(dirname "$0")" || exit 1
LOG=_agy/finish.log
: > "$LOG"

for round in 1 2 3 4 5 6 7 8; do
  echo "=== รอบ $round · $(date +%H:%M) ===" >> "$LOG"

  left=$(python -c "import json;print(len(json.load(open('data/i18n/en/missing.json',encoding='utf-8'))))" 2>/dev/null || echo 0)
  echo "ข้อความที่ยังขาด $left" >> "$LOG"
  if [ "$left" -lt 40 ]; then
    echo "เหลือน้อยพอแล้ว หยุด" >> "$LOG"
    break
  fi

  # Fresh batches from the current gap, not the gap this run started with.
  rm -rf data/i18n/en/missing-parts-round
  python run_en_missing.py >> "$LOG" 2>&1

  rm -rf site/en
  python build_site.py >> "$LOG" 2>&1
  python build_en.py >> "$LOG" 2>&1
  tail -2 "$LOG"
done

echo "=== จบ · $(date +%H:%M) ===" >> "$LOG"
python build_en.py 2>&1 | tail -2 >> "$LOG"
echo "finish_en เสร็จ" >> "$LOG"
