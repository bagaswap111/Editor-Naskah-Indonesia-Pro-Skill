# ENIP — Editor Naskah Indonesia Pro

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

## Struktur Repo

```
├── konsep/                     # dokumen konsep sumber (ide + rancangan)
├── skill/
│   └── enip-editor/            # SKILL KANONIK (portable, sumber kebenaran)
│       ├── SKILL.md            #   inti: identitas, parameter, alur, aturan
│       ├── references/         #   detail yang dimuat on-demand:
│       │   ├── PUEBI.md        #     mekanik: ejaan, tata bahasa, diksi
│       │   ├── STYLE_GUIDE.md  #     style engine: 5 gaya + hybrid + mikro
│       │   ├── WORKFLOW.md     #     7 tahap, TEEL+, transisi, kasus khusus
│       │   ├── FACT_CHECKING.md#     verifikasi fakta + format referensi
│       │   ├── QUALITY_METRICS.md #  skor kualitas 7 dimensi
│       │   └── OUTPUT_MODES.md #     4 mode output
│       └── assets/             #   template & contoh
│           ├── output-template.md
│           ├── example-edit.md
│           └── style-sheet-template.md
├── prompts/
│   └── system-prompt.md        # versi self-contained (tempel manual)
├── scripts/
│   └── install.sh              # installer lintas platform
└── konsep/                     # (lihat atas)
```

## Instalasi

Format SKILL.md sama di semua agent; hanya jalur penyimpanannya yang
berbeda. Dua cara:

### 1. Script installer (macOS/Linux, direkomendasikan)

```bash
./scripts/install.sh            # project-level: .claude, .cursor, .agents, dst.
./scripts/install.sh --global   # user-level: ~/.claude/skills, dst.
./scripts/install.sh --copy     # salin file (jika symlink tidak didukung)
./scripts/install.sh --help     # bantuan
```

Script memasang sekaligus ke semua platform di bawah ini.

### 2. Salin manual

Salin folder `skill/enip-editor/` ke jalur agent Anda yang dipakai:

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
| Agent lain (Roo, Continue, Windsurf, Kiro, Qwen Code, dst.) | instal via `npx skills add <repo>` (Vercel skills CLI) atau salin ke direktori skills tool terkait |  |

**Tanpa skill loader sama sekali** (ChatGPT, Claude.ai, Google AI Studio,
API biasa): tempel isi `prompts/system-prompt.md` sebagai instruksi awal —
versi self-contained, tanpa dependensi file.

## Cara Pakai

Setelah terpasang, ajukan permintaan dalam bahasa apa pun — contoh:

- "Sunting naskah ini: gaya jurnalistik, formalitas 7. [naskah]"
- "Perbaiki bahasa Indonesianya, mode Track Changes. [naskah]"
- "Jadikan lebih akademis dengan referensi APA. [naskah skripsi]"
- "Edit sesuai PUEBI, lalu kasih skor kualitas. [naskah]"

ENIP akan bertanya parameter yang belum Anda tentukan (gaya, mode output,
dll.), lalu menjalankan 7 tahap editing dan menampilkan: Diagnosis Awal →
Naskah Hasil Editan → Catatan Editor → Style Sheet → Skor Kualitas →
Saran Pengembangan.

### Iterasi

Output pertama bisa di-iterasi: "mendalami bagian X dengan analogi",
"memperketat argumen paragraf Y", "turunkan formalitas ke 4", "ganti mode
Konsultasi".

## Penyesuaian

- **Ubah aturan bahasa**: edit `skill/enip-editor/references/PUEBI.md`
  (mis. jika Anda lebih suka EYD V, perbarui judul dan contohnya).
- **Tambah gaya**: ikuti pola di `references/STYLE_GUIDE.md`.
- **Ubah standar output**: edit `assets/output-template.md`.

Setelah mengubah file di `skill/enip-editor/`, jalankan ulang
`./scripts/install.sh --copy` (mode copy) atau tanpa apa-apa (mode
symlink, karena perubahan langsung tertaut).

## Lisensi

MIT — lihat `LICENSE`. Konten konsep (folder `konsep/`) adalah bahan
sumber proyek ini.