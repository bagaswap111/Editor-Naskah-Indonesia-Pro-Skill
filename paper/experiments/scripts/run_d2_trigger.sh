#!/bin/bash
# D2 — Trigger reliability: jalankan 20 query di runtime utama (OpenCode).
# Tiap query = sesi BARU (opencode run tanpa --continue), direktori netral,
# sehingga aktivasi murni ditentukan oleh deskripsi skill (SKILL.md).
# Output mentah disimpan di trigger/logs/ untuk audit.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d /var/folders/ff/qc5nzz0s76q108sfm51dxgb80000gn/T/opencode/d2-run.XXXXXX)"
LOGDIR="$ROOT/trigger/logs"
mkdir -p "$LOGDIR"
echo "workdir: $WORK"

python3 - "$ROOT" <<'EOF' > "$WORK/queries.txt"
import json, sys
for q in json.load(open(sys.argv[1] + "/trigger/queries.json")):
    print(q["id"] + "\t" + q["query"])
EOF

while IFS=$'\t' read -r qid qtext; do
  echo "=== $qid $(date '+%T') ==="
  ( cd "$WORK" && timeout 300 opencode run "$qtext" \
      > "$LOGDIR/$qid.out" 2> "$LOGDIR/$qid.err" < /dev/null )
  rc=$?
  echo "    selesai rc=$rc ($(wc -c < "$LOGDIR/$qid.out") bytes)"
done < "$WORK/queries.txt"
echo "SEMUA SELESAI — log di $LOGDIR"
