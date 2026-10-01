#!/usr/bin/env python3
"""
Compare LanguageTool results with the ENIP evaluation results.

Reads the artifacts produced by run_languagetool.py / analyze_languagetool.py
and prints the per-category table. When LanguageTool has no Indonesian rules the
LanguageTool column is reported as n/a rather than fabricated counts.

Usage:
    python compare_languagetool.py [--results DIR] [--puebi-report PATH]
"""

import argparse
import json
import sys
from pathlib import Path

from analyze_languagetool import CAT_ORDER, parse_puebi_report

HERE = Path(__file__).resolve().parent
DEFAULT_RESULTS = HERE / "results"
DEFAULT_PUEBI = HERE.parent.parent / "experiments" / "metrics" / "puebi_report.md"


def load_lt_totals(results_dir: Path):
    """Aggregate LanguageTool category counts across manuscripts, if any run happened."""
    path = results_dir / "languagetool_results.json"
    if not path.exists():
        return None, None
    record = json.loads(path.read_text(encoding="utf-8"))
    if not record.get("indonesian_supported"):
        return record, None
    totals = {}
    for m in record.get("manuscripts", []):
        for cat, n in (m.get("categories") or {}).items():
            totals[cat] = totals.get(cat, 0) + n
    return record, totals


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    ap.add_argument("--puebi-report", type=Path, default=DEFAULT_PUEBI)
    args = ap.parse_args()

    record, lt_totals = load_lt_totals(args.results)
    if record is None:
        print(f"Missing {args.results / 'languagetool_results.json'} — run run_languagetool.py first.")
        return 1

    fix_rates = parse_puebi_report(args.puebi_report)
    if not fix_rates:
        print(f"Warning: no fix-rate table parsed from {args.puebi_report}")

    supported = record.get("indonesian_supported", False)
    print("=== Perbandingan ENIP vs LanguageTool ===")
    print(f"LanguageTool Indonesian support: {'YES' if supported else 'NO'} "
          f"({len(record.get('language_codes', []))} language codes)")
    print()
    header = f"{'Kat':<6}{'LT':>10}{'input':>10}{'B3':>10}{'ENIP':>10}{'B1':>10}{'B2':>10}"
    print(header)
    print("-" * len(header))

    lt_total = 0
    for cat in CAT_ORDER:
        row = fix_rates.get(cat, {})
        if lt_totals is None:
            lt_cell = "n/a"
        else:
            n = lt_totals.get(cat, 0)
            lt_cell = str(n)
            lt_total += n
        print(f"{cat:<6}{lt_cell:>10}{row.get('input', '-'):>10}{row.get('b3', '-'):>10}"
              f"{row.get('enip', '-'):>10}{row.get('b1', '-'):>10}{row.get('b2', '-'):>10}")

    print("-" * len(header))
    if lt_totals is None:
        print("LanguageTool: tidak dapat dijadikan baseline bahasa Indonesia "
              "(lihat results/RESULTS.md untuk bukti HTTP 400).")
        print("Baseline mekanis yang tersedia: B3 (hunspell id-ID, deteksi tanpa teks hasil edit).")
    else:
        print(f"LanguageTool total temuan: {lt_total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
