# Refinement Execution Plan
# Editor Naskah Indonesia Pro (ENIP) — Q1 Submission Preparation

**Created**: 2026-09-17
**Target Venue**: Journal of Natural Language Processing and Computational Linguistics (Q1/Q2)
**Status**: Ready for Execution

---

## Overview

This document outlines the complete execution plan for addressing the 4 remaining gaps before Q1 submission. All materials are prepared for immediate execution — no additional prep work needed.

---

## Gap 1: Human Editor Evaluation

### Why Critical
- Q1 journals require human validation, not just LLM-judge scores
- Most impactful gap for publication acceptance
- Provides ground truth for LLM-judge calibration

### Recruitment Strategy

| Channel | Target | Timeline | Cost |
|---------|--------|----------|------|
| **MSKI** (Masyarakat Sadar Kebahasaan) | 1-2 linguists | Week 1 | $50-100/editor |
| **University linguistics departments** (UI, UGM, Unpad) | 1-2 lecturers | Week 1 | $50-100/editor |
| **Freelance platforms** (Sribulancer, Projects.co.id) | 1 editor with PUEBI portfolio | Week 1 | $80-150/editor |
| **Publishing houses** (Gramedia, Mizan) | 1 senior editor | Week 1 | $100-200/editor |

**Minimum**: 2 editors (ideal: 3 for inter-annotator agreement)

### Evaluation Package (Prepared)

| Document | Location | Purpose |
|----------|----------|---------|
| Evaluation Rubric | `human_eval/RUBRIC.md` | 7-dimension scoring guide with examples |
| Instructions | `human_eval/INSTRUCTIONS.md` | Step-by-step evaluation guide |
| Consent Form | `human_eval/CONSENT_FORM.md` | Informed consent for participation |
| Evaluation Sheets | `human_eval/eval_sheet_E1.md` through `eval_sheet_E3.md` | One per evaluator |
| Sample Manuscripts | `human_eval/manuscripts/` | 10 manuscripts to evaluate |
| Reference Materials | `human_eval/reference/` | PUEBI rules, quality metrics |

### Manuscripts Selected (10)

| ID | Style | Type | Reason |
|----|-------|------|--------|
| aca_01 | Academic | Injected | High error density (22 errors) |
| aca_03 | Academic | Clean twin | Over-editing detection |
| jur_01 | Journalistic | Injected | Register contrast |
| jur_03 | Journalistic | Clean twin | Over-editing detection |
| pop_01 | Popular-educative | Injected | Most common style |
| pop_03 | Popular-educative | Clean twin | Over-editing detection |
| per_01 | Persuasive | Injected | Argumentative register |
| per_03 | Persuasive | Clean twin | Over-editing detection |
| bkl_01_01 | Popular-educative | Natural | Real-world validation |
| bkl_08_01 | Academic | Natural | Real-world validation |

### Evaluation Protocol

1. Each evaluator receives:
   - 10 original manuscripts (in `manuscripts/` folder)
   - 10 ENIP outputs (anonymized as OUT-0001 to OUT-0010)
   - 5 B1 outputs (anonymized as OUT-0011 to OUT-0015) for comparison
   - Rubric + Instructions + Consent form

2. Evaluator tasks:
   - Read each manuscript + output pair
   - Score 7 dimensions (1-10)
   - Provide qualitative comments for scores ≤6
   - Complete evaluation within 3-4 hours

3. Compensation:
   - $50-100 per evaluator (depending on experience)
   - Payment upon completion and submission of evaluation sheets

### Quality Checks

- [ ] Consent form signed before evaluation begins
- [ ] All 10 manuscripts included in package
- [ ] Rubric examples reviewed with evaluator before starting
- [ ] Evaluator confirms understanding of 7 dimensions
- [ ] Evaluation sheets returned with all fields completed
- [ ] Inter-annotator agreement calculated (Cohen's kappa ≥ 0.6)

---

## Gap 2: Larger Ablation Study

### Why Needed
- Current ablation used Gemini (different from original Groq)
- Smaller sample (10 vs 20 manuscripts)
- Results counterintuitive (removing components increases scores)
- Need to validate with same LLM as original evaluation

### Approach

| Parameter | Original | New Ablation |
|-----------|----------|--------------|
| LLM | Groq: openai/gpt-oss-120b | Groq: openai/gpt-oss-120b (same) |
| Manuscripts | 20 (injected + clean + semi-formal) | 20 (same set) |
| Judges | J1, J2, J3 | J1, J2, J3 (same) |
| Conditions | enip_full, b1, b2 | enip_no_puebi, enip_no_style, enip_no_workflow |

### Ablation Conditions

| Condition | What's Removed | Hypothesis |
|-----------|----------------|------------|
| enip_no_puebi | PUEBI.md reference | Mechanical quality drops, style remains |
| enip_no_style | STYLE_GUIDE.md reference | Style consistency drops, mechanics remain |
| enip_no_workflow | WORKFLOW.md reference | Structural editing drops, all layers affected |

### Multidimensional Perspective Audit

For each condition, evaluate across 5 perspectives:

1. **Mechanical Quality** (PUEBI compliance)
   - Fix rate by category (E1-E10)
   - False positive rate
   - Coverage (% errors detected)

2. **Structural Quality** (flow, coherence)
   - Paragraph structure preservation
   - Transition quality
   - Logical flow maintenance

3. **Style Consistency** (register, tone)
   - Register maintenance (formal/informal)
   - Terminology consistency
   - Tone preservation

4. **Editorial Methodology** (workflow adherence)
   - 7-stage workflow execution
   - Progressive disclosure utilization
   - Quality rubric application

5. **Process Qualities** (not captured by 7-dimension rubric)
   - Transparent justification (Editor Notes)
   - Consistent PUEBI rule application
   - Reproducible style application

### Scripts Prepared

| Script | Location | Purpose |
|--------|----------|---------|
| ablation_runner.py | `ablation/ablation_runner.py` | Run ENIP with components removed |
| ablation_judge.py | `ablation/ablation_judge.py` | Evaluate with 3 judges |
| ablation_analyzer.py | `ablation/ablation_analyzer.py` | Compute metrics + bootstrap tests |
| ablation_report.py | `ablation/ablation_report.py` | Generate paper-ready tables |

### Execution Steps

1. Run ablation_runner.py (3 conditions × 20 manuscripts = 60 API calls)
2. Run ablation_judge.py (60 outputs × 3 judges = 180 evaluations)
3. Run ablation_analyzer.py (compute means, stds, bootstrap CIs)
4. Run ablation_report.py (generate tables for paper)
5. Update §4.8 in paper with new results

### Quality Checks

- [ ] Groq API key valid and has sufficient quota
- [ ] All 20 manuscripts present in corpus/texts/
- [ ] Existing ENIP outputs available for comparison
- [ ] Judge script handles rate limits (30s sleep between calls)
- [ ] Idempotent: can resume from where it stopped
- [ ] Results saved incrementally (safe to interrupt)
- [ ] Bootstrap tests use same seed as original (42)

---

## Gap 3: LanguageTool Comparison

### Why Needed
- Q1 expects comparison to existing SOTA GEC systems
- LanguageTool is the most widely-used open-source GEC tool
- Provides baseline for mechanical editing quality

### Approach

| Parameter | Value |
|-----------|-------|
| Tool | LanguageTool 6.x (latest) |
| Language | Indonesian (id_ID) |
| Manuscripts | 10 injected manuscripts |
| Comparison | ENIP vs B1 vs B2 vs LanguageTool |

### Limitations Acknowledged

- LanguageTool only handles Layer 1 (mechanical) editing
- No structural or substantive editing capabilities
- Limited PUEBI-specific rules (general Indonesian grammar only)
- Comparison is asymmetric: ENIP provides 3 layers, LanguageTool provides 1

### Scripts Prepared

| Script | Location | Purpose |
|--------|----------|---------|
| run_languagetool.py | `languagetool/run_languagetool.py` | Run LanguageTool on manuscripts |
| compare_languagetool.py | `languagetool/compare_languagetool.py` | Compare with ENIP results |
| analyze_languagetool.py | `languagetool/analyze_languagetool.py` | Compute fix rates, FPs |

### Execution Steps

1. Install LanguageTool (brew install languagetool)
2. Download Indonesian rules (id_ID)
3. Run run_languagetool.py (10 manuscripts)
4. Run compare_languagetool.py (ENIP vs LanguageTool)
5. Run analyze_languagetool.py (compute metrics)
6. Update paper with comparison table

### Quality Checks

- [ ] LanguageTool installed and working
- [ ] Indonesian rules loaded correctly
- [ ] Same 10 manuscripts used for fair comparison
- [ ] Fix rates computed per-category (E1-E10)
- [ ] False positive rates computed
- [ ] Limitations clearly stated in paper

---

## Gap 4: Extended Portability Testing

### Why Needed
- Paper claims "7+ runtimes" but only 2/7 tested
- Strengthens portability claim
- Provides evidence for cross-runtime deployment

### Runtimes to Test

| Runtime | Install Method | Expected Issues |
|---------|----------------|-----------------|
| Claude Code | agent install script | Credential issue (resolved) |
| Cursor 2.4+ | rules/skill folder | May need manual skill loading |
| Cline | CLAUDE.md / skill | May need CLAUDE.md configuration |
| VS Code Copilot | agent skill | May not support SKILL.md natively |
| Antigravity | skill folder | Unknown |

### Testing Protocol

1. Install ENIP skill on each runtime
2. Run with pop_03 manuscript (same as OpenCode/Gemini CLI)
3. Record: loads_without_modification, activation_mechanism, output_received
4. Save logs in portability/logs/
5. Update results.json

### Checklist Prepared

See `portability/PORTABILITY_CHECKLIST.md`

### Quality Checks

- [ ] All 5 runtimes installed and accessible
- [ ] Same manuscript used for all tests (pop_03)
- [ ] Same instruction used ("Edit naskah ini sesuai PUEBI")
- [ ] Logs saved for all runtimes
- [ ] Results.json updated with all findings
- [ ] Any failures documented with reasons

---

## Execution Timeline

| Day | Task | Duration | Dependencies |
|-----|------|----------|--------------|
| 1 | Create all preparation documents | 4 hours | None |
| 1 | Start human editor recruitment | 1 hour | None |
| 2 | Run larger ablation study | 3-4 hours | Groq API key |
| 2 | Run LanguageTool comparison | 1-2 hours | LanguageTool installed |
| 3 | Extended portability testing | 2-3 hours | All runtimes installed |
| 3 | Analyze ablation results | 2 hours | Ablation complete |
| 4 | Analyze LanguageTool results | 1 hour | LanguageTool complete |
| 4 | Update paper with new results | 3-4 hours | All analyses complete |
| 5-14 | Human editor evaluations | 1-2 weeks | Editors recruited |
| 15 | Analyze human eval results | 2-3 hours | Evaluations complete |
| 16 | Final paper revisions | 4-6 hours | All analyses complete |

**Total estimated time**: 25-35 hours (excluding human eval period)
**Total estimated cost**: $200-550 (human eval compensation + API costs)

---

## Check-and-Balance System

### Before Execution

- [ ] All scripts tested with dry-run mode
- [ ] API keys verified and have sufficient quota
- [ ] Backup copies of existing results created
- [ ] Git commit with current state before changes

### During Execution

- [ ] Results saved incrementally (safe to interrupt)
- [ ] Rate limits handled (30s sleep between API calls)
- [ ] Error handling with retry logic (3 attempts)
- [ ] Progress logged to console and files

### After Execution

- [ ] All results validated (no missing data points)
- [ ] Inter-annotator agreement calculated for human eval
- [ ] Bootstrap tests run with correct seed (42)
- [ ] Tables generated in paper-ready format
- [ ] Paper sections updated with new results
- [ ] Git commit with final state

### Quality Gates

| Gate | Criteria | Action if Failed |
|------|----------|------------------|
| G1: Human eval recruitment | ≥2 editors recruited | Extend recruitment, consider alternatives |
| G2: Ablation completion | All 60 outputs generated | Resume from last checkpoint |
| G3: Judge completion | All 180 evaluations complete | Resume, handle rate limits |
| G4: Inter-annotator agreement | Cohen's kappa ≥ 0.6 | Re-train evaluators, add third evaluator |
| G5: Statistical significance | Bootstrap CI excludes zero | Acknowledge as limitation |

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Insufficient human evaluators | Medium | High | Start recruitment early, offer competitive compensation |
| Groq API rate limits | Medium | Medium | Use retry logic, sleep between calls |
| LanguageTool lacks Indonesian support | Low | Medium | Document limitation, compare with available rules |
| Runtimes don't support SKILL.md | Medium | Low | Document workarounds, note as limitation |
| Counterintuitive ablation results | Medium | Medium | Use same LLM as original, expand sample size |

---

## Success Criteria

| Metric | Target | Minimum |
|--------|--------|---------|
| Human evaluators recruited | 3 | 2 |
| Inter-annotator agreement (kappa) | ≥0.7 | ≥0.6 |
| Ablation conditions completed | 3 | 3 |
| LanguageTool comparison | Full | Partial (Layer 1 only) |
| Portability runtimes tested | 7 | 5 |
| Paper sections updated | All gaps | Critical gaps only |

---

## Appendix: File Locations

```
paper/refinement/
├── EXECUTION_PLAN.md           # This file
├── human_eval/
│   ├── RUBRIC.md               # 7-dimension scoring guide
│   ├── INSTRUCTIONS.md         # Step-by-step guide
│   ├── CONSENT_FORM.md         # Informed consent
│   ├── eval_sheet_E1.md        # Evaluator 1 sheet
│   ├── eval_sheet_E2.md        # Evaluator 2 sheet
│   ├── eval_sheet_E3.md        # Evaluator 3 sheet (backup)
│   ├── manuscripts/            # 10 manuscripts to evaluate
│   │   ├── aca_01.txt
│   │   ├── aca_03.txt
│   │   ├── jur_01.txt
│   │   ├── jur_03.txt
│   │   ├── pop_01.txt
│   │   ├── pop_03.txt
│   │   ├── per_01.txt
│   │   ├── per_03.txt
│   │   ├── bkl_01_01.txt
│   │   └── bkl_08_01.txt
│   ├── enip_outputs/           # ENIP outputs (anonymized)
│   ├── b1_outputs/             # B1 outputs (anonymized)
│   └── reference/              # PUEBI rules, quality metrics
├── ablation/
│   ├── ablation_runner.py      # Run ENIP with components removed
│   ├── ablation_judge.py       # Evaluate with 3 judges
│   ├── ablation_analyzer.py    # Compute metrics + bootstrap CIs
│   └── ablation_report.py      # Generate paper-ready tables
├── languagetool/
│   ├── run_languagetool.py     # Run LanguageTool on manuscripts
│   ├── compare_languagetool.py # Compare with ENIP results
│   └── analyze_languagetool.py # Compute fix rates, FPs
└── portability/
    └── PORTABILITY_CHECKLIST.md # Testing checklist for all runtimes
```
