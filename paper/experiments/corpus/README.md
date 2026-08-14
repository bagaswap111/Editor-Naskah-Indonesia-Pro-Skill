# Korpus Sintetis ENIP (Fase A)

20 naskah, dihasilkan `build_corpus.py` (deterministik, `seed=42`):

| Varian | Jumlah | Detail |
|---|---|---|
| A1 injeksi error | 10 (2/gaya) | `{aca,jur,sas,pop,per}_01..02` — teks bersih di-injeksi 15–25 error PUEBI |
| A2 kontrol bersih | 6 | `aca_03..04, jur_03, sas_03, pop_03, per_03` — **twin** teks A1 tanpa injeksi (ukur over-editing) |
| A3 semi-formal | 4 | `sf_01..04` — register santai blog/medsos, bersih |

## Katalog injeksi (E1–E10, dari PLAN.md)

Koma hilang sebelum tetapi/melainkan/sedangkan · di-/ke- awalan vs kata
depan · pun salah · serapan salah (praktik→praktek, risiko→resiko, …) ·
pleonasme (adalah merupakan, agar supaya, banyak para) · angka 1–9 di
awal kalimat · tahun bertitik (2.026) · kapital salah · italic hilang
(*platform*→platform) · "disebabkan karena".

Per naskah: 15–25 error, maks 6 per kategori, tersebar, **non-overlap**.
`metadata.json` berisi ground truth: `injected_errors[]` dengan `cat`,
`offset` (char di teks final), `wrong`, `right`. Relasi twin:
`aca_01↔aca_03`, `aca_02↔aca_04`, `jur_01↔jur_03`, `sas_01↔sas_03`,
`pop_01↔pop_03`, `per_01↔per_03`.

## Struktur

```
corpus/
├── build_corpus.py        # generator + injeksi + review
├── metadata.json          # id, gaya, audiens, kata, variant, twin, errors
├── raw/<id>_clean.txt     # teks bersih sebelum injeksi
└── texts/<id>.txt         # 20 naskah final (input runner Fase B)
```

Semua naskah 300–600 kata (kata bersih; final injected sedikit lebih
pendek karena penyederhanaan bentuk salah). Verifikasi injeksi: seluruh
`wrong` ada di teks final (dicek saat build).

## Reproduksi

```bash
python3 paper/experiments/corpus/build_corpus.py --build   # rebuild
python3 paper/experiments/corpus/build_corpus.py --review  # diff injeksi
```

Sebaran kategori seluruh set: E1=36, E2=35, E3=10, E4=18, E5=15, E6=34,
E7=11, E8=60, E9=15, E10=4.