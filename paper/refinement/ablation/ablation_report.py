#!/usr/bin/env python3
"""Generate paper-ready ablation tables from ablation_analysis.json.

Outputs Markdown and LaTeX (booktabs) tables in results/paper_tables.md and
results/paper_tables.tex.

Usage:
    python ablation_report.py [--analysis PATH] [--out DIR]
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_ANALYSIS = HERE / "results" / "ablation_analysis.json"
DEFAULT_OUT = HERE / "results"

DIMENSI = ["Kejelasan", "Koherensi", "Kedalaman", "Akurasi", "Gaya",
           "Mekanik", "Engagement"]
LABEL = {
    "enip_no_puebi": "ENIP w/o PUEBI",
    "enip_no_style": "ENIP w/o style engine",
    "enip_no_workflow": "ENIP w/o workflow",
    "enip_full": "ENIP-full (main study)",
}
ABLATION_ONLY = ["enip_no_puebi", "enip_no_style", "enip_no_workflow"]


def fmt(x, nd=2, signed=False):
    if x is None:
        return "—"
    return f"{x:+.{nd}f}" if signed else f"{x:.{nd}f}"


def md_tables(a):
    rows = []
    rows.append("| Condition | $n$ | Mean | Std | $\\Delta$ vs ENIP-full | 95\\% CI ($\\Delta$) |")
    rows.append("|---|---|---|---|---|---|")
    for cond in ABLATION_ONLY + ["enip_full"]:
        e = a["conditions"].get(cond)
        if not e:
            continue
        ci = e.get("ci95")
        ci_txt = f"[{ci['lo']:.2f}, {ci['hi']:.2f}]" if ci else "—"
        rows.append(f"| {LABEL[cond]} | {e['n']} | {fmt(e['mean'])} | {fmt(e['std'])} | "
                    f"{fmt(e['delta_vs_enip_full'], signed=True)} | {ci_txt} |")
    overall = "\n".join(rows)

    dims = ["| Condition | " + " | ".join(DIMENSI) + " |",
            "|---|" + "---|" * len(DIMENSI)]
    for cond in ABLATION_ONLY + ["enip_full"]:
        e = a["conditions"].get(cond)
        if not e:
            continue
        pm = e["per_dimension"]
        dims.append(f"| {LABEL[cond]} | " +
                    " | ".join(fmt(pm.get(d)) for d in DIMENSI) + " |")
    per_dim = "\n".join(dims)

    pair = ["| Contrast | $\\Delta$ | 95\\% CI | Sig. |", "|---|---|---|---|"]
    for p in a.get("pairwise_within_ablation", []):
        ci = p["ci95"]
        ci_txt = f"[{ci['lo']:.2f}, {ci['hi']:.2f}]" if ci else "—"
        pair.append(f"| {LABEL[p['a']]} − {LABEL[p['b']]} | {fmt(p['delta'], signed=True)} | "
                    f"{ci_txt} | {'yes' if p['significant'] else 'no'} |")
    pairwise = "\n".join(pair)
    return overall, per_dim, pairwise


def latex_tables(a):
    out = []
    out.append("% Table 1: overall ablation scores")
    out.append("\\begin{table}[t]")
    out.append("\\centering\\small")
    out.append("\\begin{tabular}{lrrrrr}")
    out.append("\\toprule")
    out.append("Condition & $n$ & Mean & Std & $\\Delta$ & 95\\% CI ($\\Delta$) \\\\")
    out.append("\\midrule")
    for cond in ABLATION_ONLY + ["enip_full"]:
        e = a["conditions"].get(cond)
        if not e:
            continue
        ci = e.get("ci95")
        ci_txt = f"[{ci['lo']:.2f}, {ci['hi']:.2f}]" if ci else "---"
        out.append(f"{LABEL[cond]} & {e['n']} & {fmt(e['mean'])} & {fmt(e['std'])} & "
                   f"{fmt(e['delta_vs_enip_full'], signed=True)} & {ci_txt} \\\\")
    out.append("\\bottomrule")
    out.append("\\end{tabular}")
    out.append("\\caption{Ablation study: mean quality over seven dimensions per manuscript. "
               "Rows marked *share the ablation editor and judge (Gemini 3.5 Flash Lite); "
               "the ENIP-full row comes from the main experiment (Groq gpt-oss-120b, judge J1) "
               "and is shown for reference only.}")
    out.append("\\label{tab:ablation}")
    out.append("\\end{table}")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--analysis", type=Path, default=DEFAULT_ANALYSIS)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    a = json.loads(args.analysis.read_text(encoding="utf-8"))
    overall, per_dim, pairwise = md_tables(a)
    args.out.mkdir(parents=True, exist_ok=True)

    md = [
        "# Paper-ready ablation tables",
        "",
        f"**Generated**: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"**Source**: `{args.analysis.name}` (judge {a.get('judge')}, "
        f"seed {a['bootstrap']['seed']}, {a['bootstrap']['n']} bootstrap resamples)",
        "",
        "## Table 1 — Overall",
        "", overall, "",
        "## Table 2 — Per dimension", "", per_dim, "",
        "## Table 3 — Within-ablation pairwise contrasts", "", pairwise, "",
        "> Pairwise contrasts are the only causally interpretable comparison here: "
        "all three ablation conditions share the same editor and judge.",
        "",
    ]
    (args.out / "paper_tables.md").write_text("\n".join(md), encoding="utf-8")
    (args.out / "paper_tables.tex").write_text(latex_tables(a) + "\n", encoding="utf-8")

    print(f"Wrote {args.out / 'paper_tables.md'}")
    print(f"Wrote {args.out / 'paper_tables.tex'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
