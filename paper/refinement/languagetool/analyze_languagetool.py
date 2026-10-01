#!/usr/bin/env python3
"""
Analyze LanguageTool results against the ENIP evaluation.

Handles both outcomes of run_languagetool.py:
  * Indonesian supported    -> per-category detection counts vs ENIP/B1/B2 fix rates
  * Indonesian unsupported  -> documented negative result + baseline table without LT

Usage:
    python analyze_languagetool.py [--results DIR] [--puebi-report PATH] [--out DIR]
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_RESULTS = HERE / "results"
DEFAULT_PUEBI = HERE.parent.parent / "experiments" / "metrics" / "puebi_report.md"

CAT_ORDER = [f"E{i}" for i in range(1, 11)]


def parse_puebi_report(path: Path) -> dict:
    """Parse the weighted fix-rate table from experiments/metrics/puebi_report.md."""
    if not path.exists():
        return {}
    table = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 6 or not re.match(r"^E\d{1,2}$", cells[0]):
            continue
        table[cells[0]] = dict(zip(("input", "b3", "enip", "b1", "b2"), cells[1:6]))
    return table


def write_markdown(record: dict, fix_rates: dict, out_path: Path) -> None:
    supported = record.get("indonesian_supported", False)
    lines = [
        "# LanguageTool Comparison — Result",
        "",
        f"**Generated**: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"**Endpoint**: `{record.get('endpoint')}` (probed {record.get('probed_at')})",
        "",
        "## Feasibility",
        "",
        f"- Languages exposed by LanguageTool: **{len(record.get('language_codes', []))}**",
        f"- Indonesian (`id`) supported: **{'YES' if supported else 'NO'}**",
    ]
    probe = record.get("id_check_probe")
    if probe and probe.get("error"):
        e = probe["error"]
        lines.append(
            f"- Direct `POST /check` with `language=id` → **HTTP {e.get('status')} "
            f"{e.get('reason')}**: `{e.get('body', '')[:120]}`"
        )
    for note in record.get("notes", []):
        lines.append(f"- {note}")

    lines += ["", "## Mechanical baseline: fix rate per PUEBI category (weighted)", ""]
    if fix_rates:
        header = "| Kategori | input | B3 (hunspell) | ENIP | B1 | B2 | LanguageTool |"
        lines.append(header)
        lines.append("|---|---|---|---|---|---|---|")
        for cat in CAT_ORDER:
            row = fix_rates.get(cat)
            if not row:
                continue
            lt_cell = "n/a (no id rules)" if not supported else "see results JSON"
            lines.append(
                f"| {cat} | {row['input']} | {row['b3']} | {row['enip']} | "
                f"{row['b1']} | {row['b2']} | {lt_cell} |"
            )
    else:
        lines.append("_puebi_report.md not found — fix-rate table unavailable._")

    if supported:
        lines += ["", "## LanguageTool detections per manuscript", ""]
        lines.append("| Naskah | Matches | E1..E10 + other |")
        lines.append("|---|---|---|")
        for m in record.get("manuscripts", []):
            cats = m.get("categories", {})
            detail = ", ".join(f"{k}:{v}" for k, v in cats.items() if v)
            lines.append(f"| {m['manuscript']} | {m.get('matches', '-')} | {detail} |")
    else:
        lines += [
            "",
            "## Conclusion",
            "",
            "LanguageTool cannot serve as an Indonesian GEC baseline: it publishes no "
            "Indonesian rules, so the only mechanical open-source baseline available for "
            "this corpus is the hunspell id-ID detector (B3), which flags errors without "
            "producing corrected text (fix rate not applicable). ENIP/B1/B2 remain the "
            "text-producing conditions.",
        ]

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    ap.add_argument("--puebi-report", type=Path, default=DEFAULT_PUEBI)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    out_dir = args.out or args.results

    results_file = args.results / "languagetool_results.json"
    if not results_file.exists():
        print(f"Missing {results_file} — run run_languagetool.py first.")
        return 1

    record = json.loads(results_file.read_text(encoding="utf-8"))
    fix_rates = parse_puebi_report(args.puebi_report)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "indonesian_supported": record.get("indonesian_supported", False),
        "n_languages": len(record.get("language_codes", [])),
        "fix_rates_available": bool(fix_rates),
        "manuscripts_run": len(record.get("manuscripts", [])),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "languagetool_analysis.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(record, fix_rates, out_dir / "RESULTS.md")
    print(f"Wrote {out_dir / 'RESULTS.md'} and languagetool_analysis.json")
    print(f"Indonesian supported: {summary['indonesian_supported']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
