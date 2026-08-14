#!/usr/bin/env python3
"""B3 — baseline mekanik non-LLM: hunspell + kamus id-ID (LibreOffice).

DEVASI (tercatat di README):
  LanguageTool TIDAK mendukung bahasa Indonesia (diverifikasi 2026-08:
  public API api.languagetool.org dan standalone 6.6, daftar bahasa resmi
  tanpa id-ID) -> B3 memakai hunspell + id_ID.dic/.aff dari repo resmi
  LibreOffice/dictionaries. Hanya mendeteksi KATA DI LUAR KAMUS
  (spelling); varian non-baku (resiko, praktek, ijin) ada di kamus
  LibreOffice sehingga tidak terdeteksi -> keterbatasan diakui.

Output: runs/b3/<id>.lt (raw) + runs/b3/summary.json
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # paper/experiments
CORPUS = ROOT / "corpus"
RUNS = ROOT / "runs" / "b3"
TMP = ROOT / ".tmp"
DICPATH = TMP
HUNSPELL = os.environ.get("HUNSPELL", "hunspell")


def check(text):
    env = dict(os.environ, DICPATH=str(DICPATH))
    p = subprocess.run([HUNSPELL, "-d", "id_ID", "-l"],
                       input=text, capture_output=True, text=True, env=env)
    words = [w for w in p.stdout.splitlines() if w.strip()]
    return words, p.stderr.strip()


def main():
    RUNS.mkdir(parents=True, exist_ok=True)
    meta = json.loads((CORPUS / "metadata.json").read_text(encoding="utf-8"))
    summary = {}
    for item in meta["corpus"]:
        tid = item["id"]
        text = (CORPUS / "texts" / f"{tid}.txt").read_text(encoding="utf-8")
        words, err = check(text)
        out = "\n".join(words) + ("\n" if words else "")
        (RUNS / f"{tid}.lt").write_text(out, encoding="utf-8")
        summary[tid] = {"unknown_words": words,
                        "n_unknown": len(words),
                        "stderr": err, "words_total": len(text.split())}
        print(f"  {tid}: {len(words)} kata di luar kamus / {summary[tid]['words_total']} kata")
    (RUNS / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    n_all = sum(v["n_unknown"] for v in summary.values())
    print(f"\nTotal kata di luar kamus: {n_all} di {len(summary)} naskah")


if __name__ == "__main__":
    main()