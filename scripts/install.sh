#!/usr/bin/env bash
#
# ENIP — Editor Naskah Indonesia Pro
# Installer lintas platform (Claude Code, Cursor, Codex, Cline, Gemini CLI,
# OpenCode, Antigravity, dll.). Format SKILL.md sama untuk semua tool —
# hanya jalur penyimpanan yang berbeda.
#
# Penggunaan:
#   ./scripts/install.sh             pasang project-level (symlink)
#   ./scripts/install.sh --global    pasang user-level (~/.claude/skills, dst.)
#   ./scripts/install.sh --copy      salin file alih-alih symlink
#   ./scripts/install.sh --uninstall hapus pemasangan
#   ./scripts/install.sh --list      daftar jalur yang didukung
#   ./scripts/install.sh --help      bantuan

set -euo pipefail

SKILL_NAME="enip-editor"
MODE="link"        # link | copy
SCOPE="project"    # project | global
ACTION="install"   # install | uninstall

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/skill/$SKILL_NAME"

PROJECT_TARGETS=(
  ".claude/skills"
  ".cursor/skills"
  ".agents/skills"
  ".codex/skills"
  ".opencode/skills"
  ".gemini/skills"
  ".cline/skills"
  ".clinerules/skills"
  ".agent/skills"
)

GLOBAL_TARGETS=(
  "$HOME/.claude/skills"
  "$HOME/.cursor/skills"
  "$HOME/.agents/skills"
  "$HOME/.config/opencode/skills"
  "$HOME/.gemini/skills"
  "$HOME/.cline/skills"
  "$HOME/.codex/skills"
  "$HOME/.agent/skills"
)

usage() {
  sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'
}

for arg in "$@"; do
  case "$arg" in
    --global)   SCOPE="global" ;;
    --copy)     MODE="copy" ;;
    --uninstall) ACTION="uninstall" ;;
    --list)
      echo "Project-level:"
      printf '  %s/\n' "${PROJECT_TARGETS[@]}"
      echo "Global-level:"
      printf '  %s/\n' "${GLOBAL_TARGETS[@]}"
      exit 0
      ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "Opsi tidak dikenal: $arg" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [ "$ACTION" = "install" ] && [ ! -f "$SOURCE_DIR/SKILL.md" ]; then
  echo "ERROR: $SOURCE_DIR/SKILL.md tidak ditemukan." >&2
  echo "Jalankan script dari dalam direktori repo ENIP." >&2
  exit 1
fi

if [ "$SCOPE" = "project" ]; then
  TARGETS=("${PROJECT_TARGETS[@]}")
  BASE="$PWD"
  echo "Pasang ENIP ($SKILL_NAME) di direktori project: $BASE"
else
  TARGETS=("${GLOBAL_TARGETS[@]}")
  BASE=""
  echo "Pasang ENIP ($SKILL_NAME) di direktori user."
fi

INSTALLED=0
SKIPPED=0

for dir in "${TARGETS[@]}"; do
  dest="$dir/$SKILL_NAME"

  if [ -n "$BASE" ]; then
    dest="$BASE/$dest"
  fi

  if [ "$ACTION" = "uninstall" ]; then
    if [ -L "$dest" ] || [ -d "$dest" ]; then
      rm -rf "$dest"
      echo "  dihapus: $dest"
      INSTALLED=$((INSTALLED + 1))
    fi
    continue
  fi

  if [ -L "$dest" ]; then
    target="$(readlink "$dest" 2>/dev/null || true)"
    if [ "$MODE" = "link" ] && [ "$target" = "$SOURCE_DIR" ]; then
      echo "  sudah terpasang: $dest"
      SKIPPED=$((SKIPPED + 1))
      continue
    fi
    rm "$dest"
  elif [ -e "$dest" ]; then
    echo "  LEWATI: $dest sudah ada sebagai file (bukan symlink)." >&2
    echo "         Hapus manual jika ingin diganti." >&2
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  mkdir -p "$(dirname "$dest")"

  if [ "$MODE" = "link" ]; then
    ln -s "$SOURCE_DIR" "$dest"
    echo "  symlink: $dest -> $SOURCE_DIR"
  else
    cp -R "$SOURCE_DIR" "$dest"
    echo "  salin:   $dest"
  fi
  INSTALLED=$((INSTALLED + 1))
done

if [ "$ACTION" = "uninstall" ]; then
  echo "Selesai. Dihapus: $INSTALLED."
else
  echo "Selesai. Terpasang: $INSTALLED, dilewati: $SKIPPED."
  if [ "$MODE" = "link" ]; then
    echo "Catatan: mode symlink — simpan repo ini, jangan dipindah."
    echo "Gunakan --copy bila symlink tidak didukung (mis. di Windows)."
  fi
fi