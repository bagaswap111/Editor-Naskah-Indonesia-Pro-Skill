# Keputusan & Status Eksekusi (Fase B–F)

Dokumen ini dicatat oleh eksekutor sesuai PLAN.md (bagian "Keputusan
yang Harus Diambil Saat Eksekusi"). Tanggal sesi: 2026-08-15/16.

## K1–K6

| ID | Keputusan | Status |
|---|---|---|
| K1 | Editor (B1/B2/ENIP): **llama-3.3-70b-versatile via Groq API** (pengganti Claude — user hanya punya key Groq) | ✅ B1+B2 (40/40); ⏳ ENIP 1/20 (berjalan bertahap, lihat Deviasi #4) |
| K2 | Judge (bedah dari editor): **J1 = qwen/qwen3.6-27b (Groq, utama, trial 0 & 0.7)**; J2 = llama-3.1-8b-instant (sensitivitas model lemah); J3 = gemini-3.5-flash (sensitivitas lintas-penyedia) | ⏳ J3: 2/60 (Gemini 20 req/hari); J1/J2 menunggu kuota |
| K3 | Runs via API, temperature 0 (editor); judge trial 0 & 0.7 | ✅ b1/b2 temp 0 |
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
4. **Batas tier gratis (ditemukan saat eksekusi 2026-08-16)**:
   - Groq: TPD (tokens/day) **100.000 per model per org** — B1+B2
     (40 run, ±96,6k token) sudah hampir memenuhinya. Reset ≈ 2 j.
   - Gemini (OpenAI-compat): **20 request/hari/model** free tier
     (`GenerateRequestsPerDayPerProjectPerModel-FreeTier`).
   Konsekuensi: ENIP + judge dijamu dalam **jadwal harian**; semua skrip
   idempotent (resume-safe; `run_api.py` skip file yang ada, log
   inkremental per run). Eksekutor bebas melanjutkan kapan pun dengan
   perintah di bagian bawah.
5. **J1 ≠ deepseek-r1-distill-llama-70b**: model tersebut sudah
   **decommissioned** di Groq (400 invalid_request) saat verifikasi
   (2026-08-16). Pengganti: **qwen/qwen3.6-27b** — beda family dari
   editor (Llama) sehingga ukuran "judge ≠ editor" tetap terpenuhi.
   Ditemukan pula bahwa `gemini-2.5-flash` tidak tersedia untuk user
   baru (404) → J3 memakai `gemini-3.5-flash`.

## Status per fase

| Fase | Status | Catatan |
|---|---|---|
| A korpus | ✅ | 20 naskah, injeksi E1–E10, metadata ground truth, commit `c52324d` |
| B runner | ⏳ | b1 ✅ b2 ✅ (fix rate 0.5506 / 0.4709 — C1); enip 1/20; b3 ✅ (sebelumnya) |
| C metrik | ⏳ | puebi b1/b2 ✅; proxies b1/b2 ✅ (CV 0.446/0.394); judge J3 2/60; J1/J2 pending |
| D1 portability | ⏳ manual | skema + 8 runtime siap; butuh interaksi GUI |
| D2 trigger | ⏳ manual | 20 query siap; butuh runtime lokal |
| D3 overhead | ✅ | discovery 382, aktivasi 2266, refs+assets 7941, bundle 10589 token |
| E human | SKIP | editor tidak tersedia (K6); protokol tetap di PLAN.md §7 |
| F konsolidasi | ✅ (sebagian) | laporan ini + EXPERIMENT_RESULTS.md |

## Cara menyelesaikan LLM (resume, kapan saja)

Pola 1 — koneksi & kuota:

```bash
# .env di paper/experiments/ berisi GROQ_API_KEY + GEMINI_API_KEY (gitignored)
# resume ENIP (skip file yang sudah ada, log inkremental; hentikan saat 429):
python3 scripts/run_api.py --condition enip --provider groq
# ulangi di sesi berikutnya sampai "Selesai" tanpa 429 → ENIP 20/20.
```

Pola 2 — judge (idempotent; hentikan/ulang bebas):

```bash
python3 scripts/judge.py --judges J1        # utama, trial 0 & 0.7 (Groq)
python3 scripts/judge.py --judges J2        # sensitivitas model lemah (Groq)
python3 scripts/judge.py --judges J3        # sensitivitas lintas-penyedia (Gemini)
# J3 hanya 20 request/hari → jalankan sekali per hari (maksimal).
```

Pola 3 — metrik & laporan:

```bash
python3 scripts/puebi_errors.py && python3 scripts/proxies.py
# C3 delta self-score, bootstrap, korelasi antar-judge: scripts/analyze.py (menyusul)
```

Semua output mentah wajib disimpan di runs/ tanpa retouch dan di-commit.