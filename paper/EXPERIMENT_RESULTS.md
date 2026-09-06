# EXPERIMENT_RESULTS — Status Eksekusi (2026-09-06 23:06)

Ringkasan jujur hasil eksekusi PLAN.md. Angka hanya dari
`paper/experiments/metrics/*` dan `runs/`; tidak ada perhitungan manual.

**Status besar: 2026-09-06 — judge C2 300/300 ✅ FINAL. C1/C4/D3 FINAL, D2 ✅, D1 2/8 (OpenCode+Gemini).**

## Keputusan eksekusi (K1–K6, terbaru)

K1 **openai/gpt-oss-120b (Groq)** — migrasi dari llama-3.3-70b yang
di-decommission Groq · K2 J1=qwen/qwen3.8-27b (Deviasi #9: qwen3.6 OTPM exceeded),
J2=openai/gpt-oss-20b, J3=gemini-3.5-flash · K3 API temp 0 · K4 Full 20 · K5 sesuai plan ·
K6 tidak ada editor → Fase E SKIP.

Deviasi utama (detail: `experiments/README.md` Deviasi #1–#9):

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
6. **qwen3.6-27b thinking tokens melebihi OTPM 1000 Groq** → migrasi ke
   **qwen3.8-27b** (tanpa thinking overhead, 237 token per evaluasi).

## Hasil final Fase A/B/C1/C2/C4/D3

- Re-run editor tuntas 2026-08-23 02:00–03:01 WIB: b1/b2/enip
  masing-masing **20/20**, nol kegagalan permanen (±154rb token).
- **C1 PUEBI (final)** — mean fix rate (`metrics/puebi_report.md`):
  b1 **0.9774** · b2 **0.9769** · enip **0.9681** (baseline input 0.0).
  Per kategori: ENIP unggul E1 (0.972 vs 0.944); tertinggal di E9
  (0.70 vs 0.90/0.77) dan E2/E6. B3 (hunspell) tidak menghasilkan
  teks baru → hanya baseline deteksi.
- **C2 judge (FINAL)**: 300/300 penilaian selesai 2026-09-06.
  `metrics/analysis.json` + `analysis_report.md`.
- **C4 proksi koherensi (final)**: `metrics/proxies.json`.
- **D3 overhead ✅**: discovery 382 · aktivasi 2.266 · refs+assets
  7.941 · bundle penuh 10.589 token (`metrics/overhead.json`).

## Hasil C2 Judge FINAL (300/300)

### Ringkasan skor (rata-rata 7 dimensi)

| Kondisi | n | Mean | Std |
|---|---|---|---|
| b1 | 20 | 7.99 | 0.85 |
| b2 | 20 | 8.22 | 0.32 |
| enip | 20 | 7.84 | 0.89 |

### Per dimensi (mean antar naskah)

| Dimensi | b1 | b2 | enip |
|---|---|---|---|
| Kejelasan | 8.42±0.99 | 8.63±0.43 | 8.21±1.22 |
| Koherensi | 8.46±0.94 | 8.75±0.32 | 8.12±1.09 |
| Kedalaman | 7.01±0.59 | 7.52±0.29 | 6.77±0.42 |
| Akurasi | 8.09±1.06 | 8.19±0.82 | 8.00±1.11 |
| Gaya | 8.09±1.11 | 8.09±0.36 | 8.03±0.89 |
| Mekanik | 8.54±1.14 | 8.74±0.42 | 8.41±1.22 |
| Engagement | 7.32±0.75 | 7.59±0.38 | 7.31±0.80 |

### Uji berpasangan (paired bootstrap, delta = ENIP − basis)

| Pasangan | Δ overall | CI 95% | p |
|---|---|---|---|
| enip_vs_b1 | -0.15 | [-0.45, +0.11] | 0.286 (n.s.) |
| enip_vs_b2 | -0.38 | [-0.70, -0.10] | 0.005 * |

### Korelasi antar-judge

| Pasangan | Pearson | Spearman |
|---|---|---|
| J1_vs_J2 | 0.804 | 0.766 |
| J1_vs_J3 | 0.854 | 0.737 |
| J2_vs_J3 | 0.593 | 0.552 |

## Batasan yang harus dikutip di paper

1. B3 bukan LanguageTool (tidak ada dukungan id-ID); hanya flag kata
   di luar kamus hunspell.
2. ENIP via API memuat SKILL.md saja (keterbatasan TPM free tier);
   references/assets tidak tersedia bagi model dalam mode single-shot.
3. J2 satu family dengan editor (gpt-oss); keduanya OpenAI open-weight.
4. J1 beralih dari qwen3.6-27b ke qwen3.8-27b (Deviasi #9) karena
   thinking tokens qwen3.6 melebihi OTPM 1000 Groq.
5. Label dimensi pada tabel Skor Kualitas ENIP tidak selalu persis
   rubrik (mis. "Koherensi & Kohesi", ada yang hilang) — delta
   self-score (RQ5) dilaporkan dengan liputan per dimensi.

## Belum selesai

1. **D1 portability — 2/8 ✅** — `OpenCode ✅` + `Gemini CLI ✅`.
   Sisa 6 manual: Claude Code, Cursor, Codex, Cline, Antigravity, VS Code Copilot.
2. **F konsolidasi paper** — TBD di `paper/inputs/experimental_log.md`
   (tabel 7 dimensi, PUEBI rate) → `validate_consistency.py` saat ini PASS.
