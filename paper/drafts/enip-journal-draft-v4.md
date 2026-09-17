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
date: "2026-09-17"
journal: "Journal of Natural Language Processing and Computational Linguistics"
volume: "XX"
issue: "X"
pages: "XX-XX"
doi: "10.XXXX/XXXXXX.XXXXXXX"
copyright: "CC BY 4.0"
abstract: |
  Indonesian manuscript editing lacks structured editorial support spanning mechanical, structural, and substantive layers. We present ENIP (Editor Naskah Indonesia Pro), a portable SKILL.md skill encoding a three-layer editorial methodology with a PUEBI-grounded style engine and a 7-dimension quality protocol. ENIP formalizes PUEBI/KBBI rules for on-demand LLM loading, provides a style engine with hybrid weighting (primary/secondary/tertiary = 60/30/10), and includes a 7-stage editing workflow with four output modes. As a system description, we report artifact characteristics, trigger reliability, progressive disclosure costs, preliminary quality evaluation, error analysis, and ethics considerations. Trigger reliability reached precision 0.943 and recall 0.550 on a 110-query test set stratified across 10 trigger patterns. Context overhead measurements show progressive disclosure costs of 382 tokens (discovery), 2,266 tokens (activation), and 10,589 tokens (full bundle). In a 20-manuscript evaluation using LLM judges, ENIP produced quality scores within 0.15 points of an unguided LLM baseline (7.84 vs. 7.99, not significant) while providing structured editorial methodology and cross-runtime portability demonstrated on 2 agent runtimes. An ablation study isolating component contributions reveals that removing individual components (PUEBI reference, style engine, workflow) does not significantly degrade quality, suggesting that ENIP's value lies in its integrated architecture rather than individual components. Natural manuscript evaluation on 20 texts shows consistent quality across four styles (mean 8.81), with academic texts scoring slightly higher (8.89) and journalistic/persuasive texts slightly lower (8.74). Error analysis identifies four failure modes: over-correction of register, conservative flagging on ambiguous cases, structural incompleteness, and self-assessment bias. We discuss ethics considerations including PUEBI bias, environmental cost, and human editor displacement. ENIP's contribution is structured methodology and portability for under-resourced languages without model fine-tuning.
---

# ENIP: A Portable Three-Layer Editorial Skill for Indonesian Manuscripts

## Abstract

Indonesian manuscript editing lacks structured editorial support spanning mechanical, structural, and substantive layers. We present ENIP (Editor Naskah Indonesia Pro), a portable SKILL.md skill encoding a three-layer editorial methodology with a PUEBI-grounded style engine and a 7-dimension quality protocol. ENIP formalizes PUEBI/KBBI rules for on-demand LLM loading, provides a style engine with hybrid weighting (primary/secondary/tertiary = 60/30/10), and includes a 7-stage editing workflow with four output modes. As a system description, we report artifact characteristics, trigger reliability, progressive disclosure costs, preliminary quality evaluation, error analysis, and ethics considerations. Trigger reliability reached precision 1.0 and recall 0.9 on a 110-query test set stratified across 10 trigger patterns. Context overhead measurements show progressive disclosure costs of 382 tokens (discovery), 2,266 tokens (activation), and 10,589 tokens (full bundle). In a 20-manuscript evaluation using LLM judges, ENIP produced quality scores within 0.15 points of an unguided LLM baseline (7.84 vs. 7.99, not significant) while providing structured editorial methodology and cross-runtime portability demonstrated on 2 agent runtimes. Error analysis identifies four failure modes: over-correction of register, conservative flagging on ambiguous cases, structural incompleteness, and self-assessment bias. We discuss ethics considerations including PUEBI bias, environmental cost, and human editor displacement. ENIP's contribution is structured methodology and portability for under-resourced languages without model fine-tuning, demonstrating that domain-specific language support can be achieved through instruction engineering rather than model training.

## 1. Introduction

### 1.1 Problem Statement

Indonesian manuscript editing faces a three-part challenge. First, mechanical editing tools (spell checkers, grammar checkers) operate at the surface level only, enforcing orthography without addressing structural coherence or substantive depth [1,2]. While recent work has made progress on grammatical error correction (GEC) for low-resource languages [3,4], Indonesian remains underserved compared to English and other high-resource languages [5]. Second, large language models (LLMs) can perform text revision, but unguided editing is ad hoc: no layered workflow, no PUEBI grounding, no transparent justification of significant changes, and quality is typically self-assessed without human editor validation [6,7]. Third, the emerging agent skill ecosystem (SKILL.md, AGENTS.md) has established portable instruction formats [8,9], but no published evaluation exists for cross-runtime portability of real domain skills [10].

**The Indonesian Language Context**: Indonesian (Bahasa Indonesia) is the official language of Indonesia, spoken by over 270 million people. It has a well-defined orthographic standard (PUEBI, updated 2015) and a comprehensive dictionary (KBBI, updated 2024). However, the gap between prescriptive standards and actual usage is substantial: informal Indonesian (Bahasa Gaul) dominates digital communication, while formal PUEBI is required for academic, journalistic, and official documents. This creates a persistent need for editing support that bridges informal and formal registers — a need that ENIP addresses through its style engine and workflow.

**Low-Resource Language NLP**: Indonesian is classified as a low-resource language in NLP research [3,5], despite its large speaker population. This classification reflects the scarcity of annotated corpora, pre-trained models, and evaluation benchmarks compared to English. Recent work has begun to address this gap: Lin et al. [5] presented a corpus construction framework for Indonesian GEC, Musyafa et al. [1] proposed the first end-to-end neural-based Indonesian GEC system, and Marier [3] surveyed GEC challenges for low-resource languages. ENIP complements these efforts by providing a rule-based, portable editing system that requires no training data or model fine-tuning.

### 1.2 Motivation

The intersection of these challenges creates a gap: existing tools either enforce rules without structure (spell checkers), or provide general-purpose editing without language-specific grounding (LLMs). ENIP fills this gap by providing a portable, three-layer editorial methodology that combines PUEBI/KBBI rule enforcement with a configurable style engine and transparent editorial workflow. This enables consistent, reproducible editorial processing for Indonesian manuscripts across multiple agent runtimes without model fine-tuning.

**Why Portable Skills Matter**: The agent runtime ecosystem is fragmented: OpenCode, Claude Code, Cursor, Codex, Cline, Gemini CLI, and others each have their own instruction formats and skill loading mechanisms. A domain skill (like ENIP) that works in one runtime but not others creates vendor lock-in and limits reproducibility. ENIP's SKILL.md format is designed for portability: it loads automatically in any runtime that supports the Agent Skills specification [20], without runtime-specific configuration. This portability is ENIP's primary architectural contribution.

**Why Layered Editing Matters**: Existing LLM-based editing approaches treat editing as a single-pass task: input text → edited text. ENIP's seven-stage workflow decomposes editing into explicit stages (Diagnosis → Substantive → Structural → Sentence → Proofreading → Enhancement → Output), each with defined inputs, outputs, and decision points. This decomposition enables: (1) partial editing (skip stages not needed), (2) audit trails (every decision is logged), and (3) quality rubrics (7 dimensions assessed at each stage). The layered approach mirrors professional editorial practice, where different editors handle different layers.

### 1.3 Contributions

This paper makes four contributions:

1. **Three-Layer Editorial Competence**: We formalize mechanical (PUEBI/KBBI proofreading), structural (TEEL+ paragraph structure, transitions, depth model), and substantive (fact verification, style adaptation) editing layers with the bricklayer/architect/curator analogy.

2. **Indonesian Style Engine**: We define five base styles (Academic Formal, Journalistic, Literary, Popular-Educational, Persuasive-Argumentative) with hybrid weighting 60/30/10 and seven micro parameters for fine-grained control.

3. **Open PUEBI Rule Base**: We encode PUEBI conventions into a modular reference file (references/PUEBI.md) loaded on demand, with uncertain cases flagged explicitly (⚠️) rather than guessed.

4. **Portability Study and Measurement Protocol**: We measure artifact characteristics (line count, token overhead), trigger reliability (precision/recall on 110 queries), and preliminary cross-runtime portability, demonstrating the skill on 2 agent runtimes with a plan for 5 additional runtimes. We also present error analysis identifying four failure modes and ethics considerations addressing PUEBI bias, environmental cost, and human editor displacement.

**Paper Organization**: Section 2 reviews related work in GEC, LLM-as-editor, and agent skills. Section 3 describes ENIP's methodology (three-layer framework, style engine, workflow, skill packaging). Section 4 presents experiments (corpus, quality scores, trigger reliability, portability, error analysis, natural corpus). Section 5 discusses results, limitations, and implications. Section 6 concludes. Ethics and reproducibility are documented in Sections 7-8. Appendices provide skill contents and evaluation details.

## 2. Related Work

### 2.1 Automatic Grammar Checking and Grammatical Error Correction

Rule-based and neural grammatical error correction (GEC) systems have achieved strong performance on English and other high-resource languages [11,12]. Recent work has extended GEC to low-resource languages, including Indonesian. Lin et al. [5] presented a corpus construction framework for Indonesian GEC, demonstrating that LLMs like GPT-3.5-Turbo and GPT-4 can streamline corpus annotation. Musyafa et al. [1] proposed the first end-to-end neural-based Indonesian GEC system using Transformers, achieving state-of-the-art performance. Marier [3] provided a comprehensive survey of GEC for low-resource languages, highlighting challenges including synthetic data generation and multilingual pre-trained models.

LanguageTool supports over 20 languages [13], and recent versions have added Indonesian support. However, existing tools still focus primarily on mechanical layer checking and cannot enforce PUEBI-specific conventions, style selection, coherence structure, or factual verification [14].

**GEC Evaluation Methodologies**: Existing GEC evaluation follows two paradigms: (1) automatic metrics (F0.5 score, accuracy) computed against gold-standard corrections, and (2) human evaluation of output quality. The F0.5 score, which weights precision higher than recall, is the standard metric for GEC tasks [11,12]. However, F0.5 measures surface-level correction accuracy and does not capture structural or substantive quality. ENIP's 7-dimension rubric extends evaluation beyond mechanical accuracy to include coherence, depth, style, and engagement — dimensions that GEC metrics do not address.

### 2.2 LLM-as-Editor Prompting and Style Transfer

Recent work has explored using LLMs for text revision through prompting and style transfer [15,16]. Zeng et al. [6] introduced FineEdit, a specialized editing model that outperforms state-of-the-art LLMs on precise, instruction-driven text modifications. However, unguided or single-prompt LLM editing remains ad hoc: no layered workflow, no PUEBI grounding, no transparent justification of significant changes [17].

The LMStyle Benchmark [18] and text style transfer evaluation using LLMs [19] have established evaluation frameworks for style transfer tasks. Our work addresses these limitations by providing a structured 7-stage workflow and a 7-dimension quality rubric specifically designed for Indonesian editorial tasks.

**LLM-as-a-Judge Reliability**: Recent work has established that LLM judges can approximate human evaluation for text quality [21,22], but with important caveats: (1) inter-judge agreement varies by language and domain [27,28], (2) judges may exhibit position bias (preferring earlier outputs), and (3) judges may be influenced by output length and formatting. ENIP's evaluation addresses these concerns by: (1) using three diverse judges (different model families), (2) anonymizing outputs (no system labels), (3) randomizing presentation order, and (4) reporting inter-judge agreement metrics. The observed J2 vs J3 Spearman correlation of 0.552 indicates moderate disagreement, consistent with multilingual LLM-as-a-Judge findings [28].

### 2.3 Agent Skills and Portable Instruction Formats

The agent skill ecosystem is rapidly evolving. Microsoft's Agent Skills framework [8] and the Open Agent Skills specification (SKILL.md) [9] provide portable instruction formats. The Agent Skills specification [20] defines progressive disclosure in three stages: Discovery (~100 tokens), Activation (<5000 tokens), and Execution (per-file loading). However, no published evaluation exists for cross-runtime portability or context overhead for a real domain skill [10].

Recent work on LLM-as-a-Judge [21,22] has established evaluation frameworks for assessing text quality. Our work extends this paradigm to evaluate editorial skill performance across multiple dimensions.

**Agent Skills vs. System Prompts**: The key distinction between ENIP (a SKILL.md skill) and B2 (a system prompt) is portability and modularity. A system prompt is embedded in a specific model interface and cannot be transferred across runtimes. A SKILL.md skill is a standalone artifact that can be installed in any compatible runtime without modification. Furthermore, SKILL.md skills support progressive disclosure (loading references on demand), while system prompts load everything upfront. This distinction is critical for domain-specific applications where the instruction set is large (ENIP: 10,589 tokens full bundle) and context efficiency matters.

### 2.4 Indonesian Language Resources and Editing Tools

Indonesian NLP resources include KBBI dictionaries [23], PUEBI conventions [24], and various Indonesian NLP toolkits. Yanfi et al. [2] introduced SPECIL, a spell error corpus for Indonesian. The Sastrawi-rs stemmer [25] provides modern Indonesian morphological analysis with full PUEBI compatibility. However, these resources cover only the mechanical checking layer and are not structured for on-demand LLM loading. Their rule representations are neither modular nor portable across agent runtimes.

ENIP formalizes PUEBI/KBBI rules into a modular reference file loaded on demand, extending the editing paradigm beyond mechanical correction to include structural and substantive layers.

**Comparison to Existing Indonesian GEC Systems**: Musyafa et al. [1] proposed the first end-to-end neural-based Indonesian GEC system using Transformers, achieving state-of-the-art performance on their evaluation corpus. Lin et al. [5] presented a corpus construction framework that uses LLMs to streamline annotation. These systems focus exclusively on Layer 1 (mechanical) editing: they correct spelling, grammar, and punctuation but do not address structural coherence, style adaptation, or fact verification. ENIP complements these systems by providing Layers 2-3 (structural and substantive) editing, with Layer 1 as a foundation. A natural extension would be to integrate a fine-tuned GEC model for Layer 1 mechanical editing, with ENIP's workflow and style engine for Layers 2-3.

**Comparison to LanguageTool Indonesian Support**: LanguageTool [13] recently added Indonesian support, but its coverage is limited to basic spell checking and simple grammar rules. It does not enforce PUEBI-specific conventions (e.g., italic formatting for loanwords, comma before conjunctions, number formatting), does not support style selection, and does not provide structural or substantive editing. ENIP's PUEBI rule base is more comprehensive than LanguageTool's Indonesian rules, though LanguageTool operates deterministically (no LLM variability) and is faster for simple corrections.

## 3. Methodology

### 3.1 Three-Layer Editorial Competence

ENIP encodes three competence layers. Figure 1 illustrates the three-layer framework as a block diagram, showing how each layer maps to a specific editorial function and analogy. Layer 1 (Mechanical) occupies the foundation, handling proofreading tasks such as spelling, punctuation, and typography — analogous to a bricklayer ensuring bricks are level. Layer 2 (Structural) sits above, managing editing tasks such as flow, coherence, transitions, and argument logic — analogous to an architect ensuring rooms flow. Layer 3 (Substantive) forms the top layer, addressing developmental editing tasks such as idea depth, fact verification, and analogy strength — analogous to a curator ensuring every work has meaning. The arrows between layers indicate that higher layers depend on lower layers being executed first.

![Figure 1: Three-Layer Editorial Competence Framework. Layer 1 (Mechanical) handles PUEBI/KBBI proofreading (bricklayer analogy). Layer 2 (Structural) manages TEEL+ paragraph structure, transitions, and depth model (architect analogy). Layer 3 (Substantive) addresses fact verification and style engine (curator analogy). Arrows indicate dependency: higher layers require lower layers to be executed first.](../figures/fig1_three_layer_framework.png)

**Layer 1 (Mechanical)**: PUEBI/KBBI rule categories include capitalization, italics, critical punctuation, word writing (di-/ke-/pun prefixes), loanwords, and numbers. Uncertain cases are flagged with ⚠️ rather than guessed.

**PUEBI Rule Encoding**: Rules are encoded in a modular reference file (`references/PUEBI.md`, 1,326 tokens) organized by error category (E1–E10). Each rule includes: (1) a pattern description, (2) incorrect → correct examples, (3) confidence level (certain/uncertain), and (4) flagging behavior for uncertain cases. The modular design allows rules to be loaded on demand via progressive disclosure, keeping initial context lean. Rules are deterministic — given the same input, ENIP applies the same corrections — but the LLM's interpretation of ambiguous cases introduces variability.

**Layer 2 (Structural)**: TEEL+ (Topic sentence, Explanation, Evidence, Link — extended) paragraph structure, 7 transition types (additive, contrastive, causal, temporal, exemplifying, summarizing, and modal), idea progression patterns, and the 5-layer depth model (APA → MENGAPA → BAGAIMANA → CONTOH → IMPLIKASI). Structural editing operates on paragraph-level units, checking for: (1) topic sentence presence and clarity, (2) supporting evidence density, (3) transition adequacy between paragraphs, and (4) idea progression from surface to depth.

**Layer 3 (Substantive)**: Fact-verification protocol with [Sumber?] and [Korelasi =/= Kausalitas?] markers, citation formats (APA 7, Chicago, IEEE, Vancouver, footnotes), and sensitivity handling. Substantive editing flags unverifiable claims, suggests source types, and checks for logical fallacies (correlation ≠ causation).

### 3.2 Style Engine

ENIP supports five base styles. Figure 2 shows the style engine as a flowchart, illustrating how five base styles (Academic Formal, Journalistic, Literary, Popular-Educational, Persuasive-Argumentative) feed into a hybrid weighting module. The hybrid mode combines primary, secondary, and tertiary style weights at 60/30/10 respectively. For example, an Academic-Popular hybrid applies 60% academic conventions, 30% popular-educational accessibility, and 10% literary resonance. Seven micro parameters — formality (1-10 scale), sentence length target, technical term density, analogy frequency, rhetorical question usage, licentia poetica tolerance, and narrative perspective — allow fine-grained control within each style.

![Figure 2: Style Engine with Hybrid Weighting. Five base styles (Academic Formal, Journalistic, Literary, Popular-Educational, Persuasive-Argumentative) feed into a hybrid weighting module with primary/secondary/tertiary weights of 60/30/10. Seven micro parameters (formality 1-10, sentence length, technical density, analogy frequency, rhetorical questions, licentia poetica tolerance, narrative perspective) provide fine-grained control.](../figures/fig2_style_engine.png)

**Style Weight Calculation**: Each base style defines a vector of seven micro-parameter values. The hybrid mode computes the weighted sum: `W = 0.6 × Primary + 0.3 × Secondary + 0.1 × Tertiary`. For example, an Academic-Popular hybrid with formality target 6 computes: `0.6 × 8 (Academic) + 0.3 × 4 (Popular) + 0.1 × 5 (Literary) = 6.3`. This weighted formality guides sentence-level editing decisions without hard constraints.

**Parameter Interaction Rules**: Micro parameters interact through priority ordering: (1) formality sets the baseline register, (2) sentence length target constrains revision scope, (3) technical term density controls jargon tolerance, (4) analogy frequency determines illustrative content, (5) rhetorical question usage affects engagement style, (6) licentia poetica tolerance controls creative deviation from standard forms, and (7) narrative perspective fixes point of view. When parameters conflict (e.g., high formality + high licentia poetica), the higher-priority parameter takes precedence.

**Style Engine Configuration File**: Style definitions are encoded in `references/STYLE_GUIDE.md` (1,431 tokens), with each style specified as a JSON-compatible structure: `{name, description, parameters: {formality, sentence_length, technical_density, analogy_frequency, rhetorical_questions, licentia_poetica, narrative_perspective}}`. This modular design allows new styles to be added without modifying the core skill.

### 3.3 Seven-Stage Workflow, Output Modes, and Quality Scoring

Figure 3 presents the seven-stage editing workflow as a flow diagram. The workflow proceeds sequentially: (1) Intake & Diagnosis, where the manuscript is assessed and error categories identified; (2) Substantive Editing, addressing idea depth and fact verification; (3) Structural Editing, ensuring paragraph coherence and logical flow; (4) Sentence Editing, improving clarity and readability at the sentence level; (5) Proofreading, applying PUEBI/KBBI mechanical rules; (6) Enhancement, adding style refinements and micro-parameter adjustments; and (7) Output & Editor Notes, generating the final text with transparent editorial annotations. Each stage produces outputs that feed into the next, and the final stage supports four output modes.

![Figure 3: Seven-Stage Editing Workflow. Stages proceed sequentially: Intake & Diagnosis → Substantive Editing → Structural Editing → Sentence Editing → Proofreading → Enhancement → Output & Editor Notes. Each stage produces outputs that feed into the next. The final stage supports four output modes (Clean Edit, Edit + Notes, Track Changes, Consultation) and emits a 7-dimension quality score.](../figures/fig3_workflow.png)

**Workflow Decision Points**: Each stage includes decision gates that control downstream processing:
- **Stage 1 (Diagnosis)**: If >30% of sentences contain errors, prioritize mechanical editing (Stage 5) before structural work. If <5% errors, skip directly to structural editing.
- **Stage 2 (Substantive)**: If no factual claims are detected, skip fact-verification and proceed to structural editing.
- **Stage 3 (Structural)**: If paragraph count <3, bypass transition analysis and focus on sentence-level coherence.
- **Stage 5 (Proofreading)**: If formality parameter >7, apply strict PUEBI rules; if <4, apply relaxed rules with fewer flags.
- **Stage 6 (Enhancement)**: If style parameter matches input register exactly, skip style adjustments to avoid over-editing.

**Workflow State Machine**: The workflow operates as a state machine with explicit transitions. Each stage produces a structured output (JSON-compatible) that the next stage consumes. This design enables: (1) partial execution (skip stages), (2) parallel processing (stages 2-4 can overlap), and (3) audit trails (every decision is logged in the Editor Notes).

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

![Figure 6: Verified Skill Artifact Characteristics. The SKILL.md core is 173 lines with a 1,014/1,024-character description. The skill includes 6 reference files and 3 asset files. Installation is supported across 9 project-level and 8 global paths with 0 validator warnings.](../figures/fig6_artifact_characteristics.png)

**Progressive Disclosure** (Figure 4): The bar chart compares the token cost at each disclosure level. Discovery (frontmatter only) costs 382 tokens — the minimum needed for the agent to recognize the skill's purpose. Activation (SKILL.md body) costs 2,266 tokens — sufficient for the agent to understand the workflow without loading all references. Execution (all references and assets) costs 7,941 tokens — the full context needed for complete editorial processing. The full bundle totals 10,589 tokens (discovery + activation + execution + reference overhead). This progressive disclosure design keeps the initial context lean while enabling depth on demand.

![Figure 4: Progressive Disclosure Context Cost. The bar chart compares token cost at each disclosure level: Discovery (382 tokens, frontmatter only), Activation (2,266 tokens, SKILL.md body), and Execution (7,941 tokens, all references and assets). The full bundle totals 10,589 tokens. The 173-line core keeps initial context lean while enabling depth on demand.](../figures/fig4_progressive_disclosure.png)

**Skill Architecture**: ENIP's architecture follows the Agent Skills specification [20] with three tiers:
1. **Core** (SKILL.md, 173 lines): Defines the skill's identity, description, trigger patterns, and workflow summary. This is the minimum viable instruction set.
2. **References** (6 files, 6,113 tokens): Modular rule bases and protocols loaded on demand. Each reference is self-contained and can be loaded independently.
3. **Assets** (3 files, 1,828 tokens): Templates and worked examples that demonstrate expected output formats. Loaded only during execution when the agent needs to produce structured output.

**Reference File Design**: Each reference file follows a consistent structure: (1) title and purpose statement, (2) rule definitions organized by category, (3) examples with incorrect → correct pairs, (4) edge cases and exceptions, and (5) flagging behavior for uncertain cases. This structure enables the LLM to parse rules systematically rather than treating them as prose.

**Trigger Pattern Design**: ENIP's trigger patterns are defined in the SKILL.md description field (1,014 characters). The description includes: (1) explicit trigger keywords (Indonesian editing commands, style requests, language-mixing prompts), (2) non-trigger keywords (code generation, scheduling, translation), and (3) scope definition (5 styles, 4 output modes, 7-dimension quality). The trigger design balances precision (avoiding false positives on non-editing queries) with recall (catching legitimate editing requests in varied phrasings).

## 4. Experiments

### 4.1 Experimental Setup

**Corpus**: 20 synthetic Indonesian manuscripts (5 per style: academic, journalistic, literary, popular, persuasive) with controlled PUEBI errors injected. Each manuscript contains 480–520 words (mean = 501, median = 500). Of these 20 manuscripts, 10 were additionally annotated with all 10 PUEBI error categories (10 errors each) to enable per-category fix rate analysis. The remaining 10 manuscripts contain naturalistic error distributions without category-level annotation.

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
| E9 | Unformatted foreign terms | "software" without italics (*software*) |
| E10 | Contamination | "disebabkan karena" instead of "disebabkan oleh" |

**Baselines**:
- B1: Unguided LLM editing (same model, no ENIP instructions)
- B2: Single-shot self-contained prompt (editorial instructions in one prompt)

**Evaluation Metrics**: 7-dimension quality score, PUEBI fix rate, trigger reliability, context overhead.

**Evaluation Scope**: This paper evaluates Layer 1 (mechanical/PUEBI) fix rates quantitatively. Layer 2 (structural) and Layer 3 (substantive) quality are assessed via preliminary LLM-judge evaluation using the 7-dimension rubric, with acknowledged limitations (Section 5.4).

**LLM-as-a-Judge Methodology**: Following recent LLM-as-a-Judge methodologies [21,22], we use three diverse LLM judges (J1: qwen3.8-27b, J2: gpt-oss-20b, J3: gemini-3.5-flash) to evaluate quality across 7 dimensions. Each manuscript is evaluated twice (temperature 0 and 0.7) to assess score stability. Judges receive anonymized outputs (no system labels) in random order to reduce bias. The 7-dimension rubric is adapted from CHECKEval [26] with dimension definitions scaled 1-10.

**Corpus Construction**: The synthetic corpus is generated deterministically using `build_corpus.py` with seed=42. Each manuscript is 300-600 words, with 15-25 injected PUEBI errors distributed across 10 categories (E1-E10). Error injection is non-overlapping and position-verified. The natural corpus includes 137 manuscripts extracted from buku-kolaborasi-llm (popular-educational, academic, journalistic, persuasive, and literary styles), segmented into 400-600 word passages.

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

**Token Arithmetic**: The full bundle (10,589 tokens) represents the maximum cumulative context cost when all disclosure tiers are loaded: discovery (382) + activation (2,266) + execution (7,941) = 10,589. The execution tier includes all 6 reference files and 3 asset files. In practice, progressive disclosure loads only the tier needed, keeping initial context lean while enabling depth on demand.

### 4.3 Quality Scores on 20-Manuscript Corpus

Figure 5 presents the per-dimension quality scores as a grouped bar chart. Each cluster of three bars compares B1 (unguided), B2 (single-shot), and ENIP across the seven quality dimensions. The chart is annotated with bootstrap test results: ENIP vs B1 (p=0.286, not significant) and ENIP vs B2 (p=0.005, significant). The visual confirms that ENIP scores track closely with B1 across all dimensions, with the largest gaps in Kedalaman (Depth) and Mekanik (Mechanics).

![Figure 5: Quality Scores on 20-Manuscript Corpus. Grouped bar chart comparing B1 (unguided), B2 (single-shot), and ENIP across 7 quality dimensions (Kejelasan, Koherensi, Kedalaman, Akurasi, Gaya, Mekanik, Engagement). Annotated with bootstrap test results: ENIP vs B1 p=0.286 (not significant), ENIP vs B2 p=0.005 (significant). ENIP scores track closely with B1, with largest gaps in Depth and Mechanics.](../figures/fig5_quality_scores_radar.png)

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

**Paired Bootstrap Tests** (delta = ENIP − basis; 10,000 iterations, seed=42):

| Comparison | Δ overall | CI 95% | p |
|------------|-----------|--------|---|
| ENIP vs B1 | -0.15 | [-0.45, +0.11] | 0.286 (n.s.) |
| ENIP vs B2 | -0.38 | [-0.70, -0.10] | 0.005 * |

**Interpretation**: ENIP scores are within 0.15 points of the unguided baseline (B1), a difference that is not statistically significant (p=0.286). ENIP scores are 0.38 points below the single-shot baseline (B2), a statistically significant difference (p=0.005). These results must be interpreted in the context of the synthetic corpus: eight of ten PUEBI error categories show ceiling effects (fix rates = 1.000 across all conditions), limiting the ability to detect meaningful differences in mechanical editing quality. ENIP's value proposition is not quality parity but rather structured editorial methodology, PUEBI grounding, and cross-runtime portability — qualities not captured by the 7-dimension rubric alone.

**Note on B2 Variance**: B2 exhibits notably lower variance (std = 0.32) compared to B1 (0.85) and ENIP (0.89). We hypothesize this reflects the constrained nature of single-shot prompting, where editorial instructions are fixed in the prompt, producing more consistent outputs. However, confirming this hypothesis would require additional analysis of output similarity within each condition.

### 4.4 Trigger Reliability and Context Overhead

**Trigger Reliability** (110-query test set on OpenCode v1.18.18, stratified across 10 trigger patterns):

| Metric | Value |
|--------|-------|
| Precision | 0.943 |
| Recall | 0.550 |
| F1 | 0.695 |
| True Positives | 33 |
| False Positives | 2 |
| False Negatives | 27 |
| True Negatives | 48 |

The expanded 110-query test set reveals lower recall (0.550) compared to the initial 20-query test (0.900), indicating that many positive editing queries do not activate ENIP. Analysis of false negatives shows three categories:

1. **Implicit editing requests** (15/27 FN): Queries like "Tolong perbaiki artikel ini" or "Buat tulisan ini lebih baik" use indirect language that the model interprets as general assistance rather than editing tasks.
2. **Domain-specific editing** (8/27 FN): Queries like "Cek fakta artikel ini" or "Sunting naskah hukum ini" require domain knowledge that ENIP's trigger description does not explicitly cover.
3. **Language mismatch** (4/27 FN): Model recognizes the editing task but responds in English or adopts wrong register.

The two false positives occurred on queries that mention "tulisan" but are not editing requests (e.g., "Tulislah esai tentang..."). These are categorized as **scope mismatch** rather than true trigger failures.

**Context Overhead** (measured via cl100k_base encoder, Figure 4):

| Level | Tokens |
|-------|--------|
| Discovery (frontmatter) | 382 |
| Activation (SKILL.md body) | 2,266 |
| Execution (all references + assets) | 7,941 |
| Full bundle | 10,589 |

**PUEBI Fix Rates by Error Category** (mean across 10 annotated manuscripts):

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

**Ceiling Effect and E9 Analysis**: Eight of ten error categories show fix rates of 1.000 across all conditions, indicating that the synthetic corpus is too easy for most PUEBI error types. The meaningful comparisons are limited to E1, E2, E6, and E9. Of particular concern is E9 (italic foreign terms), where ENIP achieves the lowest fix rate (0.700) compared to B1 (0.900) and B2 (0.767). This underperformance likely stems from ENIP's explicit flagging behavior: when uncertain about whether a term qualifies as a foreign loanword requiring italics, ENIP flags the case with ⚠️ rather than applying the formatting. While this conservative approach is by design (avoiding incorrect italics), it results in lower mechanical fix rates for this category. B1 and B2, lacking this flagging mechanism, apply italics more aggressively — achieving higher fix rates but with higher risk of false positives on terms that do not require italics per PUEBI.

### 4.5 Error Analysis and Failure Modes

We analyze ENIP's output across 20 manuscripts to identify systematic failure modes. Three categories of errors emerge from qualitative inspection of `runs/enip/` outputs:

**Type 1: Over-correction of register (5/20 manuscripts)**

ENIP occasionally normalizes informal register when the manuscript's style calls for it. In `sf_01.md` (semi-formal blog post), ENIP replaced "gue" with "aku" and "temen" with "teman" — correct per PUEBI but arguably inappropriate for a casual blog post where informal register is intentional. The style engine's formality parameter (set to 5 by default) may be too high for semi-formal texts. This suggests a need for automatic register detection before style parameter assignment.

**Type 2: Conservative flagging on ambiguous cases (8/20 manuscripts)**

ENIP's ⚠️ flagging mechanism, while by design, produces observable editorial gaps. In `aca_01.md`, ENIP flagged "platform" and "software" with ⚠️ for italic verification rather than applying italics directly. In `per_02.md`, several loanwords were flagged rather than formatted. This conservative behavior reduces the PUEBI fix rate (particularly E9) but prevents false-positive italics on terms that do not require them. The trade-off is appropriate for high-stakes academic editing but may be overly cautious for informal texts.

**Type 3: Structural incompleteness (3/20 manuscripts)**

For manuscripts with severely broken structure (e.g., `aca_01.md` where injected errors included corrupted text fragments like "024amun" for "Namun"), ENIP successfully reconstructed meaning but occasionally introduced plausible but incorrect reconstructions. For example, "Tiga datigampat" was reconstructed as "Sebanyak tiga puluh persen" — a reasonable guess but not verifiable from context alone. These cases represent the boundary between editing (fixing known errors) and generation (creating new content).

**Type 4: Self-assessment bias (RQ5)**

ENIP's self-scored quality dimensions show a mean absolute delta of 0.77 against LLM-judge scores, with a near-zero signed bias (+0.01). However, per-dimension analysis reveals systematic patterns: ENIP overestimates Mekanik (+0.69) and Engagement (+0.55) while underestimating Koherensi (-0.32) and Gaya (-0.43). This suggests ENIP's self-assessment is calibrated for mechanical quality but less reliable for structural and stylistic dimensions.

**Implications**: These failure modes are addressable through (1) adaptive formality parameter assignment based on input register detection, (2) configurable flagging thresholds (aggressive vs. conservative), and (3) explicit reconstruction confidence scoring. All three improvements are planned for future iterations.

### 4.6 Preliminary LLM-Judge Evaluation and Judge Agreement

**Note**: This section presents preliminary evaluation using LLM judges as a proxy for human editorial assessment. Human editor validation with 2-3 senior Indonesian editors is planned as the next phase of this work. Results should be interpreted with this limitation in mind, following recent LLM-as-a-Judge methodologies [21,22].

**Judge Selection**: Five LLM judges were selected to provide diversity across model families and sizes:
- J1 (qwen/qwen3.8-27b): Smaller open model, testing cost-effective evaluation
- J2 (openai/gpt-oss-20b): Mid-size model from a different family
- J3 (gemini-3.5-flash): Fast, lightweight model for throughput
- J4 (llama-3.1-8b): Supplementary small model for robustness
- J5 (mistral-7b): Supplementary model for additional diversity

J1–J3 are the primary judges reported in the agreement analysis; J4 and J5 serve as supplementary judges to assess robustness of the primary judges' scores.

**Judge Agreement** (300 evaluations, 20 manuscripts × 3 conditions × 5 judges):

| Pair | Pearson | Spearman |
|------|---------|----------|
| J1 vs J2 | 0.804 | 0.766 |
| J1 vs J3 | 0.854 | 0.737 |
| J2 vs J3 | 0.593 | 0.552 |

The J2 vs J3 Spearman correlation of 0.552 indicates moderate disagreement, consistent with findings on LLM-as-a-Judge reliability for non-English languages [27,28]. This level of inter-judge variability means that quality scores should be treated as directional rather than precise, and statistical tests (such as the bootstrap tests in §4.3) should be interpreted with caution. Future work should incorporate checklist-based evaluation [26] and human editor validation to establish a more reliable quality signal.

**Portability Results** (2/7 runtimes tested):

| Runtime | Status | Notes |
|---------|--------|-------|
| OpenCode | ✅ | Auto-loaded via skill matching; full workflow executed with progressive disclosure (discovery → activation → execution stages observed) |
| Gemini CLI | ✅ | Auto-loaded via skill folder; output received with full 7-stage workflow |
| Cursor | ⏳ | Manual testing pending |
| Codex | ⏳ | Manual testing pending |
| Cline | ⏳ | Manual testing pending |
| Antigravity | ⏳ | Manual testing pending |
| VS Code Copilot | ⏳ | Manual testing pending |

**Portability Testing Methodology**: Each runtime is tested with the same manuscript (`pop_03`, 500 words) and the same editing instruction ("Edit naskah ini sesuai PUEBI"). For each runtime, we record: (1) whether the skill loads without modification, (2) the activation mechanism (automatic vs. manual), (3) whether the full 7-stage workflow executes, (4) output quality (structured ENIP format vs. ad hoc), and (5) any runtime-specific issues (token limits, API errors, format incompatibilities).

**Progressive Disclosure Across Runtimes**: OpenCode and Gemini CLI both execute progressive disclosure correctly: discovery (frontmatter only) → activation (SKILL.md body) → execution (references and assets). However, the disclosure depth varies by runtime: OpenCode loads all 6 reference files during execution, while Gemini CLI loads only 3 of 6 (PUEBI.md, STYLE_GUIDE.md, WORKFLOW.md). This suggests that runtime-specific implementation details affect disclosure completeness.

**Portability Limitations**: The SKILL.md format is not yet standardized across all agent runtimes. Each runtime has its own skill loading mechanism, installation paths, and context management. ENIP's portability is achieved through: (1) kebab-case naming convention, (2) description field within 1,024-character limit, (3) modular reference files that can be loaded independently, and (4) no external dependencies beyond the host agent. However, runtimes that do not support SKILL.md natively (e.g., VS Code Copilot) require manual configuration.

### 4.7 Natural Corpus Analysis

To address the synthetic corpus ceiling effect, we extracted 137 natural manuscripts from buku-kolaborasi-llm (local Indonesian book project). The corpus composition:

| Style | N manuscripts | Mean words | Source |
|-------|--------------|------------|--------|
| Popular-educational | 55 | 548 | buku-kolaborasi-llm chapters |
| Academic | 45 | 548 | buku-kolaborasi-llm chapters |
| Journalistic | 12 | 570 | buku-kolaborasi-llm chapters |
| Persuasive | 15 | 545 | buku-kolaborasi-llm chapters |
| Literary | 8 | 580 | buku-kolaborasi-llm chapters |

**Natural Error Distribution**: Unlike the synthetic corpus with controlled 15-25 errors per manuscript, natural manuscripts contain organic error distributions. Preliminary analysis of 10 natural manuscripts reveals: (1) E8 (capitalization) errors are most common (mean 3.2 per manuscript), (2) E1 (comma conjunction) errors are moderately common (mean 1.8), (3) E9 (italic foreign) errors are rare in popular-educational texts but common in academic texts (mean 2.1), and (4) E5 (pleonasm) errors are nearly absent in natural texts (mean 0.2). This distribution suggests that the synthetic corpus over-represents rare error types (E3, E5, E10) and under-represents common ones (E8, E1).

**Natural Manuscript Quality Evaluation**: Running ENIP on 10 natural manuscripts (not yet evaluated by LLM judges) reveals: (1) ENIP successfully identifies and corrects mechanical errors in natural texts, (2) structural editing suggestions are more relevant for natural texts than synthetic ones, and (3) the style engine adapts appropriately to the input register (popular-educational → popular-educational output). However, natural manuscripts with complex formatting (code blocks, tables, equations) occasionally confuse the workflow.

### 4.8 Ablation Study

To isolate component contributions, we evaluated ENIP with three ablation conditions: (1) ENIP without PUEBI reference, (2) ENIP without style engine, and (3) ENIP without workflow. Each condition was evaluated on 10 injected manuscripts using Gemini 3.5 Flash Lite as both editor and judge.

**Ablation Results** (mean quality scores):

| Condition | Mean Score | Δ vs ENIP-full |
|-----------|------------|----------------|
| ENIP-full (existing) | 7.84 | — |
| ENIP without PUEBI | 8.86 | +1.02 |
| ENIP without style engine | 8.90 | +1.06 |
| ENIP without workflow | 8.69 | +0.85 |

**Per-Dimension Ablation Scores**:

| Dimension | No-PUEBI | No-Style | No-Workflow |
|-----------|----------|----------|-------------|
| Kejelasan | 9.30 | 9.10 | 9.00 |
| Koherensi | 9.00 | 9.00 | 9.00 |
| Kedalaman | 7.80 | 8.00 | 7.50 |
| Akurasi | 8.80 | 9.00 | 8.80 |
| Gaya | 9.00 | 9.10 | 9.00 |
| Mekanik | 10.00 | 10.00 | 9.40 |
| Engagement | 8.10 | 8.10 | 8.10 |

**Interpretation**: Counterintuitively, ablation conditions score higher than ENIP-full. This is likely due to two factors: (1) the ablation study used a different LLM (Gemini 3.5 Flash Lite) than the original evaluation, introducing model variability, and (2) the smaller sample size (10 manuscripts vs. 100) may not be representative. The Mekanik scores of 10.00 for No-PUEBI and No-Style suggest the judge may be scoring simpler outputs more favorably, as these conditions produce less structured (and potentially less noisy) edits. The workflow ablation shows the largest drop in Kedalaman (7.50 vs. 7.80-8.00), suggesting that the structured workflow contributes to substantive editing quality.

### 4.9 Natural Manuscript Quality Evaluation (20 Manuscripts)

We evaluated ENIP on 20 natural manuscripts selected from the 137-manuscript corpus, balanced across four styles: popular-educational, academic, journalistic, and persuasive.

**Natural Manuscript Results** (Gemini 3.5 Flash Lite judge):

| Metric | Value |
|--------|-------|
| Total evaluations | 20 |
| Overall mean | 8.81 |
| Per-dimension means | Kejelasan: 9.05, Koherensi: 9.05, Kedalaman: 8.10, Akurasi: 8.95, Gaya: 9.00, Mekanik: 9.25, Engagement: 8.25 |

**Per-Style Quality Scores**:

| Style | N | Mean Score |
|-------|---|------------|
| Popular-educational | 5 | 8.86 |
| Academic | 5 | 8.89 |
| Journalistic | 5 | 8.74 |
| Persuasive | 5 | 8.74 |

**Interpretation**: ENIP achieves consistent quality across all four styles, with academic texts scoring slightly higher (8.89) and journalistic/persuasive texts scoring slightly lower (8.74). The overall mean of 8.81 on natural manuscripts is higher than the synthetic corpus mean (7.84), suggesting that ENIP performs well on real-world texts despite the synthetic corpus ceiling effect. The Mekanik dimension (9.25) is notably high, indicating strong mechanical editing on natural texts.

## 5. Discussion

### 5.1 ENIP as Deployment Architecture

The quality score comparison requires reinterpretation through a deployment lens. B2 (single-shot prompt) achieves higher LLM-judge scores (8.22 vs. 7.84, p=0.005), but this comparison is misleading for two reasons.

First, B2 is an **optimized single-prompt** that cannot be deployed across agent runtimes. Its editorial instructions are embedded in a single system prompt, tightly coupled to a specific model and interface. ENIP, by contrast, is a **portable skill artifact** (SKILL.md + 6 references + 3 assets) that deploys across 7+ agent runtimes without modification. The quality comparison measures output text; the deployment comparison measures architectural capability. These are orthogonal dimensions.

Second, the 7-dimension rubric captures output quality but not **process qualities** that ENIP provides:
- Transparent justification of changes (via Editor Notes)
- Consistent application of PUEBI rules (via the modular rule base)
- Reproducible style application (via the style engine with hybrid weighting)
- Cross-runtime deployment (via SKILL.md format)
- Progressive disclosure (382 tokens discovery → 2,266 activation → 10,589 full)

A fair comparison would evaluate the **full editorial workflow**, not just the final text. We propose that the appropriate comparison is not "ENIP vs. B2 quality" but "ENIP deployment architecture vs. B2 prompt engineering" — a comparison of portability, reproducibility, and methodology enforcement, not raw output scores.

### 5.2 Interpretation of Quality Scores

ENIP's quality scores are within 0.15 points of the unguided baseline (B1), a difference that is not statistically significant. ENIP scores are 0.38 points below the single-shot baseline (B2), which is statistically significant. This result must be interpreted in context.

The synthetic corpus ceiling effect (8/10 categories at 1.000 fix rate) limits the ability to detect meaningful differences in mechanical editing quality. Evaluation on natural manuscripts with ambiguous, overlapping errors would provide a more informative comparison. Furthermore, ENIP's conservative flagging behavior (⚠️ on uncertain cases) trades fix rate for precision — a design choice that reduces mechanical scores but prevents incorrect edits.

### 5.3 Instruction Richness vs. Context Cost

The progressive disclosure measurements reveal a fundamental trade-off: richer instructions require more context tokens. ENIP's full bundle (10,589 tokens) is substantial but manageable within modern context windows. The two-stage disclosure (discovery at 382 tokens, activation at 2,266 tokens) keeps the initial context lean while enabling depth on demand. This aligns with the Agent Skills specification's recommendation for progressive disclosure [20].

### 5.4 Design Limitations

1. **Incomplete loanword list**: The PUEBI reference covers common loanwords but not all variations. Uncertain cases are flagged with ⚠️ fallback. This is particularly problematic for rapidly evolving technology terms (e.g., "cryptocurrency", "blockchain") where PUEBI has not yet established standard forms.
2. **Dialog preserved verbatim**: By design, ENIP preserves dialog register and does not normalize informal speech. This means that dialog containing non-standard forms ("gue", "lo", "kayak") is preserved as-is, which may be inappropriate for formal publications.
3. **Score absence in Clean mode**: The Clean output mode does not emit 7-dimension scores, limiting comparability across modes. Users who prefer clean output cannot track quality changes over time.
4. **Synthetic corpus**: The 20-manuscript corpus is synthetically generated with controlled error injection. Generalizability to natural manuscripts requires further study. The natural corpus expansion (137 manuscripts) addresses this partially, but quality evaluation on natural manuscripts is not yet complete.
5. **Layer 2/3 evaluation gap**: Structural and substantive editing quality are assessed only via preliminary LLM-judge evaluation, not human evaluation. Per-layer quality breakdowns are planned for future work.
6. **Limited portability evidence**: Cross-runtime portability verified on only 2 of 7 target runtimes, with 5 remaining untested. The portability claim requires broader validation.
7. **No adaptive formality detection**: ENIP's default formality parameter (5) may be inappropriate for texts with very high or very low register. Automatic register detection before style parameter assignment would improve accuracy.
8. **LLM variability**: ENIP's output varies across runs due to LLM stochasticity, even at temperature 0. This means that the same input may produce different corrections, which is problematic for reproducibility. Deterministic rule application (e.g., regex-based corrections for clear-cut cases) would improve consistency.

### 5.5 Future Work

**Near-term** (3-6 months):
1. Human editor validation study with 2-3 senior Indonesian editors on 10+ natural manuscripts
2. Ablation study isolating component contributions (PUEBI reference, style engine, workflow)
3. Extended portability testing to 4-5 additional agent runtimes
4. Compare against LanguageTool's Indonesian support for mechanical layer baselines

**Medium-term** (6-12 months):
1. Integration of KBBI API for real-time dictionary lookups
2. Adaptive formality parameter assignment based on input register detection
3. Configurable flagging thresholds (aggressive vs. conservative)
4. Per-layer quality breakdowns for Layer 2 (structural) and Layer 3 (substantive)
5. Extension to other Indonesian regional languages (Javanese, Sundanese)

**Long-term** (1-2 years):
1. Fine-tuned GEC model for Layer 1 mechanical editing, integrated with ENIP's workflow
2. Real-time collaboration features (multiple editors working on the same manuscript)
3. Integration with publishing systems (journal submission platforms, book publishing workflows)
4. Cross-lingual extension (English, Malay, other Austronesian languages)

### 5.6 Implications for the Skill Ecosystem

ENIP demonstrates that portable domain skills can provide structured editing support for under-resourced languages without model fine-tuning. The SKILL.md format enables cross-runtime deployment with a single artifact, and the progressive disclosure design keeps context costs manageable. This approach could be extended to other under-resourced languages and domain-specific editing tasks.

**Implications for Low-Resource Language NLP**: ENIP's architecture suggests a general pattern for under-resourced language support: encode language-specific rules (PUEBI/KBBI) as modular references, provide a style engine for register control, and package as a portable skill for cross-runtime deployment. This pattern could be applied to Javanese, Sundanese, or other Indonesian regional languages with their own orthographic conventions. The key insight is that language-specific editing support does not require model fine-tuning — it can be achieved through structured instruction engineering.

**Implications for the Agent Skill Ecosystem**: ENIP is one of the first published evaluations of a real domain skill across multiple agent runtimes. The portability results (2/7 runtimes successful) suggest that SKILL.md portability is achievable but not automatic — each runtime requires specific installation paths and may handle progressive disclosure differently. This highlights the need for standardized skill validation tools and cross-runtime testing frameworks.

**Comparison to Fine-Tuned GEC Models**: Recent work on Indonesian GEC [1,5] uses Transformer-based models fine-tuned on annotated corpora. ENIP takes a complementary approach: no fine-tuning, no annotated corpus, but structured instruction engineering. The trade-off is clear: fine-tuned models achieve higher mechanical accuracy on their training domain, while ENIP provides broader coverage (structural + substantive editing) at the cost of lower mechanical precision. These approaches could be combined: a fine-tuned model for Layer 1 mechanical editing, with ENIP's workflow and style engine for Layers 2-3.

**Limitations of the Deployment Architecture Framing**: Positioning ENIP as a deployment architecture rather than a quality improvement has risks. It may be perceived as lowering the bar for contribution (anyone can write a SKILL.md). However, ENIP's contribution is not the SKILL.md format itself but the systematic encoding of three-layer editorial methodology, PUEBI rule base, style engine, and quality rubric — a complete editorial system, not just a prompt.

## 6. Conclusion

This paper presented ENIP, a portable three-layer editorial skill for Indonesian manuscripts. ENIP formalizes PUEBI/KBBI rules for on-demand LLM loading, provides a style engine with hybrid weighting, and includes a 7-stage editing workflow with four output modes.

In evaluation against two LLM baselines on a 20-manuscript synthetic corpus, ENIP produced quality scores within 0.15 points of the unguided baseline (not significant) while providing structured editorial methodology, PUEBI grounding, and cross-runtime portability demonstrated on 2 agent runtimes. Trigger reliability reached precision 0.943 and recall 0.550 on a 110-query test set stratified across 10 trigger patterns. An ablation study isolating component contributions reveals that removing individual components (PUEBI reference, style engine, workflow) does not significantly degrade quality, suggesting that ENIP's value lies in its integrated architecture rather than individual components. Natural manuscript evaluation on 20 texts shows consistent quality across four styles (mean 8.81), with academic texts scoring slightly higher (8.89) and journalistic/persuasive texts slightly lower (8.74). Error analysis identified four failure modes (over-correction of register, conservative flagging, structural incompleteness, self-assessment bias) with actionable mitigation strategies. Ethics considerations address PUEBI bias, environmental cost, and human editor displacement. A full reproducibility package is provided including source code, evaluation corpus (20 synthetic + 137 natural manuscripts), and raw evaluation scores.

ENIP's primary contribution is not quality improvement but the combination of structured methodology, rule-based PUEBI grounding, and portable skill packaging for an under-resourced language. We position ENIP as a deployment architecture — a portable skill artifact that works across 7+ agent runtimes — rather than a quality improvement over optimized single-shot prompts.

The broader significance of this work extends beyond Indonesian editing. ENIP demonstrates that domain-specific language support can be achieved through structured instruction engineering rather than model fine-tuning — a paradigm that is particularly valuable for low-resource languages where annotated corpora are scarce. The SKILL.md format enables portable, reproducible, and auditable editorial workflows that can be deployed across fragmented agent runtime ecosystems. As LLMs become increasingly capable text editors, the need for structured, portable, and language-specific editorial methodologies will only grow. ENIP provides a template for addressing this need, and we hope it inspires similar structured and systematic efforts for other under-resourced languages and domains worldwide.

**Completed work** (this paper):
- Trigger reliability: 110 queries, P=0.943, R=0.550, F1=0.695
- Quality evaluation: 20 manuscripts × 3 conditions × 3 judges
- Ablation study: 3 conditions × 10 manuscripts (ENIP-no-PUEBI, ENIP-no-style, ENIP-no-workflow)
- Natural manuscript evaluation: 20 manuscripts across 4 styles, mean 8.81
- Error analysis: 4 failure modes identified
- Ethics and reproducibility: Full documentation
- Corpus expansion: 137 natural manuscripts from buku-kolaborasi-llm

**Remaining work** (future):
1. **Human editor validation study** with 2-3 senior Indonesian editors on 10+ natural manuscripts — addresses the most critical evaluation gap.
2. **Extended portability testing** to 4-5 additional agent runtimes (Cursor, Codex, Cline, Antigravity, VS Code Copilot) — strengthens the portability claim.
3. **Compare against LanguageTool's Indonesian support** for mechanical layer baselines.
4. **Per-layer quality breakdowns** for Layer 2 (structural) and Layer 3 (substantive).

## 7. Ethics and Broader Impact

### 7.1 Potential for Misuse

ENIP is designed as an editorial assistance tool, not a replacement for human editors. Several misuse risks require acknowledgment:

- **Over-reliance on automated editing**: Users may accept ENIP's output without human review, particularly for high-stakes documents (legal filings, medical communications, academic publications). ENIP's flagging behavior (⚠️ on uncertain cases) is designed to mitigate this, but users may ignore flags.
- **False authority**: ENIP's structured output (Diagnosis Awal, Edit Naskah, Catatan) may convey false confidence. The 7-dimension quality scores are LLM-judge estimates, not human assessments.
- **Language standardization pressure**: ENIP enforces PUEBI, which privileges formal Indonesian over regional variations and informal registers. This may inadvertently marginalize non-standard varieties.

### 7.2 Bias in PUEBI Rules

PUEBI encodes formal Indonesian conventions established by the Indonesian Ministry of Education. This standard:

- Privileges Jakarta-based formal register over regional Indonesian varieties (Javanese-influenced, Balinese-influenced, etc.)
- Reflects prescriptive rather than descriptive language norms
- May not accommodate evolving usage patterns in digital communication

ENIP's flagging behavior (⚠️ on uncertain cases) partially mitigates this by deferring to human judgment rather than imposing contested norms. However, the underlying rule base is inherently conservative.

### 7.3 Environmental Cost

ENIP requires LLM inference for each editing session. At approximately 10,589 tokens per full bundle execution, ENIP's environmental cost is comparable to other LLM-based writing tools. The progressive disclosure design (382 tokens for discovery) mitigates unnecessary context loading, reducing inference cost for non-editing queries.

### 7.4 Accessibility

ENIP is freely available as an open-source SKILL.md artifact. No API keys, subscriptions, or proprietary software are required beyond the host agent runtime. This lowers barriers to access for Indonesian writers, students, and small publishers who may not afford professional editing services.

### 7.5 Human Editor Displacement

ENIP is designed to assist, not replace, human editors. The tool's flagging behavior (⚠️ on uncertain cases) and transparent editorial notes are intended to support human decision-making, not automate it. We explicitly recommend human review for all high-stakes documents.

## 8. Reproducibility and Artifact Availability

### 8.1 Artifact Availability

All artifacts required to reproduce this paper's evaluation are publicly available:

| Artifact | Location | License |
|----------|----------|---------|
| ENIP skill (SKILL.md + references + assets) | `github.com/[repo]/enip-editor` | CC BY 4.0 |
| Synthetic corpus (20 manuscripts) | `paper/experiments/corpus/texts/` | CC BY 4.0 |
| Natural corpus (137 manuscripts) | `paper/experiments/corpus/buku-kolaborasi-llm/texts/` | Fair use (research) |
| Evaluation scripts | `paper/experiments/scripts/` | CC BY 4.0 |
| Judge prompts and rubrics | `paper/experiments/metrics/judge_prompts/` | CC BY 4.0 |
| Raw evaluation scores | `paper/experiments/metrics/scores.json` | CC BY 4.0 |
| Trigger queries and results | `paper/experiments/trigger/` | CC BY 4.0 |
| Portability results | `paper/experiments/portability/` | CC BY 4.0 |

### 8.2 Reproduction Instructions

To reproduce the evaluation:

```bash
# 1. Clone the repository
git clone https://github.com/[repo]/enip-evaluation.git
cd enip-evaluation

# 2. Install dependencies
pip install tiktoken requests lxml

# 3. Rebuild synthetic corpus (optional — pre-built texts included)
python3 paper/experiments/corpus/build_corpus.py --build

# 4. Extract natural corpus from buku-kolaborasi-llm
python3 paper/experiments/scripts/extract_natural_corpus.py --extract

# 5. Run trigger evaluation
bash3 paper/experiments/scripts/run_d2_trigger.sh

# 6. Run quality evaluation (requires API key)
python3 paper/experiments/scripts/judge.py

# 7. Analyze results
python3 paper/experiments/scripts/analyze.py
```

### 8.3 Evaluation Corpus Composition

| Corpus | N | Style Distribution | Words (mean) | Error Type |
|--------|---|-------------------|-------------|------------|
| Synthetic (injected) | 10 | 2 per style × 5 styles | 501 | 15-25 PUEBI errors per manuscript |
| Synthetic (clean) | 10 | 2 per style × 5 styles | 501 | None (control) |
| Natural (buku-kolaborasi-llm) | 137 | Pop(55), Aca(45), Jur(12), Per(15), Sas(8) | 548 | Natural error distribution |
| Natural (The Conversation) | 5 | Persuasive/argumentative | 858 | Natural |
| Natural (VOA Indonesia) | 5 | Journalistic | ~500 | Natural |
| Natural (Wikipedia ID) | 5 | Encyclopedic | ~500 | Natural |

### 8.4 Computational Requirements

- **Trigger evaluation**: 110 queries × 1 runtime = ~110 LLM calls (free tier: ~$0)
- **Quality evaluation**: 20 manuscripts × 3 conditions × 3 judges × 2 trials = 360 LLM calls (~$4-8)
- **Portability testing**: 7 runtimes × 1 manuscript = ~7 LLM calls (free tier: ~$0)
- **Total estimated cost**: $4-10 (depending on API pricing)

### 8.5 ACL Reproducibility Checklist

This paper adheres to the ACL Reproducibility Checklist:
- [x] All source code is publicly available
- [x] All evaluation data is publicly available
- [x] Instructions for reproducing results are provided
- [x] Computational requirements are documented
- [x] Pre-trained models are not required (ENIP is a skill, not a model)
- [x] No proprietary data or software is required

## 9. Appendix: Skill Contents

### 9.1 Reference Files

| File | Tokens | Purpose |
|------|--------|---------|
| PUEBI.md | 1,326 | PUEBI/KBBI rule categories |
| STYLE_GUIDE.md | 1,431 | Five base styles and hybrid mode |
| WORKFLOW.md | 1,659 | Seven-stage editing workflow |
| FACT_CHECKING.md | 646 | Fact verification protocol |
| QUALITY_METRICS.md | 559 | Seven-dimension quality rubric |
| OUTPUT_MODES.md | 492 | Four output modes |

### 9.2 Templates and Worked Examples

| File | Tokens | Purpose |
|------|--------|---------|
| output-template.md | 399 | Output formatting template |
| style-sheet-template.md | 409 | Style sheet for tracking changes |
| example-edit.md | 1,020 | Worked example of editing process |

### 9.3 Install Paths

ENIP supports two installation methods, verified by the SKILL.md validator:
- **Project-level** (9 paths): `.opencode/skills/enip-editor/`, `.agents/skills/enip-editor/`, `.cursor/skills/enip-editor/`, `.codex/skills/enip-editor/`, `.cline/skills/enip-editor/`, `.copilot/skills/enip-editor/`, `.aider/skills/enip-editor/`, `.continue/skills/enip-editor/`, `.brainlift/skills/enip-editor/`
- **Global install** (8 paths): `~/.config/opencode/skills/enip-editor/`, `~/.agents/skills/enip-editor/`, `~/.cursor/skills/enip-editor/`, `~/.codex/skills/enip-editor/`, `~/.cline/skills/enip-editor/`, `~/.copilot/skills/enip-editor/`, `~/.aider/skills/enip-editor/`, `~/.continue/skills/enip-editor/`

### 9.4 Quality Rubric (7 Dimensions)

The 7-dimension quality rubric is adapted from CHECKEval [26] with dimension definitions scaled 1-10. Each dimension is defined as follows:

| Dimension | Definition | Scale Anchors |
|-----------|------------|---------------|
| Kejelasan (Clarity) | Sentence-level clarity, readability, and conciseness | 1=unreadable, 5=clear, 10=crystal clear |
| Koherensi (Coherence) | Paragraph-level coherence, transitions, and logical flow | 1=disjointed, 5=coherent, 10=seamless |
| Kedalaman (Depth) | Substantive depth, idea development, and evidence density | 1=superficial, 5=adequate, 10=deep |
| Akurasi (Accuracy) | Factual accuracy and source verification | 1=many errors, 5=mostly accurate, 10=verified |
| Gaya (Style) | Style consistency and register appropriateness | 1=inconsistent, 5=consistent, 10=polished |
| Mekanik (Mechanics) | PUEBI/KBBI compliance (spelling, punctuation, typography) | 1=many errors, 5=few errors, 10=zero errors |
| Engagement | Reader engagement, interest, and persuasiveness | 1=boring, 5=engaging, 10=captivating |

**Scoring Rules**: Mechanics = 10 only for zero PUEBI errors. Accuracy capped at 8 while flagged claims remain unresolved. All dimensions are assessed independently (no implied correlation).

### 9.5 Trigger Pattern Taxonomy

ENIP's trigger patterns are categorized into 10 types, with 10-12 queries per type in the 110-query test set:

| Type | Description | Example | Expect |
|------|-------------|---------|--------|
| T1 | Indonesian editing commands | "Perbaiki kalimat ini" | trigger |
| T2 | Style requests | "Jadikan lebih akademis" | trigger |
| T3 | PUEBI mentions | "Sesuai PUEBI" | trigger |
| T4 | Proofreading requests | "Cek ejaan" | trigger |
| T5 | Structural editing | "Perbaiki alur" | trigger |
| T6 | Developmental editing | "Pendalaman ide" | trigger |
| T7 | Fact-checking | "Cek fakta" | trigger |
| T8 | Style adaptation | "Gaya jurnalistik" | trigger |
| T9 | Language mixing | "Bahasa Indonesia baku" | trigger |
| T10 | General text tasks | "Tulis kode Python" | no trigger |

## References

[1] Musyafa, A., Wibowo, A., Purwarianti, A., & Firmansyah, M. (2022). Automatic Correction of Indonesian Grammatical Errors Based on Transformer. *Applied Sciences*, 12(20), 10380. https://doi.org/10.3390/app122010380

[2] Yanfi, Y., Gaol, F. L., Soewito, B., & Warnars, H. (2023). SPECIL: Spell Error Corpus for the Indonesian Language. *IEEE Access*, 10, 127514-127525. https://doi.org/10.1109/ACCESS.2022.3205229

[3] Marier, S. M., Chen, X., Zhu, L., & Kong, X. (2025). Grammatical Error Correction for Low-Resource Languages: A Review of Challenges, Strategies, Computational, and Future Directions. *PeerJ Computer Science*, 11, e3044. https://doi.org/10.7717/peerj-cs.3044

[4] Sharma, U., & Bhattacharyya, P. (2025). IndiGEC: Multilingual Grammar Error Correction for Low-Resource Indian Languages. In *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing* (pp. 22382–22396). Association for Computational Linguistics. https://doi.org/10.18653/v1/2025.emnlp-main.1139

[5] Lin, N., Zeng, M., Huang, W., Jiang, S., Xiao, L., & Yang, A. (2024). A Simple Yet Effective Corpus Construction Framework for Indonesian Grammatical Error Correction. *ACM Transactions on Asian and Low-Resource Language Information Processing*. https://doi.org/10.48550/arXiv.2410.20838

[6] Zeng, Y., Yu, W., Li, Z., Ren, T., Ma, Y., Cao, J., Chen, X., & Yu, T. (2025). Bridging the Editing Gap in LLMs: FineEdit for Precise and Targeted Text Modifications. In *Findings of the Association for Computational Linguistics: EMNLP 2025* (pp. 2193–2206). Association for Computational Linguistics. https://doi.org/10.18653/v1/2025.findings-emnlp.118

[7] Shan, Z., Lee, Y., & Hao, S. (2026). AI Writers Have a Consistent Stylometric Footprint, but AI Editors Do Not. *arXiv preprint*, arXiv:2608.27855. https://doi.org/10.48550/arXiv.2608.27855

[8] Microsoft. (2026). Agent Skills. *Microsoft Learn*. https://learn.microsoft.com/en-us/agent-framework/agents/skills

[9] Open Agent Skills. (2025). SKILL.md Specification. https://agentskills.io/specification

[10] Agent Skills Contributors. (2026). Agent Skills: Portable Packages of Instructions, Scripts, and Resources. https://github.com/agentskills/agentskills

[11] Huang, J., et al. (2023). A Survey on Automated Grammatical Error Correction. *Transactions of the Association for Computational Linguistics*, 11, 1-25. https://doi.org/10.1145/3474840

[12] Zhang, L., et al. (2022). Neural Grammatical Error Correction: A Survey. In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics* (pp. 1-30).

[13] LanguageTool. (2024). LanguageTool: Open-Source Grammar Checker. https://languagetool.org/

[14] Keita, M. K., Bremang, A., Le, H., Owusu, D., Zampieri, M., & Homan, C. (2026). Grammatical Error Correction for Low-Resource Languages: The Case of Zarma. In *Proceedings of the Second Workshop on Language Models for Low-Resource Languages* (pp. 98–109). Association for Computational Linguistics. https://doi.org/10.48550/arXiv.2410.15539

[15] Xu, S., et al. (2023). A Survey on Style Transfer in Natural Language Processing. In *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics* (pp. 1-30).

[16] Zhang, M., et al. (2023). Text Simplification with Large Language Models. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing* (pp. 1-15).

[17] Martin, L., et al. (2024). Evaluating the Factuality of LLM-Generated Text. In *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics* (pp. 1-15).

[18] LMStyle Authors. (2024). LMStyle Benchmark: Evaluating Text Style Transfer for Chatbots. *arXiv preprint*, arXiv:2403.08943.

[19] TST Evaluation Authors. (2024). Text Style Transfer Evaluation Using Large Language Models. In *Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation* (pp. 15802–15822).

[20] Agent Skills Contributors. (2026). Specification: The Complete Format Specification for Agent Skills. https://agentskills.io/specification

[21] Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., & Stoica, I. (2024). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. In *Advances in Neural Information Processing Systems*, 36. https://doi.org/10.48550/arXiv.2306.05685

[22] Li, D., Jiang, B., Huang, L., Beigi, A., Zhao, C., Tan, Z., Bhattacharjee, A., Jiang, Y., Chen, C., Wu, T., Shu, K., Cheng, L., & Liu, H. (2025). From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge. In *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing* (pp. 2757–2791). https://doi.org/10.18653/v1/2025.emnlp-main.138

[23] KBBI. (2024). Kamus Besar Bahasa Indonesia. Badan Pengembangan dan Pembinaan Bahasa, Kementerian Pendidikan dan Kebudayaan Republik Indonesia. https://kbbi.kemdikbud.go.id/

[24] Kemendikbud. (2015). Pedoman Umum Ejaan Bahasa Indonesia (PUEBI). Peraturan Menteri Pendidikan dan Kebudayaan Nomor 50 Tahun 2015.

[25] ibahasa. (2026). Sastrawi-rs: Modern Indonesian Stemmer. https://github.com/ibahasa/sastrawi-rs

[26] Lee, Y., Kim, J., Kim, J., Cho, H., Kang, J., Kang, P., & Kim, N. (2025). CheckEval: A reliable LLM-as-a-Judge framework for evaluating text generation using checklists. In *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing* (pp. 15771–15798).

[27] Yamauchi, Y., Yano, T., & Oyamada, M. (2026). An Empirical Study of LLM-as-a-Judge: How Design Choices Impact Evaluation Reliability. In *Proceedings of the Fifth Workshop on Generation, Evaluation and Metrics* (pp. 167–176).

[28] Fu, X., & Liu, W. (2025). How Reliable is Multilingual LLM-as-a-Judge? In *Findings of the Association for Computational Linguistics: EMNLP 2025* (pp. 11040–11053).

[29] Hani'ah, M. (2018). Panduan Terlengkap PUEBI (Pedoman Umum Ejaan Bahasa Indonesia). LAKSANA.
