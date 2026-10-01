#!/usr/bin/env python3
"""Ablation analyzer — within-study comparison of ENIP components.

Compares the ablation conditions against the ENIP-full control that was run
with the *same* editor model and the same judge on the same manuscripts, so the
deltas are interpretable. Optionally prints the main evaluation's ENIP row as a
clearly-labelled cross-study reference (different editor + judge panel).

Inputs (paper/experiments/metrics/):
  ablation_scores.json  conditions x manuscripts x judge x trial
  scores.json           main evaluation (b1/b2/enip, judges J1/J2/J3)

Outputs (paper/refinement/ablation/results/):
  ablation_analysis.json, ablation_analysis.md

Statistics: per-manuscript mean over the 7 rubric dimensions (averaged across
trials), paired differences against the control, percentile bootstrap for the
95% CI (default 10,000 resamples, seed 42).

Usage:
    python ablation_analyzer.py [--scores DIR] [--out DIR] [--bootstrap 10000]
"""

import argparse
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_METRICS = HERE.parent.parent / "experiments" / "metrics"
DEFAULT_OUT = HERE / "results"

DIMENSI = ["Kejelasan", "Koherensi", "Kedalaman", "Akurasi", "Gaya",
           "Mekanik", "Engagement"]
BASELINE = "enip_full"
SEED = 42


def load_rows(path: Path):
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def per_manuscript_mean(rows, condition):
    """condition -> id -> mean over 7 dimensions (trials averaged)."""
    acc = {}
    for r in rows:
        if r["condition"] != condition:
            continue
        skor = r.get("skor") or {}
        vals = [skor[d] for d in DIMENSI if isinstance(skor.get(d), (int, float))]
        if vals:
            acc.setdefault(r["id"], []).append(sum(vals) / len(vals))
    return {k: statistics.fmean(v) for k, v in acc.items()}


def dim_means(rows, condition):
    acc = {d: [] for d in DIMENSI}
    for r in rows:
        if r["condition"] != condition:
            continue
        for d in DIMENSI:
            v = (r.get("skor") or {}).get(d)
            if isinstance(v, (int, float)):
                acc[d].append(v)
    return {d: (statistics.fmean(v) if v else None) for d, v in acc.items()}


def bootstrap_ci(diffs, seed=SEED, n=10000, alpha=0.05):
    if not diffs:
        return None
    import random
    rng = random.Random(seed)
    m = len(diffs)
    means = []
    for _ in range(n):
        means.append(sum(diffs[rng.randrange(m)] for _ in range(m)) / m)
    means.sort()
    return {"lo": round(means[int((alpha / 2) * n)], 4),
            "hi": round(means[int((1 - alpha / 2) * n) - 1], 4),
            "n_bootstrap": n, "seed": seed}


def fmt(x, nd=3, signed=False):
    if x is None:
        return "—"
    return f"{x:+.{nd}f}" if signed else f"{x:.{nd}f}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--scores", type=Path, default=DEFAULT_METRICS)
    ap.add_argument("--ablation-scores", type=Path, default=None)
    ap.add_argument("--main-scores", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--bootstrap", type=int, default=10000)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    abl_path = args.ablation_scores or (args.scores / "ablation_scores.json")
    main_path = args.main_scores or (args.scores / "scores.json")
    abl = load_rows(abl_path)
    main_rows = load_rows(main_path)
    if not abl:
        print(f"No ablation scores at {abl_path}")
        return 1

    conditions = [BASELINE] + sorted({r["condition"] for r in abl} - {BASELINE})
    judges = sorted({f"{r['judge']}/{r.get('model', '?')}" for r in abl})
    editors = sorted({r.get("model", "?") for r in abl})
    manuscripts = sorted({r["id"] for r in abl})

    pm = {c: per_manuscript_mean(abl, c) for c in conditions}
    base = pm[BASELINE]
    if not base:
        print(f"Baseline condition '{BASELINE}' missing — cannot compute deltas.")
        return 1

    analysis = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ablation_scores_file": str(abl_path),
        "baseline": BASELINE,
        "judges": judges,
        "editor_models": editors,
        "manuscripts": manuscripts,
        "n_manuscripts": len(manuscripts),
        "n_rows": len(abl),
        "bootstrap": {"n": args.bootstrap, "seed": SEED, "ci": 0.95},
        "conditions": {},
    }

    lines = [
        "# Ablation Analysis (within-study)", "",
        f"**Generated**: {analysis['generated_at']}",
        f"**Judges**: {', '.join(judges)}",
        f"**Editor model (all conditions)**: {', '.join(editors)}",
        f"**Manuscripts**: {len(manuscripts)} ({manuscripts[0]} … {manuscripts[-1]})",
        f"**Evaluations**: {len(abl)} | **Bootstrap**: {args.bootstrap} resamples, seed {SEED}, 95% CI",
        "", "All conditions share editor, judge, prompt template and manuscript set; the only",
        "difference is which reference file is withheld. Deltas are therefore interpretable.",
        "",
        "## Overall quality (mean of 7 dimensions, per manuscript)", "",
        "| Condition | n | Mean | Std | Δ vs ENIP-full | 95% CI (Δ) | Significant |",
        "|---|---|---|---|---|---|---|",
    ]

    for cond in conditions:
        shared = sorted(set(pm[cond]) & set(base))
        vals = [pm[cond][i] for i in shared]
        diffs = [pm[cond][i] - base[i] for i in shared]
        entry = {
            "n": len(vals),
            "mean": round(statistics.fmean(vals), 4) if vals else None,
            "std": round(statistics.stdev(vals), 4) if len(vals) > 1 else None,
            "delta_vs_enip_full": round(statistics.fmean(diffs), 4) if diffs else None,
            "per_dimension": dim_means(abl, cond),
        }
        if cond == BASELINE:
            entry.update({"delta_vs_enip_full": 0.0, "ci95": None,
                          "significant": False, "ci_excludes_zero": False})
            ci_txt, sig = "—", "control"
        else:
            ci = bootstrap_ci(diffs, n=args.bootstrap)
            excl = bool(ci and (ci["hi"] < 0 or ci["lo"] > 0))
            entry.update({"ci95": ci, "significant": excl, "ci_excludes_zero": excl})
            ci_txt = f"[{ci['lo']:.3f}, {ci['hi']:.3f}]" if ci else "—"
            sig = "yes" if excl else "no"
        analysis["conditions"][cond] = entry
        lines.append(f"| {cond} | {entry['n']} | {fmt(entry['mean'])} | {fmt(entry['std'])} | "
                     f"{fmt(entry['delta_vs_enip_full'], signed=True)} | {ci_txt} | {sig} |")

    # Cross-study reference (different editor + judge panel) — reference only.
    if main_rows:
        enip_pm = per_manuscript_mean([r for r in main_rows if r["condition"] == "enip"], "enip")
        shared = sorted(set(base) & set(enip_pm))
        if shared:
            analysis["cross_study_reference"] = {
                "condition": "enip (main study)",
                "editor": "openai/gpt-oss-120b (Groq)",
                "judges": "J1/J2/J3",
                "n": len(shared),
                "mean": round(statistics.fmean([enip_pm[i] for i in shared]), 4),
                "note": "different editor model and judge panel — not comparable to the rows above",
            }

    lines += ["", "## Per-dimension means", "",
              "| Condition | " + " | ".join(DIMENSI) + " |", "|---|" + "---|" * len(DIMENSI)]
    for cond in conditions:
        d = analysis["conditions"][cond]["per_dimension"]
        lines.append(f"| {cond} | " + " | ".join(fmt(d.get(x), 2) for x in DIMENSI) + " |")

    lines += ["", "## Pairwise contrasts", "", "| Contrast (A − B) | Δ | 95% CI | Significant |",
              "|---|---|---|---|"]
    for i, a in enumerate(conditions):
        for b in conditions[i + 1:]:
            shared = sorted(set(pm[a]) & set(pm[b]))
            if not shared:
                continue
            diffs = [pm[a][m] - pm[b][m] for m in shared]
            ci = bootstrap_ci(diffs, n=args.bootstrap)
            excl = bool(ci and (ci["hi"] < 0 or ci["lo"] > 0))
            analysis.setdefault("pairwise", []).append(
                {"a": a, "b": b, "delta": round(statistics.fmean(diffs), 4),
                 "ci95": ci, "significant": excl})
            lines.append(f"| {a} − {b} | {fmt(statistics.fmean(diffs), signed=True)} | "
                         f"[{ci['lo']:.3f}, {ci['hi']:.3f}] | {'yes' if excl else 'no'} |")

    sig = {c: v["significant"] for c, v in analysis["conditions"].items() if c != BASELINE}
    lines += ["", "## Interpretation", ""]
    for cond, s in sig.items():
        e = analysis["conditions"][cond]
        direction = "lower" if e["delta_vs_enip_full"] < 0 else "higher"
        if s:
            lines.append(f"- Withholding **{cond.replace('enip_', '').replace('_', ' ')}** yields a "
                         f"significantly {direction} score than ENIP-full "
                         f"(Δ {e['delta_vs_enip_full']:+.3f}, 95% CI "
                         f"[{e['ci95']['lo']:.3f}, {e['ci95']['hi']:.3f}]).")
        else:
            lines.append(f"- Withholding **{cond.replace('enip_', '').replace('_', ' ')}** does not "
                         f"change judged quality (Δ {e['delta_vs_enip_full']:+.3f}, 95% CI "
                         f"[{e['ci95']['lo']:.3f}, {e['ci95']['hi']:.3f}] includes 0).")
    if "cross_study_reference" in analysis:
        cs = analysis["cross_study_reference"]
        lines.append(f"- Cross-study reference only: the main evaluation's ENIP "
                     f"({cs['editor']}, judges {cs['judges']}) scores {cs['mean']:.2f} on the same "
                     f"manuscripts; the gap to the rows above reflects the editor/judge change, "
                     f"not a component effect.")
    lines += [
        "", "## Caveats", "",
        f"- Single judge panel ({', '.join(judges)}) and one editor model; the main evaluation "
        "used three judges, so absolute values are not comparable to it.",
        "- Reference removal is operationalised as an explicit exclusion note appended to "
        "SKILL.md (see experiments/scripts/run_ablation.py), not by deleting the file, because "
        "the API path loads the activation layer only.",
        "- The Groq key used for the main evaluation has expired, so the original editor "
        "(openai/gpt-oss-120b) and judges J1/J2 could not be reused for this re-run.",
    ]

    (args.out / "ablation_analysis.json").write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.out / "ablation_analysis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {args.out / 'ablation_analysis.md'}")
    for c, v in analysis["conditions"].items():
        print(f"  {c}: mean={v['mean']} delta={v['delta_vs_enip_full']} sig={v.get('significant')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
