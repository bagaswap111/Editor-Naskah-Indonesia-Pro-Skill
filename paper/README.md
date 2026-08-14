# Paper ENIP — Workspace & Status Pipeline

Workspace untuk makalah "ENIP: A Portable Layered Editing Skill for
Indonesian Manuscripts", dijalankan mengikuti pipeline
**PaperOrchestra** (Song et al., arXiv:2604.05018) versi skill pack.

## Status pipeline

| Step | Artefak | Status |
|---|---|---|
| Pre-flight | validasi input, densitas, konsistensi | ✅ LULUS (4/4 gates) |
| **1. Outline** | `outline.json` | ✅ LULUS (validate_outline.py) |
| 2. Plotting | `figures/*` | ⏸️ belum (paralel, butuh host+matplotlib/PaperBanana) |
| 3. Lit Review | `drafts/intro_relwork.tex`, `refs.bib` | ⏸️ belum (~20–30 pencarian, web + Semantic Scholar) |
| 3.5 Reconcile | `outline_reconciled.json` | ⏸️ menunggu Step 3 |
| 4. Section Writing | `drafts/paper.tex` | ⏸️ belum (1 call multimodal) |
| 5. Refinement | `refinement/` | ⏸️ belum (3 iterasi, halt rules) |
| Final | `final/paper.tex` + `.pdf` | ⏸️ belum (butuh template + latexmk) |

## Apa yang dikupas dalam paper (inti outline)

1. **Formalisasi 3-lapis kompetensi editorial** (Mekanik/Struktural/
   Substantif) untuk Bahasa Indonesia — adaptasi IELTS Band 9 (TEEL+,
   kohesi-koherensi) + Model Kedalaman 5 lapis.
2. **Style engine** — 5 gaya + hybrid 60/30/10 + 7 parameter mikro;
   diklaim sebagai formalisasi pertama untuk Bahasa Indonesia.
3. **Basis aturan PUEBI yang dapat dimuat on-demand LLM** —
   representasi modular `references/PUEBI.md` dengan kebijakan ⚠️
   (tidak menebak).
4. **Portabilitas lintas-agent** — satu SKILL.md, 9 jalur project + 8
   global via `install.sh`, pengukuran karakteristik artefak
   (173 baris inti, description 1014/1024) dan rencana uji 8 runtime.
5. **Protokol evaluasi 7 dimensi + desain validasi manusia** — untuk
   mengatasi self-assessment bias; eksperimen formal vs 3 baseline
   (B1 LLM polos, B2 prompt sekali, B3 mekanik).

## Aturan data (jujur/anti-halusinasi)

- `inputs/experimental_log.md` membedakan **[SUDAH DIVERIFIKASI]**
  (karakteristik artefak, skor diri worked examples) vs
  **[DI-RENCANAKAN]** (eksperimen formal, portabilitas, evaluasi
  manusia) — TBD diisi saat eksperimen dijalankan.
- Semua angka di paper final WAJIB grounded ke log ini
  (`claim_evidence_gate.py` memeriksanya di Step 5).
- Anti-leakage prompt (App. D.4) diterapkan: makalah anonim, dibangun
  hanya dari input workspace ini.

## Reproduksi

```bash
# 1. setup tooling (sekali)
python3 -m venv paper/tools/.venv
paper/tools/.venv/bin/pip install jsonschema

# 2. pre-flight (gate wajib sebelum Step 1)
paper/tools/.venv/bin/python paper/tools/paper-orchestra-scripts/validate_inputs.py --workspace paper/
paper/tools/.venv/bin/python paper/tools/paper-orchestra-scripts/check_idea_density.py --idea paper/inputs/idea.md --log paper/inputs/experimental_log.md
paper/tools/.venv/bin/python paper/tools/paper-orchestra-scripts/validate_consistency.py --idea paper/inputs/idea.md --log paper/inputs/experimental_log.md

# 3. validasi outline
paper/tools/.venv/bin/python paper/tools/outline-scripts/validate_outline.py paper/outline.json
```

## Input yang masih perlu dilengkapi user

- `inputs/figures/` — opsional; kosong ⇒ plotting agent yang buat.
- **Eksperimen nyata** (isi TBD di experimental_log.md): korpus 20
  naskah uji, skor 3 baseline, uji trigger 20 query, pengukuran token,
  validasi 2–3 editor manusia.
- Konfirmasi target venue & deadline (placeholder: ACL-style,
  deadline 2026-10-01, cutoff lit-review 2026-09-01).

## Referensi pipeline

- Prompt verbatim outline: `tools/prompt.md` (App. F.1)
- Anti-leakage: `tools/anti-leakage-prompt.md` (App. D.4)
- Sumber skill pack: PaperOrchestra (Song et al., 2026, arXiv:2604.05018)