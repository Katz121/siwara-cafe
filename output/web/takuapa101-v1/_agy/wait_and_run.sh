#!/usr/bin/env bash
# Wait out the agy quota window, then work the queue one job at a time so a
# single job cannot exhaust the allowance for the rest.
cd "$(dirname "$0")/.." || exit 1
sleep 840
for job in en-ui shop-coords en-places; do
  for attempt in 1 2 3; do
    python run_agy_queue.py "$job" >> _agy/queue.log 2>&1
    if grep -q "Individual quota reached" "_agy/$job.log" 2>/dev/null; then
      echo "[$job] โควตาเต็ม รออีก 15 นาที (ครั้งที่ $attempt)" >> _agy/queue.log
      sleep 900
      continue
    fi
    break
  done
done
echo "คิวจบ" >> _agy/queue.log
