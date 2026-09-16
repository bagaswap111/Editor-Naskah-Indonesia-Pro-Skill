# Comprehensive Cross-Version Research Review: ENIP Paper

**Reviewed drafts**: `enip-editor-naskah-indonesia.md` (v1), `enip-journal-draft.md` (v1b), `enip-journal-draft-v2.md`, `enip-journal-draft-v3.md`, `enip-journal-draft-v4.md` (current)
**Review date**: 2026-09-17
**Reviewer**: opencode (mimo-v2.5-free)
**Method**: Feynman research-review skill — full cross-version analysis

---

## Executive Summary

The ENIP paper has undergone 4 major revisions. The trajectory is positive: framing has shifted from overclaiming quality parity to honest positioning of methodology/portability as the contribution. However, v4 introduces new bugs (typo, figure numbering confusion, token arithmetic inconsistency) while some original issues persist (synthetic corpus, no human evaluation, thin portability evidence).

**Current verdict (v4): 6.5/10** — improved from 5/10 (v3), 6.5/10 (v1), 7.5/10 (v2 review). The paper is publishable with one more focused revision round.

---

## Version Evolution Tracker

### What Changed Across Versions

| Issue | v1 | v2 | v3 | v4 | Status |
|-------|-----|-----|-----|-----|--------|
| "Comparable quality" framing | Overclaimed | Fixed | Fixed | Fixed | ✅ Resolved |
| Self-reported worked example scores | Included | Removed | Removed | Removed | ✅ Resolved |
| Duplicate reference [29] | Present | Removed | Removed | Removed | ✅ Resolved |
| TEEL+ not expanded | Not expanded | Expanded | Expanded | Expanded | ✅ Resolved |
| Portability overclaimed (8 runtimes) | "8 runtimes" | "2/8" | "2/7" | "2/7" | ✅ Resolved |
| Token inconsistency (abstract vs body) | Inconsistent | Consistent | Consistent | Consistent | ✅ Resolved |
| B3 baseline (hunspell) | Included | Removed | Removed | Removed | ✅ Resolved |
| Self-assessment bias section | Present | Present | Removed | Removed | ✅ Resolved |
| Evaluation scope statement | Unclear | Added | Added | Added | ✅ Resolved |
| Judge naming (5 judges) | Unnamed | Unnamed | Named | Named + rationale | ✅ Resolved |
| E9 ceiling effect discussion | Not discussed | Not discussed | Added | Added | ✅ Resolved |
| B2 variance explanation | Not discussed | Not discussed | Speculative | Hypothesized (softer) | ⚠️ Improved |
| Bootstrap test details | Missing | Missing | Missing | Added (10K iterations, seed=42) | ✅ Resolved |
| Failure mode categorization | Not done | Not done | Not done | Added (3 categories) | ✅ Resolved |
| Motivation positive framing | Negative list | Negative list | Negative list | Positive framing | ✅ Resolved |
| Next steps priority ranking | Unranked | Unranked | Unranked | Ranked by impact | ✅ Resolved |
| Natural corpus evaluation | Not mentioned | Not mentioned | Not mentioned | Mentioned as next step | ⚠️ Partial |
| Ablation study | Not mentioned | Not mentioned | Listed as next step | Listed as next step | ⚠️ Unchanged |
| Human editor validation | Planned | Planned | Planned | Planned | ⚠️ Unchanged |
| Synthetic corpus limitation | Listed | Listed | Listed | Listed + discussed in §4.3 | ⚠️ Improved |

### What Was NOT Fixed (Persists Across All Versions)

| Issue | Severity | First Flagged | Current Status |
|-------|----------|---------------|----------------|
| No human editor evaluation | Critical | v1 review | Still planned, not executed |
| Synthetic corpus too easy | Critical | v2 review | Acknowledged more prominently but no natural corpus added |
| Portability only 2/7 runtimes | Critical | v1 review | Downgraded to "preliminary" but still thin |
| No ablation study | Major | v1 review | Listed as next step only |
| No comparison to LanguageTool | Major | v1 review | Listed as next step only |
| No per-layer quality breakdowns | Major | v2 review | Listed as next step only |

---

## v4-Specific Issues (New Bugs Introduced)

### BUG-1. Typo in Per-Dimension Scores Table (§4.3)

**Line 192**: "Kejerasan" should be "Kejelasan"

| Dimension | B1 | B2 | ENIP |
|-----------|-----|-----|------|
| **Kejerasan** ← wrong | 8.42±0.99 | 8.63±0.43 | 8.21±1.22 |

This typo appears in the body table but the figure caption (line 180) correctly says "Kejelasan." Fix immediately.

### BUG-2. Token Arithmetic Explanation Is Self-Contradictory (§4.2, line 174)

The v4 text states:

> "The full bundle (10,589 tokens) comprises discovery (382) + activation (2,266) + execution (7,941) = 10,589."

But 382 + 2,266 + 7,941 = **10,589**. This is correct arithmetic. However, the sentence continues:

> "The full bundle equals the sum of all three tiers because each tier loads independently and cumulatively in the progressive disclosure model."

This is misleading. In progressive disclosure, the tiers are **not** all loaded simultaneously — that's the point. The full bundle represents the **maximum** context cost when all tiers are loaded. The tiers are cumulative in the sense that activation includes discovery, and execution includes activation + discovery. The explanation should clarify that the full bundle = maximum cumulative cost, not that all three load independently.

**Suggested fix**: "The full bundle (10,589 tokens) represents the maximum cumulative context cost when all disclosure tiers are loaded: discovery (382) + activation (2,266) + execution (7,941). In practice, progressive disclosure loads only the tier needed, keeping initial context lean."

### BUG-3. E9 Example Direction Reversed (Table 1, line 150)

v3 had: `"software" without italics` (correct — the error is missing italics)
v4 has: `*software* → software (italics removed)` (wrong direction — this shows italics being **removed**, but the error category is about **missing** italics)

The E9 category is "Unformatted foreign terms" — the error is that foreign terms lack italics. The example should show the correction **adding** italics, not removing them.

**Suggested fix**: Revert to v3's example: `"software" without italics` or use `"software"` → `*software*` (italics added).

### BUG-4. Figure Numbering Is Confused

v4 renumbered figures but introduced inconsistencies:

- Line 119: "ENIP is packaged as a SKILL.md skill (Figure 4)" — but the actual figure referenced is `fig6_artifact_characteristics.png`
- Line 128: "Progressive Disclosure (Figure 5)" — but the actual figure referenced is `fig4_progressive_disclosure.png`
- Line 178: "Figure 6 presents the per-dimension quality scores" — but the actual figure referenced is `fig5_quality_scores_radar.png`

The in-text figure numbers (4, 5, 6) do not match the actual file names (fig6, fig4, fig5). This will confuse readers who try to locate the figures.

**Suggested fix**: Either (a) renumber the figure files to match the in-text order, or (b) revert to v3's figure numbering which was consistent.

### BUG-5. Portability Runtime Count Dropped Without Explanation

v1/v2: "8 agent runtimes"
v3: "7 runtimes" (Claude Code removed)
v4: "7 runtimes" (same as v3)

The reduction from 8 to 7 (removing Claude Code) happened between v2 and v3 without explanation. v4 should note this change or restore the original count if Claude Code testing has been completed.

---

## Persistent Issues (From Earlier Reviews, Still Unresolved)

### P1. No Human Editor Evaluation

**First flagged**: v1 review (enip-review.md)
**Current status**: Still "planned" in v4 §4.5

This remains the single most critical gap. An editorial skill paper without human editor validation is incomplete. The LLM-as-a-Judge approach with J2 vs J3 Spearman = 0.552 is acknowledged but not resolved.

**Recommendation**: Even 2 editors evaluating 5 manuscripts would substantially strengthen the paper. If human evaluation is truly impossible before submission, reframe the paper explicitly as a "system description and preliminary evaluation" rather than an evaluation paper.

### P2. Synthetic Corpus Ceiling Effect

**First flagged**: v2 review (enip-review-v2.md)
**Current status**: Better discussed in v4 §4.3 and §4.4, but no natural corpus added

Eight of ten PUEBI error categories show 1.000 fix rates across all conditions. The evaluation is effectively measuring only 2-3 error types (E1, E2, E9). The v4 discussion of this is improved but the fundamental problem persists.

**Recommendation**: Add even 5 natural manuscripts. The synthetic results can remain as controlled diagnostics alongside natural manuscript results.

### P3. Portability Evidence Is Thin

**First flagged**: v1 review
**Current status**: Downgraded to "preliminary" in v4, which is honest

2/7 runtimes tested. The notes for each runtime are qualitative ("Auto-loaded," "output received"). No quantitative metrics (token usage per runtime, workflow completion rate, error rates).

**Recommendation**: Test 3-4 more runtimes. Even basic "does the skill load and produce output" testing on Cursor, Codex, and Cline would double the evidence base.

### P4. No Ablation Study

**First flagged**: v1 review
**Current status**: Listed as next step #4 in v4 §6

Without ablation, the reader cannot distinguish "ENIP works because of its three-layer structure" from "ENIP works because it's a well-crafted prompt." The style engine, PUEBI reference, and workflow are all bundled together.

**Recommendation**: At minimum, add a discussion of what an ablation would look like and why it was not feasible in this work.

### P5. No LanguageTool Comparison

**First flagged**: v1 review
**Current status**: Removed from v4's next steps entirely

v2 listed "Compare against LanguageTool's Indonesian support" as next step #6. v4 dropped this entirely. LanguageTool's Indonesian support is the most direct existing baseline for mechanical PUEBI checking. Omitting this comparison weakens the related work and evaluation.

**Recommendation**: Restore to next steps or add a brief discussion of why LanguageTool was not used as a baseline.

---

## Structural and Writing Quality Assessment

### Abstract

v4 abstract is well-structured: problem → method → result → contribution. At ~170 words it is within typical limits. The contribution sentence ("ENIP's contribution is structured methodology and portability for under-resourced languages without model fine-tuning") is clear and honest.

**Minor issue**: The abstract mentions "LLM judges" but the body uses "preliminary LLM-judge evaluation." Align terminology.

### Introduction

v4 §1.2 (Motivation) is improved with positive framing: "ENIP fills this gap by providing..." This is better than v1-v3's negative list of what doesn't exist.

### Related Work

Thorough and well-organized across all versions. §2.3 on Agent Skills is particularly strong. No changes needed.

### Methodology

v3 and v4 have detailed figure descriptions embedded in the text (e.g., "Figure 1 illustrates the three-layer framework as a block diagram..."). This is helpful for accessibility but makes the methodology section dense. Consider moving detailed figure descriptions to captions only.

### Experiments

v4 is the strongest version:
- Exact word counts (mean=501, median=500) replace "approximately 500 words"
- Bootstrap test details (10,000 iterations, seed=42) added
- Failure mode categorization for trigger test added
- Judge selection rationale added
- Token arithmetic explained

### Discussion

v4 §5.1 properly synthesizes the quality score interpretation with the ceiling effect caveat. The process qualities list (transparent justification, consistent PUEBI application, reproducible style, cross-runtime deployment) is well-articulated.

### Conclusion

v4's ranked next steps are clear and actionable. The priority ordering (human eval > natural corpus > trigger expansion > ablation > portability) is reasonable.

---

## Reference Quality Check

| Reference | Status | Notes |
|-----------|--------|-------|
| [1] Musyafa et al. 2022 | ✅ | Published in Applied Sciences |
| [2] Yanfi et al. 2023 | ✅ | Published in IEEE Access |
| [3] Marier et al. 2025 | ✅ | Published in PeerJ CS |
| [4] Sharma & Bhattacharyya 2025 | ✅ | EMNLP 2025 |
| [5] Lin et al. 2024 | ⚠️ | arXiv DOI — verify acceptance status |
| [6] Zeng et al. 2025 | ✅ | EMNLP 2025 Findings |
| [7] Shan et al. 2026 | ⚠️ | arXiv preprint |
| [8] Microsoft 2026 | ✅ | Microsoft Learn |
| [9] Open Agent Skills 2025 | ✅ | Specification |
| [10] Agent Skills Contributors 2026 | ⚠️ | GitHub repo — verify distinct from [20] |
| [11]-[12] GEC surveys | ✅ | Published |
| [13] LanguageTool 2024 | ✅ | Website |
| [14] Keita et al. 2026 | ⚠️ | arXiv DOI — verify acceptance |
| [15]-[19] Style transfer refs | ✅ | Published |
| [20] Agent Skills spec 2026 | ⚠️ | Same domain as [10] — confirm distinct |
| [21] Zheng et al. 2024 | ✅ | NeurIPS |
| [22] Li et al. 2025 | ✅ | EMNLP 2025 |
| [23]-[25] Indonesian resources | ✅ | Published |
| [26] Lee et al. 2025 | ✅ | EMNLP 2025 |
| [27]-[28] LLM-as-Judge studies | ✅ | Published |
| [29] Hani'ah 2018 | ✅ | Book |

---

## Scoring Comparison Across Reviews

| Dimension | v1 (enip-review.md) | v2 (enip-review-v2.md) | v3 (enip-review-v3.md) | v4 (this review) |
|-----------|---------------------|------------------------|------------------------|------------------|
| Framing honesty | 5/10 | 9/10 | 9/10 | 9/10 |
| Evaluation rigor | 5/10 | 6/10 | 5/10 | 6/10 |
| Writing quality | 7/10 | 8/10 | 8/10 | 7.5/10 (new bugs) |
| Novelty clarity | 6/10 | 7/10 | 7/10 | 7/10 |
| Limitations acknowledgment | 7/10 | 9/10 | 9/10 | 9/10 |
| Methodology soundness | 7/10 | 7/10 | 8/10 | 8/10 |
| **Overall** | **6.5/10** | **7.5/10** | **5/10** | **6.5/10** |

**Note**: The v3 score (5/10) was lower than v2 because the v3 review was more thorough and identified issues the v2 review missed. v4 recovers to 6.5/10 due to improvements in bootstrap details, failure mode categorization, and judge rationale — but new bugs (typos, figure numbering) prevent reaching v2's 7.5/10.

---

## Priority Actions for v5

Ranked by expected impact on paper quality:

| Priority | Action | Addresses | Effort |
|----------|--------|-----------|--------|
| 1 | Fix typo "Kejerasan" → "Kejelasan" | BUG-1 | Trivial |
| 2 | Fix E9 example direction | BUG-3 | Trivial |
| 3 | Fix figure numbering consistency | BUG-4 | Low |
| 4 | Clarify token arithmetic explanation | BUG-2 | Low |
| 5 | Add human editor evaluation (2 editors, 5 manuscripts) | P1 | Medium |
| 6 | Add natural manuscript evaluation (5 documents) | P2 | Medium |
| 7 | Expand portability to 4+ runtimes | P3 | Medium |
| 8 | Add ablation discussion | P4 | Low |
| 9 | Restore LanguageTool comparison | P5 | Low |
| 10 | Verify reference [5] and [14] acceptance status | Ref check | Low |

---

## Bottom Line

v4 is a solid system description paper with honest framing and transparent limitations. The three-layer framework, style engine, and progressive disclosure design are genuine contributions to the agent skill ecosystem for under-resourced languages. The evaluation is preliminary but properly contextualized.

**The paper is one focused revision away from submission readiness.** The highest-impact changes are:
1. Fix the 4 new bugs (trivial — 30 minutes of work)
2. Add human editor evaluation or explicitly frame as "preliminal evaluation"
3. Add natural manuscript evaluation

With these changes, the paper would be suitable for a workshop or venue that values system descriptions and tool contributions.
