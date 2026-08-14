# Set Bahan Uji: VOA Indonesia (kategori Berita)

Sumber: https://www.voaindonesia.com · Lisensi: Public domain (US gov work)

## Karakteristik
- Register: jurnalistik, berita
- Catatan sumber: Feed RSS kategori Berita (/api/zmgqol-…); item gagal ekstrak (video/laporan audio) dilewati dan dicatat

## Isi (5 naskah)

| id | Judul | Kata | SHA-256 (awal) |
|---|---|---|---|
| voa-id_trump-bertekad-minta-pertanggungjawaban-pihak-yang-menuntutnya_8011524.html | Trump Bertekad Minta Pertanggungjawaban Pihak yang Menuntutnya | 410 | `081b9087ce…` |
| voa-id_militer-pakistan-korban-tewas-pembajakan-kereta-api-bertambah-jadi-31-orang_8011268.html | Militer Pakistan: Korban Tewas Pembajakan Kereta Api Bertambah Jadi 31 | 520 | `d8453f041b…` |
| voa-id_utusan-as-hamas-salah-mengartikan-pembebasan-sandera_8011260.html | Utusan AS: Hamas Salah Mengartikan Pembebasan Sandera | 561 | `94999d693c…` |
| voa-id_shutdown-kegiatan-pemerintah-amerika-kemungkinan-terhindari_8011453.html | Shutdown Kegiatan Pemerintah Amerika Kemungkinan Terhindari | 674 | `e30cca0963…` |
| voa-id_irak-pemimpin-kunci-isis-tewas_8011274.html | Irak: Pemimpin Kunci ISIS Tewas | 432 | `9ee9bb94e1…` |

Catatan: `texts/*.txt` = teks bersih hasil ekstraksi (input runner eksperimen).
Orisinal dapat diakses via URL pada metadata.json. Teks tidak diterbitkan
ulang di paper — hanya statistik yang dilaporkan, setiap angka dirujuk ke
file set ini (kebijakan sama dengan set buku-kolaborasi-llm).

## Sampling (reproduksi)
```python
import random
random.seed(20260814)
sample = random.sample(sorted(candidates), k=5)
```
Kandidat = 20 item tersedia saat pengambilan
(2026-08-14 11:37 WIB). Skrip pengambil: `scripts/fetch_corpus.py`.
