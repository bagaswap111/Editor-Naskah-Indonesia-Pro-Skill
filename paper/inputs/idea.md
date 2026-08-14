# Idea Summary — ENIP Paper (Sparse variant)

## Problem Statement

Penyuntingan naskah Bahasa Indonesia (proofreading, editing struktural,
dan developmental editing) belum terlayani dengan baik oleh alat bantu
otomatis:

1. **Tidak ada standar editorial terstruktur untuk LLM.** Perintah
   "perbaiki kalimat ini" menghasilkan editing yang ad hoc: LLM generik
   mengoreksi ejaan tanpa mengelola alur, koherensi, kedalaman, atau
   register — dan tanpa justifikasi perubahan.
2. **Alat ejaan/koreksi yang ada bersifat mekanik-sentris.** Alat seperti
   spell/grammar checker (termasuk yang berbasis PUEBI) menangani lapisan
   mekanik saja; lapisan struktural dan substantif tidak tersentuh.
3. **Basis aturan PUEBI belum diformalisasi untuk konsumsi LLM.** Aturan
   ejaan (kapital, miring, tanda baca, penulisan kata, angka) tersebar di
   dokumen referensi; tidak ada representasi ringkas yang bisa dimuat
   on-demand oleh agent.
4. **Format skill lintas-agent masih muda.** Munculnya format SKILL.md
   (Open Agent Skills) memungkinkan satu artefak berjalan di 25+ runtime,
   tetapi belum ada evaluasi publik soal portabilitas nyata sebuah skill
   editorial, termasuk biaya konteks (progressive disclosure) dan
   keandalan pemicu (trigger reliability).

## Core Hypothesis

Mengenkodekan metodologi editorial berlapis — 3 lapis kompetensi
(mekanik/struktural/substantif), basis aturan PUEBI, style engine 5 gaya +
hybrid (bobot 60/30/10) + parameter mikro, struktur paragraf TEEL+,
workflow 7 tahap, protokol verifikasi fakta, dan skor kualitas 7 dimensi
— sebagai satu skill deklaratif berformat SKILL.md akan menghasilkan
kualitas editing yang lebih tinggi daripada (a) LLM tanpa panduan
terstruktur dan (b) pipeline grammar-checker mekanik, sementara (c) tetap
portabel lintas runtime agent dengan satu artefak tanpa modifikasi.

## Proposed Methodology (High-Level Technical Approach)

Sistem ENIP terdiri atas empat modul fungsional:

1. **Tiga Lapis Kompetensi** — Lapis 1 (Mekanik): proofreading PUEBI &
   KBBI (huruf kapital, huruf miring, tanda baca kritis, penulisan
   di-/ke-/pun, kata serapan, angka). Lapis 2 (Struktural): TEEL+ per
   paragraf, 7 jenis transisi antarparagraf, pola perkembangan ide, Model
   Kedalaman Berlapis 5 lapis (APA→MENGAPA→BAGAIMANA→CONTOH→IMPLIKASI).
   Lapis 3 (Substantif): protokol verifikasi fakta (penanda `[Sumber?]`,
   `[Korelasi ≠ Kausalitas?]`), format referensi (APA 7/Chicago/IEEE/
   Vancouver/catatan kaki), penanganan sensitivitas bahasa.
2. **Style Engine** — 5 gaya (Akademis, Jurnalistik, Sastrawi, Populer,
   Persuasif), mode hybrid (Primer 60% / Sekunder 30% / Tersier 10%),
   7 parameter mikro (formalitas 1–10, panjang kalimat, densitas
   terminologi, frekuensi analogi, retoris, licentia poetica, perspektif).
3. **Workflow 7 Tahap** — Intake & Diagnosis → Editing Substantif →
   Editing Struktural → Editing Kalimat → Proofreading → Enhancement →
   Output & Catatan Editor; dengan 4 mode output (Clean, Edit+Catatan,
   Track Changes, Konsultasi) dan skor kualitas 7 dimensi (Kejelasan,
   Koherensi, Kedalaman, Akurasi, Gaya, Mekanik, Engagement).
4. **Portabilitas** — satu direktori skill (`enip-editor/`) berformat
   SKILL.md: frontmatter name+description (pemicu), body <500 baris,
   detail di `references/` (6 file, progressive disclosure), template di
   `assets/`. Installer deterministik `install.sh` untuk 9 jalur project
   + 8 jalur global. Validator `validate.sh` + CI GitHub Actions.

## Expected Contribution

1. **Framework konseptual**: formalisasi 3-lapis kompetensi editorial dan
   style engine untuk Bahasa Indonesia, adaptasi prinsip IELTS Band 9
   (TEEL+, kohesi/koherensi) ke bahasa Indonesia.
2. **Artefak terbuka**: basis aturan PUEBI yang dapat dimuat on-demand
   oleh LLM (ringkas, terstruktur, berpenanda ⚠️ untuk ketidakpastian),
   template output, dan contoh before/after — semua MIT, dapat
   direproduksi.
3. **Studi portabilitas**: pengukuran empiris jumlah runtime yang memuat
   skill tanpa modifikasi, overhead konteks, dan keandalan pemicu.
4. **Protokol evaluasi**: rubrik 7 dimensi + rencana evaluasi editor
   manusia untuk mengatasi self-assessment bias.