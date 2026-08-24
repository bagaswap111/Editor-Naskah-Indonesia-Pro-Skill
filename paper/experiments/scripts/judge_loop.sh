#!/bin/bash
# Babysitter judge C2 — ulangi sampai scores.json lengkap (300 entri).
# Idempotent: tiap putaran hanya mengisi sel (condition,id,judge,trial)
# yang belum ada. Aman dihentikan kapan pun (Ctrl-C / kill).
set -u
cd "$(dirname "$0")/.."
TARGET=300
for i in $(seq 1 200); do
  n=$(python3 -c "import json;print(len(json.load(open('metrics/scores.json'))))" \
      2>/dev/null || echo 0)
  if [ "${n:-0}" -ge "$TARGET" ]; then
    echo "SELESAI: $n/$TARGET penilaian lengkap."
    break
  fi
  echo "=== putaran $i — $n/$TARGET — $(date '+%F %T') ==="
  python3 scripts/judge.py --judges J1,J2,J3 || true
  sleep 900
done
