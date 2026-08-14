# Set Bahan Uji: buku-kolaborasi-llm (5 sub-bab acak)

Sebuah set bahan teks **nyata** (bukan sintetis) untuk eksperimen ENIP —
5 sub-bab diambil **acak** dari 100 sub-bab buku LLM kolaboratif
(<https://github.com/bagaswap111/buku-kolaborasi-llm>, folder `konten/`).

## Karakteristik

- Register: populer-edukatif (semi-formal, kaya analogi, istilah
  teknis Inggris dipadukan bahasa Indonesia) — contoh sempurna untuk
  uji transformasi dan konsistensi gaya.
- Panjang: 3.400–5.300 kata/sub-bab (UTUH — melebihi target 300–600
  kata korpus sintetis; eksekutor dapat memilih memproses utuh atau
  menyegmen).

## Isi

| id | Judul sub-bab | Kata (txt) | SHA256 |
|---|---|---|---|
| jilid-2_bab-05_sub-bab-4 | Continuous Batching | 3779 | 1c24c0ed… |
| jilid-2_bab-07_sub-bab-7 | Resource Allocation | 3459 | 3e02c011… |
| jilid-2_bab-08_sub-bab-8 | Maintenance & Failover | 4367 | 066673e9… |
| jilid-2_bab-10_sub-bab-4 | Local vs Cloud | 4919 | dd4b1cab… |
| jilid-2_bab-10_sub-bab-5 | Green AI | 4927 | 440fb732… |

Format: `*id*.md` = asli dari repo; `texts/*id*.txt` = versi
ter-strip markdown (input untuk runner eksperimen).

## Sampling (reproduksi)

```python
import random
random.seed(20260814)
sample = random.sample(100_sub_bab_list, k=10)   # ambil 5 non-kosong berurutan
```

Satu file dari sample (`bab-10/sub-bab-9`) KOSONG di repo → dilewati,
digantikan `bab-10/sub-bab-5`. Detail lengkap: `metadata.json`.

## Lisensi & etika

Repo **tidak memiliki LICENSE** (all rights reserved secara default).
Penggunaan di sini: bahan uji evaluasi riset (fair use) — teks TIDAK
diterbitkan ulang di paper; hanya statistik (skor, error rate) yang
dilaporkan, tiap angka di referensikan ke file set ini.