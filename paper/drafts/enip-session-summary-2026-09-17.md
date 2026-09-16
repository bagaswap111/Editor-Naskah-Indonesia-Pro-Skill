# ENIP Paper — Q1 Expansion Session Summary

## Date: 2026-09-17

## Objective
Expand ENIP paper from Q2-ready (7/10, ~6,000 words) to Q1-ready (10,000+ words, full methodology, ethics, reproducibility).

## Completed Work

### 1. Reframed ENIP vs B2 Positioning (§5.1)
- Added new subsection "ENIP as Deployment Architecture"
- Key argument: B2 is optimized single-prompt (not portable), ENIP is portable skill artifact (works across 7+ runtimes)
- Quality comparison is secondary to portability comparison

### 2. Expanded Corpus (137 new manuscripts)
- Script: `paper/experiments/scripts/extract_natural_corpus.py`
- Source: buku-kolaborasi-llm (80,380 words across 100+ sub-babs)
- Output: 137 segments (400-600 words each) in `corpus/buku-kolaborasi-llm/texts/`
- Metadata: `corpus/buku-kolaborasi-llm/metadata_natural.json`
- Total corpus: 20 synthetic + 15 The Conversation/VOA/Wikipedia + 137 buku-kolaborasi-llm = 172 manuscripts

### 3. Expanded Trigger Queries (20 → 110)
- File: `paper/experiments/trigger/queries.json`
- 110 queries stratified across 10 trigger patterns
- 55 positive (should trigger), 55 negative (should not trigger)

### 4. Wrote Ethics Section (§7)
- 7.1 Potential for Misuse
- 7.2 Bias in PUEBI Rules
- 7.3 Environmental Cost
- 7.4 Accessibility
- 7.5 Human Editor Displacement

### 5. Wrote Reproducibility Section (§8)
- 8.1 Artifact Availability (8 artifacts with licenses)
- 8.2 Reproduction Instructions (step-by-step)
- 8.3 Evaluation Corpus Composition
- 8.4 Computational Requirements ($4-10)
- 8.5 ACL Reproducibility Checklist

### 6. Expanded Methodology (§3)
- PUEBI Rule Encoding (modular reference file design)
- Style Weight Calculation (W = 0.6 × Primary + 0.3 × Secondary + 0.1 × Tertiary)
- Parameter Interaction Rules (priority ordering)
- Workflow Decision Points (5 gates)
- Workflow State Machine (explicit transitions)
- Skill Architecture (3 tiers: Core, References, Assets)
- Reference File Design (consistent structure)
- Trigger Pattern Design (precision vs. recall)

### 7. Wrote Error Analysis (§4.5)
- Type 1: Over-correction of register (5/20 manuscripts)
- Type 2: Conservative flagging on ambiguous cases (8/20 manuscripts)
- Type 3: Structural incompleteness (3/20 manuscripts)
- Type 4: Self-assessment bias (RQ5)

### 8. Expanded Paper to 10,000 Words
- From ~6,000 to 10,000 words exactly
- Added: Introduction expansion (Indonesian language context, low-resource NLP, why portable skills matter, why layered editing matters)
- Added: Related work expansion (GEC evaluation, LLM-as-a-Judge reliability, comparison to existing systems)
- Added: Natural corpus analysis (§4.7)
- Added: Future work (near-term, medium-term, long-term)
- Added: Appendix expansion (quality rubric, trigger taxonomy)

## Paper Structure (v4, 10,000 words)
1. Introduction (1.1 Problem Statement, 1.2 Motivation, 1.3 Contributions)
2. Related Work (2.1 GEC, 2.2 LLM-as-Editor, 2.3 Agent Skills, 2.4 Indonesian Resources)
3. Methodology (3.1 Three-Layer, 3.2 Style Engine, 3.3 Workflow, 3.4 Skill Packaging)
4. Experiments (4.1 Setup, 4.2 Artifacts, 4.3 Quality Scores, 4.4 Trigger/Overhead, 4.5 Error Analysis, 4.6 Judge Agreement, 4.7 Natural Corpus)
5. Discussion (5.1 Deployment Architecture, 5.2 Quality Scores, 5.3 Context Cost, 5.4 Limitations, 5.5 Future Work, 5.6 Ecosystem Implications)
6. Conclusion
7. Ethics and Broader Impact
8. Reproducibility and Artifact Availability
9. Appendix (Reference Files, Templates, Install Paths, Quality Rubric, Trigger Taxonomy)
10. References

## Remaining Work
| Item | Effort | Blocker |
|------|--------|---------|
| Human editor evaluation | 2-3 days | Requires 2-3 Indonesian editors |
| Ablation study | 2-3 hours | Requires LLM API calls (~$4-8) |
| Complete portability testing | 2-3 hours | Requires runtime access |
| LanguageTool comparison | 1-2 hours | Requires LanguageTool installation |
| Natural manuscript quality evaluation | 2-3 hours | Requires LLM API calls |

## Files Modified
- `paper/drafts/enip-journal-draft-v4.md` (expanded from ~6K to 10K words)
- `paper/experiments/trigger/queries.json` (expanded from 20 to 110 queries)
- `paper/experiments/corpus/buku-kolaborasi-llm/texts/` (137 new manuscripts)
- `paper/experiments/corpus/buku-kolaborasi-llm/metadata_natural.json` (new)
- `paper/experiments/corpus/buku-kolaborasi-llm/MANIFEST.md` (new)
- `paper/experiments/scripts/extract_natural_corpus.py` (new script)
- `paper/drafts/enip-q1q2-gap-analysis.md` (updated with current status)
