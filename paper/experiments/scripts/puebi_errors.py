#!/usr/bin/env python3
"""C1 — PUEBI error rate terhadap ground truth injeksi (v2).

Metode occurrence-ratio per kategori (Deviasi #8):
  fix_rate(kategori, naskah) = max(0, 1 - out/input)
dengan out/input = jumlah kemunculan POLA error di badan output vs teks
asli. Pola spesifik per kategori:

  E1 koma konjungsi : konjungsi (tetapi/melainkan/sedangkan) TANPA koma
                      sebelumnya
  E2 di- vs di      : bentuk terpisah salah dari metadata (\b-delimited)
  E3 pun            : "walau pun"
  E4 serapan        : kata non-baku dari metadata (ijin, kwalitas, ...)
  E5 pleonasme      : frasa dari metadata ("agar supaya", ...)
  E6 angka awal     : digit di awal kalimat
  E7 tahun bertitik : "2.024" dsb dari metadata
  E8 kapital        : kata metadata (lowercase) di AWAL kalimat
  E9 italic         : istilah asing TANPA pembungkus *...* / _..._
  E10 kontaminasi   : "disebabkan karena"

Alasan bukan substring-murni: (a) string ' tetapi' tetap ada pada teks
yang SUDAH diberi koma; (b) angka '4' cocok di mana pun; (c) output
terstruktur ENIP mengutip bentuk salah di catatan — badan naskah
diekstrak lebih dulu (scripts/output_body.py).

Output: metrics/puebi_report.md + metrics/puebi_errors.json
"""
import json
import re
from collections import defaultdict
from pathlib import Path

from output_body import extract_body

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
RUNS = ROOT / "runs"
METRICS = ROOT / "metrics"


def esc(words):
    return "|".join(re.escape(w) for w in sorted(words))


def build_patterns(errors):
    """Pola regex per kategori, dibangun dari union ground truth."""
    by = defaultdict(set)
    for e in errors:
        by[e["cat"]].add(e["wrong"])
    pat = {}
    if "E1" in by:
        conj = esc({w.strip() for w in by["E1"]})
        pat["E1"] = re.compile(rf"(?<![,\n;:])\s(?:{conj})\b")
    for cat in ("E2", "E3", "E4", "E5"):
        if cat in by:
            pat[cat] = re.compile(rf"(?<![\w-])(?:{esc(by[cat])})(?![\w-])",
                                  re.IGNORECASE)
    if "E6" in by:
        pat["E6"] = re.compile(r"(?:^[ \t]*|[.!?…]\s+|\n\s*)(?:[-–—]\s*)?\d",
                               re.M)
    if "E7" in by:
        # tolak lanjutan digit ('2.0245') / desimal ('2.024.5'), TAPI
        # tetap terima titik akhir kalimat ('tahun 2.024.')
        pat["E7"] = re.compile(
            rf"(?<![\w.])(?:{esc(by['E7'])})(?!\d)(?!\.\d)")
    if "E8" in by:
        words = esc(w.lower() for w in by["E8"])
        # case-sensitive: lowercase di awal kalimat = error
        pat["E8"] = re.compile(rf"(?:^|[.!?\u2026]\s+|\n)\s*(?:{words})\b",
                               re.M)
    if "E9" in by:
        terms = esc(by["E9"])
        pat["E9"] = re.compile(rf"(?<![\*_\w])(?:{terms})\b(?![\*_])",
                               re.IGNORECASE)
    if "E10" in by:
        pat["E10"] = re.compile(rf"\b(?:{esc(by['E10'])})\b", re.IGNORECASE)
    return pat


def count(pat, text):
    return len(pat.findall(text)) if text else 0


def load_output(cond, tid):
    if cond == "input":
        return (CORPUS / "texts" / f"{tid}.txt").read_text(encoding="utf-8")
    p = RUNS / cond / f"{tid}.md"
    return p.read_text(encoding="utf-8") if p.exists() else None


def main():
    meta = json.loads((CORPUS / "metadata.json").read_text(encoding="utf-8"))
    injected = [m for m in meta["corpus"] if m["variant"] == "injected"]
    all_errors = [e for m in injected for e in m["injected_errors"]]
    patterns = build_patterns(all_errors)
    conditions = ["input", "b3", "enip", "b1", "b2"]

    rows = {}
    for cond in conditions:
        per_item, per_cat_num, per_cat_den = {}, defaultdict(float), \
            defaultdict(float)
        for item in injected:
            tid = item["id"]
            n_by_cat = defaultdict(int)
            for e in item["injected_errors"]:
                n_by_cat[e["cat"]] += 1
            if cond == "b3":
                per_item[tid] = {"n": sum(n_by_cat.values()), "fix_rate": None,
                                 "note": "b3 tanpa output teks"}
                continue
            src = load_output("input", tid)
            out_raw = load_output(cond, tid)
            if out_raw is None:
                per_item[tid] = {"n": sum(n_by_cat.values()), "fix_rate": None,
                                 "note": "menunggu run"}
                continue
            body = extract_body(out_raw)
            num, den = 0.0, 0.0
            detail = {}
            for cat, n in sorted(n_by_cat.items()):
                pat = patterns.get(cat)
                if pat is None:
                    continue
                c_in, c_out = count(pat, src), count(pat, body)
                if c_in == 0:
                    detail[cat] = {"n": n, "fix_rate": None,
                                   "note": "pola tak terdeteksi di input"}
                    continue
                fix = max(0.0, 1 - c_out / c_in)
                detail[cat] = {"n": n, "in": c_in, "out": c_out,
                               "fix_rate": round(fix, 4)}
                num += n * fix
                den += n
                per_cat_num[cat] += n * fix
                per_cat_den[cat] += n
            overall = round(num / den, 4) if den else None
            per_item[tid] = {"n": int(den), "fix_rate": overall,
                             "per_category": detail}
        agg = {c: round(per_cat_num[c] / per_cat_den[c], 4)
               for c in sorted(per_cat_den)}
        rows[cond] = {"items": per_item, "per_category": agg}
        done = [v["fix_rate"] for v in per_item.values()
                if v["fix_rate"] is not None]
        if done:
            rows[cond]["mean_fix_rate"] = round(sum(done) / len(done), 4)
            rows[cond]["n_done"] = len(done)
            rows[cond]["n_total"] = len(per_item)

    METRICS.mkdir(exist_ok=True)
    (METRICS / "puebi_errors.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Laporan PUEBI Error Rate (C1, v2 occurrence-ratio)", "",
        "fix_rate(kategori, naskah) = max(0, 1 - kemunculan_pola_out /",
        "kemunculan_pola_input), dihitung di BADAN naskah hasil edit",
        "(output terstruktur diekstrak dulu — lihat scripts/output_body.py).",
        "Bobot kategori = jumlah error terinjeksi per kategori.", "",
        "| Kondisi | Naskah | Mean fix rate | Catatan |",
        "|---|---|---|---|"]
    for cond in conditions:
        r = rows[cond]
        n, tot = r.get("n_done", 0), r.get("n_total", len(r["items"]))
        m = r.get("mean_fix_rate")
        note = ("b3 (hunspell) tidak menghasilkan teks baru"
                if cond == "b3" else "baseline (teks asli)"
                if cond == "input" else "")
        lines.append(f"| {cond} | {n}/{tot} | "
                     f"{m if m is not None else '-'} | {note} |")
    lines += ["", "## Fix rate per kategori (agregat tertimbang)", "",
              "| Kategori | " + " | ".join(conditions) + " |",
              "|---|" + "---|" * len(conditions)]
    cats = sorted({c for cond in conditions
                   for c in rows[cond].get("per_category", {})})
    for c in cats:
        vals = [str(rows[cond].get("per_category", {}).get(c, "-"))
                for cond in conditions]
        lines.append(f"| {c} | " + " | ".join(vals) + " |")
    lines += ["", "Rincian per naskah: metrics/puebi_errors.json"]
    (METRICS / "puebi_report.md").write_text("\n".join(lines),
                                             encoding="utf-8")
    print("\n".join(lines[:16]))
    print("  → metrics/puebi_report.md")


if __name__ == "__main__":
    main()
