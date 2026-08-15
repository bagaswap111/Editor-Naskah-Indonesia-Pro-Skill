#!/usr/bin/env python3
"""D3 — Context overhead ENIP (progressive disclosure).

Mengukur token per komponen skill dengan tiktoken (cl100k_base):
  - discovery : frontmatter (name + description) SKILL.md
  - aktivasi  : body SKILL.md
  - eksekusi  : tiap file references/ dan assets/ (token per file)
Output: metrics/overhead.json
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "metrics"
SKILL = Path(__file__).resolve().parents[3] / "skill" / "enip-editor"

ENC_NAME = "cl100k_base"


def main():
    import tiktoken
    enc = tiktoken.get_encoding(ENC_NAME)
    skill_md = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    fm = skill_md.split("---", 2)[1]
    body = skill_md.split("---", 2)[2]
    out = {
        "encoder": ENC_NAME,
        "discovery": {"frontmatter_full": len(enc.encode(skill_md.split("---", 2)[1])),
                      "name_description": len(enc.encode("\n".join(
                          l for l in fm.splitlines()
                          if l.startswith(("name:", "description:", "  "))))),
                      "note": "progressive disclosure: hanya frontmatter yang ter-petakan di discovery"},
        "activation": {"SKILL.md_body": len(enc.encode(body))},
        "execution": {},
        "totals": {},
    }
    exec_tokens = 0
    for sub in ("references", "assets"):
        for f in sorted((SKILL / sub).glob("*")):
            t = len(enc.encode(f.read_text(encoding="utf-8")))
            out["execution"][f"{sub}/{f.name}"] = t
            exec_tokens += t
    total = (int(out["activation"]["SKILL.md_body"]) + exec_tokens
             + int(out["discovery"]["frontmatter_full"]))
    out["totals"] = {"full_bundle": total,
                     "discovery_only": out["discovery"]["frontmatter_full"],
                     "execution_all_references_assets": exec_tokens,
                     "note": "runtime agent memuat hanya file yang dibutuhkan; "
                             "angka ini = worst case seluruh file dimuat"}
    (METRICS / "overhead.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Token: discovery={out['discovery']['frontmatter_full']}, "
          f"aktivasi={out['activation']['SKILL.md_body']}, "
          f"eksekusi(total refs+assets)={exec_tokens}, "
          f"bundle penuh={total}")


if __name__ == "__main__":
    main()