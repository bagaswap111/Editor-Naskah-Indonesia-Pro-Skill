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
- **Runtimes uji portabilitas**: Claude Code (belum login), Cursor 2.4+
  (manual), OpenAI Codex (manual), Cline (manual), Gemini CLI ✅,
  OpenCode ✅, Google Antigravity (manual), VS Code Copilot (manual).
  Metrik: skill dimuat tanpa modifikasi (ya/tidak), jalur instalasi,
  mekanisme aktivasi.
- **Baselines**:
  - B1: LLM tanpa skill (prompt polos "perbaiki naskah ini").
  - B2: LLM + prompt satu-kali (system prompt self-contained ENIP tanpa
    progressive disclosure).
  - B3: hunspell id-ID (LanguageTool tidak mendukung bahasa Indonesia).
- **Evaluation metrics**:
  - **Skor kualitas 7 dimensi** (1–10): Kejelasan, Koherensi, Kedalaman,
    Akurasi, Gaya, Mekanik, Engagement — rubrik di references
    QUALITY_METRICS.md.
  - **Trigger reliability**: 20 query (10 harus memicu, 10 tidak boleh)
    => presisi/re-call aktivasi skill. ✅ precision=1.0, recall=0.9.
  - **Context overhead**: token discovery vs aktivasi vs eksekusi. ✅
    382 / 2.266 / 7.941 token.
  - **PUEBI error rate**: fix rate terhadap error terinjeksi per 1.000
    kata. ✅ ENIP 0.9681, B1 0.9774, B2 0.9769.
- **Implementation details**: skill murni instruksi (tanpa kode);
  evaluasi dijalankan oleh host agent masing-masing runtime; 20 naskah
  sintetis (5/gaya) dengan injeksi error PUEBI (deterministik, seed
  tetap).

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

### 2.3 Hasil eksperimen formal terhadap baselines [SUDAH DIVERIFIKASI — 2026-08-29]

Status 2026-08-29: Fase A–D sebagian besar selesai. Korpus 20 sintetis
(v2 bersih, bug offset diperbaiki). B3 = hunspell id-ID (LanguageTool
tidak mendukung bahasa Indonesia). B1/B2/ENIP di-re-run dengan
gpt-oss-120b via Groq API. Judge C2: 236/300 (J1=56/120, J2=120/120✅,
J3=60/60✅) — J1 diblokir TPD rolling Groq (loop hidup).

| Metrik | ENIP | B1 (LLM polos) | B2 (prompt sekali) | B3 (mekanik) |
|---|---|---|---|---|
| Skor 7 dimensi rata-rata (judge LLM) | 7.95 ± 0.72 | 8.01 ± 0.84 | 8.22 ± 0.32 | — |
| PUEBI fix rate (terhadap error terinjeksi) | 0.9681 | 0.9774 | 0.9769 | — |
| Coverage lapisan (mekanik/struktural/substantif) | TBD | TBD | TBD | TBD |
| Waktu penyuntingan per naskah (menit) | TBD | TBD | TBD | TBD |

Catatan:
- B3 (hunspell) tidak menghasilkan teks baru → hanya baseline deteksi.
- Skor judge = rata-rata 7 dimensi (Kejelasan, Koherensi, Kedalaman,
  Akurasi, Gaya, Mekanik, Engagement) dari 3 juri (J1, J2, J3),
  2 trial per item (temperature 0 & 0.7).
- PUEBI fix rate = max(0, 1 - kemunculan_pola_out /
  kemunculan_pola_input), dihitung di badan naskah hasil edit.
- ENIP unggul tipis vs B1 di Akurasi (+0.18) & Mekanik (+0.05);
  tertinggal di Koherensi (-0.27) & Kedalaman (-0.24).
- ENIP vs B2: selisih signifikan (p=0.024), terutama Koherensi &
  Kedalaman.

Referensi data: `paper/experiments/metrics/puebi_report.md`,
`metrics/analysis_report.md`, `metrics/overhead.json`, `runs/b3/`.

### 2.4 Trigger reliability [SUDAH DIVERIFIKASI — 2026-08-25]

Dieksekusi di OpenCode v1.18.18 (model mimo-v2.5-free). Kriteria
aktivasi: peran editor diadopsi / deklarasi eksplisit skill / kosakata
khas SKILL.md.

| Metrik | Nilai |
|---|---|
| Precision (memicu benar / memicu total) | 1.0 |
| Recall (memicu benar / harus memicu) | 0.9 |
| True Positive | 9 |
| False Negative | 1 (trig_05: "Jadikan teks ini lebih akademis dan formal") |
| True Negative | 10 |
| False Positive | 0 |

Catatan:
- trig_05 (FN): model menjawab dalam bahasa Inggris secara generik,
  persona editor tidak muncul.
- Semua TN benar tidak memicu skill (kode, belanja, jadwal, dll.).
- Log mentah: `trigger/logs/trig_NN.out`

### 2.5 Context overhead [SUDAH DIVERIFIKASI — 2026-08-23]

Token diukur via tiktoken (cl100k_base). Progressive disclosure: hanya
frontmatter yang ter-petakan di discovery.

| Level disclosure | Token |
|---|---|
| Discovery (frontmatter: name + description) | 382 |
| Aktivasi (body SKILL.md) | 2.266 |
| Eksekusi (semua references + assets) | 7.941 |
| Full bundle (semua file) | 10.589 |

Rincian eksekusi:
- references/FACT_CHECKING.md: 646
- references/OUTPUT_MODES.md: 492
- references/PUEBI.md: 1.326
- references/QUALITY_METRICS.md: 559
- references/STYLE_GUIDE.md: 1.431
- references/WORKFLOW.md: 1.659
- assets/example-edit.md: 1.020
- assets/output-template.md: 399
- assets/style-sheet-template.md: 409

Catatan: runtime agent memuat hanya file yang dibutuhkan; angka
eksekusi = worst case seluruh file dimuat. Angka discovery/activation
diukur dari SKILL.md; eksekusi dari indeks file di folder
references/ dan assets/.

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