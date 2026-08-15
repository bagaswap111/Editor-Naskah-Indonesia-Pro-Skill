# EXPERIMENT_RESULTS — Status Eksekusi (2026-08-15)

Ringkasan jujur hasil eksekusi PLAN.md. Angka hanya dari
`paper/experiments/metrics/*` dan `runs/`; tidak ada perhitungan manual.

## Keputusan eksekusi (K1–K6)

K1 **llama-3.3-70b-versatile (Groq)** · K2 J1=qwen/qwen3.6-27b, J2=llama-3.1-8b-instant, J3=gemini-3.5-flash · K3 API temp 0
· K4 Full 20 · K5 sesuai plan · K6 tidak ada editor -> ENIP + judge
**berjalan bertahap** (batas free tier: Groq 100k token/hari/model;
Gemini 20 request/hari/model — lihat `experiments/README.md` Deviasi #4).

Deviasi utama: **B3 = LanguageTool tidak feasible** (tidak mendukung
id-ID, diverifikasi public API + standalone 6.6) → diganti **hunspell +
kamus id-ID** LibreOffice, keterbatasan diakui (hanya kata di luar
kamus; varian non-baku seperti "resiko" ada di kamus → tidak terdeteksi).
Detail: `paper/experiments/README.md`.

## Hasil yang sudah ada

### RQ4 — Context overhead (D3, selesai; `metrics/overhead.json`)

| Komponen | Token (cl100k_base) |
|---|---|
| Discovery (frontmatter name+description) | 382 |
| Aktivasi (body SKILL.md) | 2.266 |
| Eksekusi — total references + assets (worst case full load) | 7.941 |
| Bundle penuh | 10.589 |

### C1 — PUEBI error rate (`metrics/puebi_errors.json`, 2026-08-16)

| Kondisi | Fix rate (mean) | Catatan |
|---|---|---|
| input (baseline) | 0.0 | teks asli — seluruh 238 error injeksi masih ada |
| b3 (hunspell) | n/a | tidak menghasilkan teks baru (hanya flag kata) |
| b1 (instruksi polos) | **0.5506** | 10 naskah injeksi, temp 0 |
| b2 (system prompt) | **0.4709** | 10 naskah injeksi, temp 0 |
| enip | — | berjalan bertahap (1/20 per 2026-08-16) |

Total error injeksi: **238** di 10 naskah (15–25/naskah; sebaran
E1–E10: 36/35/10/18/15/34/11/60/15/4).

### C4 — Proksi koherensi (`metrics/proxies.json`, 2026-08-16)

| Kondisi | CV kalimat (mean) | Variasi konjungsi | Top-10 leksikal |
|---|---|---|---|
| input | 0.364 | 0.494 | 0.171 |
| b1 | 0.446 | 0.449 | 0.189 |
| b2 | 0.394 | 0.411 | 0.171 |
| enip | — | — | — |

### Fase B3 (selesai, `runs/b3/`)

20 naskah di-periksa hunspell id-ID: total **421 kata di luar kamus**
(sebagian besar dari sf_* — slang santai tidak ada di kamus; ini
menunjukkan batas mekanik, bukan klaim kualitas teks).

## Belum selesai (blokir eksplisit)

- **ENIP 19/20 + judge (C2, C3, RQ5)**: jalan bertahap karena batas
  free tier (Groq TPD 100k/hari/model; Gemini 20 req/hari/model) —
  resume: `experiments/README.md` "Cara menyelesaikan LLM".
- **D1 portability (8 runtime)** dan **D2 trigger (20 query)**: butuh
  interaksi GUI runtime lokal — skema & berkas siap.
- **Fase E**: SKIP (K6) — protokol terdokumentasi di PLAN.md §7.

## Batasan yang harus dikutip di paper

1. B3 bukan LanguageTool (tidak ada dukungan id-ID di ekosistem
   LanguageTool); hasil mekanik hanya kata di luar kamus.
2. ENIP dijalankan via API dengan bundle penuh (SKILL.md + refs +
   assets); overhead aktual progressive disclosure diukur D3, efek
   prompting tetap terukur dengan jelas sebagai sistem-prompt eksplisit.
3. RQ1/RQ2/RQ3 belum final — tabel hasil resmi akan mengikuti run LLM.