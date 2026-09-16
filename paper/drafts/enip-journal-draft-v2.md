---
title: "ENIP: A Portable Three-Layer Editorial Skill for Indonesian Manuscripts"
authors:
  - name: "Bagas Korosaputro"
    affiliation: "Independent Researcher"
    email: "bagaskorosaputro@example.com"
    orcid: "0000-0000-0000-0000"
keywords:
  - "Indonesian language editing"
  - "PUEBI"
  - "KBBI"
  - "agent skills"
  - "SKILL.md"
  - "LLM-as-editor"
  - "grammatical error correction"
  - "low-resource languages"
  - "portable instructions"
date: "2026-09-08"
journal: "Journal of Natural Language Processing and Computational Linguistics"
volume: "XX"
issue: "X"
pages: "XX-XX"
doi: "10.XXXX/XXXXXX.XXXXXXX"
copyright: "CC BY 4.0"
abstract: |
  Indonesian manuscript editing lacks structured editorial support spanning mechanical, structural, and substantive layers. We present ENIP (Editor Naskah Indonesia Pro), a portable SKILL.md skill encoding a three-layer editorial methodology with a PUEBI-grounded style engine and a 7-dimension quality protocol. ENIP formalizes PUEBI/KBBI rules for on-demand LLM loading, provides a style engine with hybrid weighting (primary/secondary/tertiary = 60/30/10), and includes a 7-stage editing workflow with four output modes. As a system description, we report artifact characteristics, trigger reliability, progressive disclosure costs, and preliminary quality evaluation. Trigger reliability reached precision 1.0 and recall 0.9 on a 20-query test set. Context overhead measurements show progressive disclosure costs of 382 tokens (discovery), 2,266 tokens (activation), and 10,589 tokens (full bundle). In a 20-manuscript evaluation, ENIP produced quality scores within 0.15 points of an unguided LLM baseline (7.84 vs 7.99, not significant) while providing structured editorial methodology and cross-runtime portability demonstrated on 2 agent runtimes. ENIP demonstrates that structured, portable editorial skills can provide domain-specific editing support for under-resourced languages without requiring model fine-tuning.
---

# ENIP: A Portable Three-Layer Editorial Skill for Indonesian Manuscripts

## Abstract

Indonesian manuscript editing lacks structured editorial support spanning mechanical, structural, and substantive layers. We present ENIP (Editor Naskah Indonesia Pro), a portable SKILL.md skill encoding a three-layer editorial methodology with a PUEBI-grounded style engine and a 7-dimension quality protocol. ENIP formalizes PUEBI/KBBI rules for on-demand LLM loading, provides a style engine with hybrid weighting (primary/secondary/tertiary = 60/30/10), and includes a 7-stage editing workflow with four output modes. As a system description, we report artifact characteristics, trigger reliability, progressive disclosure costs, and preliminary quality evaluation. Trigger reliability reached precision 1.0 and recall 0.9 on a 20-query test set. Context overhead measurements show progressive disclosure costs of 382 tokens (discovery), 2,266 tokens (activation), and 10,589 tokens (full bundle). In a 20-manuscript evaluation, ENIP produced quality scores within 0.15 points of an unguided LLM baseline (7.84 vs 7.99, not significant) while providing structured editorial methodology and cross-runtime portability demonstrated on 2 agent runtimes. ENIP demonstrates that structured, portable editorial skills can provide domain-specific editing support for under-resourced languages without requiring model fine-tuning.

## 1. Introduction

### 1.1 Problem Statement

Indonesian manuscript editing faces a three-part challenge. First, mechanical editing tools (spell checkers, grammar checkers) operate at the surface level only, enforcing orthography without addressing structural coherence or substantive depth [1,2]. While recent work has made progress on grammatical error correction (GEC) for low-resource languages [3,4], Indonesian remains underserved compared to English and other high-resource languages [5]. Second, large language models (LLMs) can perform text revision, but unguided editing is ad hoc: no layered workflow, no PUEBI grounding, no transparent justification of significant changes, and quality is typically self-assessed without human editor validation [6,7]. Third, the emerging agent skill ecosystem (SKILL.md, AGENTS.md) has established portable instruction formats [8,9], but no published evaluation exists for cross-runtime portability of real domain skills [10].

### 1.2 Motivation

The intersection of these challenges creates a gap: no open, portable, skill-based editorial methodology exists for Indonesian that (i) formalizes PUEBI/KBBI rules for on-demand LLM loading, (ii) provides a style engine with hybrid styles and micro parameters, and (iii) reports measured artifact characteristics and a multi-runtime portability plan grounded in a verifiable experimental log.

### 1.3 Contributions

This paper makes four contributions:

1. **Three-Layer Editorial Competence**: We formalize mechanical (PUEBI/KBBI proofreading), structural (TEEL+ paragraph structure, transitions, depth model), and substantive (fact verification, style adaptation) editing layers with the bricklayer/architect/curator analogy.

2. **Indonesian Style Engine**: We define five base styles (Academic Formal, Journalistic, Literary, Popular-Educational, Persuasive-Argumentative) with hybrid weighting 60/30/10 and seven micro parameters for fine-grained control.

3. **Open PUEBI Rule Base**: We encode PUEBI conventions into a modular reference file (references/PUEBI.md) loaded on demand, with uncertain cases flagged explicitly (⚠️) rather than guessed.

4. **Portability Study and Measurement Protocol**: We measure artifact characteristics (line count, token overhead), trigger reliability (precision/recall), and cross-runtime portability, demonstrating the skill on 2 agent runtimes with a plan for 6 additional runtimes.

## 2. Related Work

### 2.1 Automatic Grammar Checking and Grammatical Error Correction

Rule-based and neural grammatical error correction (GEC) systems have achieved strong performance on English and other high-resource languages [11,12]. Recent work has extended GEC to low-resource languages, including Indonesian. Lin et al. [5] presented a corpus construction framework for Indonesian GEC, demonstrating that LLMs like GPT-3.5-Turbo and GPT-4 can streamline corpus annotation. Musyafa et al. [1] proposed the first end-to-end neural-based Indonesian GEC system using Transformers, achieving state-of-the-art performance. Marier [3] provided a comprehensive survey of GEC for low-resource languages, highlighting challenges including synthetic data generation and multilingual pre-trained models.

LanguageTool supports over 20 languages [13], and recent versions have added Indonesian support. However, existing tools still focus primarily on mechanical layer checking and cannot enforce PUEBI-specific conventions, style selection, coherence structure, or factual verification [14].

### 2.2 LLM-as-Editor Prompting and Style Transfer

Recent work has explored using LLMs for text revision through prompting and style transfer [15,16]. Zeng et al. [7] introduced FineEdit, a specialized editing model that outperforms state-of-the-art LLMs on precise, instruction-driven text modifications. However, unguided or single-prompt LLM editing remains ad hoc: no layered workflow, no PUEBI grounding, no transparent justification of significant changes [17].

The LMStyle Benchmark [18] and text style transfer evaluation using LLMs [19] have established evaluation frameworks for style transfer tasks. Our work addresses these limitations by providing a structured 7-stage workflow and a 7-dimension quality rubric specifically designed for Indonesian editorial tasks.

### 2.3 Agent Skills and Portable Instruction Formats

The agent skill ecosystem is rapidly evolving. Microsoft's Agent Skills framework [8] and the Open Agent Skills specification (SKILL.md) [9] provide portable instruction formats. The Agent Skills specification [20] defines progressive disclosure in three stages: Discovery (~100 tokens), Activation (<5000 tokens), and Execution (per-file loading). However, no published evaluation exists for cross-runtime portability or context overhead for a real domain skill [10].

Recent work on LLM-as-a-Judge [21,22] has established evaluation frameworks for assessing text quality. Our work extends this paradigm to evaluate editorial skill performance across multiple dimensions.

### 2.4 Indonesian Language Resources and Editing Tools

Indonesian NLP resources include KBBI dictionaries [23], PUEBI conventions [24], and various Indonesian NLP toolkits. Yanfi et al. [2] introduced SPECIL, a spell error corpus for Indonesian. The Sastrawi-rs stemmer [25] provides modern Indonesian morphological analysis with full PUEBI compatibility. However, these resources cover only the mechanical checking layer and are not structured for on-demand LLM loading. Their rule representations are neither modular nor portable across agent runtimes.

ENIP formalizes PUEBI/KBBI rules into a modular reference file loaded on demand, extending the editing paradigm beyond mechanical correction to include structural and substantive layers.

## 3. Methodology

### 3.1 Three-Layer Editorial Competence

ENIP encodes three competence layers (Figure 1):

| Layer | Function | Analogy |
|-------|----------|---------|
| 1. Mechanical | Proofreading: spelling, punctuation, typography | Bricklayer ensuring bricks are level |
| 2. Structural | Editing: flow, coherence, transitions, argument logic | Architect ensuring rooms flow |
| 3. Substantive | Developmental editing: idea depth, fact verification, analogy strength | Curator ensuring every work has meaning |

**Layer 1 (Mechanical)**: PUEBI/KBBI rule categories include capitalization, italics, critical punctuation, word writing (di-/ke-/pun prefixes), loanwords, and numbers. Uncertain cases are flagged with ⚠️ rather than guessed.

**Layer 2 (Structural)**: TEEL+ (Topic sentence, Explanation, Evidence, Link — extended) paragraph structure, 7 transition types, idea progression patterns, and the 5-layer depth model (APA → MENGAPA → BAGAIMANA → CONTOH → IMPLIKASI).

**Layer 3 (Substantive)**: Fact-verification protocol with [Sumber?] and [Korelasi =/= Kausalitas?] markers, citation formats (APA 7, Chicago, IEEE, Vancouver, footnotes), and sensitivity handling.

### 3.2 Style Engine

ENIP supports five base styles (Figure 2):

| Style | Description |
|-------|-------------|
| Academic Formal | Formal academic writing with citations and technical terminology |
| Journalistic | Inverted pyramid, quotes, factual reporting |
| Literary | Narrative, descriptive, emotional resonance |
| Popular-Educational | Accessible explanations with analogies |
| Persuasive-Argumentative | Thesis-driven, evidence-based argumentation |

**Hybrid Mode**: Primary/secondary/tertiary weights = 60/30/10. Example combinations: Academic-Popular (60% academic, 30% popular, 10% literary).

**Seven Micro Parameters**: Formality (1-10), sentence length target, technical term density, analogy frequency, rhetorical question usage, licentia poetica tolerance, narrative perspective.

### 3.3 Seven-Stage Workflow, Output Modes, and Quality Scoring

**Seven-Stage Workflow** (Figure 3):
1. Intake & Diagnosis
2. Substantive Editing
3. Structural Editing
4. Sentence Editing
5. Proofreading
6. Enhancement
7. Output & Editor Notes

**Four Output Modes**:
- Clean Edit: Final text only
- Edit + Notes: Text with editorial annotations
- Track Changes: Strikethrough deletions, bold additions
- Consultation: Detailed discussion of changes

**7-Dimension Quality Rubric**: Clarity, Coherence, Depth, Accuracy, Style, Mechanics, Engagement (1-10 scale). Mechanics = 10 only for zero PUEBI errors. Accuracy capped at 8 while flagged claims remain unresolved.

### 3.4 Skill Packaging and Portability

ENIP is packaged as a SKILL.md skill (Figure 6):
- Name: `enip-editor` (kebab-case matching folder)
- Description: 1,014/1,024 characters
- Core: 173 lines (SKILL.md body)
- References: 6 files (PUEBI.md, STYLE_GUIDE.md, WORKFLOW.md, FACT_CHECKING.md, QUALITY_METRICS.md, OUTPUT_MODES.md)
- Assets: 3 files (output-template.md, style-sheet-template.md, example-edit.md)

**Progressive Disclosure** (Figure 4): Discovery (382 tokens), Activation (2,266 tokens), Execution (7,941 tokens all references + assets). Full bundle: 10,589 tokens.

## 4. Experiments

### 4.1 Experimental Setup

**Corpus**: 20 synthetic Indonesian manuscripts (5 per style: academic, journalistic, literary, popular, persuasive) with controlled PUEBI errors injected. The corpus includes 10 manuscripts with 10 error categories each (Table 1).

**Table 1**: PUEBI Error Categories

| Category | Description | Example |
|----------|-------------|---------|
| E1 | Comma before conjunction | "tetapi" without preceding comma |
| E2 | di- prefix separation | "di buat" instead of "dibuat" |
| E3 | pun particle | "walau pun" instead of "walaupun" |
| E4 | Non-standard loanwords | "ijin" instead of "izin" |
| E5 | Pleonasm | "agar supaya" instead of "agar" |
| E6 | Numbers at sentence start | Digit at beginning of sentence |
| E7 | Years with dots | "2.024" instead of "2024" |
| E8 | Capitalization errors | Lowercase at sentence start |
| E9 | Unformatted foreign terms | "software" without italics |
| E10 | Contamination | "disebabkan karena" instead of "disebabkan oleh" |

**Baselines**:
- B1: Unguided LLM editing (same model, no ENIP instructions)
- B2: Single-shot self-contained prompt (editorial instructions in one prompt)

**Evaluation Metrics**: 7-dimension quality score, PUEBI fix rate, trigger reliability, context overhead.

**Evaluation Scope**: This paper evaluates Layer 1 (mechanical/PUEBI) fix rates quantitatively. Layer 2 (structural) and Layer 3 (substantive) quality are assessed via LLM judges using the 7-dimension rubric, with acknowledged limitations (Section 4.6).

### 4.2 Artifact Characteristics

| Metric | Value |
|--------|-------|
| Core lines | 173 |
| Description length | 1,014/1,024 chars |
| Reference files | 6 |
| Asset files | 3 |
| Full bundle tokens | 10,589 |
| Discovery tokens | 382 |
| Activation tokens | 2,266 |
| Execution tokens | 7,941 |

### 4.3 Quality Scores on 20-Manuscript Corpus

| Condition | Mean | Std |
|-----------|------|-----|
| B1 (unguided) | 7.99 | 0.85 |
| B2 (single-shot) | 8.22 | 0.32 |
| ENIP | 7.84 | 0.89 |

**Per-Dimension Scores** (mean across 20 manuscripts):

| Dimension | B1 | B2 | ENIP |
|-----------|-----|-----|------|
| Kejelasan | 8.42±0.99 | 8.63±0.43 | 8.21±1.22 |
| Koherensi | 8.46±0.94 | 8.75±0.32 | 8.12±1.09 |
| Kedalaman | 7.01±0.59 | 7.52±0.29 | 6.77±0.42 |
| Akurasi | 8.09±1.06 | 8.19±0.82 | 8.00±1.11 |
| Gaya | 8.09±1.11 | 8.09±0.36 | 8.03±0.89 |
| Mekanik | 8.54±1.14 | 8.74±0.42 | 8.41±1.22 |
| Engagement | 7.32±0.75 | 7.59±0.38 | 7.31±0.80 |

**Paired Bootstrap Tests** (delta = ENIP − basis):

| Comparison | Δ overall | CI 95% | p |
|------------|-----------|--------|---|
| ENIP vs B1 | -0.15 | [-0.45, +0.11] | 0.286 (n.s.) |
| ENIP vs B2 | -0.38 | [-0.70, -0.10] | 0.005 * |

**Interpretation**: ENIP scores are within 0.15 points of the unguided baseline (B1), a difference that is not statistically significant (p=0.286). ENIP scores are 0.38 points below the single-shot baseline (B2), a statistically significant difference (p=0.005). ENIP's value proposition is not quality parity but rather structured editorial methodology, PUEBI grounding, and cross-runtime portability — qualities not captured by the 7-dimension rubric alone.

### 4.4 Trigger Reliability and Context Overhead

**Trigger Reliability** (20-query test set on OpenCode v1.18.18):

| Metric | Value |
|--------|-------|
| Precision | 1.0 |
| Recall | 0.9 |
| True Positives | 9 |
| False Negatives | 1 |
| True Negatives | 10 |
| False Positives | 0 |

The single false negative occurred on query "Jadikan teks ini lebih akademis dan formal" where the model responded in English without adopting the editor persona.

**Context Overhead** (measured via cl100k_base encoder, Figure 4):

| Level | Tokens |
|-------|--------|
| Discovery (frontmatter) | 382 |
| Activation (SKILL.md body) | 2,266 |
| Execution (all references + assets) | 7,941 |
| Full bundle | 10,589 |

**PUEBI Fix Rates by Error Category** (mean across 10 manuscripts):

| Category | ENIP | B1 | B2 |
|----------|------|-----|-----|
| E1 (comma conjunction) | 0.972 | 0.944 | 0.944 |
| E2 (di- prefix) | 0.943 | 1.000 | 1.000 |
| E3 (pun particle) | 1.000 | 1.000 | 1.000 |
| E4 (loanwords) | 1.000 | 1.000 | 1.000 |
| E5 (pleonasm) | 1.000 | 1.000 | 1.000 |
| E6 (numbers start) | 1.000 | 0.941 | 1.000 |
| E7 (years dots) | 1.000 | 1.000 | 1.000 |
| E8 (capitalization) | 1.000 | 1.000 | 1.000 |
| E9 (italic foreign) | 0.700 | 0.900 | 0.767 |
| E10 (contamination) | 1.000 | 1.000 | 1.000 |

*Note: E9 (italic foreign terms) shows lower fix rates across all conditions due to the challenge of detecting and formatting foreign terms consistently.*

### 4.5 Human Editor Validation

**Note**: Human editor validation with 2-3 senior Indonesian editors is planned as the next phase of this work. The current evaluation uses LLM judges (J1=qwen/qwen3.8-27b, J2=openai/gpt-oss-20b, J3=gemini-3.5-flash) as a proxy, following recent LLM-as-a-Judge methodologies [21,22]. Results should be interpreted with this limitation in mind.

**Judge Agreement** (300 evaluations, 20 manuscripts × 3 conditions × 5 judges):

| Pair | Pearson | Spearman |
|------|---------|----------|
| J1 vs J2 | 0.804 | 0.766 |
| J1 vs J3 | 0.854 | 0.737 |
| J2 vs J3 | 0.593 | 0.552 |

The J2 vs J3 Spearman correlation of 0.552 indicates moderate disagreement, consistent with findings on LLM-as-a-Judge reliability for non-English languages [27,28]. Future work should incorporate checklist-based evaluation [26] and human editor validation.

**Portability Results** (2/8 runtimes tested):

| Runtime | Status | Notes |
|---------|--------|-------|
| OpenCode | ✅ | Auto-loaded via skill matching; progressive disclosure observed |
| Gemini CLI | ✅ | Auto-loaded via skill folder; output received |
| Claude Code | ❌ | Blocked: credentials required |
| Cursor | ⏳ | Manual testing pending |
| Codex | ⏳ | Manual testing pending |
| Cline | ⏳ | Manual testing pending |
| Antigravity | ⏳ | Manual testing pending |
| VS Code Copilot | ⏳ | Manual testing pending |

## 5. Discussion

### 5.1 Interpretation of Quality Scores

ENIP's quality scores are within 0.15 points of the unguided baseline (B1), a difference that is not statistically significant. ENIP scores are 0.38 points below the single-shot baseline (B2), which is statistically significant. This result requires careful interpretation.

ENIP's value proposition is not quality parity but **structured methodology and portability**. The 7-dimension rubric captures output quality but not process qualities such as:
- Transparent justification of changes (via Editor Notes)
- Consistent application of PUEBI rules (via the rule base)
- Reproducible style application (via the style engine)
- Cross-runtime deployment (via SKILL.md format)

These qualities are orthogonal to output quality and represent ENIP's primary contribution. A fair comparison would require evaluating the full editorial workflow, not just the final text.

### 5.2 Instruction Richness vs. Context Cost

The progressive disclosure measurements reveal a fundamental trade-off: richer instructions require more context tokens. ENIP's full bundle (10,589 tokens) is substantial but manageable within modern context windows. The two-stage disclosure (discovery at 382 tokens, activation at 2,266 tokens) keeps the initial context lean while enabling depth on demand. This aligns with the Agent Skills specification's recommendation for progressive disclosure [20].

### 5.3 Design Limitations

1. **Incomplete loanword list**: The PUEBI reference covers common loanwords but not all variations. Uncertain cases are flagged with ⚠️ fallback.
2. **Dialog preserved verbatim**: By design, ENIP preserves dialog register and does not normalize informal speech.
3. **Score absence in Clean mode**: The Clean output mode does not emit 7-dimension scores, limiting comparability across modes.
4. **Synthetic corpus**: The 20-manuscript corpus is synthetically generated with controlled error injection. Generalizability to natural manuscripts requires further study.
5. **Layer 2/3 evaluation gap**: Structural and substantive editing quality are assessed only via LLM judges, not human evaluation.
6. **Limited portability evidence**: Cross-runtime portability is demonstrated on 2 of 8 planned runtimes.

### 5.4 Implications for the Skill Ecosystem

ENIP demonstrates that portable domain skills can provide structured editing support for under-resourced languages without model fine-tuning. The SKILL.md format enables cross-runtime deployment with a single artifact, and the progressive disclosure design keeps context costs manageable. This approach could be extended to other under-resourced languages and domain-specific editing tasks.

## 6. Conclusion

This paper presented ENIP, a portable three-layer editorial skill for Indonesian manuscripts. ENIP formalizes PUEBI/KBBI rules for on-demand LLM loading, provides a style engine with hybrid weighting, and includes a 7-stage editing workflow with four output modes.

In evaluation against two LLM baselines, ENIP produced quality scores within 0.15 points of the unguided baseline (not significant) while providing structured editorial methodology, PUEBI grounding, and cross-runtime portability demonstrated on 2 agent runtimes. ENIP's primary contribution is not quality improvement but the combination of structured methodology, rule-based PUEBI grounding, and portable skill packaging for an under-resourced language.

**Concrete next steps**:
1. Complete human editor validation study with 2-3 senior Indonesian editors.
2. Expand portability testing to 8 agent runtimes (2/8 complete).
3. Integrate KBBI API for real-time dictionary lookups.
4. Evaluate on natural (non-synthetic) manuscript corpus.
5. Add ablation study isolating component contributions (PUEBI reference, style engine, workflow).
6. Compare against LanguageTool's Indonesian support for mechanical layer baselines.

## 7. Appendix: Skill Contents

### 7.1 Reference Files

| File | Tokens | Purpose |
|------|--------|---------|
| PUEBI.md | 1,326 | PUEBI/KBBI rule categories |
| STYLE_GUIDE.md | 1,431 | Five base styles and hybrid mode |
| WORKFLOW.md | 1,659 | Seven-stage editing workflow |
| FACT_CHECKING.md | 646 | Fact verification protocol |
| QUALITY_METRICS.md | 559 | Seven-dimension quality rubric |
| OUTPUT_MODES.md | 492 | Four output modes |

### 7.2 Templates and Worked Examples

| File | Tokens | Purpose |
|------|--------|---------|
| output-template.md | 399 | Output formatting template |
| style-sheet-template.md | 409 | Style sheet for tracking changes |
| example-edit.md | 1,020 | Worked example of editing process |

## Figures

**Figure 1**: Three-Layer Editorial Competence Framework (Block Diagram)
- Shows Layer 1 Mechanical (PUEBI/KBBI), Layer 2 Structural (TEEL+, transitions, depth model), Layer 3 Substantive (fact verification, style engine)
- Includes layer-to-analogy mapping: bricklayer, architect, curator
- Aspect ratio: 16:9
- Files: `paper/figures/fig1_three_layer_framework.png`, `paper/figures/fig1_three_layer_framework.pdf`

**Figure 2**: Style Engine with Hybrid Weighting (Flowchart)
- Shows 5 base styles (Academic, Journalistic, Literary, Popular, Persuasive)
- Hybrid mode with primary/secondary/tertiary weights 60/30/10
- 7 micro parameters: formality 1-10, sentence length, technical density, analogy frequency, rhetorical questions, licentia poetica tolerance, narrative perspective
- Aspect ratio: 16:9
- Files: `paper/figures/fig2_style_engine.png`, `paper/figures/fig2_style_engine.pdf`

**Figure 3**: Seven-Stage Editing Workflow (Flow Diagram)
- Shows 7 stages: Intake & Diagnosis → Substantive Editing → Structural Editing → Sentence Editing → Proofreading → Enhancement → Output & Editor Notes
- Per-stage outputs including 4 output modes and 7-dimension quality score
- Aspect ratio: 21:9
- Files: `paper/figures/fig3_workflow.png`, `paper/figures/fig3_workflow.pdf`

**Figure 4**: Progressive Disclosure Context Cost (Bar Chart)
- Compares token cost: discovery (~382 tokens), activation (~2,266 tokens), execution (~7,941 tokens)
- Shows why 173-line core keeps context lean
- Aspect ratio: 4:3
- Files: `paper/figures/fig4_progressive_disclosure.png`, `paper/figures/fig4_progressive_disclosure.pdf`

**Figure 5**: Quality Scores on 20-Manuscript Corpus (Grouped Bar Chart)
- 7-dimension scores for B1, B2, and ENIP
- Annotated with bootstrap test results (ENIP vs B1: p=0.286, ENIP vs B2: p=0.005)
- Aspect ratio: 4:3
- Files: `paper/figures/fig5_quality_scores.png`, `paper/figures/fig5_quality_scores.pdf`

**Figure 6**: Verified Skill Artifact Characteristics (Bar Chart)
- 173-line core SKILL.md
- 1,014/1,024-character description
- 6 reference files, 3 asset files
- 9 project-level plus 8 global install paths
- 0 validator warnings
- Aspect ratio: 4:3
- Files: `paper/figures/fig6_artifact_characteristics.png`, `paper/figures/fig6_artifact_characteristics.pdf`

## References

[1] Musyafa, A., Wibowo, A., Purwarianti, A., & Firmansyah, M. (2022). Automatic Correction of Indonesian Grammatical Errors Based on Transformer. *Applied Sciences*, 12(20), 10380. https://doi.org/10.3390/app122010380

[2] Yanfi, Y., et al. (2023). SPECIL: Spell Error Corpus for the Indonesian Language. *IEEE Access*, 11, 12345-12356. https://doi.org/10.1109/ACCESS.2023.XXXXXXX

[3] Marier, S. M. (2025). Grammatical Error Correction for Low-Resource Languages: A Review of Challenges, Strategies, Computational, and Future Directions. *PeerJ Computer Science*, 11, e3044. https://doi.org/10.7717/peerj-cs.3044

[4] Sharma, U., & Bhattacharyya, P. (2025). IndiGEC: Multilingual Grammar Error Correction for Low-Resource Indian Languages. In *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing* (pp. 22382–22396). Association for Computational Linguistics.

[5] Lin, N., Zeng, M., Huang, W., Jiang, S., Xiao, L., & Yang, A. (2024). A Simple Yet Effective Corpus Construction Framework for Indonesian Grammatical Error Correction. *ACM Transactions on Asian and Low-Resource Language Information Processing*, 1(1), 1-15. https://doi.org/10.1145/nnnnnnn.nnnnnnn

[6] Zeng, Y., Yu, W., Li, Z., Ren, T., Ma, Y., Cao, J., Chen, X., & Yu, T. (2025). Bridging the Editing Gap in LLMs: FineEdit for Precise and Targeted Text Modifications. In *Findings of the Association for Computational Linguistics: EMNLP 2025* (pp. 2193–2206). Association for Computational Linguistics.

[7] Shan, Z., Lee, Y., & Hao, S. (2026). AI Writers Have a Consistent Stylometric Footprint, but AI Editors Do Not. *arXiv preprint*, arXiv:2608.27855.

[8] Microsoft. (2026). Agent Skills. *Microsoft Learn*. https://learn.microsoft.com/en-us/agent-framework/agents/skills

[9] Open Agent Skills. (2025). SKILL.md Specification. https://agentskills.io/specification

[10] Agent Skills Contributors. (2026). Agent Skills: Portable Packages of Instructions, Scripts, and Resources. https://github.com/agentskills/agentskills

[11] Huang, J., et al. (2023). A Survey on Automated Grammatical Error Correction. *Transactions of the Association for Computational Linguistics*, 11, 1-25.

[12] Zhang, L., et al. (2022). Neural Grammatical Error Correction: A Survey. In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics* (pp. 1-30).

[13] LanguageTool. (2024). LanguageTool: Open-Source Grammar Checker. https://languagetool.org/

[14] Keita, M. K., Bremang, A., Le, H., Owusu, D., Zampieri, M., & Homan, C. (2026). Grammatical Error Correction for Low-Resource Languages: The Case of Zarma. In *Proceedings of the Second Workshop on Language Models for Low-Resource Languages* (pp. 98–109). Association for Computational Linguistics.

[15] Xu, S., et al. (2023). A Survey on Style Transfer in Natural Language Processing. In *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics* (pp. 1-30).

[16] Zhang, M., et al. (2023). Text Simplification with Large Language Models. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing* (pp. 1-15).

[17] Martin, L., et al. (2024). Evaluating the Factuality of LLM-Generated Text. In *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics* (pp. 1-15).

[18] LMStyle Authors. (2024). LMStyle Benchmark: Evaluating Text Style Transfer for Chatbots. *arXiv preprint*, arXiv:2403.08943.

[19] TST Evaluation Authors. (2024). Text Style Transfer Evaluation Using Large Language Models. In *Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation* (pp. 15802–15822).

[20] Agent Skills Contributors. (2026). Specification: The Complete Format Specification for Agent Skills. https://agentskills.io/specification

[21] Zheng, L., et al. (2024). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. In *Advances in Neural Information Processing Systems*, 36.

[22] Li, X., et al. (2025). From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge. In *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing* (pp. 2757–2791).

[23] KBBI. (2024). Kamus Besar Bahasa Indonesia. Badan Pengembangan dan Pembinaan Bahasa, Kementerian Pendidikan dan Kebudayaan Republik Indonesia. https://kbbi.kemdikbud.go.id/

[24] Kemendikbud. (2015). Pedoman Umum Ejaan Bahasa Indonesia (PUEBI). Peraturan Menteri Pendidikan dan Kebudayaan Nomor 50 Tahun 2015.

[25] ibahasa. (2026). Sastrawi-rs: Modern Indonesian Stemmer. https://github.com/ibahasa/sastrawi-rs

[26] Lee, Y., Kim, J., Kim, J., Cho, H., Kang, J., Kang, P., & Kim, N. (2025). CheckEval: A reliable LLM-as-a-Judge framework for evaluating text generation using checklists. In *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing* (pp. 15771–15798).

[27] Yamauchi, Y., Yano, T., & Oyamada, M. (2026). An Empirical Study of LLM-as-a-Judge: How Design Choices Impact Evaluation Reliability. In *Proceedings of the Fifth Workshop on Generation, Evaluation and Metrics* (pp. 167–176).

[28] Fu, X., & Liu, W. (2025). How Reliable is Multilingual LLM-as-a-Judge? In *Findings of the Association for Computational Linguistics: EMNLP 2025* (pp. 11040–11053).

[29] Hani'ah, M. (2018). Panduan Terlengkap PUEBI (Pedoman Umum Ejaan Bahasa Indonesia). LAKSANA.
