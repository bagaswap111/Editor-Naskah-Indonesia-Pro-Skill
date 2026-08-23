#!/usr/bin/env python3
"""Ekstraksi badan naskah dari output kondisi (shared).

Output ENIP berformat terstruktur (Diagnosis -> Naskah Hasil Edit ->
Catatan -> Style Sheet -> Skor). Metrik C1/C4 hanya boleh menilai BADAN
NASKAH HASIL EDIT, bukan kutipan error di bagian diagnosis/catatan
(artefak pengukuran — lihat Deviasi #8 di experiments/README.md).

Aturan deterministik:
  - Cari header "Naskah Hasil Edit*" -> mulai setelah baris itu.
  - Berhenti di section bernomor berikutnya (mis. "3. Catatan Editor").
  - Buang penanda blockquote "> ".
  - Fallback: jika tidak ada header ATAU hasil < 50 kata -> teks utuh
    (kasus B1/B2 yang berupa prosa polos).
"""
import re

START = re.compile(r"Naskah\s+Hasil\s+Edit", re.I)
NEXT_SECTION = re.compile(r"^\s*(?:\*\*)?\s*\d+\s*\.\s+\S", re.M)
BQ = re.compile(r"^\s*>\s?", re.M)


def extract_body(text):
    m = START.search(text)
    if not m:
        return text.strip()
    lines = text[m.start():].splitlines()[1:]
    tail = "\n".join(lines)
    nxt = NEXT_SECTION.search(tail)
    limit = nxt.start() if nxt else len(tail)
    body, consumed = [], 0
    for ln in lines:
        if consumed >= limit:
            break
        body.append(ln)
        consumed += len(ln) + 1
    out = BQ.sub("", "\n".join(body))
    if len(out.split()) < 50:
        return text.strip()
    return out.strip()
