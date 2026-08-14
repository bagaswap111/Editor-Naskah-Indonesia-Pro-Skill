# Set Bahan Uji: The Conversation Indonesia

Sumber: https://theconversation.com/id · Lisensi: CC BY-ND 4.0

## Karakteristik
- Register: opini/argumentatif populer-akademik
- Catatan sumber: Feed Atom /id/articles.atom; item gagal ekstrak dilewati dan dicatat

## Isi (5 naskah)

| id | Judul | Kata | SHA-256 (awal) |
|---|---|---|---|
| theconversation-id_sudah-tahu-keliru-tapi-tetap-diulang-alasan-di-balik-kesalahan-berpikir-kita-287972 | Sudah tahu keliru, tapi tetap diulang: Alasan di balik kesalahan berpi | 867 | `28dde59edc…` |
| theconversation-id_jejak-jalur-dagang-ilegal-palembang-singapura-membantu-indonesia-di-awal-kemerdekaan-289509 | Jejak jalur dagang ‘ilegal’ Palembang - Singapura, membantu Indonesia  | 875 | `0986992086…` |
| theconversation-id_tekanan-keuangan-berkepanjangan-membuat-otak-menyusut-temuan-dari-studi-80-tahun-289191 | Tekanan keuangan berkepanjangan membuat otak menyusut? Temuan dari stu | 793 | `240c73861a…` |
| theconversation-id_realita-kebun-binatang-kita-dana-operasional-dikorupsi-hewan-rentan-mati-di-mana-pengawasan-288385 | Realita kebun binatang kita: Dana operasional dikorupsi, hewan rentan  | 860 | `52bf958c13…` |
| theconversation-id_orang-disabilitas-juga-berhak-berwisata-pelajaran-dari-tamansari-yogyakarta-289361 | Orang disabilitas juga berhak berwisata: Pelajaran dari Tamansari Yogy | 895 | `8058899b7f…` |

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
Kandidat = 50 item tersedia saat pengambilan
(2026-08-14 11:37 WIB). Skrip pengambil: `scripts/fetch_corpus.py`.
