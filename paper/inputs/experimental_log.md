# Experimental Log — ENIP Paper

*Catatan: log ini membedakan [SUDAH DIVERIFIKASI] (angka terukur dari
artefak saat pengembangan) dan [DI-RENCANAKAN] (protokol yang dirancang
untuk paper final, belum dijalankan). Aturan PaperOrchestra: tidak ada
angka yang boleh dikarang.*

## 1. Experimental Setup

- **Objek studi**: skill `enip-editor` v2.0 (SKILL.md, 6 files
  references, 3 files assets, install.sh, validate.sh). Repo:
  Editor-Naskah-Indonesia-Pro.
- **Bahasa target**: Bahasa Indonesia (PUEBI/KBBI).
- **Runtimes uji portabilitas (plan)**: Claude Code, Cursor 2.4+,
  OpenAI Codex, Cline, Gemini CLI, OpenCode, Google Antigravity,
  VS Code Copilot. Metrik: skill dimuat tanpa modifikasi (ya/tidak),
  jalur instalasi, mekanisme aktivasi.
- **Baselines (direncanakan)**:
  - B1: LLM tanpa skill (prompt polos "perbaiki naskah ini").
  - B2: LLM + prompt satu-kali (system prompt self-contained ENIP tanpa
    progressive disclosure).
  - B3: alat koreksi mekanik non-LLM (grammar/spell checker PUEBI).
- **Evaluation metrics**:
  - **Skor kualitas 7 dimensi** (1–10): Kejelasan, Koherensi, Kedalaman,
    Akurasi, Gaya, Mekanik, Engagement — rubrik di references
    QUALITY_METRICS.md.
  - **Agreement editor manusia** [DI-RENCANAKAN]: 2–3 editor senior
    memberi skor pada subset naskah; metrik: mean abs. delta vs skor
    ENIP, Cohen's kappa antar editor.
  - **Trigger reliability** [DI-RENCANAKAN]: 20 query (10 harus
    memicu, 10 tidak boleh) => presisi/re-call aktivasi skill.
  - **Context overhead** [DI-RENCANAKAN]: token discovery (name +
    description) vs token aktivasi (body) vs token eksekusi
    (references yang dibaca).
  - **PUEBI error rate** [DI-RENCANAKAN]: # kesalahan mekanik tersisa
    di output ENIP vs baseline, per 1.000 kata (korpus naskah uji).
- **Implementation details**: skill murni instruksi (tanpa kode);
  evaluasi dijalankan oleh host agent masing-masing runtime; jumlah
  naskah uji target 20 (5/gaya) + 3 studi kasus yang sudah ada.

## 2. Raw Numeric Data

### 2.1 Karakteristik artefak skill [SUDAH DIVERIFIKASI]

| Metrik | Nilai |
|---|---|
| Baris SKILL.md inti | 173 |
| Panjang description (karakter) | 1014 (maks 1024) |
| Jumlah file references | 6 |
| Jumlah file assets | 3 |
| Jalur instalasi project (install.sh) | 9 |
| Jalur instalasi global (install.sh) | 8 |
| Peringatan validator saat pengembangan | 0 |

### 2.2 Worked examples (skor dilaporkan oleh ENIP sendiri) [DIVERIFIKASI sebagai laporan diri — bukan validasi eksternal]

| Dimensi | Contoh 1 (Akademis+Populer) | Contoh 2 (Jurnalistik) | Contoh 3 (Sastrawi) |
|---|---|---|---|
| Kejelasan | 9 | — (mode Clean tanpa skor) | 8 |
| Koherensi | 9 | — | 9 |
| Kedalaman | 8 | — | 9 |
| Akurasi | 8 | — | 10 |
| Gaya | 9 | — | 10 |
| Mekanik | 10 | — | 10 |
| Engagement | 8 | — | 9 |

### 2.3 Hasil eksperimen formal terhadap baselines [DI-RENCANAKAN — belum dijalankan]

| Metrik | ENIP | B1 (LLM polos) | B2 (prompt sekali) | B3 (mekanik) |
|---|---|---|---|---|
| Skor 7 dimensi rata-rata (dari editor manusia) | TBD | TBD | TBD | TBD |
| PUEBI error rate /1000 kata | TBD | TBD | TBD | TBD |
| Coverage lapisan (mekanik/struktural/substantif) | TBD | TBD | TBD | TBD |
| Waktu penyuntingan per naskah (menit) | TBD | TBD | TBD | TBD |

### 2.4 Trigger reliability [DI-RENCANAKAN]

| Set | Jumlah query | Presisi target | Re-call target |
|---|---|---|---|
| Harus memicu (10) | 10 | ≥0.9 | — |
| Tidak boleh memicu (10) | 10 | — | ≥0.9 |

### 2.5 Context overhead [DI-RENCANAKAN]

| Level disclosure | Token estimasi |
|---|---|
| Discovery (frontmatter) | ~100 |
| Aktivasi (body SKILL.md) | <5000 |
| Eksekusi (references termuat on-demand) | per-file |

## 3. Qualitative Observations [SUDAH DIVERIFIKASI — faktual dari pengembangan]

- Skill murni instruksi berhasil dijalankan di OpenCode tanpa kode
  tambahan; semua penalaran dilakukan host agent.
- Symlink instalasi awalnya ter-commit ke git dan mengandung path
  absolut; masalah portabilitas ini ditemukan saat persiapan publikasi
  dan diperbaiki (symlink dikeluarkan dari tracking; .gitignore
  menambahkan direktori instalasi).
- Validator menangkap pelanggaran format (nama folder vs name, panjang
  description >1024) sebelum CI diaktifkan; skor ini mendukung klaim
  bahwa pemeriksaan deterministik diperlukan di samping instruksi.
- Mode output yang berbeda mengubah struktur jawaban secara signifikan;
  hasil mode Clean tidak menyertakan skor, sehingga laporan skor 7
  dimensi hanya tersedia pada mode Edit+Catatan.
- Keterbatasan desain teridentifikasi: skor kualitas dilaporkan oleh
  model yang sama yang menyunting (self-assessment bias); dialog fiksi
  tidak diedit (keputusan desain); daftar kata serapan belum lengkap —
  kasus di luar tabel ditandai ⚠️ alih-alih ditebak.