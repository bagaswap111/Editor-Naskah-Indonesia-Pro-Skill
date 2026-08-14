# Changelog

Semua perubahan penting dicatat di sini. Format mengikuti
[Keep a Changelog](https://keepachangelog.com/) dan versi mengikuti
[SemVer](https://semver.org/).

## [0.1.0] - 2026-08-14

### Added

- Skill portabel `enip-editor` (format Open Agent Skills / SKILL.md):
  - Inti SKILL.md: identitas ENIP v2.0, parameter sesi, alur 7 tahap,
    aturan mutlak, format output, penanganan ketidakpastian.
  - `references/`: PUEBI.md (mekanik & tata bahasa), STYLE_GUIDE.md
    (5 gaya + hybrid + parameter mikro), WORKFLOW.md (7 tahap, TEEL+,
    transisi, kedalaman berlapis, kasus khusus), FACT_CHECKING.md,
    QUALITY_METRICS.md, OUTPUT_MODES.md.
  - `assets/`: output-template.md, style-sheet-template.md, example-edit.md.
- Prompt self-contained (`prompts/system-prompt.md`) untuk platform tanpa
  skill loader.
- Installer lintas platform (`scripts/install.sh`) untuk 9 jalur agent.
- Validator SKILL.md (`scripts/validate.sh`) + GitHub Actions
  (`validate-skills.yml`).
- 3 contoh before/after nyata di `examples/`.
- Checklist submit marketplace (`docs/MARKETPLACES.md`).
- README.md (Inggris), README.id.md (Indonesia), CONTRIBUTING.md,
  template issue/PR, banner sosial, lisensi MIT.

[0.1.0]: https://github.com/bagaswap111/Editor-Naskah-Indonesia-Pro/releases/tag/v0.1.0