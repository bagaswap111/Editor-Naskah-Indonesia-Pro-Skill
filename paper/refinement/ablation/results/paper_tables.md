# Paper-ready ablation tables

**Generated**: 2026-10-01T13:58:13+00:00
**Source**: `ablation_analysis.json` (judge J1 (gemini-3.5-flash-lite), seed 42, 10000 bootstrap resamples)

## Table 1 — Overall

| Condition | $n$ | Mean | Std | $\Delta$ vs ENIP-full | 95\% CI ($\Delta$) |
|---|---|---|---|---|---|
| ENIP w/o PUEBI | 10 | 8.86 | 0.19 | +1.69 | [0.83, 2.66] |
| ENIP w/o style engine | 10 | 8.90 | 0.22 | +1.73 | [0.81, 2.76] |
| ENIP w/o workflow | 10 | 8.69 | 0.18 | +1.51 | [0.66, 2.47] |
| ENIP-full (main study) | 10 | 7.17 | 1.54 | +0.00 | — |

## Table 2 — Per dimension

| Condition | Kejelasan | Koherensi | Kedalaman | Akurasi | Gaya | Mekanik | Engagement |
|---|---|---|---|---|---|---|---|
| ENIP w/o PUEBI | 9.30 | 9.00 | 7.80 | 8.80 | 9.00 | 10.00 | 8.10 |
| ENIP w/o style engine | 9.10 | 9.00 | 8.00 | 9.00 | 9.10 | 10.00 | 8.10 |
| ENIP w/o workflow | 9.00 | 9.00 | 7.50 | 8.80 | 9.00 | 9.40 | 8.10 |
| ENIP-full (main study) | 7.40 | 7.40 | 6.50 | 6.90 | 7.60 | 7.50 | 6.90 |

## Table 3 — Within-ablation pairwise contrasts

| Contrast | $\Delta$ | 95\% CI | Sig. |
|---|---|---|---|
| ENIP w/o PUEBI − ENIP w/o style engine | -0.04 | [-0.24, 0.11] | no |
| ENIP w/o PUEBI − ENIP w/o workflow | +0.17 | [0.09, 0.27] | yes |
| ENIP w/o style engine − ENIP w/o workflow | +0.21 | [0.03, 0.43] | yes |

> Pairwise contrasts are the only causally interpretable comparison here: all three ablation conditions share the same editor and judge.
