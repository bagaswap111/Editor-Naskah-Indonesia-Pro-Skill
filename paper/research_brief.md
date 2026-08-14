# Research Brief — ENIP Paper

## §1 · Core Claim and Narrative
_Written by: outline-agent, Step 1_

**Core claim:** Sebuah skill editorial berformat SKILL.md yang
mengenkodekan metodologi tiga lapis (mekanik PUEBI/KBBI, struktural
TEEL+, substantif verifikasi fakta) plus style engine hybrid untuk Bahasa
Indonesia menghasilkan kualitas editing unggul vs LLM tanpa panduan dan
pipeline mekanik, sekaligus portabel lintas 8+ runtime agent dengan satu
artefak tanpa modifikasi.

**Narrative tension:** Editing naskah Indonesia terpecah antara
(1) alat mekanik yang hanya menyentuh ejaan, (2) LLM generik yang
menyunting ad hoc tanpa struktur/justifikasi, dan (3) ekosistem skill
agent yang formatnya sudah mapan (SKILL.md) namun belum punya evaluasi
portabilitas untuk skill domain nyata — termasuk tidak ada sama sekali
skill editorial Bahasa Indonesia di registry publik.

**Key novelty framing:** Bukan model bahasa baru, melainkan
*formalization + packaging*: aturan PUEBI yang diformalisasi untuk
dimuat on-demand oleh LLM, style engine dengan pembobotan hybrid 60/30/10,
dan pengukuran artefak yang jujur (vs klaim umum). Posisi: di antara
"grammar checking" (terlalu mekanik) dan "LLM prompt editing" (terlalu
ad hoc), di atas format skill portabel yang belum teruji.

**Outline decisions:**
- Plotting plan: 6 figures (3 diagram konseptual, 3 plot data terverifikasi)
- Related Work clusters: GEC & grammar checking (2.1), LLM-as-editor (2.2),
  agent skills & portable formats (2.3), sumber daya bahasa Indonesia (2.4)
- Section structure: Abstract → Introduction → Related Work → Methodology
  (5 sub) → Experiments (6 sub) → Discussion → Conclusion → Appendix

**Potential weaknesses flagged at outline stage:**
- Skor kualitas 7 dimensi pada worked examples adalah **laporan diri
  model** (self-assessment bias) — eksperimen formal terhadap baseline dan
  validasi editor manusia masih [DI-RENCANAKAN], sehingga Claims di bagian
  hasil hanya bisa didukung data artefak, bukan data komparatif;
- Satu contoh (jurnalistik) tidak memiliki skor karena mode Clean
  (keterbatasan desain yang harus diungkap);
- Tidak ada dataset naskah uji publik untuk Bahasa Indonesia yang
  distandardisasi — korpus 20 naskah dibuat sendiri (kritik
  generalizability);
- Angka token progressive disclosure adalah estimasi, bukan pengukuran
  runtime aktual.