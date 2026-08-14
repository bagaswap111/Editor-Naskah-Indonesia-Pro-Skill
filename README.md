# ENIP — Editor Naskah Indonesia Pro

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Validate SKILL.md](https://github.com/bagaswap111/Editor-Naskah-Indonesia-Pro/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/bagaswap111/Editor-Naskah-Indonesia-Pro/actions/workflows/validate-skills.yml)

**ENIP (Editor Naskah Indonesia Pro)** is a senior Indonesian-language
editing skill for AI agents. It is not a spell-checker — it is a full
editorial workflow in three layers: **mechanical proofreading** (PUEBI &
KBBI), **structural editing** (flow, coherence, transitions), and
**developmental editing** (depth of ideas, factual accuracy).

Built on the open **Agent Skills (SKILL.md)** format — one portable skill
that runs natively in 25+ agents without rewriting anything.

## Features

- **5 writing styles**: Academic Formal, Journalistic, Literary (Sastrawi),
  Popular-Educational, Persuasive-Argumentative + **hybrid mode**
  (60/30/10 weighting) + micro parameters (formality 1–10, sentence length,
  analogy frequency, technical density).
- **IELTS Band 9 structure adapted to Indonesian**: TEEL+ paragraphs,
  7 transition types, 5-layer depth model, analogy & example techniques
  (including local cultural analogies).
- **4 output modes**: Clean Edit, Edit + Notes, Track Changes, Consultation.
- **7-dimension quality score**: Clarity, Coherence, Depth, Accuracy,
  Style, Mechanics, Engagement.
- **Fact-verification protocol**: `[Sumber?]`, `[Korelasi ≠ Kausalitas?]`
  markers; APA 7 / Chicago / IEEE / Vancouver / footnote citation formats.
- **Progressive disclosure**: lean core `SKILL.md`; details in
  `references/` load only when needed.
- **Preserves the author's voice**: clarify, never rewrite.

## Try it

Every output follows the same structure:

```
1. Early Diagnosis (2–3 sentences)
2. Edited Manuscript (per output mode)
3. Editor's Notes (significant changes + reasons)
4. Style Sheet (term/spelling decisions)
5. Quality Score (7 dimensions, 1–10)
6. Development Suggestions (optional)
```

> **Before:** "Inflasi itu kayak harga barang naik terus. Jadi uang kita
> nilainya turun. Ini bahaya buat ekonomi."
> **After:** a structured academic-popular paragraph: definition →
> mechanism (*demand-pull* / *cost-push*) → impact → policy response, with
> the "glass of water" analogy and citations.
> Full before/after: [`examples/inflasi-akademis-populer.md`](examples/inflasi-akademis-populer.md)

## Install

The `SKILL.md` format is identical everywhere — only the install path
differs. Pick one:

### Via `npx skills add` (recommended)

```bash
npx skills add bagaswap111/Editor-Naskah-Indonesia-Pro
```

### Clone + installer script (macOS/Linux)

```bash
git clone https://github.com/bagaswap111/Editor-Naskah-Indonesia-Pro.git
cd Editor-Naskah-Indonesia-Pro
./scripts/install.sh              # project-level (symlink into every agent dir)
./scripts/install.sh --global     # user-level (~/.claude/skills, etc.)
./scripts/install.sh --copy       # copy instead of symlink (Windows/Git Bash)
```

### Manual copy

Copy `skill/enip-editor/` into your agent's skills directory:

| Agent | Project path | User/global path |
|---|---|---|
| Claude Code | `.claude/skills/enip-editor/` | `~/.claude/skills/enip-editor/` |
| Cursor 2.4+ | `.cursor/skills/enip-editor/` (or `.agents/skills/`) | `~/.cursor/skills/` |
| OpenAI Codex | `.agents/skills/enip-editor/` | per Codex docs |
| Cline | `.cline/skills/`, `.clinerules/skills/`, or `.claude/skills/` | `~/.cline/skills/` |
| Gemini CLI | `.gemini/skills/enip-editor/` (or `.agents/skills/`) | `~/.gemini/skills/` |
| OpenCode | `.opencode/skills/enip-editor/` | `~/.config/opencode/skills/` |
| Google Antigravity | `.agent/skills/enip-editor/` | per docs |
| VS Code (GitHub Copilot) | per Copilot Agent Skills docs | per docs |
| Anything else | use `npx skills add` or copy into the tool's skills dir | varies |

### No skill loader at all (ChatGPT, Claude.ai, Google AI Studio, plain APIs)

Paste the contents of [`prompts/system-prompt.md`](prompts/system-prompt.md)
as your first message — it is a self-contained system prompt with zero file
dependencies.

## Usage

Ask in any language; ENIP asks for missing session parameters (style,
output mode, target audience), then runs its 7-stage workflow:

- "Edit this text: journalistic style, formality 7. \<text\>"
- "Perbaiki bahasa Indonesianya, mode Track Changes. \<naskah\>"
- "Make it more academic with APA references. \<thesis draft\>"
- "Sunting sesuai PUEBI lalu beri skor kualitas. \<naskah\>"

Iterate after the first pass: "deepen section X with an analogy",
"tighten the argument in paragraph Y", "lower formality to 4".

## Repository layout

```
├── skill/enip-editor/          # CANONICAL SKILL (portable, source of truth)
│   ├── SKILL.md                #   core: identity, session params, 7 stages, rules
│   ├── references/             #   loaded on demand
│   │   ├── PUEBI.md            #     mechanics: spelling, grammar, diction
│   │   ├── STYLE_GUIDE.md      #     style engine: 5 styles + hybrid + micro
│   │   ├── WORKFLOW.md         #     7 stages, TEEL+, transitions, special cases
│   │   ├── FACT_CHECKING.md    #     fact verification + citation formats
│   │   ├── QUALITY_METRICS.md  #     7-dimension scoring
│   │   └── OUTPUT_MODES.md     #     4 output modes
│   └── assets/                 #   templates & examples
├── examples/                   # real before/after editing results
├── prompts/system-prompt.md    # self-contained prompt (no skill loader)
├── scripts/                    # install + validate tooling
├── docs/MARKETPLACES.md        # marketplace submission checklist
├── konsep/                     # original concept documents (Indonesian)
└── .github/                    # CI validation + issue/PR templates
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Validate your changes locally:

```bash
bash scripts/validate.sh
```

## Marketplaces

ENIP is listed in the marketplaces below (see
[docs/MARKETPLACES.md](docs/MARKETPLACES.md) for the full checklist):

- [ ] agentskills.io — Open Agent Skills showcase
- [ ] GuildSkills
- [ ] skills.sh
- [ ] `npx skills add` compatible

## License

[MIT](LICENSE). Concept documents in `konsep/` are the source material of
this project.