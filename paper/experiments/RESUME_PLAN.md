# RESUME_PLAN — Lanjutan eksekusi (ditulis 2026-08-24 ±14:30 WIB)

Dokumen ini = panduan tunggal sesi berikutnya. Baca bagian
"Keadaan sekarang", lalu jalankan langkah-langkahnya berurutan.
Tidak perlu membaca ulang PLAN.md/README untuk memutuskan.

## Keadaan sekarang (snapshot 2026-08-28 17:42)

- `metrics/scores.json`: **220/300** (J1=40, J2=120 ✅, J3=60 ✅) — judge C2
  berjalan otomatis via `scripts/judge_loop.sh` (idempotent, putaran
  tiap 15 menit, berhenti sendiri saat 300/300). Sisa: 80 J1.
- Fase A/B/C1/C4/D3 **FINAL** — jangan disentuh/di-re-run:
  korpus v2, runs editor gpt-oss-120b 20/20/20,
  `puebi_report.md` (fix rate enip 0.9681 < b1 0.9774 ≈ b2 0.9769),
  `proxies.json`, `overhead.json`.
- **D2 trigger** ✅ — precision 1.0, recall 0.9; **D1 portability** 🔶 1/8
  (OpenCode ✅ dengan telemetri progressive disclosure).
- `scripts/analyze.py` sudah jadi & teruji di data parsial.
- `caffeinate` aktif agar Mac tidak tidur.

## Peta kuota (mengapa jadwalnya begitu)

Semua TPD Groq itu **jendela rolling 24 jam** — token kembali tepat
24 jam setelah dipakai. Gemini reset kuota harian tiap tengah malam
Pacific (±14:00 WIB).

Biaya per evaluasi ±4–5 ribu token (rubrik + naskah + thinking +
cap). Karena TPD Groq = 200K/hari/model, **J1 sisa ±111 evaluasi
≈ 550rb token ≈ 3 hari kuota** — tidak mungkin tuntas sehari.

| Judge | Model | Sisa (28 Agu 17:42) | Perkiraan tuntas |
|---|---|---|---|
| J1 | qwen/qwen3.6-27b | 80 | **±30 Agu** — laju TPD ≈ 43 evaluasi/hari (200K ÷ ±4,6rb); tersisa ~368rb token |
| J2 | openai/gpt-oss-20b | 0 | ✅ selesai 120/120 (25 Agu) |
| J3 | gemini-3.5-flash | 0 | ✅ selesai 60/60 (27 Agu 14:28) |

Tanda "GAGAL (HARD_QUOTA ...)" di log = normal saat menunggu kuota;
loop otomatis mengulang tiap 15 menit. Probe kecil (max_tokens 5)
SELALU terlihat berhasil walau kuota sesak — jangan jadi patokan;
cek pesan 429 ukuran penuh untuk angka "Used X / Limit 200000".

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
bash scripts/status.sh   # ringkas: skor, yang kurang, loop, caffeinate
```

- Hanya J1 tersisa **80 evaluasi**; loop mengisi otomatis — cukup pantau sekali sehari via `bash scripts/status.sh`.

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

- **Fase D1 portability**: 1/8 selesai (OpenCode); 7 runtime tersisa,
  naskah uji pop_03, skema di PLAN.md §6. Claude Code menunggu `/login`.
- **Fase D2 trigger** ✅ selesai — tetap arsipkan log `trigger/logs/`.
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
