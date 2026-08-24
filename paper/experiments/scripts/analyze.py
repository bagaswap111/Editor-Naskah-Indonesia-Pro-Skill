#!/usr/bin/env python3
"""Fase C2/C3 — analisis skor juri & delta self-score (analyze.py).

Input:
  metrics/scores.json   (hasil judge.py)
  runs/enip/<id>.md     (tabel Skor Kualitas dari ENIP — untuk C3)

Analisis:
  C2 - ringkasan per kondisi & dimensi (mean ± std antar naskah),
       delta ENIP−B1 dan ENIP−B2 dengan paired bootstrap
       (resampling naskah, dua sisi, CI 95%),
       korelasi antar-judge (Pearson & Spearman, level naskah).
  C3 - delta self-score ENIP vs juri: label dimensi pada tabel
       Skor Kualitas dipetakan ke 7 dimensi rubrik memakai aturan
       kata-kunci; baris tak terpetakan dilaporkan apa adanya.

Output: metrics/analysis.json + metrics/analysis_report.md

Usage:
  python3 scripts/analyze.py [--bootstrap 10000] [--seed 20260823]
"""
import argparse
import json
import math
import random
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "metrics"
RUNS = ROOT / "runs"

DIMENSI = ["Kejelasan", "Koherensi", "Kedalaman", "Akurasi", "Gaya",
           "Mekanik", "Engagement"]

# Urutan aturan = prioritas pemetaan (label self-score → dimensi rubrik)
ATURAN = [
    ("Mekanik", re.compile(
        r"mekanik|ejaan|tanda baca|kapital|puebi|kbbi|kebakuan|kebahasaan|"
        r"kbakuan|typo|kualitas teknis", re.I)),
    ("Kejelasan", re.compile(r"kejelasan|keterbacaan", re.I)),
    ("Koherensi", re.compile(r"koheren|kohesi|struktur", re.I)),
    ("Kedalaman", re.compile(r"kedalaman|kelengkapan|substantif", re.I)),
    ("Akurasi", re.compile(r"akurasi", re.I)),
    ("Gaya", re.compile(r"gaya|tone", re.I)),
    ("Engagement", re.compile(
        r"target pembaca|kreativitas|estetika|kekayaan|engagement|menarik",
        re.I)),
]

ROW_RE = re.compile(r"^\s*\|")


def parse_self_scores(path):
    """Ambil tabel 'Skor Kualitas' dari output ENIP → {dimensi: skor}."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if re.search(r"skor\s+kualitas", ln, re.I):
            start = i
            break
    unparsed = []
    if start is None:
        return {}, unparsed
    hasil, terpakai = {}, []
    for ln in lines[start + 1:]:
        if re.search(r"rata\s*[-\u2011]?\s*rata\s+skor", ln, re.I):
            break
        if not ROW_RE.match(ln):
            if hasil:
                break
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        label = cells[0].strip("* ").strip()
        skor = None
        for c in cells[1:]:
            m = re.match(r"^\*{0,2}(\d{1,2})(?:\s*\(|$|\s)", c.strip("* "))
            if m and 1 <= int(m.group(1)) <= 10:
                skor = int(m.group(1))
                break
        if skor is None or not label:
            continue
        dim = None
        for target, pola in ATURAN:
            if pola.search(label) and target not in hasil:
                dim = target
                break
        if dim:
            hasil[dim] = skor
            terpakai.append((label, dim, skor))
        else:
            unparsed.append((label, skor))
    return hasil, unparsed


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs)


def stdev(xs):
    if len(xs) < 2:
        return 0.0
    mu = mean(xs)
    return math.sqrt(sum((x - mu) ** 2 for x in xs) / (len(xs) - 1))


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs)
                    * sum((y - my) ** 2 for y in ys))
    return num / den if den else None


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def spearman(xs, ys):
    return pearson(ranks(xs), ranks(ys))


def paired_bootstrap(diffs, n_boot, rng):
    """diffs: selisih berpasangan per naskah. Kembalikan (obs, p, lo, hi)."""
    obs = mean(diffs)
    boots = []
    n = len(diffs)
    for _ in range(n_boot):
        samp = [diffs[rng.randrange(n)] for _ in range(n)]
        boots.append(mean(samp))
    p_le = sum(1 for b in boots if b <= 0) / n_boot
    p_ge = sum(1 for b in boots if b >= 0) / n_boot
    boots.sort()
    lo = boots[int(0.025 * n_boot)]
    hi = boots[min(n_boot - 1, int(0.975 * n_boot))]
    return obs, 2 * min(p_le, p_ge), lo, hi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bootstrap", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=20260823)
    ap.add_argument("--full", action="store_true",
                    help="abaikan scores.json yang sudah ada (mulai ulang)")
    a = ap.parse_args()

    rows = json.loads((METRICS / "scores.json").read_text(encoding="utf-8"))
    if not rows:
        raise SystemExit("scores.json kosong — jalankan judge.py dulu")

    kondisi = sorted({r["condition"] for r in rows})
    judges = sorted({r["judge"] for r in rows})
    trials = sorted({r["trial"] for r in rows})

    # ---- agregat level naskah -------------------------------------------
    # skor[(cond,id)] = {("J1",0): {dim: v}, ...} ; overall per sel
    skor = defaultdict(dict)
    for r in rows:
        skor[(r["condition"], r["id"])][(r["judge"], r["trial"])] = r["skor"]

    def overall(d):
        return mean(d[x] for x in DIMENSI)

    def item_scores(cond, dims=DIMENSI):
        """Rata-rata lintas juri & trial per naskah → {id: {dim: v}}."""
        out = {}
        for (c, cid), sel in skor.items():
            if c != cond:
                continue
            agg = {}
            for dim in dims:
                vals = [s[dim] for s in sel.values() if dim in s]
                if vals:
                    agg[dim] = mean(vals)
            if agg:
                out[cid] = agg
        return out

    ringkas = {}
    for cond in kondisi:
        items = item_scores(cond)
        per_dim = {}
        for dim in DIMENSI:
            vals = [it[dim] for it in items.values() if dim in it]
            per_dim[dim] = {"mean": round(mean(vals), 3),
                            "std": round(stdev(vals), 3), "n": len(vals)}
        ovs = [overall(it) for it in items.values()]
        ringkas[cond] = {
            "n_naskah": len(items),
            "overall": {"mean": round(mean(ovs), 3),
                        "std": round(stdev(ovs), 3)},
            "per_dimensi": per_dim,
            # rincian per juri × trial (sel)
            "per_sel": {},
        }
        for (c, cid), sel in skor.items():
            if c != cond:
                continue
            for key, s in sel.items():
                cell = ringkas[cond]["per_sel"].setdefault(
                    f"{key[0]}@t{key[1]}", defaultdict(list))
                for dim in DIMENSI:
                    cell[dim].append(s[dim])
        ringkas[cond]["per_sel"] = {
            k: {dim: round(mean(v), 3) for dim, v in d.items()}
            for k, d in ringkas[cond]["per_sel"].items()}

    # ---- uji berpasangan ENIP vs B1/B2 ----------------------------------
    uji = {}
    rng = random.Random(a.seed)
    for base in kondisi:
        if base == "enip":
            continue
        ie, ib = item_scores("enip"), item_scores(base)
        common = sorted(set(ie) & set(ib))
        if not common:
            continue
        entri = {}
        diffs_all = [overall(ie[c]) - overall(ib[c]) for c in common]
        obs, p, lo, hi = paired_bootstrap(diffs_all, a.bootstrap,
                                          random.Random(a.seed))
        entri["overall"] = {
            "delta": round(obs, 3), "p": round(p, 4),
            "ci95": [round(lo, 3), round(hi, 3)], "n": len(common)}
        entri["per_dimensi"] = {}
        for dim in DIMENSI:
            dd = [ie[c][dim] - ib[c][dim] for c in common
                  if dim in ie[c] and dim in ib[c]]
            if len(dd) >= 5:
                o2, p2, l2, h2 = paired_bootstrap(dd, a.bootstrap,
                                                  random.Random(a.seed))
                entri["per_dimensi"][dim] = {
                    "delta": round(o2, 3), "p": round(p2, 4),
                    "ci95": [round(l2, 3), round(h2, 3)]}
        uji[f"enip_vs_{base}"] = entri

    # ---- korelasi antar-judge ------------------------------------------
    def per_judge_items(judge):
        out = defaultdict(list)
        for (c, cid), sel in skor.items():
            for (j, t), s in sel.items():
                if j == judge:
                    out[cid].append(overall(s))
        return {cid: mean(v) for cid, v in out.items()}

    kor = {}
    ji = {j: per_judge_items(j) for j in judges}
    for i in range(len(judges)):
        for k in range(i + 1, len(judges)):
            ja, jb = judges[i], judges[k]
            common = sorted(set(ji[ja]) & set(ji[jb]))
            xs = [ji[ja][c] for c in common]
            ys = [ji[jb][c] for c in common]
            pr, sp = pearson(xs, ys), spearman(xs, ys)
            kor[f"{ja}_vs_{jb}"] = {
                "pearson": round(pr, 3) if pr is not None else None,
                "spearman": round(sp, 3) if sp is not None else None,
                "n": len(common)}

    # ---- C3 delta self-score --------------------------------------------
    meta_ids = []
    c3_rows = []
    for (cond, cid) in sorted(skor):
        if cond != "enip":
            continue
        self_s, unparsed = parse_self_scores(RUNS / "enip" / f"{cid}.md")
        j_mean = defaultdict(list)
        for s in skor[(cond, cid)].values():
            for dim in DIMENSI:
                j_mean[dim].append(s[dim])
        j_mean = {d: mean(v) for d, v in j_mean.items()}
        deltas = {}
        for dim in DIMENSI:
            if dim in self_s and dim in j_mean:
                deltas[dim] = self_s[dim] - j_mean[dim]
        c3_rows.append({"id": cid, "self": self_s, "unmapped": unparsed,
                        "delta_self_minus_judge": {
                            d: round(v, 3) for d, v in deltas.items()}})
    c3 = {"n": len(c3_rows),
          "coverage_per_dimensi": {
              d: sum(1 for r in c3_rows
                     if d in r["delta_self_minus_judge"])
              for d in DIMENSI},
          "mean_abs_delta": {}, "bias_signed": {}}
    for dim in DIMENSI:
        ds = [abs(r["delta_self_minus_judge"][dim]) for r in c3_rows
              if dim in r["delta_self_minus_judge"]]
        sg = [r["delta_self_minus_judge"][dim] for r in c3_rows
              if dim in r["delta_self_minus_judge"]]
        if ds:
            c3["mean_abs_delta"][dim] = round(mean(ds), 3)
            c3["bias_signed"][dim] = round(mean(sg), 3)
    semua = [abs(v) for r in c3_rows
             for v in r["delta_self_minus_judge"].values()]
    semua_signed = [v for r in c3_rows
                    for v in r["delta_self_minus_judge"].values()]
    if semua:
        c3["mean_abs_delta"]["SEMUA"] = round(mean(semua), 3)
        c3["bias_signed"]["SEMUA"] = round(mean(semua_signed), 3)

    hasil = {"ringkasan": ringkas, "uji_paired_bootstrap": uji,
             "korelasi_antar_judge": kor, "c3_delta_self_score": c3,
             "c3_detail_per_naskah": c3_rows}
    (METRICS / "analysis.json").write_text(
        json.dumps(hasil, ensure_ascii=False, indent=2),
        encoding="utf-8")

    # ---- laporan --------------------------------------------------------
    L = []
    L.append("# Analisis Judge (C2) & Delta Self-Score (C3)\n")
    L.append(f"Sumber: metrics/scores.json ({len(rows)} penilaian; "
             f"kondisi {', '.join(kondisi)}; juri {', '.join(judges)}; "
             f"trial {trials}). Bootstrap {a.bootstrap}x, "
             f"unit resampling = naskah (paired).\n")
    L.append("## Ringkasan skor (rata-rata 7 dimensi)\n")
    L.append("| Kondisi | n | Mean | Std |")
    L.append("|---|---|---|---|")
    for cond in kondisi:
        r = ringkas[cond]["overall"]
        L.append(f"| {cond} | {ringkas[cond]['n_naskah']} | "
                 f"{r['mean']:.2f} | {r['std']:.2f} |")
    L.append("\n### Per dimensi (mean antar naskah)\n")
    hdr = "| Dimensi | " + " | ".join(kondisi) + " |"
    L.append(hdr)
    L.append("|---|" + "---|" * len(kondisi))
    for dim in DIMENSI:
        row = [f"{ringkas[c]['per_dimensi'][dim]['mean']:.2f}"
               f"±{ringkas[c]['per_dimensi'][dim]['std']:.2f}"
               for c in kondisi]
        L.append(f"| {dim} | " + " | ".join(row) + " |")

    L.append("\n## Uji berpasangan (paired bootstrap, delta = ENIP − basis)\n")
    L.append("| Pasangan | Δ overall | CI 95% | p | n |")
    L.append("|---|---|---|---|---|")
    for nama, e in uji.items():
        o = e["overall"]
        L.append(f"| {nama} | {o['delta']:+.2f} | "
                 f"[{o['ci95'][0]:+.2f}, {o['ci95'][1]:+.2f}] | "
                 f"{o['p']:.3f} | {o['n']} |")
    L.append("\nDelta per dimensi:\n")
    L.append("| Pasangan | " + " | ".join(DIMENSI) + " |")
    L.append("|---|" + "---|" * len(DIMENSI))
    for nama, e in uji.items():
        row = []
        for dim in DIMENSI:
            d = e["per_dimensi"].get(dim)
            row.append(f"{d['delta']:+.2f} (p={d['p']:.3f})"
                       if d else "-")
        L.append(f"| {nama} | " + " | ".join(row) + " |")

    L.append("\n## Korelasi antar-judge (level naskah, mean 7 dimensi)\n")
    L.append("| Pasangan | Pearson | Spearman | n |")
    L.append("|---|---|---|---|")
    for nama, k in kor.items():
        L.append(f"| {nama} | {k['pearson']} | {k['spearman']} | {k['n']} |")

    L.append("\n## C3 — Delta self-score ENIP (skor sendiri − juri)\n")
    L.append(f"n = {c3['n']} naskah ENIP; baris tabel Skor Kualitas yang "
             "tak dapat dipetakan ke rubrik diabaikan (liputan per dimensi "
             "pada analysis.json).\n")
    L.append("| Dimensi | Mean abs delta | Bias (signed) | Liputan |")
    L.append("|---|---|---|---|")
    for dim in DIMENSI + ["SEMUA"]:
        if dim in c3["mean_abs_delta"]:
            L.append(f"| {dim} | {c3['mean_abs_delta'][dim]:.2f} | "
                     f"{c3['bias_signed'][dim]:+.2f} | "
                     f"{c3['coverage_per_dimensi'].get(dim, c3['n'])}/{c3['n']} |")
    L.append("\nInterpretasi: bias positif = ENIP menilai dirinya lebih "
             "tinggi daripada juri (self-assessment bias, RQ5).")
    (METRICS / "analysis_report.md").write_text("\n".join(L) + "\n",
                                                encoding="utf-8")

    print(f"OK → metrics/analysis.json + analysis_report.md")
    print("\nOverall per kondisi:")
    for cond in kondisi:
        r = ringkas[cond]["overall"]
        print(f"  {cond}: {r['mean']:.2f} ± {r['std']:.2f} "
              f"(n={ringkas[cond]['n_naskah']})")
    for nama, e in uji.items():
        o = e["overall"]
        print(f"  {nama}: Δ={o['delta']:+.2f}, p={o['p']:.3f}")
    for nama, k in kor.items():
        print(f"  korelasi {nama}: r={k['pearson']}, ρ={k['spearman']} "
              f"(n={k['n']})")
    if "SEMUA" in c3["mean_abs_delta"]:
        print(f"  C3 mean abs delta (semua dim): "
              f"{c3['mean_abs_delta']['SEMUA']}, bias "
              f"{c3['bias_signed']['SEMUA']:+.2f}")


if __name__ == "__main__":
    main()
