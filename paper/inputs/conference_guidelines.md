# Conference Guidelines — ENIP Paper

*Target venue: ACL-style main conference submission (placeholder — dapat
diganti EMNLP/COLING/ICLR; memengaruhi page limit dan cutoff literature).*

## Format

- **Page limit**: 8 pages (references tidak dihitung) + 2 halaman appendix
  opsional.
- **Layout**: two-column, ACL-style LaTeX template, font 10pt.
- **Bahasa**: Inggris (makalah menargetkan audiens internasional; objek
  studi adalah Bahasa Indonesia).
- **Sections wajib**: Abstract, Introduction, Methodology, Experiments,
  Conclusion. Related Work wajib ada.

## Submission & deadline

- **Deadline submission**: 2026-10-01 (placeholder).
- **Literature cutoff date (CRITICAL for outline)**: `2026-09-01`.
  Literature review TIDAK boleh menginstruksikan pencarian paper setelah
  tanggal ini.

## Konten yang diminta (khusus paper ini)

- Paper harus berbasis pada artefak nyata: skill `enip-editor` (SKILL.md
  Open Agent Skills) dan contoh before/after di `examples/`.
- Klaim numerik eksperimen WAJIB merujuk `experimental_log.md`.
- Jangan mengarang referensi; semua klaim literatur harus diverifikasi.
- Struktur makalah harus menonjolkan 4 kontribusi:
  1. Formalization lapisan kompetensi editorial (3 lapis).
  2. Style engine untuk Bahasa Indonesia (5 gaya + hybrid + parameter mikro).
  3. Portabilitas lintas-agent (format SKILL.md) + pengukuran overhead.
  4. Protokol evaluasi kualitas editing 7 dimensi (rubrik + rencana
     evaluasi manusia).

## Reviewer expectations

- Bagian eksperimen harus membahas *self-assessment bias* secara eksplisit
  (skor kualitas dilaporkan oleh model sendiri) dan merencanakan evaluasi
  manusia/editor sebagai validasi.
- Bagian portabilitas harus melaporkan jumlah runtime yang berhasil
  memuat skill tanpa modifikasi + metode pengujiannya.