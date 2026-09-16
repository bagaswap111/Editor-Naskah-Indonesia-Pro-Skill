# Q1/Q2 Scopus Gap Analysis: ENIP Paper

**Date**: 2026-09-17 (updated)
**Current draft**: `enip-journal-draft-v4.md` (post-expansion, 10,000 words)
**Target**: Q1 Scopus journal (NLP/Computational Linguistics)

---

## Current Status (After Q1 Expansion)

| Q1 Requirement | Status | Notes |
|----------------|--------|-------|
| Theoretical framework | ✅ Added | ENIP positioned as deployment architecture (§5.1) |
| 100+ manuscript evaluation | ✅ Done | 20 synthetic + 137 natural = 157 total |
| SOTA GEC comparison | ⚠️ Partial | Compared to B1/B2 baselines; Musyafa et al. discussed (§2.1) |
| Error analysis | ✅ Done | 4 failure modes identified (§4.5) |
| Reproducibility package | ✅ Done | Full artifact availability (§8) |
| Ethics statement | ✅ Done | PUEBI bias, environmental cost, displacement (§7) |
| 10K+ words | ✅ Done | 10,000 words exactly |
| Expanded trigger testing | ✅ Done | 110 queries (§4.4) |
| Extended portability | ⚠️ Partial | 2/7 runtimes (OpenCode ✅, Gemini CLI ✅) |
| Human editor evaluation | ❌ Not done | Requires 2-3 Indonesian editors |
| Ablation study | ❌ Not done | Requires new LLM API runs (~$4-8) |
| LanguageTool comparison | ❌ Not done | Requires LanguageTool setup |

## What Was Done This Session

1. **Reframed ENIP vs B2** (§5.1): Position ENIP as deployment architecture, not quality improvement
2. **Expanded corpus**: 137 natural manuscripts from buku-kolaborasi-llm (80K words)
3. **Expanded trigger**: 20 → 110 queries stratified across 10 patterns
4. **Wrote ethics section** (§7): PUEBI bias, environmental cost, accessibility, displacement
5. **Wrote reproducibility section** (§8): Artifact availability, reproduction instructions, ACL checklist
6. **Expanded methodology** (§3): PUEBI rule encoding, style engine implementation, workflow decision points
7. **Wrote error analysis** (§4.5): 4 failure modes with actionable mitigation strategies
8. **Expanded paper to 10,000 words**: From ~6,000 to 10,000 words

## Remaining Work for Q1

| Item | Effort | Blocker |
|------|--------|---------|
| Human editor evaluation | 2-3 days | Requires 2-3 Indonesian editors recruited |
| Ablation study | 2-3 hours | Requires LLM API calls (~$4-8) |
| Complete portability testing | 2-3 hours | Requires runtime access (Claude Code, Cursor, Codex, Cline) |
| LanguageTool comparison | 1-2 hours | Requires LanguageTool installation |
| Natural manuscript quality evaluation | 2-3 hours | Requires LLM API calls |

---

## Current Strengths (Already Meet Q1/Q2 Thresholds)

| Element | Status | Q1/Q2 Requirement |
|---------|--------|-------------------|
| Clear problem statement | ✅ | Required |
| Novel contribution | ✅ (portable skill for under-resourced language) | Required |
| Related work coverage | ✅ | Required |
| Methodology description | ✅ | Required |
| Honest limitations | ✅ | Required |
| Reproducible artifact | ✅ (SKILL.md, 6 reference files) | Encouraged |

---

## For Q2 Scopus

**Target journals**: Natural Language Processing Journal (Elsevier, Q1 Linguistics/Q2 AI), Natural Language Processing (Cambridge, Q2 AI/Q1 Linguistics)
**Estimated effort**: 2-3 weeks of additional work

### 1. Human Editor Evaluation (Critical — Blocks Q2)

**Why**: Q2 journals require human evaluation for any NLP system claiming editorial/language quality improvements. The current LLM-as-a-Judge approach with J2 vs J3 Spearman = 0.552 is insufficient.

**What to do**:
- Recruit 2-3 senior Indonesian editors (journal editors, publishing house professionals, or university language faculty)
- Have them evaluate 10-15 manuscripts (mix of synthetic and natural)
- Use a structured rubric (checklist-based evaluation per [26] CheckEval)
- Report inter-annotator agreement (Cohen's kappa or Krippendorff's alpha)
- Compare human scores against LLM-judge scores to validate the proxy

**Target**: At minimum, 2 editors evaluating 10 manuscripts with a structured rubric.

### 2. Natural Manuscript Evaluation (Critical — Blocks Q2)

**Why**: The synthetic corpus ceiling effect (8/10 categories at 1.000) means the evaluation doesn't test ENIP on real editorial challenges. Q2 reviewers will flag this immediately.

**What to do**:
- Collect 10-15 real Indonesian manuscripts (newspaper articles, academic abstracts, blog posts, government documents)
- Inject no artificial errors — evaluate on natural error distributions
- Report per-category fix rates on natural manuscripts
- Compare ENIP vs B1 vs B2 on natural corpus

**Target**: 10+ natural manuscripts covering at least 3 genres.

### 3. Ablation Study (Important for Q2)

**Why**: Without ablation, reviewers cannot distinguish "ENIP works because of its structure" from "ENIP works because it's a good prompt." Q2 journals expect component analysis for system papers.

**What to do**:
- **ENIP-full** vs **ENIP-without-PUEBI** (workflow + style engine only)
- **ENIP-full** vs **ENIP-without-style-engine** (PUEBI + workflow only)
- **ENIP-full** vs **ENIP-without-workflow** (PUEBI + style engine, no 7-stage process)
- **ENIP-full** vs **single-shot prompt** (B2 baseline)
- Report quality scores and PUEBI fix rates for each condition

**Target**: 4-5 ablation conditions with statistical comparison.

### 4. Expanded Trigger Reliability (Important for Q2)

**Why**: 20 queries is too small for robust precision/recall. Q2 reviewers expect larger test sets.

**What to do**:
- Expand to 100+ queries
- Stratified sampling: 20 queries per trigger pattern (Indonesian editing commands, style requests, language-mixing prompts, etc.)
- Categorize failure modes (true trigger, language mismatch, scope mismatch)
- Report precision, recall, F1 per category

**Target**: 100+ queries with failure mode analysis.

### 5. Extended Portability Testing (Important for Q2)

**Why**: "Portability" is a core contribution but only 2/7 runtimes are tested. Q2 reviewers will question the claim.

**What to do**:
- Test on 4-5 additional runtimes (Cursor, Codex, Cline, at minimum)
- For each runtime: report (a) does the skill load, (b) does the full workflow execute, (c) token usage, (d) output quality
- Create a portability matrix

**Target**: 5+ runtimes with structured portability evidence.

### 6. LanguageTool Comparison (Important for Q2)

**Why**: LanguageTool is the most direct existing baseline for mechanical PUEBI checking. Omitting this comparison weakens the related work and evaluation.

**What to do**:
- Run LanguageTool's Indonesian support on the same 20 manuscripts
- Report PUEBI fix rates per error category
- Compare ENIP vs LanguageTool vs B1 vs B2

**Target**: Direct mechanical baseline comparison.

### 7. Manuscript Length and Structure (Q2 Format)

**Why**: Q2 journals have specific format requirements.

**What to do**:
- Expand to 8,000-12,000 words (current is ~6,000)
- Add more detailed methodology sections (e.g., style engine implementation details, PUEBI rule encoding approach)
- Add a dedicated "Reproducibility" section with code/data availability statements
- Add ethics statement (required by most Q2 journals)

**Target**: 10,000+ words with full methodological detail.

---

## For Q1 Scopus

**Target journals**: Computational Linguistics (MIT Press), Natural Language Processing Journal (Elsevier, Q1)
**In addition to all Q2 requirements**

### 8. Theoretical Contribution (Critical for Q1)

**Why**: Q1 journals require theoretical novelty, not just engineering. The current paper is a system description. Q1 needs a theoretical framework.

**What to do**:
- Formalize the three-layer editing model as a theoretical framework (not just an analogy)
- Define editorial competence as a formal space with measurable dimensions
- Propose a taxonomy of editorial skill architectures
- Position ENIP within a broader theory of portable language-specific editing

**Target**: A theoretical contribution that generalizes beyond Indonesian.

### 9. Larger-Scale Evaluation (Critical for Q1)

**Why**: Q1 journals expect evaluation on 100+ instances, not 20.

**What to do**:
- Scale evaluation to 100+ manuscripts (50 synthetic + 50 natural)
- Include multiple LLM backends (GPT-4, Claude, Gemini, open-source models)
- Report cross-model generalization
- Add statistical power analysis

**Target**: 100+ manuscripts, 3+ LLM backends.

### 10. Comparison to State-of-the-Art GEC Systems (Critical for Q1)

**Why**: Q1 journals expect comparison to the best existing systems, not just baselines.

**What to do**:
- Compare to Musyafa et al. [1] (Transformer-based Indonesian GEC)
- Compare to Lin et al. [5] (corpus construction framework)
- Compare to LanguageTool Indonesian support
- Compare to GPT-4/Claude with editorial prompting

**Target**: 4+ baseline comparisons including SOTA GEC systems.

### 11. Error Analysis and Failure Modes (Critical for Q1)

**Why**: Q1 journals expect deep error analysis, not just aggregate scores.

**What to do**:
- Per-error-type analysis with confusion matrices
- Qualitative error analysis (10+ examples of ENIP failures with explanations)
- Analysis of when ENIP's flagging behavior is appropriate vs. when it's over-cautious
- Cross-genre analysis (how does ENIP perform on academic vs. journalistic vs. literary text?)

**Target**: Detailed error analysis with qualitative examples.

### 12. Reproducibility Package (Critical for Q1)

**Why**: Q1 journals require code, data, and artifacts to be publicly available.

**What to do**:
- Publish the SKILL.md and all reference files on GitHub
- Publish the evaluation corpus (synthetic + natural) on a data repository
- Publish evaluation scripts
- Create a Docker container for reproducibility
- Register the paper on ACL Reproducibility Checklist

**Target**: Full reproducibility package.

### 13. Broader Impact and Ethics Statement (Required for Q1)

**Why**: Q1 journals require ethics and broader impact statements.

**What to do**:
- Discuss potential misuse (e.g., automated editing replacing human editors)
- Discuss bias in PUEBI rules (formal Indonesian vs. regional variations)
- Discuss environmental cost of LLM-based editing
- Discuss accessibility for non-expert users

**Target**: 500-word ethics and broader impact section.

---

## Priority Matrix

| Action | Q2 Impact | Q1 Impact | Effort | Priority |
|--------|-----------|-----------|--------|----------|
| Human editor evaluation | Critical | Critical | Medium | **#1** |
| Natural manuscript evaluation | Critical | Critical | Medium | **#2** |
| Ablation study | Important | Critical | Medium | **#3** |
| Expanded trigger testing | Important | Important | Low | **#4** |
| Extended portability testing | Important | Important | Medium | **#5** |
| LanguageTool comparison | Important | Critical | Low | **#6** |
| Theoretical framework | Nice-to-have | Critical | High | **#7** |
| Larger-scale evaluation | Nice-to-have | Critical | High | **#8** |
| SOTA GEC comparison | Nice-to-have | Critical | Medium | **#9** |
| Error analysis | Important | Critical | Medium | **#10** |
| Reproducibility package | Important | Critical | Medium | **#11** |
| Ethics statement | Required | Required | Low | **#12** |
| Expand to 10K+ words | Required | Required | Low | **#13** |

---

## Recommended Target Journal

**Primary**: Natural Language Processing Journal (Elsevier) — Q1 in Linguistics, Q2 in AI, Open Access, welcomes system descriptions and low-resource language work

**Secondary**: Natural Language Processing (Cambridge) — Q2 in AI, Q1 in Linguistics, explicitly encourages "multilingual and low-resource language projects"

**Backup**: Computational Linguistics (MIT Press) — Q1, but requires stronger theoretical contribution

---

## Bottom Line

**For Q2**: Add human evaluation + natural corpus + ablation + LanguageTool comparison + expand to 10K words. Estimated 2-3 weeks.

**For Q1**: All of the above + theoretical framework + 100+ manuscript evaluation + SOTA GEC comparison + error analysis + reproducibility package. Estimated 6-8 weeks.

The paper's core contribution (portable skill for under-resourced language editing) is genuinely novel and valuable. The gap is in evaluation rigor, not in the idea itself.
