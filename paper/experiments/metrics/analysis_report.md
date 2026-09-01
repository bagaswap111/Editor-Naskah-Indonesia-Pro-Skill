# Analisis Judge (C2) & Delta Self-Score (C3)

Sumber: metrics/scores.json (236 penilaian; kondisi b1, b2, enip; juri J1, J2, J3; trial [0, 0.7]). Bootstrap 10000x, unit resampling = naskah (paired).

## Ringkasan skor (rata-rata 7 dimensi)

| Kondisi | n | Mean | Std |
|---|---|---|---|
| b1 | 20 | 8.01 | 0.84 |
| b2 | 20 | 8.22 | 0.32 |
| enip | 20 | 7.95 | 0.72 |

### Per dimensi (mean antar naskah)

| Dimensi | b1 | b2 | enip |
|---|---|---|---|
| Kejelasan | 8.41±0.99 | 8.67±0.43 | 8.35±0.87 |
| Koherensi | 8.45±0.94 | 8.77±0.33 | 8.18±0.87 |
| Kedalaman | 7.05±0.56 | 7.54±0.33 | 6.81±0.51 |
| Akurasi | 8.11±1.06 | 8.29±0.74 | 8.29±0.99 |
| Gaya | 8.15±1.01 | 7.99±0.32 | 8.07±0.78 |
| Mekanik | 8.54±1.13 | 8.77±0.41 | 8.59±0.91 |
| Engagement | 7.32±0.75 | 7.54±0.42 | 7.33±0.77 |

## Uji berpasangan (paired bootstrap, delta = ENIP − basis)

| Pasangan | Δ overall | CI 95% | p | n |
|---|---|---|---|---|
| enip_vs_b1 | -0.06 | [-0.33, +0.23] | 0.672 | 20 |
| enip_vs_b2 | -0.28 | [-0.56, -0.03] | 0.024 | 20 |

Delta per dimensi:

| Pasangan | Kejelasan | Koherensi | Kedalaman | Akurasi | Gaya | Mekanik | Engagement |
|---|---|---|---|---|---|---|---|
| enip_vs_b1 | -0.07 (p=0.679) | -0.27 (p=0.101) | -0.24 (p=0.037) | +0.18 (p=0.294) | -0.08 (p=0.680) | +0.05 (p=0.851) | +0.02 (p=0.883) |
| enip_vs_b2 | -0.32 (p=0.030) | -0.59 (p=0.000) | -0.73 (p=0.000) | +0.00 (p=0.995) | +0.08 (p=0.582) | -0.17 (p=0.280) | -0.21 (p=0.249) |

## Korelasi antar-judge (level naskah, mean 7 dimensi)

| Pasangan | Pearson | Spearman | n |
|---|---|---|---|
| J1_vs_J2 | 0.646 | 0.669 | 19 |
| J1_vs_J3 | 0.698 | 0.592 | 19 |
| J2_vs_J3 | 0.593 | 0.552 | 20 |

## C3 — Delta self-score ENIP (skor sendiri − juri)

n = 20 naskah ENIP; baris tabel Skor Kualitas yang tak dapat dipetakan ke rubrik diabaikan (liputan per dimensi pada analysis.json).

| Dimensi | Mean abs delta | Bias (signed) | Liputan |
|---|---|---|---|
| Kejelasan | 0.71 | -0.25 | 20/20 |
| Koherensi | 0.83 | -0.38 | 20/20 |
| Kedalaman | 0.31 | +0.10 | 15/20 |
| Akurasi | 0.60 | -0.60 | 5/20 |
| Gaya | 0.77 | -0.47 | 20/20 |
| Mekanik | 0.63 | +0.51 | 20/20 |
| Engagement | 0.75 | +0.58 | 8/20 |
| SEMUA | 0.67 | -0.08 | 20/20 |

Interpretasi: bias positif = ENIP menilai dirinya lebih tinggi daripada juri (self-assessment bias, RQ5).
