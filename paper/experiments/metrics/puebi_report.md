# Laporan PUEBI Error Rate (C1, v2 occurrence-ratio)

fix_rate(kategori, naskah) = max(0, 1 - kemunculan_pola_out /
kemunculan_pola_input), dihitung di BADAN naskah hasil edit
(output terstruktur diekstrak dulu — lihat scripts/output_body.py).
Bobot kategori = jumlah error terinjeksi per kategori.

| Kondisi | Naskah | Mean fix rate | Catatan |
|---|---|---|---|
| input | 10/10 | 0.0 | baseline (teks asli) |
| b3 | 0/10 | - | b3 (hunspell) tidak menghasilkan teks baru |
| enip | 10/10 | 0.9681 |  |
| b1 | 10/10 | 0.9774 |  |
| b2 | 10/10 | 0.9769 |  |

## Fix rate per kategori (agregat tertimbang)

| Kategori | input | b3 | enip | b1 | b2 |
|---|---|---|---|---|---|
| E1 | 0.0 | - | 0.9722 | 0.9444 | 0.9444 |
| E10 | 0.0 | - | 1.0 | 1.0 | 1.0 |
| E2 | 0.0 | - | 0.9429 | 1.0 | 1.0 |
| E3 | 0.0 | - | 1.0 | 1.0 | 1.0 |
| E4 | 0.0 | - | 1.0 | 1.0 | 1.0 |
| E5 | 0.0 | - | 1.0 | 1.0 | 1.0 |
| E6 | 0.0 | - | 1.0 | 0.9412 | 1.0 |
| E7 | 0.0 | - | 1.0 | 1.0 | 1.0 |
| E8 | 0.0 | - | 1.0 | 1.0 | 1.0 |
| E9 | 0.0 | - | 0.7 | 0.9 | 0.7667 |

Rincian per naskah: metrics/puebi_errors.json