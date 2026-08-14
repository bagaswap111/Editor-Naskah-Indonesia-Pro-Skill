#!/usr/bin/env python3
"""C1 — PUEBI error rate terhadap ground truth injeksi.

Membandingkan tiap output kondisi (runs/<kondisi>/<id>.md) dengan
injected_errors di metadata: apakah bentuk 'wrong' MASIH ada di output.

Kondisi khusus:
  'input' : teks korpus apa adanya (baseline: fix rate = 0)
  'b3'    : hunspell tidak menghasilkan teks baru -> diselewatkan (NaN)

Output: metrics/puebi_report.md + metrics/puebi_errors.json
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
RUNS = ROOT / "runs"
METRICS = ROOT / "metrics"


def load_output(cond, tid):
    if cond == "input":
        return (CORPUS / "texts" / f"{tid}.txt").read_text(encoding="utf-8")
    p = RUNS / cond / f"{tid}.md"
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8")


def main():
    meta = json.loads((CORPUS / "metadata.json").read_text(encoding="utf-8"))
    conditions = ["input", "b3", "enip", "b1", "b2"]
    rows = {}
    for cond in conditions:
        per_item, per_cat = {}, Counter()
        for item in meta["corpus"]:
            tid = item["id"]
            if item["variant"] != "injected":
                continue
            errors = item["injected_errors"]
            if not errors:
                continue
            if cond == "b3":
                per_item[tid] = {"n": len(errors), "remaining": None,
                                 "fix_rate": None, "note": "b3 tanpa output teks"}
                continue
            out = load_output(cond, tid)
            if out is None:
                per_item[tid] = {"n": len(errors), "remaining": None,
                                 "fix_rate": None, "note": "menunggu run"}
                continue
            remaining = [e for e in errors if e["wrong"] in out]
            per_cat.update(e["cat"] for e in errors)
            per_item[tid] = {"n": len(errors), "remaining": len(remaining),
                             "fix_rate": round(1 - len(remaining) / len(errors), 4),
                             "n_out_words": len(out.split())}
        rows[cond] = {"items": per_item, "category_totals": dict(per_cat)}
        if per_item and any(v["remaining"] is not None for v in per_item.values()):
            rs = [v["fix_rate"] for v in per_item.values() if v["fix_rate"] is not None]
            rows[cond]["mean_fix_rate"] = round(sum(rs) / len(rs), 4) if rs else None
            rows[cond]["n_done"] = len(rs)
            rows[cond]["n_total"] = len(per_item)
    (METRICS / "puebi_errors.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Laporan PUEBI Error Rate (C1)", "",
             "Metode: untuk tiap error injeksi (ground truth di "
             "corpus/metadata.json), cek apakah bentuk salah masih ada di output.",
             "Fix rate = 1 - (error tersisa / total error injeksi).", "",
             "| Kondisi | Naskah selesai | Mean fix rate | Catatan |"]
    for cond in conditions:
        r = rows[cond]
        n = r.get("n_done", 0); tot = r.get("n_total", len(r["items"]))
        m = r.get("mean_fix_rate")
        note = "menunggu API key" if n < tot and cond != "b3" else \
               "b3 (hunspell) tidak menghasilkan teks baru" if cond == "b3" else \
               "baseline (teks asli)"
        lines.append(f"| {cond} | {n}/{tot} | {m if m is not None else '-':} | {note} |")
    lines += ["", "## Per kategori (total error per kategori, seluruh set injeksi)", "",
              "| Kategori | Total injeksi |"]
    for cat, n in sorted(rows["input"]["category_totals"].items()):
        lines.append(f"| {cat} | {n} |")
    lines += ["", "Catatan: rincian per naskah di metrics/puebi_errors.json"]
    (METRICS / "puebi_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:12]))


if __name__ == "__main__":
    main()