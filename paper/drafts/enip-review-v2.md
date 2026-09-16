# Research Review: ENIP Draft Paper v2

**Reviewer**: opencode (automated)
**Date**: 2026-09-16
**Draft**: `paper/drafts/enip-journal-draft-v2.md`
**Previous review**: `paper/drafts/enip-review.md` (v1 review)

## Overall Assessment

**Score: 7.5/10** — Substantial improvement over v1. The framing is now honest, the quality claims are properly contextualized, and the paper reads as a credible system description. Remaining weaknesses are mostly in evaluation depth and a few lingering inconsistencies.

---

## 1. Improvements from v1 (What Changed)

| v1 Issue | v2 Fix | Status |
|----------|--------|--------|
| Misleading "comparable quality" framing | Now says "within 0.15 points" with honest interpretation | ✅ Fixed |
| Self-reported worked example scores removed | Old Section 4.3 radar chart table gone | ✅ Fixed |
| Portability overclaimed (8 runtimes) | Now "2/8 runtimes" with clear status table | ✅ Fixed |
| TEEL+ not expanded | Now "(Topic sentence, Explanation, Evidence, Link — extended)" | ✅ Fixed |
| Duplicate reference [29] | Removed, references renumbered | ✅ Fixed |
| Token inconsistency (abstract vs body) | Both now say 10,589 full bundle | ✅ Fixed |
| Section 4.1 evaluation scope unclear | Now explicitly states Layer 1 quantitative, Layers 2/3 via LLM judges | ✅ Fixed |
| Discussion section weak | New Section 5.1 properly interprets quality scores | ✅ Fixed |
| Conclusion oversold | Now honestly states "primary contribution is not quality improvement" | ✅ Fixed |

---

## 2. Remaining Weaknesses

### 2.1 Judge Agreement Still Problematic (Minor — Acknowledged)

J2 vs J3 Spearman = 0.552 (line 269) is moderate disagreement. The paper now acknowledges this and cites [27,28], which is appropriate. However, the paper still uses 5 judges with only 3 named in the text (J1, J2, J3). The other 2 judges are unexplained. This is a minor inconsistency.

**Suggested fix**: Either name all 5 judges or clarify that J1-J3 are the primary judges and J4-J5 are supplementary.

### 2.2 Evaluation Scope Mismatch Between Title and Content

The title says "Three-Layer Editorial Skill" but the evaluation only quantitatively measures Layer 1 (PUEBI fix rates). Layer 2 and 3 quality is measured only via LLM judges on a 7-dimension rubric that doesn't distinguish between layers. The paper acknowledges this in Section 4.1 but the title still implies all three layers are equally evaluated.

**Suggested fix**: Consider adding a subtitle like "A System Description and Layer 1 Evaluation" or adjusting the title to "A Portable Editorial Skill for Indonesian Manuscripts: Design and Preliminary Evaluation."

### 2.3 No Quantitative Layer 2/3 Evaluation

The paper states "Layer 2 (structural) and Layer 3 (substantive) quality are assessed via LLM judges" (line 174) but no separate Layer 2/3 scores are reported. The 7-dimension scores aggregate across all layers. A reader cannot tell whether ENIP improves structural coherence or fact-checking specifically.

**Suggested fix**: Either add per-layer quality breakdowns or explicitly state that per-layer evaluation is future work.

### 2.4 PUEBI Fix Rate Ceiling Effect

Table at lines 244-255 shows that 8 out of 10 error categories have fix rates of 1.000 across all conditions (B1, B2, ENIP). This means the synthetic corpus is too easy for most error types. The only meaningful comparisons are:
- E1 (comma conjunction): ENIP 0.972 vs B1/B2 0.944
- E2 (di- prefix): ENIP 0.943 vs B1/B2 1.000
- E6 (numbers start): ENIP 1.000 vs B1 0.941
- E9 (italic foreign): ENIP 0.700 vs B1 0.900 / B2 0.767

E9 is particularly concerning: ENIP performs worst on italic foreign terms (0.700), which is a Layer 1 mechanical task. This undermines the PUEBI grounding claim.

**Suggested fix**: Acknowledge the ceiling effect and discuss why E9 is harder for ENIP than baselines.

### 2.5 B2 Consistency Anomaly

B2 (single-shot) has std = 0.32 (line 194) while B1 has 0.85 and ENIP has 0.89. B2 is 2.6x more consistent than the other conditions. This is suspicious — either the single-shot prompt is unusually stable, or the evaluation has a bias toward B2-style outputs. The paper doesn't discuss this.

**Suggested fix**: Add a brief note on why B2 has lower variance.

### 2.6 Figure 5 Description Mismatch

Figure 5 description (lines 379-383) says "Grouped Bar Chart" but the old radar chart description was replaced without updating the aspect ratio. The old radar chart was 1:1; a grouped bar chart should be wider (e.g., 16:9 or 4:3). The aspect ratio is listed as 4:3 which is fine, but the description should be verified against the actual figure.

---

## 3. Structural Observations

### 3.1 Paper Length and Density

The paper is 452 lines (~10,000 words estimated). For a system description paper, this is appropriate. The structure is clean: Introduction → Related Work → Methodology → Experiments → Discussion → Conclusion → Appendix.

### 3.2 Abstract Quality

The v2 abstract is honest and well-written. It correctly frames the paper as a system description, reports key metrics, and avoids overclaiming. The sentence "ENIP's primary contribution is not quality improvement but the combination of structured methodology, rule-based PUEBI grounding, and portable skill packaging" (from the conclusion) should be echoed in the abstract.

**Suggested fix**: Add one sentence to the abstract: "ENIP's contribution is structured methodology and portability rather than quality improvement over unguided LLM editing."

### 3.3 Related Work Section

The related work is thorough and well-organized. Section 2.3 on Agent Skills is particularly strong — it establishes the gap clearly. The LLM-as-a-Judge discussion (Section 2.3, paragraph 2) is appropriately positioned.

### 3.4 Methodology Section

The three-layer framework, style engine, and workflow are clearly described. The TEEL+ expansion (line 97) is helpful. The 7-dimension quality rubric is well-defined.

One gap: the paper describes the "7 transition types" (line 97) but never lists them. For a methodology paper, this should be in the appendix or a table.

---

## 4. Minor Issues

| Line | Issue | Severity |
|------|-------|----------|
| 7 | ORCID placeholder — acceptable for draft | Low |
| 145 | "Execution (7,941 tokens all references + assets)" — the sum 382+2,266+7,941 = 10,589 checks out | None |
| 151 | "20 synthetic Indonesian manuscripts (5 per style)" but "10 manuscripts with 10 error categories each" — clarify the relationship between these two groups | Low |
| 231 | False negative explanation is clear and specific | None |
| 263 | "300 evaluations, 20 manuscripts × 3 conditions × 5 judges" = 300, checks out | None |
| 325 | Next steps include ablation and LanguageTool comparison — good additions | None |
| 390 | "9 project-level plus 8 global install paths" — where does this come from? Not mentioned elsewhere in the paper | Medium |
| 404 | Reference [5] DOI is placeholder "nnnnnnn.nnnnnnn" | Low |
| 408 | Reference [7] is arXiv preprint — acceptable | Low |

---

## 5. Recommendation

**Minor revision required.** The paper is in good shape after v1 fixes. Remaining actions:

1. **Clarify judge naming**: Explain all 5 judges or reduce to 3.
2. **Discuss E9 weakness**: Why does ENIP perform worst on italic foreign terms? This is a meaningful finding.
3. **Discuss B2 low variance**: Why is B2 2.6x more consistent?
4. **Add abstract sentence on contribution framing**: "structured methodology and portability, not quality improvement."
5. **List the 7 transition types** in the appendix.
6. **Clarify corpus structure**: Are the 20 manuscripts the same as the 10 with error categories, or a different set?
7. **Verify Figure 6 claim**: "9 project-level plus 8 global install paths" — source this.

The paper is publishable with these fixes. The core contribution (portable editorial skill for Indonesian with PUEBI grounding) is genuine, the evaluation is honest, and the writing is clear.

---

## 6. Comparison to v1

| Dimension | v1 Score | v2 Score | Change |
|-----------|----------|----------|--------|
| Framing honesty | 5/10 | 9/10 | +4 |
| Evaluation rigor | 5/10 | 6/10 | +1 |
| Writing quality | 7/10 | 8/10 | +1 |
| Novelty clarity | 6/10 | 7/10 | +1 |
| Limitations acknowledgment | 7/10 | 9/10 | +2 |
| **Overall** | **6.5/10** | **7.5/10** | **+1.0** |

The biggest improvement is in framing honesty. The paper no longer overclaims quality parity and instead positions ENIP's true contribution (structured methodology + portability) clearly.
