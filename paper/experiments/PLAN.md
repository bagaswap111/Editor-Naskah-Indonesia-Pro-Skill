# PLAN — Eksperimen Nyata Paper ENIP

Dokumen kendali untuk menjalankan eksperimen paper "ENIP: A Portable
Layered Editing Skill for Indonesian Manuscripts". Dibuat agar dapat
dieksekusi kapan saja oleh agent/peneliti mana pun, dengan semua
keputusan terbuka ditandai **K1..K6** dan nilai default yang disarankan.

Alur dokumen: Keputusan → Prasyarat → Fase A–F → Definition of Done →
Estimasi → Pencatatan hasil.

---

## 0. Pertanyaan Riset yang Dijawab (peta ke outline paper)

| RQ | Pertanyaan | Metrik | File hasil |
|---|---|---|---|
| RQ1 | Apakah ENIP lebih unggul dari B1/B2/B3? | Skor 7 dimensi (judge), PUEBI error rate | `metrics/scores.json`, `metrics/puebi_report.md` |
| RQ2 | Apakah satu SKILL.md dipakai tanpa modifikasi di 8 runtime? | ya/tidak per runtime + mekanisme aktivasi | `portability/results.json` |
| RQ3 | Apakah deskripsi skill memicu dengan benar? | precision / recall 20 query | `trigger/results.json` |
| RQ4 | Berapa biaya konteks progressive disclosure? | token discovery/aktivasi/eksekusi | `metrics/overhead.json` |
| RQ5 | Seberapa besar self-assessment bias ENIP? | delta skor-diri ENIP vs judge vs manusia | `metrics/scores.json` |

**Kondisi eksperimen:**

| Kondisi | Deskripsi | Model | Cara |
|---|---|---|---|
| ENIP | skill enip-editor dimuat di runtime agent | editor (K1) | via agent runtime |
| B1 | prompt polos "Perbaiki naskah ini sesuai PUEBI." | editor (K1, SAMA) | API/UI |
| B2 | system prompt self-contained (`prompts/system-prompt.md`) | editor (K1, SAMA) | API/UI |
| B3 | LanguageTool id-ID (non-LLM mekanik) | — | CLI jar |

Aturan kunci: **B1/B2/ENIP wajib memakai model dasar yang sama** agar
yang diukur adalah efek instruksi, bukan efek model. Judge (C2) wajib
model BERBEDA dari editor.

---

## 1. Keputusan yang Harus Diambil Saat Eksekusi

| ID | Keputusan | Default rekomendasi | Alternatif |
|---|---|---|---|
| K1 | Model editor (B1/B2/ENIP) | Claude Sonnet 4.x via Anthropic API | GPT-4o, Gemini 2.5, Llama API |
| K2 | Model judge (harus beda dari K1) | GPT-4o (jika K1=Claude); jika K1=GPT-4o → Claude Sonnet atau Gemini | Gemini 2.5 |
| K3 | Cara menjalankan runs | API (temperature=0, reproducible) | UI runtime manual (catat model+tanggal) |
| K4 | Ukuran korpus | Pilot 5 (1/gaya) → Full 20 | Langsung 20 |
| K5 | Komposisi korpus | 10 sintetis+injeksi, 6 sintetis bersih (kontrol), 4 semi-formal | + teks publik domain bila ada sumber berlisensi |
| K6 | Validasi editor manusia | Tersedia → Fase E (2–3 editor); tidak tersedia → lewati, protokol tetap terdokumentasi | tunda sampai editor ada |

Eksekutor menjawab K1–K6 di awal, tulis jawabannya di
`paper/experiments/README.md` (bagian "Keputusan eksekusi"). Jika tidak
ada jawaban, pakai default dan catat.

---

## 2. Prasyarat

```bash
# Tooling (sekali saja)
brew install languagetool          # B3, dukungan id-ID (jar CLI)
paper/tools/.venv/bin/pip install tiktoken   # RQ4 overhead
# API keys (jika K3=API): EXPORT ANTHROPIC_API_KEY / OPENAI_API_KEY / GEMINI_API_KEY
```

Struktur direktori hasil (dibuat saat eksekusi Fase B–F):

```
paper/experiments/
├── PLAN.md                      # dokumen ini
├── README.md                    # hasil eksekusi: keputusan + ringkasan log
├── corpus/
│   ├── build_corpus.py          # Fase A: generator + injeksi error (seed tetap)
│   ├── raw/                     # teks sumber sebelum injeksi
│   ├── texts/                   # 20 naskah final (txt)
│   └── metadata.json            # id, gaya, audiens, kata, error_injected[]
├── runs/
│   ├── <kondisi>/<text_id>.md   # output MENTAH setiap kondisi
│   └── run_log.json             # model, timestamp, prompt hash per run
├── metrics/
│   ├── puebi_errors.py          # detektor error mekanik deterministik
│   ├── proxies.py               # koherensi: variansi panjang kalimat, rasio konjungsi, repetisi
│   ├── judge.py                 # llm-as-judge (rubrik 7 dimensi, 2 trial)
│   ├── judge_prompts/rubric.md  # dari references/QUALITY_METRICS.md
│   ├── scores.json  overhead.json  puebi_report.md
├── portability/
│   └── results.json
├── trigger/
│   ├── queries.json             # 20 query (10 memicu / 10 tidak)
│   └── results.json
└── human/
    ├── instruksi-editor.md      # lembar kerja buta
    ├── scores_raw.csv
    └── analyze.py               # mean abs delta, Cohen's kappa, sign test
```

Semua hasil eksperimen **di-commit ke git** (data paper, bukan artefak
yang di-gitignore).

---

## 3. Fase A — Korpus (build_corpus.py)

**Tujuan: 20 naskah, 5 per gaya (Akademis, Jurnalistik, Sastrawi,
Populer, Persuasif), 300–600 kata/naskah, dengan metadata mesin-baca.**

Tiga varian (sesuai K5):

| Varian | Jumlah | Konten |
|---|---|---|
| A1 sintetis + injeksi | 10 (2/gaya) | teks bersih ditulis template → lalu di-injeksi error PUEBI oleh script |
| A2 sintetis bersih | 6 (kontrol) | teks yang sama tanpa injeksi → mengukur over-editing & stabilitas |
| A3 semi-formal | 4 | register santai (gaya sosial media/blog) → uji transformasi gaya |
| A4 set nyata (opsional) | 5 | sub-bab acak buku teknis populer `corpus/buku-kolaborasi-llm/` (3.4–5.3 rb kata; register populer-edukatif; tanpa LICENSE → fair use riset, hanya statistik yang dilaporkan) |

**Katalog injeksi error (10 kategori, deterministik, seed tetap):**

| # | Kategori | Contoh salah → benar |
|---|---|---|
| E1 | Koma hilang sebelum tetapi/melainkan/sedangkan | "dia pergi tetapi lupa" → "dia pergi, tetapi lupa" |
| E2 | di-/ke- awalan vs kata depan | "di rumah" tertulis "dirumah"; "dibaca" tertulis "di baca" |
| E3 | pun salah | "walaupun" → "walau pun" |
| E4 | Serapan salah | analisa, praktek, resiko, apotik |
| E5 | Pleonasme | agar supaya, adalah merupakan, banyak para |
| E6 | Angka 1–9 di awal kalimat | "3 orang datang" |
| E7 | Tahun bertitik | 2.026 |
| E8 | Kapital salah | "presiden soekarno" |
| E9 | Italic hilang (istilah asing) | deadline tanpa miring |
| E10 | Kontaminasi struktur | "disebabkan karena" |

Aturan script: `random.seed(42)`; per naskah injeksi 15–25 error
tersebar; hasil injeksi **disimpan** `corpus/texts/<id>.txt` + daftar
error persis di `metadata.json` (menjadi ground truth untuk Fase C1);
script melaporkan jumlah error per naskah.

Metadata (`metadata.json`):

```json
{
  "id": "aca_01",
  "style": "academic",
  "audience": "akademisi",
  "words": 412,
  "variant": "injected",
  "clean_twin": "aca_02",
  "injected_errors": [{"cat": "E2", "offset": 87, "wrong": "dirumah", "right": "di rumah"}]
}
```

Kontrol kualitas: 1 naskah dari tiap varian ditinjau manual oleh
eksekutor sebelum lanjut (script `--review` menampilkan diff injeksi).

---

## 4. Fase B — Runner (eksekusi 4 kondisi)

Prosedur SERAGAM per naskah (hindari bias eksekusi):

1. Ambil `<id>.txt` dari korpus.
2. Parameter sesi ENIP tetap: gaya sesuai `metadata.style`,
   formalitas 5, panjang kalimat target sedang, analogi sedang,
   mode **Edit + Catatan** (menghasilkan skor-diri juga — dibutuhkan RQ5).
3. Simpan output MENTAH tanpa retouch ke `runs/<kondisi>/<id>.md`.
4. Catat ke `run_log.json`: kondisi, id, model, temperature (0 jika
   API), timestamp, dan hash prompt+input (untuk audit).

Per kondisi:

| Kondisi | Eksekusi |
|---|---|
| ENIP | runtime agent (OpenCode/Claude Code) — gunakan skill `enip-editor`; tambahkan parameter sesi di atas pada perintah |
| B1 | API/UI: satu instruksi "Perbaiki naskah ini sesuai PUEBI." |
| B2 | API/UI: system prompt = isi `prompts/system-prompt.md`, instruksi yang sama |
| B3 | `languagetool --language id-ID <id>.txt > runs/b3/<id>.lt` (simpan raw output); automatic-fix version juga disimpan jika tersedia |

Catatan: jika K3=API, eksekutor membangun `run_api.py` kecil (wrapper
seragam ke provider K1; input prompt file, output ke runs/) — sekali
tulis, pakai untuk 20×3 runs. Jika K3=UI, jalankan manual dan isi
run_log dengan model yang tampil di UI (mis. "Claude Sonnet 4.6, UI
ChatGPT, 2026-08-15").

---

## 5. Fase C — Metrik Otomatis

### C1. PUEBI error rate (`puebi_errors.py`)
- Input: `runs/<kondisi>/<id>.md` + korpus metadata.
- Deteksi: (a) untuk naskah **injected**: hitung berapa error E1–E10
  MASIH ADA di output (ground truth dari metadata) → *error
  remaining/1000 kata* dan *fix rate*; (b) untuk semua output: proxy
  LanguageTool diff (jumlah peringatan) sebagai ukuran kedua.
- Output: `metrics/puebi_report.md` — tabel per kondisi, mean & median
  per 1000 kata, persentase fix per kategori.

### C2. LLM-as-judge (`judge.py` + `judge_prompts/rubric.md`)
- Model: K2 (WAJIB berbeda dari editor).
- Input per penilaian: naskah asli + satu output (anonymized: tanpa
  label sistem, urutan acak).
- Rubrik: transkripsi 7 dimensi dari `skill/enip-editor/references/
  QUALITY_METRICS.md` (definisi 9–10 per dimensi), output JSON
  `{clarity, coherence, depth, accuracy, style, mechanics, engagement}`.
- 2 trial per item (temperature 0 dan 0.7); laporkan mean ± std.
- Output: `metrics/scores.json` + ringkasan `scores_repoort.md` (tabel
  per kondisi: mean 7 dimensi, delta ENIP−B1/B2/B3, uji signifikan
  sederhana — paired bootstrap atau sign test).

### C3. Delta self-score (RQ5)
- ENIP mode Edit+Catatan berisi skor-diri (di output ENIP). Bandingkan
  dengan judge (C2) per dimensi → rata-rata abs delta.
- Interpretasi ditulis ke `metrics/puebi_report.md` atau terpisah.

### C4. Proksi koherensi deterministik (`proxies.py`, opsional)
- Variansi panjang kalimat (target: sedang ±; ENIP diharapkan lebih
  terkontrol), rasio konjungsi unik/konjungsi total (variasi transisi),
  tingkat repetisi leksikal (X teratas kata paling sering / total kata).

---

## 6. Fase D — Portabilitas, Trigger, Overhead

### D1. Portabilitas (RQ2)
- 1 naskah uji (id termudah, mis. pop_03) × 8 runtime: Claude Code,
  Cursor 2.4+, OpenAI Codex, Cline, Gemini CLI, OpenCode, Google
  Antigravity, VS Code Copilot.
- Per runtime catat `portability/results.json`:
  `{runtime, install_method, loads_without_modification: bool,
    activation_mechanism, output_received: bool, notes}`.
- Kriteria lulus: skill dimuat + output valid tanpa editing file skill.

### D2. Trigger reliability (RQ3)
- `trigger/queries.json`: 20 query realistis pengguna Indonesia —
  10 harus memicu ("perbaiki kalimat ini, ada typo", "jadikan gaya
  akademis", "sunting naskah skripsi saya", dsb.), 10 tidak boleh
  ("tulis kode python", "jelaskan cara kerja CPU", "buatkan saya
  daftar belanja", dsb.).
- Prosedur: jalankan tiap query di runtime utama (Claude Code atau
  OpenCode) dengan skill terpasang; catat apakah skill teraktivasi
  (referensi SKILL.md dimuat / aktivasi eksplisit).
- Output: precision (memicu benar/memicu total), recall
  (memicu benar/yang harus memicu) → `trigger/results.json`.

### D3. Context overhead (RQ4)
- `metrics/overhead.json`:
  - Discovery: token frontmatter (`name` + `description`) via tiktoken.
  - Aktivasi: token body `SKILL.md`.
  - Eksekusi: token tiap file di `references/` dan `assets/` (diukur
    per file; yang benar-benar dibaca dicatat dari pengamatan runs ENIP).
- Opsional: ukur token aktual yang masuk konteks di runtime (log
  verbose) dan bandingkan estimasi vs aktual.

---

## 7. Fase E — Validasi Editor Manusia (jika editor tersedia; K6)

1. **Paket buta**: 10 naskah × 2 output (ENIP vs B1), tanpa label
   sistem, urutan acak per editor, format `human/instruksi-editor.md`
   + lembar skor CSV (kolom: item, dimensi 1–7, preferensi A/B opsional).
2. **Editor**: 2–3 orang penutur asli dengan latar editing/penerbitan
   (latar belakang disamarkan di paper).
3. **Analisis** (`human/analyze.py`):
   - mean abs delta (skor editor vs ENIP self-score dan vs judge);
   - Cohen's kappa antar-editor (per dimensi);
   - pairwise preference ENIP vs B1 (sign test, α=0.05).
4. Estimasi: 10 item × 2 output × 7 dimensi ≈ 30–45 menit/editor.

Jika editor tidak tersedia: SKIP, tulis di README "Fase E ditunda
sampai editor tersedia"; paper menyatakan 4.6 sebagai validasi rencana
(jangan klaim hasil).

---

## 8. Fase F — Konsolidasi & Integrasi Paper

1. **Isi `paper/inputs/experimental_log.md`**: ganti semua `TBD` di
   Section 2.3/2.4/2.5 dengan angka nyata dari `metrics/*.json` —
   ditambahkan baris referensi ke file hasil (`lihat results.json`).
   **Penting**: angka harus persis dari data; jangan rata-rata manual
   di luar script.
2. **Tulis `paper/EXPERIMENT_RESULTS.md`** — ringkasan eksekusi:
   keputusan K1–K6, tabel hasil RQ1–RQ5, keterbatasan, apa yang
   di-skip.
3. **Jalankan gates** (dari `paper/tools/`):
   ```bash
   paper/tools/.venv/bin/python paper/tools/paper-orchestra-scripts/validate_consistency.py \
     --idea paper/inputs/idea.md --log paper/inputs/experimental_log.md
   ```
4. **Update `paper/README.md`** status tabel: Fase eksperimen ✅.
5. (Lanjutan paper, sesi terpisah) Step 2–5 pipeline: plotting,
   lit review, section writing, refinement — `claim_evidence_gate.py`
   akan memverifikasi angka eksperimen di naskah final ber-grounding
   di log.

---

## 9. Definition of Done (semua harus terpenuhi)

- [ ] `corpus/` — 20 naskah + metadata.json (ground truth error) + review manual 1/variant dicatat
- [ ] `runs/` — output mentah 4 kondisi × 20 naskah (atau 5 pilot), `run_log.json` lengkap
- [ ] `metrics/puebi_report.md`, `metrics/scores.json`, `metrics/overhead.json` (jumlah & isi sesuai spec)
- [ ] `portability/results.json` (8 runtime) dan `trigger/results.json` (20 query, precision/recall)
- [ ] RQ5 delta self-score dihitung & dicatat
- [ ] K6=ya → `human/` lengkap dengan analisis; K6=tidak → tercatat sebagai ditunda
- [ ] `experimental_log.md` tanpa TBD di Section 2 (kecuali yang memang ditunda, ditandai)
- [ ] `paper/EXPERIMENT_RESULTS.md` ditulis
- [ ] `validate_consistency.py` PASS
- [ ] Semua hasil ter-commit di git

---

## 10. Estimasi Biaya & Waktu

| Cakupan | LLM calls | Estimasi biaya | Waktu eksekusi |
|---|---|---|---|
| Pilot (5 naskah × 3 kondisi LLM + judge 2 trial) | ~35 | $1–2 | 20–40 menit |
| Full (20 naskah + 8 runtime + trigger) | ~140 + overhead runtime | $4–8 | 2–4 jam (parallel sub-agent membantu) |
| Human eval (opsional) | 0 | biaya editor (2–3 jam kerja) | 1–2 hari kalender |

Catatan: B3 gratis; judge 2× call per item. Trigger & portability
memakai runtime lokal (perangkat sendiri), tidak ada biaya API.

---

## 11. Langkah Pertama Saat Eksekusi

1. Jawab K1–K6, tulis di `paper/experiments/README.md`.
2. `pip install tiktoken` di venv; cek `languagetool` terpasang.
3. Bangun & jalankan `build_corpus.py` (Fase A), review 1 naskah/variant.
4. Jalankan pilot 5 naskah (Fase B) — verifikasi pipeline sebelum full.
5. Fase C → D → (E) → F.
6. Selesaikan Definition of Done; commit.