# Laporan PUEBI Error Rate (C1)

Metode: untuk tiap error injeksi (ground truth di corpus/metadata.json), cek apakah bentuk salah masih ada di output.
Fix rate = 1 - (error tersisa / total error injeksi).

| Kondisi | Naskah selesai | Mean fix rate | Catatan |
| input | 10/10 | 0.0 | baseline (teks asli) |
| b3 | 0/10 | - | b3 (hunspell) tidak menghasilkan teks baru |
| enip | 0/10 | - | menunggu API key |
| b1 | 0/10 | - | menunggu API key |
| b2 | 0/10 | - | menunggu API key |

## Per kategori (total error per kategori, seluruh set injeksi)

| Kategori | Total injeksi |
| E1 | 36 |
| E10 | 4 |
| E2 | 35 |
| E3 | 10 |
| E4 | 18 |
| E5 | 15 |
| E6 | 34 |
| E7 | 11 |
| E8 | 60 |
| E9 | 15 |

Catatan: rincian per naskah di metrics/puebi_errors.json