#!/usr/bin/env bash
# Runs after the first queue: the rest page depends on nothing else, but the
# quota does, so it waits its turn.
cd "$(dirname "$0")/.." || exit 1
sleep 2700
for attempt in 1 2 3; do
  python run_agy_queue.py rest-page >> _agy/queue.log 2>&1
  if grep -q "Individual quota reached" _agy/rest-page.log 2>/dev/null; then
    echo "[rest-page] โควตาเต็ม รออีก 15 นาที (ครั้งที่ $attempt)" >> _agy/queue.log
    sleep 900
    continue
  fi
  break
done
echo "rest-page จบ" >> _agy/queue.log
