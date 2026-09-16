# Research Review: ENIP — A Portable Three-Layer Editorial Skill for Indonesian Manuscripts

**Reviewed draft**: `enip-journal-draft-v3.md`
**Review date**: 2026-09-17
**Reviewer**: opencode (mimo-v2.5-free)
**Method**: Feynman research-review skill

---

## Overall Assessment

**Verdict: Major revision required before submission.**

The paper tackles a genuinely interesting problem — structured editorial support for an under-resourced language via portable agent skills. The three-layer framework and style engine are well-designed. However, the evaluation has critical gaps that would undermine credibility at a peer-reviewed venue. The good news: most issues are addressable with targeted additional work.

**Score: 5/10** (below acceptance threshold; strong foundation but insufficient evidence)

---

## Strengths

1. **Clear problem framing** (§1.1): The three-part challenge (mechanical-only tools, ad hoc LLM editing, no cross-runtime portability evidence) is well-articulated and the gap statement in §1.2 is precise.

2. **Novel contribution framing**: Positioning ENIP as "methodology and portability" rather than "quality improvement" is honest and avoids overclaiming.

3. **Progressive disclosure design** (§3.4): The three-tier token cost model (382 / 2,266 / 10,589) is a concrete, measurable contribution to the agent skill ecosystem.

4. **Three-layer framework with analogies** (§3.1): The bricklayer/architect/curator mapping is memorable and pedagogically effective.

5. **Transparent limitations** (§5.3): The six listed design limitations are specific and honest, particularly acknowledging the synthetic corpus and LLM judge limitation.

---

## Critical Issues (must fix before submission)

### C1. Synthetic corpus undermines generalizability (§4.1)

The 20 manuscripts are synthetically generated with "controlled PUEBI error injection." Eight of ten error categories show 1.000 fix rates across all conditions — a textbook ceiling effect. This means the evaluation primarily measures the trivial ability of LLMs to fix obvious errors, not ENIP's structured methodology.

**Impact**: The headline quality result (7.84 vs 7.99, not significant) is uninterpretable because the corpus is too easy. A real editorial skill must be evaluated on natural manuscripts with ambiguous, overlapping, and context-dependent errors.

**Recommendation**: Add a natural manuscript evaluation set (even 5-10 real manuscripts from Indonesian publications) as a primary or supplementary evaluation. The current synthetic results can remain as controlled diagnostics.

### C2. No human evaluation (§4.5)

The paper acknowledges this ("Human editor validation with 2-3 senior Indonesian editors is planned"), but an editor for an editor tool without human editor validation is a fundamental gap. The LLM-as-a-Judge approach is a reasonable proxy, but:

- The J2 vs J3 Spearman correlation of 0.552 is concerning (§4.5). The paper cites [27,28] for "consistent with findings on LLM-as-a-Judge reliability for non-English languages" but doesn't discuss what this means for the validity of the quality scores.
- 5 judges with only 3 reported in agreement analysis is unclear. Why 5 judges if only 3 are primary? What do J4 and J5 contribute?

**Recommendation**: Either (a) conduct the human editor evaluation before submission, or (b) reframe the quality score section as "preliminary LLM-judge evaluation" and remove statistical claims that rely on judge agreement. The bootstrap tests (p=0.286, p=0.005) are meaningless if the judges themselves disagree.

### C3. Portability claim is overstated (§1.3, §3.4)

The paper claims "cross-runtime portability demonstrated on 2 agent runtimes" but the evidence is minimal:

- OpenCode: "Auto-loaded via skill matching; progressive disclosure observed" — what does "observed" mean quantitatively?
- Gemini CLI: "Auto-loaded via skill folder; output received" — no mention of whether the full workflow executed correctly.

5 of 7 runtimes are listed as "Manual testing pending." A portability study with 2/7 tested runtimes is not a portability study — it's a preliminary check.

**Recommendation**: Either test all 7 runtimes (or at least 4-5 with meaningful diversity), or reduce the claim to "preliminary portability demonstrated on 2 runtimes with 5 additional runtimes planned."

### C4. Missing figures (§3.2, §3.3)

The text references Figures 1-6 but figure numbering skips: Figure 4 is referenced in §3.4 and §4.4 as a "bar chart" for progressive disclosure, and Figure 5 in §4.3 as a "grouped bar chart" for quality scores. But the figure captions suggest Figures 4 and 5 exist — are they included as actual images? The references `../figures/fig4_progressive_disclosure.png` and `../figures/fig5_quality_scores_radar.png` suggest they should exist. Verify all 6 figures are present and correctly referenced.

---

## Major Issues (should fix)

### M1. Token arithmetic inconsistency (§3.4, §4.2)

- §3.4 states: "Execution (all references and assets) costs 7,941 tokens" and "full bundle totals 10,589 tokens"
- §4.2 Table confirms: Execution = 7,941, Full bundle = 10,589
- But 7,941 + 2,266 (activation) = 10,207, not 10,589. The numbers don't add up. Where do the remaining 382 tokens come from? Is the full bundle = activation + execution + something else? This needs clarification.

### M2. Ablation study is listed as "next step" but is critical for the contribution claim (§6)

The paper's core contribution is "structured methodology." An ablation study isolating (a) PUEBI reference alone, (b) style engine alone, (c) workflow alone, (d) all combined would directly test whether the structure matters. Without it, the reader cannot distinguish "ENIP works because of its structure" from "ENIP works because it's a good prompt."

**Recommendation**: At minimum, frame this as a limitation rather than just a "next step." Ideally, run a minimal ablation (e.g., ENIP-without-PUEBI-reference vs ENIP-full).

### M3. Trigger reliability test is underpowered (§4.4)

20 queries is too small for precision/recall claims. The single false negative is described as: "Jadikan teks ini lebih akademis dan formal" where the model "responded in English without adopting the editor persona." This is a prompt-language mismatch, not a trigger failure per se. The analysis should distinguish between:

- True trigger failures (model doesn't recognize the editing task)
- Language mismatch (model recognizes the task but responds in wrong language)
- Scope mismatch (model recognizes editing but not the specific layer)

**Recommendation**: Expand to 50-100 queries with stratified sampling across trigger patterns, and categorize failure modes.

### M4. B2 variance explanation is speculative (§4.3, "Note on B2 Variance")

The claim that B2's lower variance "reflects the constrained nature of single-shot prompting" is plausible but unsupported. Without evidence (e.g., analyzing token-level output similarity), this is speculation.

---

## Minor Issues

### m1. Reference quality varies
- [7] (Shan et al. 2026, arXiv) — preprint, not peer-reviewed. Fine for now but flag if the venue requires published references.
- [10] and [20] appear to reference the same GitHub repository (`agentskills/agentskills`). Confirm they are distinct sources.
- [29] (Hani'ah 2018) is a book, not a journal article — fine, but verify the venue's reference style requirements.

### m2. Abstract is long
At ~200 words, the abstract is dense. Consider trimming to 150 words by removing methodological details (the 60/30/10 weighting, 7-dimension list) and focusing on contribution + key result.

### m3. §1.2 Motivation could be sharper
The gap statement is accurate but reads as a list of what doesn't exist. Rephrase as what becomes possible with ENIP (positive framing).

### m4. PUEBI error categories table (Table 1)
E9 ("Unformatted foreign terms") examples use "software" — but the description says "without italics." The example should show the before/after formatting difference.

### m5. §5.1 interpretation
The sentence "ENIP's value proposition is not quality parity but structured methodology and portability" is repeated from §4.3. Consolidate.

### m6. Install paths (§7.3)
Lists 9 project-level and 8 global paths. The `.brainlift/skills/` path in project-level is not mirrored in global. Verify this is intentional.

---

## Questions for the Author

1. **What is ENIP's actual use case?** The paper describes the tool but not who uses it. Is it a developer installing a skill for personal use? A publishing house integrating into a workflow? A journalist? The audience affects what evaluation matters.

2. **Why 5 LLM judges?** The paper uses 5 judges but reports agreement on only 3. What was the rationale for this design? Were J4 and J5 chosen for diversity (different model families)?

3. **Has ENIP been used on real manuscripts?** Even informally? One real-world usage anecdote would strengthen the motivation more than any synthetic evaluation.

4. **What is the false positive rate for the ⚠️ flagging behavior?** The paper mentions ENIP flags uncertain cases. How often does it flag when it shouldn't (over-cautious) vs. doesn't flag when it should (under-cautious)?

---

## Specific Revision Suggestions

| Section | Issue | Suggested Fix |
|---------|-------|---------------|
| Abstract | Too long, too detailed | Trim to 150 words; cut method details, keep contribution + result |
| §4.1 | "approximately 500 words" is vague | Report exact mean/median word count |
| §4.3 | Bootstrap test details missing | Report number of bootstrap iterations, seed, and confidence interval method |
| §4.4 | Trigger test is underpowered | Expand to 50+ queries; categorize failure modes |
| §4.5 | Judge selection rationale missing | Explain why these 5 models were chosen |
| §5.1 | Repeated claim | Merge with §4.3 interpretation |
| §5.3 | Limitation 6 is future work, not a limitation | Recast: "Cross-runtime portability verified on only 2 of 7 target runtimes" |
| §6 | Next steps lack priority ordering | Rank by expected impact: human eval > natural corpus > ablation |

---

## Reference Verification Spot-Check

The reference list includes 29 entries. I note:
- [5] (Lin et al. 2024) has an arXiv DOI (`10.48550/arXiv.2410.20838`) — verify this has been accepted to a venue or update the reference type.
- [6] (Zeng et al. 2025) is from EMNLP 2025 Findings — verify the page range (2193–2206) is correct.
- [14] (Keita et al. 2026) also has an arXiv DOI — same caveat as [5].

---

## Bottom Line

The paper has a strong conceptual foundation. The three-layer framework, style engine, and progressive disclosure design are genuine contributions. But the evaluation is not submission-ready: the synthetic corpus is too easy, there's no human evaluation, the portability claim is thin, and the ablation is missing.

**Priority actions:**
1. Add human editor evaluation (even 2 editors, 5 manuscripts)
2. Add natural manuscript evaluation (5-10 real documents)
3. Expand trigger reliability test to 50+ queries
4. Clarify the token arithmetic inconsistency
5. Test at least 4-5 additional runtimes for portability
6. Add at least a minimal ablation study

These changes would move the paper from "interesting prototype" to "credible contribution."
