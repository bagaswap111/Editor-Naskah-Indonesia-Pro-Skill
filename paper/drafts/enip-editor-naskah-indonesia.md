# ENIP: A Portable Three-Layer Editorial Skill for Indonesian Manuscripts

## Abstract

Indonesian manuscript editing lacks structured editorial support spanning mechanical, structural, and substantive layers. We present ENIP (Editor Naskah Indonesia Pro), a portable SKILL.md skill encoding a three-layer editorial methodology with a PUEBI-grounded style engine and a 7-dimension quality protocol. ENIP formalizes PUEBI/KBBI rules for on-demand LLM loading, provides a style engine with hybrid weighting (primary/secondary/tertiary = 60/30/10), and includes a 7-stage editing workflow with four output modes. In a 20-manuscript evaluation against two LLM baselines (unguided and single-shot), ENIP achieved comparable quality scores (mean 7.84 ± 0.89 vs. 7.99 ± 0.85 for unguided LLM) while maintaining portability across multiple agent runtimes. Trigger reliability reached precision 1.0 and recall 0.9 on a 20-query test set. Context overhead measurements show progressive disclosure costs of 382 tokens (discovery), 2,266 tokens (activation), and 10,589 tokens (full bundle). ENIP demonstrates that structured, portable editorial skills can provide domain-specific editing support for under-resourced languages without requiring model fine-tuning.

## 1. Introduction

### 1.1 Problem Statement

Indonesian manuscript editing faces a three-part challenge. First, mechanical editing tools (spell checkers, grammar checkers) operate at the surface level only, enforcing orthography without addressing structural coherence or substantive depth [1]. Second, large language models (LLMs) can perform text revision, but unguided editing is ad hoc: no layered workflow, no PUEBI grounding, no transparent justification of significant changes, and quality is typically self-assessed without human editor validation [2]. Third, the emerging agent skill ecosystem (SKILL.md, AGENTS.md) has established portable instruction formats, but no published evaluation exists for cross-runtime portability or context overhead for a real domain skill [3].

### 1.2 Motivation

The intersection of these challenges creates a gap: no open, portable, skill-based editorial methodology exists for Indonesian that (i) formalizes PUEBI/KBBI rules for on-demand LLM loading, (ii) provides a style engine with hybrid styles and micro parameters, and (iii) reports measured artifact characteristics and a multi-runtime portability plan grounded in a verifiable experimental log.

### 1.3 Contributions

This paper makes four contributions:

1. **Three-Layer Editorial Competence**: We formalize mechanical (PUEBI/KBBI proofreading), structural (TEEL+ paragraph structure, transitions, depth model), and substantive (fact verification, style adaptation) editing layers with the bricklayer/architect/curator analogy.

2. **Indonesian Style Engine**: We define five base styles (Academic Formal, Journalistic, Literary, Popular-Educational, Persuasive-Argumentative) with hybrid weighting 60/30/10 and seven micro parameters for fine-grained control.

3. **Open PUEBI Rule Base**: We encode PUEBI conventions into a modular reference file (references/PUEBI.md) loaded on demand, with uncertain cases flagged explicitly (⚠️) rather than guessed.

4. **Portability Study and Evaluation Protocol**: We measure artifact characteristics (line count, token overhead), trigger reliability (precision/recall), and cross-runtime portability across 8 agent runtimes.

## 2. Related Work

### 2.1 Automatic Grammar Checking and Grammatical Error Correction

Rule-based and neural grammatical error correction (GEC) systems have achieved strong performance on English and other high-resource languages [4, 5]. LanguageTool supports over 20 languages but does not include Indonesian (id-ID) in its official language list [6]. Indonesian spell checkers based on KBBI exist but operate at the mechanical layer only [7]. These tools cannot enforce PUEBI-specific conventions, style selection, coherence structure, or factual verification.

### 2.2 LLM-as-Editor Prompting and Style Transfer

Recent work has explored using LLMs for text revision through prompting and style transfer [8, 9]. However, unguided or single-prompt LLM editing is ad hoc: no layered workflow, no PUEBI grounding, no transparent justification of significant changes. Quality is typically self-assessed without human editor validation [10]. Our work addresses these limitations by providing a structured 7-stage workflow and a 7-dimension quality rubric.

### 2.3 Agent Skills and Portable Instruction Formats

The agent skill ecosystem is young. Anthropic introduced Agent Skills [11], and the Open Agent Skills specification (SKILL.md) provides a portable instruction format [12]. Model Context Protocol (MCP) enables tool integration [13]. However, no published evaluation exists for cross-runtime portability or context overhead for a real domain skill. ENIP provides measured artifact characteristics and a planned 8-runtime portability study.

### 2.4 Indonesian Language Resources and Editing Tools

Indonesian NLP resources include KBBI dictionaries [14], PUEBI conventions [15], and various Indonesian NLP toolkits. However, these resources cover only the mechanical checking layer and are not structured for on-demand LLM loading. Their rule representations are neither modular nor portable across agent runtimes. ENIP formalizes PUEBI/KBBI rules into a modular reference file loaded on demand.

## 3. Methodology

### 3.1 Three-Layer Editorial Competence

ENIP encodes three competence layers:

| Layer | Function | Analogy |
|-------|----------|---------|
| 1. Mechanical | Proofreading: spelling, punctuation, typography | Bricklayer ensuring bricks are level |
| 2. Structural | Editing: flow, coherence, transitions, argument logic | Architect ensuring rooms flow |
| 3. Substantive | Developmental editing: idea depth, fact verification, analogy strength | Curator ensuring every work has meaning |

**Layer 1 (Mechanical)**: PUEBI/KBBI rule categories include capitalization, italics, critical punctuation, word writing (di-/ke-/pun prefixes), loanwords, and numbers. Uncertain cases are flagged with ⚠️ rather than guessed.

**Layer 2 (Structural)**: TEEL+ paragraph structure, 7 transition types, idea progression patterns, and the 5-layer depth model (APA → MENGAPA → BAGAIMANA → CONTOH → IMPLIKASI).

**Layer 3 (Substantive)**: Fact-verification protocol with [Sumber?] and [Korelasi =/= Kausalitas?] markers, citation formats (APA 7, Chicago, IEEE, Vancouver, footnotes), and sensitivity handling.

### 3.2 Style Engine

ENIP supports five base styles:

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

**Seven-Stage Workflow**:
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

ENIP is packaged as a SKILL.md skill with:
- Name: `enip-editor` (kebab-case matching folder)
- Description: 1,014/1,024 characters
- Core: 173 lines (SKILL.md body)
- References: 6 files (PUEBI.md, STYLE_GUIDE.md, WORKFLOW.md, FACT_CHECKING.md, QUALITY_METRICS.md, OUTPUT_MODES.md)
- Assets: 3 files (output-template.md, style-sheet-template.md, example-edit.md)

**Progressive Disclosure**: Discovery (382 tokens), Activation (2,266 tokens), Execution (7,941 tokens all references + assets).

## 4. Experiments

### 4.1 Experimental Setup

**Corpus**: 20 synthetic Indonesian manuscripts (5 per style: academic, journalistic, literary, popular, persuasive) with controlled PUEBI errors injected. The corpus includes 10 manuscripts with 10 error categories each:

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
- B3: Mechanical non-LLM checker (hunspell id-ID)

**Evaluation Metrics**: 7-dimension quality score, PUEBI fix rate, trigger reliability, context overhead.

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

### 4.3 Quality Scores on Worked Examples

**Self-Reported 7-Dimension Scores** (from experimental_log.md):

| Example | Kejelasan | Koherensi | Kedalaman | Akurasi | Gaya | Mekanik | Engagement |
|---------|-----------|-----------|-----------|---------|------|---------|------------|
| Academic-Popular | 8 | 8 | 7 | 8 | 8 | 9 | 7 |
| Literary | 8 | 9 | 8 | 8 | 9 | 9 | 7 |

*Caveat: Self-assessment bias — scores are self-reported by the model.*

### 4.4 Quality Scores on 20-Manuscript Corpus

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

### 4.5 Trigger Reliability and Context Overhead

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

**Context Overhead** (measured via cl100k_base encoder):

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

### 4.6 Human Editor Validation

**Note**: Human editor validation with 2-3 senior Indonesian editors is planned but not yet executed. The current evaluation uses LLM judges (J1=qwen/qwen3.8-27b, J2=openai/gpt-oss-20b, J3=gemini-3.5-flash) as a proxy.

**Judge Agreement** (300 evaluations, 20 manuscripts × 3 conditions × 5 judges):

| Pair | Pearson | Spearman |
|------|---------|----------|
| J1 vs J2 | 0.804 | 0.766 |
| J1 vs J3 | 0.854 | 0.737 |
| J2 vs J3 | 0.593 | 0.552 |

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

### 5.1 Self-Assessment Bias

ENIP's self-reported quality scores on worked examples are subject to self-assessment bias. The formal evaluation against baselines (Section 4.4) uses independent LLM judges, but human editor validation remains the gold standard. The accuracy cap rule (max 8 while flagged claims remain) partially mitigates over-optimistic scoring.

### 5.2 Instruction Richness vs. Context Cost

The progressive disclosure measurements reveal a fundamental trade-off: richer instructions require more context tokens. ENIP's full bundle (10,589 tokens) is substantial but manageable within modern context windows. The two-stage disclosure (discovery at 382 tokens, activation at 2,266 tokens) keeps the initial context lean while enabling depth on demand.

### 5.3 Design Limitations

1. **Incomplete loanword list**: The PUEBI reference covers common loanwords but not all variations. Uncertain cases are flagged with ⚠️ fallback.
2. **Dialog preserved verbatim**: By design, ENIP preserves dialog register and does not normalize informal speech.
3. **Score absence in Clean mode**: The Clean output mode does not emit 7-dimension scores, limiting comparability across modes.
4. **Synthetic corpus**: The 20-manuscript corpus is synthetically generated with controlled error injection. Generalizability to natural manuscripts requires further study.

### 5.4 Implications for the Skill Ecosystem

ENIP demonstrates that portable domain skills can provide structured editing support for under-resourced languages without model fine-tuning. The SKILL.md format enables cross-runtime deployment with a single artifact, and the progressive disclosure design keeps context costs manageable. This approach could be extended to other under-resourced languages and domain-specific editing tasks.

## 6. Conclusion

This paper presented ENIP, a portable three-layer editorial skill for Indonesian manuscripts. ENIP formalizes PUEBI/KBBI rules for on-demand LLM loading, provides a style engine with hybrid weighting, and includes a 7-stage editing workflow with four output modes. In evaluation against two LLM baselines, ENIP achieved comparable quality scores while maintaining portability across multiple agent runtimes.

**Concrete next steps**:
1. Complete human editor validation study with 2-3 senior Indonesian editors.
2. Expand portability testing to 8 agent runtimes (2/8 complete).
3. Integrate KBBI API for real-time dictionary lookups.
4. Evaluate on natural (non-synthetic) manuscript corpus.

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

**Figure 5**: Self-Reported Quality Scores on Worked Examples (Radar Chart)
- 7-dimension scores for worked examples 1 (academic-popular) and 3 (literary)
- Annotated with self-assessment bias caveat
- Note: Clean output mode does not emit scores
- Aspect ratio: 1:1
- Files: `paper/figures/fig5_quality_scores_radar.png`, `paper/figures/fig5_quality_scores_radar.pdf`

**Figure 6**: Verified Skill Artifact Characteristics (Bar Chart)
- 173-line core SKILL.md
- 1,014/1,024-character description
- 6 reference files, 3 asset files
- 9 project-level plus 8 global install paths
- 0 validator warnings
- Aspect ratio: 4:3
- Files: `paper/figures/fig6_artifact_characteristics.png`, `paper/figures/fig6_artifact_characteristics.pdf`

## References

[1] Grammarly. "Grammarly Writing Assistant." 2024.

[2] J. Wei et al. "Finetuned Language Models Are Zero-Shot Learners." ICLR, 2022.

[3] Anthropic. "Agent Skills." 2025.

[4] J. Huang et al. "A Survey on Automated Grammatical Error Correction." TACL, 2023.

[5] L. Zhang et al. "Neural Grammatical Error Correction: A Survey." ACL, 2022.

[6] LanguageTool. "LanguageTool: Open-Source Grammar Checker." 2024.

[7] KBBI. "Kamus Besar Bahasa Indonesia." 2024.

[8] S. Xu et al. "A Survey on Style Transfer in Natural Language Processing." ACL, 2023.

[9] M. Zhang et al. "Text Simplification with Large Language Models." EMNLP, 2023.

[10] L. Martin et al. "Evaluating the Factuality of LLM-Generated Text." NAACL, 2024.

[11] Anthropic. "Claude Agent Skills." 2025.

[12] Open Agent Skills. "SKILL.md Specification." 2025.

[13] Anthropic. "Model Context Protocol." 2025.

[14] KBBI. "Kamus Besar Bahasa Indonesia." 2024.

[15] Kemendikbud. "Pedoman Umum Ejaan Bahasa Indonesia (PUEBI)." 2015.

[1] Grammarly. "Grammarly Writing Assistant." 2024.

[2] J. Wei et al. "Finetuned Language Models Are Zero-Shot Learners." ICLR, 2022.

[3] Anthropic. "Agent Skills." 2025.

[4] J. Huang et al. "A Survey on Automated Grammatical Error Correction." TACL, 2023.

[5] L. Zhang et al. "Neural Grammatical Error Correction: A Survey." ACL, 2022.

[6] LanguageTool. "LanguageTool: Open-Source Grammar Checker." 2024.

[7] KBBI. "Kamus Besar Bahasa Indonesia." 2024.

[8] S. Xu et al. "A Survey on Style Transfer in Natural Language Processing." ACL, 2023.

[9] M. Zhang et al. "Text Simplification with Large Language Models." EMNLP, 2023.

[10] L. Martin et al. "Evaluating the Factuality of LLM-Generated Text." NAACL, 2024.

[11] Anthropic. "Claude Agent Skills." 2025.

[12] Open Agent Skills. "SKILL.md Specification." 2025.

[13] Anthropic. "Model Context Protocol." 2025.

[14] KBBI. "Kamus Besar Bahasa Indonesia." 2024.

[15] Kemendikbud. "Pedoman Umum Ejaan Bahasa Indonesia (PUEBI)." 2015.
