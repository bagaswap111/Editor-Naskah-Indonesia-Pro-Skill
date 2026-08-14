#!/usr/bin/env bash
#
# Validasi struktur skill ENIP (dipakai CI lokal & GitHub Actions).
# Memeriksa konvensi Open Agent Skills (agentskills.io):
#   - SKILL.md wajib ada, ber-frontmatter YAML dengan name + description
#   - name: kebab-case, <=64 char, cocok dengan nama folder
#   - description: 1-1024 karakter, tanpa tag XML
#   - semua file yang dirujuk di body (references/, assets/) ada
#   - SKILL.md < 500 baris (peringatan)

set -uo pipefail

SKILL_DIR="${1:-skill/enip-editor}"
SKILL_FILE="$SKILL_DIR/SKILL.md"

FAIL=0
WARN=0

fail() { echo "  [GAGAL] $*"; FAIL=$((FAIL + 1)); }
warn() { echo "  [PERINGATAN] $*"; WARN=$((WARN + 1)); }

echo "== Validasi skill: $SKILL_DIR =="

if [ ! -f "$SKILL_FILE" ]; then
  echo "[GAGAL] $SKILL_FILE tidak ditemukan."
  exit 1
fi

if ! head -1 "$SKILL_FILE" | grep -q '^---$'; then
  fail "SKILL.md tidak diawali frontmatter YAML (---)"
fi

F_END=$(awk '/^---$/{n++} n==2{print NR; exit}' "$SKILL_FILE")
if [ -z "$F_END" ]; then
  fail "frontmatter YAML tidak ditutup (---)"
  exit 1
fi

# --- name ---
NAME=$(sed -n 's/^name: *//p' "$SKILL_FILE" | tr -d '[:space:]')
DIRNAME=$(basename "$SKILL_DIR")

if [ -z "$NAME" ]; then fail "frontmatter tidak punya field 'name'."; else
  if ! echo "$NAME" | grep -Eq '^[a-z0-9]+(-[a-z0-9]+)*$'; then
    fail "name '$NAME' tidak valid (harus kebab-case: a-z0-9 + '-' )."
  fi
  if [ "${#NAME}" -gt 64 ]; then fail "name >64 karakter."; fi
  if [ "$NAME" != "$DIRNAME" ]; then
    fail "name '$NAME' tidak cocok dengan nama folder '$DIRNAME'."
  fi
fi

# --- description ---
DESC=$(awk '
  /^description: *>/ {flag=1; sub(/^description: *>[-+]* *$/, ""); if ($0 != "") {print; flag=0; next} next}
  flag && /^[a-zA-Z_-]+:/ {flag=0}
  flag {print}
  /^description: / && !/^description: *>/ {sub(/^description: */, ""); print; next}
' "$SKILL_FILE" | tr -d '\n')

if [ -z "$DESC" ]; then
  fail "frontmatter tidak punya field 'description'."
else
  LEN=${#DESC}
  if [ "$LEN" -gt 1024 ]; then fail "description $LEN karakter (>1024)."; fi
  if [ "$LEN" -lt 1 ]; then fail "description kosong."; fi
  if echo "$DESC" | grep -qE '<[a-zA-Z/][^>]*>'; then fail "description mengandung tag XML."; fi
fi

# --- rujukan file di body ---
BODY=$(tail -n +"$((F_END + 1))" "$SKILL_FILE")
for ref in $(echo "$BODY" | grep -oE '`(references|assets)/[A-Za-z0-9_.-]+`' | tr -d '`' | sort -u); do
  if [ ! -f "$SKILL_DIR/$ref" ]; then fail "file yang dirujuk tidak ada: $ref"; fi
done

# --- panjang ---
LINES=$(wc -l < "$SKILL_FILE")
if [ "$LINES" -gt 500 ]; then warn "SKILL.md $LINES baris (>500, pindahkan detail ke references/)."; fi

# --- semua references/assets terpakai atau terdokumentasi ---
for f in "$SKILL_DIR"/references/*.md "$SKILL_DIR"/assets/*.md; do
  [ -e "$f" ] || continue
  base="$(basename "$f")"
  if ! echo "$BODY" | grep -q "references/$base\|assets/$base"; then
    warn "$base tidak dirujuk dari SKILL.md (mungkin masih berguna sebagai referensi opsional)."
  fi
done

echo ""
if [ "$FAIL" -gt 0 ]; then
  echo "HASIL: GAGAL ($FAIL kesalahan)."
  exit 1
fi
echo "HASIL: LULUS${WARN:+ ($WARN peringatan)}."
exit 0