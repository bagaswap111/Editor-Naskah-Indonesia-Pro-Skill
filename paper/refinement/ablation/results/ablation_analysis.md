# Ablation Analysis

**Generated**: 2026-10-01T13:57:16+00:00
**Judge**: J1 (gemini-3.5-flash-lite) | **Baseline**: ENIP-full (trial 0)
**Manuscripts**: 10 injected (aca_01, aca_02, jur_01, jur_02, per_01, per_02, pop_01, pop_02, sas_01, sas_02)
**Bootstrap**: 10000 resamples, seed 42, 95% CI

## Overall quality (mean of 7 dimensions, per manuscript)

| Kondisi | n | Mean | Std | Δ vs ENIP-full | 95% CI (Δ) | Significant? |
|---|---|---|---|---|---|---|
| enip_no_puebi | 10 | 8.857 | 0.191 | +1.686 | [0.829, 2.657] | yes |
| enip_no_style | 10 | 8.900 | 0.224 | +1.729 | [0.814, 2.757] | yes |
| enip_no_workflow | 10 | 8.686 | 0.176 | +1.514 | [0.657, 2.471] | yes |
| enip_full | 10 | 7.171 | 1.537 | +0.000 | - | baseline |

> **Reading note**: rows `enip_no_*` share the same editor and judge (Gemini 3.5 Flash Lite) and are comparable to each other. The `enip_full` row comes from the main experiment (Groq gpt-oss-120b + judge J1) and is shown for reference only — deltas against it are confounded by model and judge differences.

## Per-dimension means

| Kondisi | Kejelasan | Koherensi | Kedalaman | Akurasi | Gaya | Mekanik | Engagement |
|---|---|---|---|---|---|---|---|
| enip_no_puebi | 9.30 | 9.00 | 7.80 | 8.80 | 9.00 | 10.00 | 8.10 |
| enip_no_style | 9.10 | 9.00 | 8.00 | 9.00 | 9.10 | 10.00 | 8.10 |
| enip_no_workflow | 9.00 | 9.00 | 7.50 | 8.80 | 9.00 | 9.40 | 8.10 |
| enip_full | 7.40 | 7.40 | 6.50 | 6.90 | 7.60 | 7.50 | 6.90 |

## Within-ablation pairwise differences (same editor + judge)

| Perbandingan (A − B) | Δ mean | 95% CI (Δ) | Significant? |
|---|---|---|---|
| enip_no_puebi − enip_no_style | -0.043 | [-0.243, 0.114] | no |
| enip_no_puebi − enip_no_workflow | +0.171 | [0.086, 0.271] | yes |
| enip_no_style − enip_no_workflow | +0.214 | [0.029, 0.429] | yes |

## Interpretation

- **Within-ablation**: at least one pair of conditions differs significantly (CI excludes zero).
- **Against ENIP-full (main study)**: all three ablation conditions score higher than the ENIP-full row, but that comparison is **confounded**: the ablation used Gemini 3.5 Flash Lite as editor *and* judge, whereas the main evaluation used Groq gpt-oss-120b (editor) with J1/J2/J3. Treat it as a model/judge artefact, not as evidence that removal improves quality.

## Caveats

- Single judge (J1) and 10 injected manuscripts; the main evaluation used 3 judges x 20 manuscripts. Extending to J2/J3 and 20 manuscripts requires API access.
- Ablation was executed with Gemini 3.5 Flash Lite while the main evaluation used Groq gpt-oss-120b / qwen3.8 / gpt-oss-20b; model differences confound the comparison.
- Reference removal is simulated via exclusion notes appended to SKILL.md (see experiments/scripts/run_ablation.py), not by physically deleting files.
