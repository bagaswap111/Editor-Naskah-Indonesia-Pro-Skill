# Research Review: ENIP Draft Paper

**Reviewer**: opencode (automated)
**Date**: 2026-09-16
**Draft**: `paper/drafts/enip-journal-draft.md`

## Overall Assessment

**Score: 6.5/10** — Solid contribution with clear writing, but the experimental claims significantly overreach the evidence. The paper's strongest element is its engineering design; its weakest is the evaluation methodology.

---

## 1. Strengths

- **Well-structured argument**: The 4 contributions map cleanly to sections. The bricklayer/architect/curator analogy is memorable.
- **Honest about limitations**: Section 5.3 openly flags synthetic corpus, incomplete loanword lists, and score absence in Clean mode.
- **Progressive disclosure measurement** (382/2,266/10,589 tokens) is genuinely useful for the agent skill ecosystem.
- **PUEBI error taxonomy** (Table 1) is concrete and reproducible.

---

## 2. Critical Weaknesses

### 2.1 Experimental Claims Don't Match Evidence

The title says "Three-Layer Editorial Skill" but **Section 4 only evaluates Layer 1 (mechanical/PUEBI) fix rates**. Layers 2 and 3 have no quantitative evaluation. The 7-dimension quality scores use LLM judges, which is acknowledged but still problematic given:
- J2 vs J3 Spearman is only 0.552 (line 276) — weak inter-judge agreement
- 20 manuscripts is small for bootstrap tests
- The ENIP vs B2 p=0.005 result (line 224) shows ENIP is **worse** than the single-shot baseline — yet this is presented as a contribution

### 2.2 The "Comparable Quality" Framing is Misleading

ENIP scored **lower** than both baselines (7.84 vs 7.99 for B1, 8.22 for B2). The paper frames this as "comparable" but the statistical tests show:
- ENIP vs B1: p=0.286 (not significant — could be equivalent, but sample size is tiny)
- ENIP vs B2: p=0.005 (ENIP is **significantly worse**)

The value proposition of ENIP is **portability and structure**, not quality parity. The paper should lean into that instead of defending a quality claim it can't support.

### 2.3 Self-Reported Scores in Section 4.3

The worked-example scores (lines 192-196) are self-reported by the model using ENIP. This is acknowledged but then published in a table as if it's data. It should be removed or clearly marked as "illustrative, not evaluative."

### 2.4 Synthetic Corpus

The 20-manuscript corpus is synthetically generated with controlled error injection (line 151). This means:
- No natural error distributions
- No real-world noise (mixed errors, ambiguous cases)
- Generalizability is unestablished

---

## 3. Methodological Gaps

### 3.1 No Human Evaluation

Human editor validation is "planned but not yet executed" (line 269). For a paper about editorial quality, this is a significant gap. LLM-as-a-Judge is a proxy, not a substitute.

### 3.2 Portability is Claimed but Barely Tested

The paper claims "cross-runtime portability across 8 agent runtimes" (line 55) but only 2/8 are tested (lines 279-290). One is blocked, five are pending. The claim should be downgraded to "portability demonstrated on 2 runtimes with a plan for 6 more."

### 3.3 Missing Ablation

There's no ablation isolating which component contributes what:
- How much does the PUEBI reference file add vs. just the workflow?
- How much does the style engine improve over the workflow alone?
- Which micro parameters actually matter?

### 3.4 No Comparison to Existing Tools

LanguageTool is mentioned but never evaluated. A comparison to LanguageTool's Indonesian support would ground the contribution.

---

## 4. Writing Issues

| Line | Issue |
|------|-------|
| 39 | "no published evaluation exists for cross-runtime portability" — this is the paper's own contribution, but phrased as if it's someone else's gap |
| 55 | "8 agent runtimes" — only 2 tested, should say "up to 8" or "2 runtimes with 6 planned" |
| 97 | "TEEL+" is used without expansion — unfamiliar to non-Indonesian readers |
| 145 | "Full bundle tokens" says 10,589 in abstract but 7,941 in Section 3.4 — verify consistency |
| 219 | Bootstrap test delta is -0.15 and -0.38 — both negative. ENIP is the weakest condition. Frame accordingly. |
| 316 | "comparable quality scores" — should say "comparable or slightly lower quality scores with structured portability" |

---

## 5. Novelty Assessment

**Moderate novelty.** The core ideas (layered editing, progressive disclosure, portable skills) are not individually new. The contribution is the **specific combination for Indonesian** and the measurement of skill artifact characteristics. The PUEBI encoding and style engine are genuinely useful. However:
- "Three-layer editorial" is a well-established concept in publishing
- Progressive disclosure is a standard UX pattern
- The novelty is in the implementation, not the theory

---

## 6. Recommendation

**Major revision required before submission.** Specific actions:

1. **Downgrade quality claims**: Frame ENIP as a structured alternative that trades marginal quality for portability and transparency, not as quality-equivalent.
2. **Add human evaluation** or clearly mark the paper as a "system description" rather than an evaluation paper.
3. **Complete portability testing** or reduce the claim.
4. **Add ablation study** isolating component contributions.
5. **Fix the token inconsistency** between abstract/Section 3.4 and Section 4.2.
6. **Evaluate on natural manuscripts** even if just 5-10 examples to demonstrate real-world viability.
7. **Clarify the framing**: The paper oscillates between "system description" and "evaluation paper." Pick one.

---

## 7. Minor Issues

- Reference [29] is a duplicate of [22] (Yanfi et al.)
- ORCID is placeholder (0000-0000-0000-0000) — acceptable for draft
- Figure files referenced but not verified to exist
- Section 7 (Appendix) mixes reference tables with figure descriptions — consider splitting

---

## 8. Specific Line Edits

| Line | Current | Suggested |
|------|---------|-----------|
| 39 | "no published evaluation exists for cross-runtime portability" | "no published evaluation exists for cross-runtime portability of real domain skills (this paper addresses that gap)" |
| 55 | "cross-runtime portability across 8 agent runtimes" | "cross-runtime portability across 2 agent runtimes (with 6 additional runtimes planned)" |
| 97 | "TEEL+" | "TEEL+ (Topic sentence, Explanation, Evidence, Link — extended)" |
| 145 | "Execution (7,941 tokens all references + assets)" vs abstract "10,589 tokens" | Unify to "Full bundle: 10,589 tokens" |
| 219 | "ENIP achieved comparable quality scores" | "ENIP achieved quality scores within 0.38 points of the single-shot baseline" |
| 316 | "ENIP achieved comparable quality scores while maintaining portability" | "ENIP achieved quality scores within 0.15 points of the unguided baseline (not significant) while providing structured editorial methodology and cross-runtime portability" |
