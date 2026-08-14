# Contributing to ENIP

Terima kasih sudah ingin berkontribusi. Semua bentuk kontribusi
diterima: perbaikan aturan bahasa, contoh baru, bug report, dokumen.

## Alur

1. **Fork** dan buat branch: `git checkout -b fix/nama-perubahan`
2. **Ubah** file yang relevan (lihat "Area perubahan")
3. **Validasi**: `bash scripts/validate.sh`
4. **Commit** dengan pesan jelas, **push**, buat **Pull Request**

## Area perubahan

| Area | File | Catatan |
|---|---|---|
| Aturan bahasa (PUEBI, KBBI, serapan) | `skill/enip-editor/references/PUEBI.md` | Tambahkan sumber/rujukan untuk klaim |
| Gaya bahasa | `skill/enip-editor/references/STYLE_GUIDE.md` | Ikuti pola gaya yang sudah ada |
| Workflow/tahapan | `skill/enip-editor/references/WORKFLOW.md` | Jangan hapus tahap inti tanpa diskusi |
| Aturan inti/prompt | `skill/enip-editor/SKILL.md` | Perubahan besar → buka issue dulu |
| Contoh before/after | `examples/` | Beri parameter sesi yang jelas |
| Tooling (install/validate) | `scripts/` | Uji dengan naskah sungguhan |
| Dokumen | `README*.md`, `docs/` | Ikuti bahasa: Inggris di README.md, Indonesia boleh di README.id.md |

## Aturan

- **Simpan format portable**: hanya `name` + `description` di frontmatter;
  jangan tambah field khusus tool (bisa diabaikan tool lain, tapi jangan
  jadi ketergantungan).
- **SKILL.md tetap <500 baris**; detail panjang pindah ke `references/`
  atau `assets/`.
- Perubahan bahasa harus mengacu PUEBI resmi; jika tidak yakin, tandai
  dengan ⚠️ bukan langsung menebak.
- Jangan pernah mengarang contoh referensi/citraan pada konten skill.

## Standar PR

- Pesan commit: `fix(rule): koma sebelum 'sedangkan'`, `feat(style): gaya
  baru ...`, `docs: ...`, `ci: ...`
- Sertakan tangkapan hasil `bash scripts/validate.sh`
- Untuk perubahan perilaku skill: sertakan contoh input → output
  sebelum/sesudah.

## Menjalankan tes

```bash
bash scripts/validate.sh          # validasi format skill
./scripts/install.sh --list       # cek jalur installer
```