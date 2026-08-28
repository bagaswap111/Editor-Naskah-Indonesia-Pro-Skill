# Analisis Judge (C2) & Delta Self-Score (C3)

Sumber: metrics/scores.json (220 penilaian; kondisi b1, b2, enip; juri J1, J2, J3; trial [0, 0.7]). Bootstrap 10000x, unit resampling = naskah (paired).

## Ringkasan skor (rata-rata 7 dimensi)

| Kondisi | n | Mean | Std |
|---|---|---|---|
| b1 | 20 | 8.14 | 0.64 |
| b2 | 20 | 8.23 | 0.32 |
| enip | 20 | 7.95 | 0.72 |

### Per dimensi (mean antar naskah)

| Dimensi | b1 | b2 | enip |
|---|---|---|---|
| Kejelasan | 8.55±0.77 | 8.67±0.43 | 8.33±0.88 |
| Koherensi | 8.62±0.69 | 8.78±0.33 | 8.17±0.87 |
| Kedalaman | 7.18±0.51 | 7.55±0.33 | 6.82±0.51 |
| Akurasi | 8.18±0.90 | 8.30±0.74 | 8.29±0.99 |
| Gaya | 8.31±0.85 | 7.99±0.32 | 8.07±0.78 |
| Mekanik | 8.69±0.83 | 8.77±0.41 | 8.62±0.89 |
| Engagement | 7.47±0.63 | 7.55±0.42 | 7.33±0.77 |

## Uji berpasangan (paired bootstrap, delta = ENIP − basis)

| Pasangan | Δ overall | CI 95% | p | n |
|---|---|---|---|---|
| enip_vs_b1 | -0.19 | [-0.43, +0.03] | 0.097 | 20 |
| enip_vs_b2 | -0.28 | [-0.56, -0.03] | 0.024 | 20 |

Delta per dimensi:

| Pasangan | Kejelasan | Koherensi | Kedalaman | Akurasi | Gaya | Mekanik | Engagement |
|---|---|---|---|---|---|---|---|
| enip_vs_b1 | -0.22 (p=0.111) | -0.44 (p=0.001) | -0.36 (p=0.000) | +0.11 (p=0.503) | -0.23 (p=0.195) | -0.07 (p=0.674) | -0.14 (p=0.282) |
| enip_vs_b2 | -0.34 (p=0.023) | -0.60 (p=0.000) | -0.73 (p=0.000) | -0.01 (p=0.963) | +0.09 (p=0.565) | -0.14 (p=0.375) | -0.22 (p=0.230) |

## Korelasi antar-judge (level naskah, mean 7 dimensi)

| Pasangan | Pearson | Spearman | n |
|---|---|---|---|
| J1_vs_J2 | 0.468 | 0.487 | 17 |
| J1_vs_J3 | 0.789 | 0.349 | 17 |
| J2_vs_J3 | 0.593 | 0.552 | 20 |

## C3 — Delta self-score ENIP (skor sendiri − juri)

n = 20 naskah ENIP; baris tabel Skor Kualitas yang tak dapat dipetakan ke rubrik diabaikan (liputan per dimensi pada analysis.json).

| Dimensi | Mean abs delta | Bias (signed) | Liputan |
|---|---|---|---|
| Kejelasan | 0.70 | -0.23 | 20/20 |
| Koherensi | 0.84 | -0.37 | 20/20 |
| Kedalaman | 0.31 | +0.10 | 15/20 |
| Akurasi | 0.60 | -0.60 | 5/20 |
| Gaya | 0.77 | -0.47 | 20/20 |
| Mekanik | 0.60 | +0.48 | 20/20 |
| Engagement | 0.76 | +0.59 | 8/20 |
| SEMUA | 0.67 | -0.08 | 20/20 |

Interpretasi: bias positif = ENIP menilai dirinya lebih tinggi daripada juri (self-assessment bias, RQ5).
