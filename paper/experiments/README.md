# Keputusan & Status Eksekusi (Fase B–F)

Dokumen ini dicatat oleh eksekutor sesuai PLAN.md (bagian "Keputusan
yang Harus Diambil Saat Eksekusi"). Tanggal sesi: 2026-08-15.

## K1–K6

| ID | Keputusan | Status |
|---|---|---|
| K1 | Editor (B1/B2/ENIP): Claude Sonnet 4.x via Anthropic API (default plan) | **DITUNDA** — env `ANTHROPIC_API_KEY` kosong; runner siap (`scripts/run_api.py`) |
| K2 | Judge: GPT-4o (berbeda dari editor) | **DITUNDA** — env `OPENAI_API_KEY` kosong; rubrik siap (dari references/QUALITY_METRICS.md) |
| K3 | Runs via API, temperature 0 | **DITUNDA** — menunggu K1/K2 |
| K4 | Ukuran korpus: Full 20 | ✅ korpus 20 sintetis + 20 nyata (4 set) |
| K5 | Komposisi: 10 injeksi + 6 kontrol + 4 semi-formal | ✅ Fase A selesai |
| K6 | Editor manusia | TIDAK tersedia → Fase E **SKIP**, protokol terdokumentasi |

## Deviasi yang dicatat (penting)

1. **B3 = LanguageTool TIDAK FEASIBLE**: LanguageTool (public API dan
   standalone 6.6) TIDAK mendukung bahasa Indonesia (daftar bahasa resmi
   tanpa id-ID; diverifikasi 2026-08-15). B3 diganti **hunspell + kamus
   id-ID** (LibreOffice/dictionaries, 46.905 entri) — hanya mendeteksi
   kata di luar kamus; varian non-baku (resiko, praktek, ijin) ada di
   kamus LibreOffice → keterbatasan diakui.
2. **A4 set nyata**: 20 naskah tersedia (buku-kolaborasi-llm, wikipedia-id,
   voa-indonesia, the-conversation-id) — dipakai bila Fase B diperluas;
   eksekusi utama tetap 20 naskah sintetis (K5).
3. **ENIP via API**: kondisi ENIP di-run dengan system prompt = SKILL.md +
   semua references + assets (bundle penuh, lihat overhead.json).
   Progressive disclosure yang terjadi di runtime agent tidak terlihat
   oleh model — ini setara aktivasi penuh; overhead nyata diukur D3.

## Status per fase

| Fase | Status | Catatan |
|---|---|---|
| A korpus | ✅ | 20 naskah, injeksi E1–E10, metadata ground truth, commit `c52324d` |
| B runner | ⏸ B3 ✅, B1/B2/ENIP ⏳ | b3: 20 naskah (runs/b3/); LLM menunggu key |
| C metrik | ⏸ offline ✅, LLM ⏳ | puebi baseline (fix 0.0), proxies input; judge menunggu K2 |
| D1 portability | ⏳ manual | skema + 8 runtime siap; butuh interaksi GUI |
| D2 trigger | ⏳ manual | 20 query siap; butuh runtime lokal |
| D3 overhead | ✅ | discovery 382, aktivasi 2266, refs+assets 7941, bundle 10589 token |
| E human | SKIP | editor tidak tersedia (K6); protokol tetap di PLAN.md §7 |
| F konsolidasi | ✅ (sebagian) | laporan ini + EXPERIMENT_RESULTS.md |

## Cara menyelesaikan LLM (kapan saja)

```bash
export ANTHROPIC_API_KEY=...   # editor
export OPENAI_API_KEY=...      # judge (K2, harus beda model dari editor)
python3 paper/experiments/scripts/run_api.py --condition enip --provider anthropic
python3 paper/experiments/scripts/run_api.py --condition b1   --provider anthropic
python3 paper/experiments/scripts/run_api.py --condition b2   --provider anthropic
python3 paper/experiments/scripts/puebi_errors.py   # perbarui laporan
# judge + delta self-score + signifikan: scripts/judge.py (disusul)
```

Semua output mentah wajib disimpan di runs/ tanpa retouch dan di-commit.