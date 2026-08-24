# RESUME_PLAN — Lanjutan eksekusi (ditulis 2026-08-24 ±14:30 WIB)

Dokumen ini = panduan tunggal sesi berikutnya. Baca bagian
"Keadaan sekarang", lalu jalankan langkah-langkahnya berurutan.
Tidak perlu membaca ulang PLAN.md/README untuk memutuskan.

## Keadaan sekarang (snapshot saat dokumen ditulis)

- `metrics/scores.json`: **93/300** (J1=3, J2=73, J3=17) — judge C2
  berjalan otomatis via `scripts/judge_loop.sh` (idempotent, putaran
  tiap 15 menit, berhenti sendiri saat 300/300).
- Fase A/B/C1/C4/D3 **FINAL** — jangan disentuh/di-re-run:
  korpus v2, runs editor gpt-oss-120b 20/20/20,
  `puebi_report.md` (fix rate enip 0.9681 < b1 0.9774 ≈ b2 0.9769),
  `proxies.json`, `overhead.json`.
- `scripts/analyze.py` sudah jadi & teruji di data parsial.
- `caffeinate` aktif agar Mac tidak tidur (pid 76741 saat ini).

## Peta kuota (mengapa jadwalnya begitu)

Semua TPD Groq itu **jendela rolling 24 jam** — token kembali tepat
24 jam setelah dipakai. Gemini reset kuota harian tiap tengah malam
Pacific (±14:00 WIB).

| Judge | Model | Sisa | Kapan kuota kembali |
|---|---|---|---|
| J1 | qwen/qwen3.6-27b | 117 | **2026-08-25 ±10:45–12:30 WIB** (pemakaian 24 Agu 10:45–12:30 kedaluwarsa) |
| J2 | openai/gpt-oss-20b | 47 | **2026-08-25 ±12:47–14:00 WIB** |
| J3 | gemini-3.5-flash | 43 | reset harian; setelah 14:00 WIB 24 Agu kapasitas terisi cepat |

## Langkah sesi berikutnya (jalankan berurutan)

### 0. Pastikan mesin menyala & loop hidup

```bash
cd /Users/bagaskorosaputro/Documents/GithubDesktop/Editor-Naskah-Indonesia-Pro/paper/experiments
pgrep -f judge_loop || nohup bash scripts/judge_loop.sh > judge_loop.local.log 2>&1 &
# jika Mac sempat tidur/restart, aktifkan lagi anti-tidur:
pgrep caffeinate || nohup caffeinate -i -s > /dev/null 2>&1 &
```

### 1. Pantau sampai lengkap (target: 300)

```bash
python3 - <<'EOF'
import json
from collections import Counter
rows = json.load(open("metrics/scores.json"))
print("total:", len(rows), "/300 |", dict(Counter(r["judge"] for r in rows)))
EOF
tail -5 judge_loop.local.log   # GAGAL HARD_QUOTA = masih menunggu kuota, normal
```

- J1+J2 diperkirakan lengkap **siang 25 Agu** (refund rolling).
- J3 mengikuti reset harian Gemini; bila suatu hari J3 macet
  (< 20 sukses/hari), biarkan — loop otomatis mengisi lagi esoknya.

### 2. Verifikasi LENGKAP (jangan lewati)

```bash
python3 - <<'EOF'
import json
ids = [m["id"] for m in
       json.load(open("corpus/metadata.json"))["corpus"]]
need = {(c, i, j, t)
        for c in ("b1", "b2", "enip") for i in ids
        for j, ts in (("J1", (0, 0.7)), ("J2", (0, 0.7)), ("J3", (0,)))
        for t in ts}
have = {(r["condition"], r["id"], r["judge"], r["trial"])
        for r in json.load(open("metrics/scores.json"))}
print(f"kurang: {len(need - have)} dari {len(need)}")
for x in sorted(need - have)[:10]:
    print(" ", x)
EOF
```

Wajib `kurang: 0` sebelum lanjut. Kalau ada sisa, ulangi langkah 1
(esoknya juga tidak apa-apa — semua idempotent).

### 3. Analisis final

```bash
python3 scripts/analyze.py          # bootstrap 10k default
```

Output: `metrics/analysis.json` + `metrics/analysis_report.md`
(ringkasan per kondisi & dimensi, uji paired bootstrap ENIP−B1/B2,
korelasi antar-judge Pearson/Spearman, C3 delta self-score + liputan).

### 4. Catat hasil ke dokumentasi

1. Salin angka utama dari `analysis_report.md` ke
   `paper/EXPERIMENT_RESULTS.md` (ganti bagian "Belum selesai" →
   jawaban **RQ1** (unggul/tidaknya ENIP vs B1/B2, bandingkan juga
   dengan C1) dan **RQ5** (bias self-assessment)).
2. Perbarui baris "C metrik" di tabel status `experiments/README.md`.
3. Jawaban yang harus dicek konsistensinya dengan C1 (`puebi_report.md`):
   - ENIP unggul E1 tapi kalah E9/E2/E6 pada fix rate;
   - apakah judge melihat hal yang sama pada dimensi Mekanik?

### 5. Setelah C2/C3 tuntas — sisa eksperimen

- **Fase D1 portability** (manual GUI): isi
  `portability/results.json` — 8 runtime, naskah uji pop_03,
  skema di PLAN.md §6.
- **Fase D2 trigger** (manual GUI): 20 query di
  `trigger/queries.json`, isi `trigger/results.json`.
- **Fase F**: konsolidasi ke draft paper (`paper/drafts/`).

## Jangan lakukan

- Jangan re-run editor / puebi / proxies / overhead — sudah FINAL.
- Jangan hapus `runs/` atau edit output mentah.
- Jangan kutip angka judge parsial di paper.
- Jangan pakai `--full` pada judge.py — memaksa menilai ulang SEMUA
  item dan membakar kuota harian tanpa manfaat (hasilnya pun di-merge
  dengan yang lama).

## Commit

Setelah langkah 3–4 tuntas, commit bersama-sama:
scores.json final, analysis.*, judge.py + analyze.py +
judge_loop.sh, RESUME_PLAN.md (hapus/tandai selesai),
EXPERIMENT_RESULTS.md, README.md experiments.
