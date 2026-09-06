# Analisis Judge (C2) & Delta Self-Score (C3)

Sumber: metrics/scores.json (300 penilaian; kondisi b1, b2, enip; juri J1, J2, J3; trial [0, 0.7]). Bootstrap 10000x, unit resampling = naskah (paired).

## Ringkasan skor (rata-rata 7 dimensi)

| Kondisi | n | Mean | Std |
|---|---|---|---|
| b1 | 20 | 7.99 | 0.85 |
| b2 | 20 | 8.22 | 0.32 |
| enip | 20 | 7.84 | 0.89 |

### Per dimensi (mean antar naskah)

| Dimensi | b1 | b2 | enip |
|---|---|---|---|
| Kejelasan | 8.42±0.99 | 8.63±0.43 | 8.21±1.22 |
| Koherensi | 8.46±0.94 | 8.75±0.32 | 8.12±1.09 |
| Kedalaman | 7.01±0.59 | 7.52±0.29 | 6.77±0.42 |
| Akurasi | 8.09±1.06 | 8.19±0.82 | 8.00±1.11 |
| Gaya | 8.09±1.11 | 8.09±0.36 | 8.03±0.89 |
| Mekanik | 8.54±1.14 | 8.74±0.42 | 8.41±1.22 |
| Engagement | 7.32±0.75 | 7.59±0.38 | 7.31±0.80 |

## Uji berpasangan (paired bootstrap, delta = ENIP − basis)

| Pasangan | Δ overall | CI 95% | p | n |
|---|---|---|---|---|
| enip_vs_b1 | -0.15 | [-0.45, +0.11] | 0.286 | 20 |
| enip_vs_b2 | -0.38 | [-0.70, -0.10] | 0.005 | 20 |

Delta per dimensi:

| Pasangan | Kejelasan | Koherensi | Kedalaman | Akurasi | Gaya | Mekanik | Engagement |
|---|---|---|---|---|---|---|---|
| enip_vs_b1 | -0.21 (p=0.320) | -0.34 (p=0.054) | -0.24 (p=0.019) | -0.09 (p=0.582) | -0.06 (p=0.784) | -0.13 (p=0.552) | -0.01 (p=0.993) |
| enip_vs_b2 | -0.42 (p=0.034) | -0.63 (p=0.000) | -0.75 (p=0.000) | -0.19 (p=0.181) | -0.06 (p=0.764) | -0.33 (p=0.117) | -0.28 (p=0.085) |

## Korelasi antar-judge (level naskah, mean 7 dimensi)

| Pasangan | Pearson | Spearman | n |
|---|---|---|---|
| J1_vs_J2 | 0.804 | 0.766 | 20 |
| J1_vs_J3 | 0.854 | 0.737 | 20 |
| J2_vs_J3 | 0.593 | 0.552 | 20 |

## C3 — Delta self-score ENIP (skor sendiri − juri)

n = 20 naskah ENIP; baris tabel Skor Kualitas yang tak dapat dipetakan ke rubrik diabaikan (liputan per dimensi pada analysis.json).

| Dimensi | Mean abs delta | Bias (signed) | Liputan |
|---|---|---|---|
| Kejelasan | 0.91 | -0.11 | 20/20 |
| Koherensi | 0.98 | -0.32 | 20/20 |
| Kedalaman | 0.32 | +0.13 | 15/20 |
| Akurasi | 0.64 | -0.40 | 5/20 |
| Gaya | 0.85 | -0.43 | 20/20 |
| Mekanik | 0.77 | +0.69 | 20/20 |
| Engagement | 0.65 | +0.55 | 8/20 |
| SEMUA | 0.77 | +0.01 | 20/20 |

Interpretasi: bias positif = ENIP menilai dirinya lebih tinggi daripada juri (self-assessment bias, RQ5).
