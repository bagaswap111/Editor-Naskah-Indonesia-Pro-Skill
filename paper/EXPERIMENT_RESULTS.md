# EXPERIMENT_RESULTS — Status Eksekusi (2026-08-24)

Ringkasan jujur hasil eksekusi PLAN.md. Angka hanya dari
`paper/experiments/metrics/*` dan `runs/`; tidak ada perhitungan manual.

**Status besar: re-run editor selesai di korpus bersih (gpt-oss-120b,
20/20/20); C1/C4 final terbit; judge C2 berjalan bertahap mengikuti
kuota harian free tier** (lihat "Blokir eksplisit").

## Keputusan eksekusi (K1–K6, terbaru)

K1 **openai/gpt-oss-120b (Groq)** — migrasi dari llama-3.3-70b yang
di-decommission Groq · K2 J1=qwen/qwen3.6-27b, J2=openai/gpt-oss-20b,
J3=gemini-3.5-flash · K3 API temp 0 · K4 Full 20 · K5 sesuai plan ·
K6 tidak ada editor → Fase E SKIP.

Deviasi utama (detail: `experiments/README.md` Deviasi #1–#8):

1. B3 = hunspell id-ID (LanguageTool tidak mendukung bahasa Indonesia).
2. Batas free tier Groq aktual: **TPM 8K / TPD 200K per model**
   (TPD = jendela rolling — pemakaian usai >24 jam kembali tersedia).
3. ENIP via API = **lapisan aktivasi (SKILL.md)** saja — bundle penuh
   10.589 token mustahil lewat TPM 8K; setara tahap 2 progressive
   disclosure yang selalu dimuat runtime.
4. **Bug korpus diperbaiki**: 65% injeksi lama korup (splice offset);
   korpus v2 tervalidasi 238/238 error tepat posisi & bentuk.
5. Qwen3.6 (J1) menyisipkan `<think>` di content → parser JSON judge
   diperkeras; label dimensi self-score ENIP bervariasi → analyze.py
   memetakan via aturan kata-kunci, baris tak terpetakan dilaporkan.

## Hasil final Fase A/B/C1/C4/D3 (korpus bersih, gpt-oss-120b)

- Re-run editor tuntas 2026-08-23 02:00–03:01 WIB: b1/b2/enip
  masing-masing **20/20**, nol kegagalan permanen (±154rb token).
- **C1 PUEBI (final)** — mean fix rate (`metrics/puebi_report.md`):
  b1 **0.9774** · b2 **0.9769** · enip **0.9681** (baseline input 0.0).
  Per kategori: ENIP unggul E1 (0.972 vs 0.944); tertinggal di E9
  (0.70 vs 0.90/0.77) dan E2/E6. B3 (hunspell) tidak menghasilkan
  teks baru → hanya baseline deteksi.
- **C4 proksi koherensi (final)**: `metrics/proxies.json`.
- **D3 overhead ✅**: discovery 382 · aktivasi 2.266 · refs+assets
  7.941 · bundle penuh 10.589 token (`metrics/overhead.json`).

## Belum selesai (blokir eksplisit)

1. **C2 judge** — 25 Agu: J2 selesai **120/120**; J3 mengikuti reset
   harian Gemini; J1 terkendala TPD rolling Groq (biaya ±4–5rb token
   per evaluasi → sisa ±110 evaluasi ≈ 3 hari kuota 200K) — tuntas
   ±27 Agu. Semua idempotent via `scripts/judge_loop.sh`.
2. **C3 delta self-score + statistik** — `scripts/analyze.py` siap;
   jalankan setelah scores.json = 300.
3. **D1 portability** — 🔶 **OpenCode ✅ (1/8)**: skill aktif tanpa
   modifikasi, telemetri progressive disclosure terekam
   (`portability/logs/opencode_pop03.out`). Claude Code: skill
   terpasang di `.claude/skills/` tetapi kredensial tidak ada
   (`/login` dulu). 6 runtime lain: butuh aplikasi GUI pengguna.
   **D2 trigger ✅ (RQ3 jawab)**: precision **1.0**, recall **0.9**
   (1 FN: trig_05 dijawab generik bahasa Inggris); TN 10/10; log
   `trigger/logs/`, hasil `trigger/results.json`.
4. **Fase E**: SKIP (K6) — protokol tetap di PLAN.md §7.
5. **F konsolidasi paper** — setelah analysis_report.md final.

## Temuan audit sementara (data parsial, jangan dikutip)

- Judge memberi **Mekanik=10 pada 26% penilaian** padahal C1
  mendeteksi sisa error pada mayoritas output — divergensi judge vs
  detektor deterministik; ENIP justru paling sering dapat 10 (22/41).
- **J3 lebih tajam** dari J2 (semua skor terendah miliknya, min 4.4);
  reliabilitas intra-judge antar-trial r=0.56; J2–J3 r=0.55 (n=25).

## Batasan yang harus dikutip di paper

1. B3 bukan LanguageTool (tidak ada dukungan id-ID); hanya flag kata
   di luar kamus hunspell.
2. ENIP via API memuat SKILL.md saja (keterbatasan TPM free tier);
   references/assets tidak tersedia bagi model dalam mode single-shot.
3. J2 satu family dengan editor (gpt-oss); keduanya OpenAI open-weight.
4. Label dimensi pada tabel Skor Kualitas ENIP tidak selalu persis
   rubrik (mis. "Koherensi & Kohesi", ada yang hilang) — delta
   self-score (RQ5) dilaporkan dengan liputan per dimensi.
