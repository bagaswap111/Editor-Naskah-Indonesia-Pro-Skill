# Checklist Submit ke Marketplace Skill

ENIP berformat **SKILL.md (Open Agent Skills / agentskills.io)** — satu
folder portable yang bisa masuk ke semua direktori di bawah ini tanpa
konversi. Urutkan berdasarkan dampak (terbesar dulu).

## 1. GitHub repo live (prasyarat semua)

- [ ] `gh auth login` lalu buat repo & push (lihat README "Instalasi")
- [ ] Repo **public**, About terisi: 1 kalimat + URL skill
- [ ] Topics: `agent-skills`, `skills`, `llm-agents`, `bahasa-indonesia`,
      `indonesian-language`, `puebi`, `editing`, `ai-writing`,
      `claude-skills`, `open-agent-skills`
- [ ] Social preview: upload `assets/banner.svg` di Settings → Social preview
- [ ] Badge CI hijau (workflow `validate-skills`)
- [ ] Release v0.1.0 (tag `v0.1.0`) + CHANGELOG

## 2. `npx skills add` compatibility (Vercel skills installer)

- [ ] Uji: `npx skills add <owner>/Editor-Naskah-Indonesia-Pro`
- [ ] Pastikan folder skill di `skill/enip-editor/` dengan `SKILL.md`
      sesuai spec (name = nama folder)
- [ ] Buka PR/issue di [vercel-labs/skills](https://github.com/vercel-labs/skills)
      jika installer gagal mendeteksi path custom

## 3. Direktori skill (submit manual, gratis)

| Marketplace | URL | Status |
|---|---|---|
| agentskills.io (showcase) | https://agentskills.io | [ ] |
| GuildSkills | https://guildskills.com | [ ] |
| skills.sh (agentproto) | https://skills.sh | [ ] |
| OpenCode skills registry | https://opencode.ai/docs/skills | [ ] |
| Cursor marketplace (jika ada) | https://cursor.com/docs/context/skills | [ ] |

Bahan yang harus disiapkan tiap submit: nama, deskripsi 1 kalimat,
screenshot/contoh output, link repo, tags, kategori (writing/editing).

## 4. GitHub ekosistem

- [ ] Star/bintang dari kolega dan komunitas (bukan beli/fake)
- [ ] GitHub Discussions aktif (Gunakan repositori → Discussions)
- [ ] Jawab issue dalam 48 jam pertama setelah rilis
- [ ] Tag orang yang relevan di issue pertama (penulis PUEBI community, dsb.)

## 5. Distribusi sosial (urutan dampak)

- [ ] **X/Twitter**: thread demo 1 (screenshot before/after)
- [ ] **r/indonesia**, **r/indonesian**, komunitas dev Indonesia
      (Telegram/Facebook: grup developer & content creator)
- [ ] **Dev.to / Medium**: artikel "Saya membuat skill editing Bahasa
      Indonesia untuk semua AI agent"
- [ ] **LinkedIn**: post + demo singkat
- [ ] **Reddit r/LocalLLaMA**, r/CursorAI, r/ClaudeAI (jika relevan:
      "skill Bahasa Indonesia yang jalan di semua agent")
- [ ] Video demo 60 detik (Loom/YouTube Short) — demonstrasi skill
      mengedit naskah nyata

## 6. Pengulangan & momentum

- [ ] Update mingguan: changelog, contoh baru di `examples/`
- [ ] Roadmap publik di GitHub (Projects): mis. integrasi KBBI API,
      mode suara, evaluasi A/B dengan editor manusia
- [ ] Rilis minor saat fitur bertambah (semver)
- [ ] Minta testimoni pemakai → jadi badge quote di README

## Catatan penting

- Jangan membeli star; algoritma GitHub menghapus akun/token curang.
- Kualitas > volume: 1 marketplace diisi dengan baik > 5 diisi asal-asalan.
- Dokumentasikan proses di sini; tandai [x] saat selesai.