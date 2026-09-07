#!/usr/bin/env bash
# Logos wait for the translation loop: running more than three agy jobs at once
# hits the quota and everything slows down.
cd "$(dirname "$0")/.." || exit 1
for i in $(seq 1 120); do
  grep -q "finish_en เสร็จ" _agy/finish.log 2>/dev/null && break
  sleep 30
done
python brand/run_logo_agy.py >> _agy/logos.log 2>&1
echo "logos เสร็จ" >> _agy/logos.log
