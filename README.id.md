# ENIP — Editor Naskah Indonesia Pro

Bahasa Inggris: [README.md](README.md) · Bahasa Indonesia: README ini

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Validate SKILL.md](https://github.com/bagaswap111/Editor-Naskah-Indonesia-Pro/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/bagaswap111/Editor-Naskah-Indonesia-Pro/actions/workflows/validate-skills.yml)

Skill AI editor Bahasa Indonesia yang menjalankan workflow editorial
3 lapis: **proofreading mekanik** (PUEBI & KBBI), **editing struktural**
(alur, koherensi, transisi), dan **developmental editing** (kedalaman ide,
akurasi fakta) — berdasarkan konsep di `konsep/` (ide.md dan rancangan.md).

Satu sumber skill (`skill/enip-editor/`) yang berjalan di banyak agent
tanpa ditulis ulang, karena menggunakan **format SKILL.md standar terbuka
(Open Agent Skills)** — dibaca native oleh 25+ agent di pasar.

## Fitur

- **5 gaya bahasa**: Akademis Formal, Jurnalistik Informatif, Naratif
  Sastrawi, Populer-Edukatif, Persuasif-Argumentatif + mode hybrid
  (bobot 60/30/10) + parameter mikro (formalitas, panjang kalimat, dll.).
- **Struktur IELTS Band 9 yang diadaptasi**: TEEL+, 7 jenis transisi,
  Model Kedalaman Berlapis 5 lapis, teknik analogi & contoh.
- **4 mode output**: Clean Edit, Edit + Catatan, Track Changes, Konsultasi.
- **Skor kualitas 7 dimensi** (Kejelasan, Koherensi, Kedalaman, Akurasi,
  Gaya, Mekanik, Engagement).
- **Protokol verifikasi fakta**: penanda `[Sumber?]`, `[Korelasi ≠
  Kausalitas?]`, format referensi APA 7/Chicago/IEEE/Vancouver/catatan kaki.
- **Progressive disclosure**: SKILL.md inti ringkas; detail di
  `references/` dibaca hanya saat dibutuhkan.

## Instalasi

Format SKILL.md sama di semua agent; hanya jalur penyimpanannya yang
berbeda. Tiga cara:

### 1. Via `npx skills add`

```bash
npx skills add bagaswap111/Editor-Naskah-Indonesia-Pro
```

### 2. Script installer (macOS/Linux)

```bash
./scripts/install.sh            # project-level: .claude, .cursor, .agents, dst.
./scripts/install.sh --global   # user-level: ~/.claude/skills, dst.
./scripts/install.sh --copy     # salin file (jika symlink tidak didukung)
./scripts/install.sh --help     # bantuan
```

### 3. Salin manual

Salin folder `skill/enip-editor/` ke jalur agent yang dipakai:

| Agent | Jalur project | Jalur user/global |
|---|---|---|
| Claude Code | `.claude/skills/enip-editor/` | `~/.claude/skills/enip-editor/` |
| Cursor (2.4+) | `.cursor/skills/enip-editor/` atau `.agents/skills/enip-editor/` | `~/.cursor/skills/enip-editor/` |
| OpenAI Codex | `.agents/skills/enip-editor/` | sesuai docs Codex |
| Cline | `.cline/skills/`, `.clinerules/skills/`, atau `.claude/skills/` | `~/.cline/skills/` |
| Gemini CLI | `.gemini/skills/enip-editor/` atau `.agents/skills/` | `~/.gemini/skills/` |
| OpenCode | `.opencode/skills/enip-editor/` | `~/.config/opencode/skills/` |
| Google Antigravity | `.agent/skills/enip-editor/` | sesuai docs |
| VS Code (GitHub Copilot) | sesuai docs Copilot Agent Skills | sesuai docs |
| Agent lain (Roo, Continue, Windsurf, Kiro, Qwen Code, dst.) | `npx skills add` atau salin ke direktori skills tool terkait | bervariasi |

**Tanpa skill loader sama sekali** (ChatGPT, Claude.ai, Google AI Studio,
API biasa): tempel isi `prompts/system-prompt.md` sebagai instruksi awal —
versi self-contained, tanpa dependensi file.

## Cara Pakai

Ajukan permintaan dalam bahasa apa pun — ENIP akan menanyakan parameter
yang belum Anda tentukan (gaya, mode output, dll.), lalu menjalankan
7 tahap editing:

- "Sunting naskah ini: gaya jurnalistik, formalitas 7. [naskah]"
- "Perbaiki bahasa Indonesianya, mode Track Changes. [naskah]"
- "Jadikan lebih akademis dengan referensi APA. [naskah skripsi]"
- "Edit sesuai PUEBI, lalu kasih skor kualitas. [naskah]"

Output: Diagnosis Awal → Naskah Hasil Editan → Catatan Editor → Style
Sheet → Skor Kualitas → Saran Pengembangan. Bisa di-iterasi ("mendalami
bagian X dengan analogi", "memperketat argumen paragraf Y", "turunkan
formalitas ke 4").

## Struktur Repo

```
├── skill/enip-editor/            # SKILL KANONIK (portable)
│   ├── SKILL.md                  #   inti: identitas, parameter, alur, aturan
│   ├── references/               #   detail on-demand (PUEBI, gaya, workflow, dsb.)
│   └── assets/                   #   template & contoh
├── examples/                     # hasil edit before/after nyata
├── prompts/system-prompt.md      # versi self-contained
├── scripts/                      # install.sh + validate.sh
├── docs/MARKETPLACES.md          # checklist submit marketplace
├── konsep/                       # dokumen konsep sumber
└── .github/                      # CI validasi + template issue/PR
```

## Kontribusi

Lihat [CONTRIBUTING.md](CONTRIBUTING.md). Validasi lokal sebelum PR:

```bash
bash scripts/validate.sh
```

## Marketplace

ENIP kompatibel dengan direktori skill utama (checklist lengkap di
[docs/MARKETPLACES.md](docs/MARKETPLACES.md)):

- [ ] agentskills.io — showcase Open Agent Skills
- [ ] GuildSkills
- [ ] skills.sh
- [ ] kompatibel `npx skills add`

## Lisensi

[MIT](LICENSE). Dokumen konsep di `konsep/` adalah bahan sumber proyek ini.