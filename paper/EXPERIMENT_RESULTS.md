# EXPERIMENT_RESULTS — Status Eksekusi (2026-08-23)

Ringkasan jujur hasil eksekusi PLAN.md. Angka hanya dari
`paper/experiments/metrics/*` dan `runs/`; tidak ada perhitungan manual.

**Status besar: pipeline teruji end-to-end; menunggu satu hari kuota
untuk re-run final di atas korpus bersih** (lihat "Blokir eksplisit").

## Keputusan eksekusi (K1–K6, terbaru)

K1 **openai/gpt-oss-120b (Groq)** — migrasi dari llama-3.3-70b yang
di-decommission Groq · K2 J1=qwen/qwen3.6-27b, J2=openai/gpt-oss-20b,
J3=gemini-3.5-flash · K3 API temp 0 · K4 Full 20 · K5 sesuai plan ·
K6 tidak ada editor → Fase E SKIP.

Deviasi utama (detail: `experiments/README.md` Deviasi #1–#8):

1. B3 = hunspell id-ID (LanguageTool tidak mendukung bahasa Indonesia).
2. Batas free tier Groq aktual: **TPM 8K / TPD 200K per model**.
3. ENIP via API = **lapisan aktivasi (SKILL.md)** saja — bundle penuh
   10.589 token mustahil lewat TPM 8K; setara tahap 2 progressive
   disclosure yang selalu dimuat runtime.
4. **Bug korpus diperbaiki**: 65% injeksi lama korup (splice offset);
   korpus v2 tervalidasi 238/238 error tepat posisi & bentuk.

## Infrastruktur yang sudah tervalidasi (pilot era gpt-oss-120b)

- Runner API: b1/b2/enip masing-masing **20/20 tuntas < 1 jam**
  (±154rb token dari TPD 200K) — nol kegagalan permanen.
- C1 detektor v2 (`scripts/puebi_errors.py` + `output_body.py`):
  occurrence-ratio per kategori di badan naskah hasil edit;
  tervalidasi **nol kategori ter-skip**, baseline input tepat 0.0,
  E7 tidak lagi tertelan titik akhir kalimat.
- C4 proksi koherensi memakai ekstraksi badan yang sama (output
  terstruktur ENIP tidak lagi mengotori statistik prosa).
- D3 overhead ✅: discovery 382 · aktivasi 2.266 · refs+assets 7.941 ·
  bundle penuh 10.589 token (`metrics/overhead.json`).

Angka C1/C4 yang beredar saat ini dihitung atas run pilot di teks
korup — **jangan dikutip**; akan ditimpa setelah re-run.

## Belum selesai (blokir eksplisit)

1. **Re-run editor (b1/b2/enip ×20) di korpus v2** — menunggu reset
   TPD harian; perintah siap di `experiments/README.md` §"Cara
   menyelesaikan LLM" (Tahap 1–2, ±1 jam proses).
2. **Judge C2 (J1–J3)** + C3 delta self-score + `analyze.py`
   (bootstrap paired, korelasi antar-judge) — setelah Tahap 1.
3. **D1 portability (8 runtime)** dan **D2 trigger (20 query)**:
   butuh interaksi GUI runtime lokal — skema & berkas siap.
4. **Fase E**: SKIP (K6) — protokol terdokumentasi di PLAN.md §7.

## Batasan yang harus dikutip di paper

1. B3 bukan LanguageTool (tidak ada dukungan id-ID); hanya flag kata
   di luar kamus hunspell.
2. ENIP via API memuat SKILL.md saja (keterbatasan TPM free tier);
   references/assets tidak tersedia bagi model dalam mode single-shot.
3. J2 satu family dengan editor (gpt-oss); keduanya OpenAI open-weight.
4. Judge & metrik final menyusul re-run; klaim RQ1–RQ5 menunggu angka
   resmi dari `metrics/*.json`.
