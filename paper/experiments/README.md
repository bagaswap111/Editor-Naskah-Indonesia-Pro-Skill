# Keputusan & Status Eksekusi (Fase B–F)

Dokumen ini dicatat oleh eksekutor sesuai PLAN.md (bagian "Keputusan
yang Harus Diambil Saat Eksekusi"). Tanggal sesi: 2026-08-15/16.

## K1–K6

| ID | Keputusan | Status |
|---|---|---|
| K1 | Editor (B1/B2/ENIP): **openai/gpt-oss-120b via Groq API** (migrasi dari llama-3.3-70b yang decommissioned — Deviasi #6) | ⏳ re-run penuh di korpus bersih; pilot 60/60 tuntas |
| K2 | Judge (beda family dari editor): **J1 = qwen/qwen3.6-27b** (utama, trial 0 & 0.7); J2 = **openai/gpt-oss-20b** (lemah, Deviasi #6); J3 = gemini-3.5-flash (lintas-penyedia) | ⏳ menunggu re-run editor |
| K3 | Runs via API, temperature 0 (editor); judge trial 0 & 0.7 | ✅ |
| K4 | Ukuran korpus: Full 20 | ✅ korpus 20 sintetis (v2 bersih) + 20 nyata (4 set) |
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
6. **Migrasi model editor (2026-08-22)**: `llama-3.3-70b-versatile`
   DAN `llama-3.1-8b-instant` **decommissioned** Groq (tidak ada lagi
   model Llama di daftar model). Sesuai keputusan eksekutor:
   editor = **`openai/gpt-oss-120b`** untuk SEMUA kondisi (B1/B2/ENIP
   di-re-run penuh; hasil era llama menjadi pilot), J2 = **`openai/
   gpt-oss-20b`** (satu family dengan editor — dicatat sebagai
   keterbatasan). Batas free tier aktual: TPM 8K, TPD 200K per model.
7. **ENIP via API = lapisan aktivasi saja (SKILL.md)**: bundle penuh
   (10.589 token) melampaui TPM 8K sehingga mustahil di SEMUA model
   Groq gratis. System prompt ENIP kini = body SKILL.md + parameter
   sesi (±2,1rb token) — setara tahap 2 progressive disclosure yang
   dijamin selalu dimuat runtime; references/assets bersifat on-demand
   dan tak dapat dieksekusi model dalam satu panggilan API.
8. **Bug korpus ditemukan & diperbaiki (2026-08-22)**: `inject()` di
   build_corpus.py menerapkan penggantian kiri-ke-kanan memakai offset
   teks ASLI pada string yang sudah berubah panjang → 65% injeksi
   (156/238) menghasilkan splice salah (mis. "kualkwalitasf"). Fix:
   penggantian kanan-ke-kiri + offset final dihitung dari delta kiri.
   Korpus diregenerasi (seed sama): 238/238 offset kini tepat menunjuk
   bentuk salah; distribusi kategori identik. **Seluruh run LLM harus
   dilakukan ulang** di atas teks bersih (run sebelumnya = pilot).

## Status per fase

| Fase | Status | Catatan |
|---|---|---|
| A korpus | ✅ (v2 bersih) | Bug offset diperbaiki; 238/238 error terverifikasi di teks (Deviasi #8) |
| B runner | ✅ final | Re-run gpt-oss-120b di korpus v2 tuntas 2026-08-23 (20/20 per kondisi) |
| C metrik | 🔶 sebagian final | C1 fix rate final (enip 0.9681 < b1 0.9774 ≈ b2 0.9769); C4 final; **C2 judge berjalan bertahap** (kuota harian: J2 live, J1 tunggu refund TPD rolling, J3 tunggu reset harian); C3+analyze.py siap, jalankan setelah scores lengkap |
| D1 portability | ⏳ manual | skema + 8 runtime siap; butuh interaksi GUI |
| D2 trigger | ⏳ manual | 20 query siap; butuh runtime lokal |
| D3 overhead | ✅ | discovery 382, aktivasi 2266, refs+assets 7941, bundle 10589 token |
| E human | SKIP | editor tidak tersedia (K6); protokol tetap di PLAN.md §7 |
| F konsolidasi | ⏳ | EXPERIMENT_RESULTS.md menyusul setelah re-run |

## Cara menyelesaikan LLM (resume, kapan saja)

Tahap 1–2 (editor + metrik otomatis) **sudah tuntas** di korpus v2
(2026-08-23). Sisa pekerjaan = judge C2 bertahap + analisis:

```bash
# .env di paper/experiments/ berisi GROQ_API_KEY + GEMINI_API_KEY (gitignored)
cd paper/experiments

# Tahap 3 — judge (idempotent; jalankan berulang sampai lengkap):
python3 scripts/judge.py --judges J2   # Groq gpt-oss-20b — bucket TPD longgar
python3 scripts/judge.py --judges J1   # Groq qwen3.6-27b — tunggu refund TPD rolling (malam)
python3 scripts/judge.py --judges J3   # Gemini 20 req/hari → sekali/hari

# Tahap 4 — analisis & laporan (lokal, instan):
python3 scripts/analyze.py             # → metrics/analysis.json + analysis_report.md
```

Catatan infrastruktur judge: pacing per model (`JUDGE_MIN_INTERVAL`,
default 32 s) menghindari tabrakan TPM 8K; scores.json ditulis atomik
+ merge antar proses sehingga beberapa juri boleh paralel.

Semua output mentah wajib disimpan di runs/ tanpa retouch dan di-commit.