#!/bin/bash
# Status sekilas eksperimen ENIP — jalankan kapan pun.
set -u
cd "$(dirname "$0")/.."
echo "=== $(date '+%F %T') ==="
python3 - <<'EOF'
import json
from collections import Counter
rows = json.load(open("metrics/scores.json"))
c = Counter(r["judge"] for r in rows)
print(f"scores : {len(rows)}/300 | J1={c.get('J1',0)}/120 "
      f"J2={c.get('J2',0)}/120 J3={c.get('J3',0)}/60")
ids = [m["id"] for m in json.load(open("corpus/metadata.json"))["corpus"]]
need = {(co, i, j, t)
        for co in ("b1", "b2", "enip") for i in ids
        for j, ts in (("J1", (0, 0.7)), ("J2", (0, 0.7)), ("J3", (0,)))
        for t in ts}
have = {(r["condition"], r["id"], r["judge"], r["trial"]) for r in rows}
miss = need - have
if miss:
    from collections import Counter as C
    print(f"kurang : {len(miss)} →", dict(C(j for _, _, j, _ in miss)))
else:
    print("kurang : 0 — LENGKAP ✓ jalankan: python3 scripts/analyze.py")
EOF
pgrep -f judge_loop >/dev/null && echo "loop   : hidup ($(pgrep -f judge_loop | head -1))" \
  || echo "loop   : MATI — restart: nohup bash scripts/judge_loop.sh > judge_loop.local.log 2>&1 &"
pgrep caffeinate >/dev/null && echo "caffeinate: aktif" || echo "caffeinate: mati"
echo "log terakhir:"
tail -2 judge_loop.local.log 2>/dev/null | sed 's/^/  /'
