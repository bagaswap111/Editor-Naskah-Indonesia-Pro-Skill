# Set Bahan Uji: Wikipedia Bahasa Indonesia (Kategori:Artikel pilihan)

Sumber: https://id.wikipedia.org/w/api.php · Lisensi: CC BY-SA 4.0

## Karakteristik
- Register: populer-ensiklopedis, semi-formal
- Catatan sumber: Teks via prop=extracts (explaintext=1); kalimat pertama = judul artikel

## Isi (5 naskah)

| id | Judul | Kata | SHA-256 (awal) |
|---|---|---|---|
| wikipedia-id_saqifah_bani_sa_idah | Saqifah Bani Sa'idah | 4615 | `aeff2e0290…` |
| wikipedia-id_jerman_nazi | Jerman Nazi | 15313 | `659f500d1f…` |
| wikipedia-id_slamet_rijadi | Slamet Rijadi | 1052 | `bc0d1b9ea7…` |
| wikipedia-id_pengepungan_damaskus_1148 | Pengepungan Damaskus (1148) | 1948 | `9ff94a6043…` |
| wikipedia-id_nestor_lakoba | Nestor Lakoba | 3959 | `0c75aae368…` |

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
Kandidat = 458 item tersedia saat pengambilan
(2026-08-14 11:35 WIB). Skrip pengambil: `scripts/fetch_corpus.py`.
