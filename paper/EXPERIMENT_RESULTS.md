# EXPERIMENT_RESULTS — Status Eksekusi (2026-08-29 19:24)

Ringkasan jujur hasil eksekusi PLAN.md. Angka hanya dari
`paper/experiments/metrics/*` dan `runs/`; tidak ada perhitungan manual.

**Status besar: 2026-08-29 — judge C2 228/300 (J1 48/120, J2 120/120 ✅, J3 60/60 ✅); sisa 72 J1 diblokir TPD rolling Groq (loop hidup). C1/C4/D3 FINAL, D2 ✅, D1 2/8 (OpenCode+Gemini).** Detail blokir lihat bawah.

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

## Belum selesai (blokir eksplisit — update 2026-08-29)

1. **C2 judge — 228/300 (kurang 72 J1)** — J2 120/120 (25 Agu) ✅, J3 60/60 (27 Agu) ✅, J1 48/120 🔶.
   Hari ini (19:23 WIB) `judge_loop.sh` PID 80255 masih hidup, `caffeinate` aktif, log terakhir `HARD_QUOTA groq qwen/qwen3.6-27b`.
   Estimasi rolling TPD: last success 2026-08-29 12:01 → next window 2026-08-30 12:01 (+16.6 jam); butuh ~1.5–2 hari lagi @ ~43 eval/hari (200K TPD ÷ 4.6K/eval). Cek `bash scripts/status.sh`.
2. **C3 + statistik interim** — `metrics/analysis_report.md` (228) sudah di-refresh: `enip_vs_b1 Δ -0.12 p=0.425` (n.s.), `enip_vs_b2 Δ -0.28 p=0.024 *` ; `J1-J2 r=0.629, J1-J3 r=0.685` — **jangan dikutip final** sampai 300/300. Final `python3 scripts/analyze.py` setelah lengkap.
3. **D1 portability — 2/8 ✅** — `OpenCode ✅` (25 Agu, telemetri progressive disclosure) + `Gemini CLI ✅` (28 Agu, `portability/logs/gemini_pop03.out`) — `portability/results.json`.
   Sisa 6 manual: Claude Code (butuh `/login`), Cursor, Codex, Cline, Antigravity, VS Code Copilot (butuh GUI).
   **D2 trigger ✅ (RQ3)**: precision **1.0**, recall **0.9** (FN trig_05), `trigger/results.json` + `trigger/logs/`.
4. **Fase E**: SKIP (K6) — protokol tetap di PLAN.md §7.
5. **F konsolidasi paper** — TBD di `paper/inputs/experimental_log.md` (tabel 7 dimensi, PUEBI rate) menunggu 300; `validate_consistency.py` saat ini PASS interim — re-run setelah TBD terisi.

## Temuan audit interim (228/300 — jangan dikutip final)

- Interim 228: `b1 8.06±0.87, b2 8.22±0.32, enip 7.95±0.72` — ENIP sedikit di bawah B1/B2 overall; per dimensi ENIP unggul tipis Akurasi (+0.16 vs B1) & Mekanik (+0.03 vs B1) tapi kalah Koherensi (-0.33) & Kedalaman (-0.33) — lihat `metrics/analysis_report.md`.
- Korelasi antar-judge menguat di 228: `J1-J2 r=0.629 ρ=0.614 (n=19), J1-J3 r=0.685, J2-J3 r=0.593` vs r=0.55 parsial lama.
- Divergensi tetap: C1 fix_rate mekanik tinggi (ENIP 0.9681) tapi judge masih variatif Mekanik (std 0.91 ENIP).

## Batasan yang harus dikutip di paper

1. B3 bukan LanguageTool (tidak ada dukungan id-ID); hanya flag kata
   di luar kamus hunspell.
2. ENIP via API memuat SKILL.md saja (keterbatasan TPM free tier);
   references/assets tidak tersedia bagi model dalam mode single-shot.
3. J2 satu family dengan editor (gpt-oss); keduanya OpenAI open-weight.
4. Label dimensi pada tabel Skor Kualitas ENIP tidak selalu persis
   rubrik (mis. "Koherensi & Kohesi", ada yang hilang) — delta
   self-score (RQ5) dilaporkan dengan liputan per dimensi.
