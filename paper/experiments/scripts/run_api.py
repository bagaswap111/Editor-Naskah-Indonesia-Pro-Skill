#!/usr/bin/env python3
"""Fase B — runner API untuk kondisi LLM (B1, B2, ENIP).

K3 = API (temperature 0). Key dibaca dari paper/experiments/.env (satu
key per baris, `KEY=VALUE`, komentar #) atau env var shell:
  anthropic -> ANTHROPIC_API_KEY    (SDK anthropic)
  openai    -> OPENAI_API_KEY       (SDK openai)
  gemini    -> GEMINI_API_KEY       (SDK google-generativeai)
  groq      -> GROQ_API_KEY         (endpoint OpenAI-compatible api.groq.com)

Kondisi:
  b1  : tanpa system prompt, instruksi "Perbaiki naskah ini sesuai PUEBI."
  b2  : system = prompts/system-prompt.md (self-contained), instruksi sama
  enip: system = SKILL.md + references/ + assets/ (aktivasi penuh via API;
        catatan: runtime agent menyediakan progressive disclosure — di API
        semua file diload, overhead diukur terpisah di D3)

Output: runs/<kondisi>/<id>.md (MENTAH) + run_log.json.
Ukuran run: 20 naskah; ENIP dipanggil dengan parameter sesi dari
metadata (gaya, formalitas 5, kalimat sedang, analogi sedang, Edit+Catatan).
"""
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path(__file__).resolve().parents[3] / "skill" / "enip-editor"
RUNS = ROOT / "runs"
CORPUS = ROOT / "corpus"

SESSION = ("Parameter sesi: gaya sesuai gaya naskah (metadata.style), "
           "formalitas 5, panjang kalimat sedang, densitas terminologi "
           "sedang, frekuensi analogi sedang, mode Edit + Catatan, "
           "format referensi APA 7.")
INSTRUCTION = "Perbaiki naskah ini sesuai PUEBI."

DEFAULT_MODEL = {
    "anthropic": "claude-sonnet-4-5",
    "openai": "gpt-4o",
    "gemini": "gemini-2.5-pro",
    "groq": "llama-3.3-70b-versatile",
}


def load_env():
    """Baca paper/experiments/.env -> os.environ (tanpa overwrite shell)."""
    envfile = ROOT / ".env"
    if not envfile.exists():
        return
    for line in envfile.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


def build_enip_system():
    parts = [(SKILL / "SKILL.md").read_text(encoding="utf-8")]
    for sub in ("references", "assets"):
        for f in sorted((SKILL / sub).glob("*")):
            parts.append(f"\n\n===== FILE: {sub}/{f.name} =====\n"
                         + f.read_text(encoding="utf-8"))
    parts.append(f"\n\n===== PARAMETER SESI EKSPERIMEN =====\n{SESSION}")
    return "\n".join(parts)


class Provider:
    def __init__(self, name, model):
        self.name = name
        self.model = model

    def complete(self, system, user):
        if self.name == "anthropic":
            import anthropic
            c = anthropic.Anthropic()
            m = c.messages.create(model=self.model, max_tokens=4096,
                                  temperature=0,
                                  system=system or None,
                                  messages=[{"role": "user",
                                             "content": user}])
            return "".join(b.text for b in m.content if b.type == "text")
        if self.name == "openai":
            from openai import OpenAI
            c = OpenAI()
            msgs = []
            if system:
                msgs.append({"role": "system", "content": system})
            msgs.append({"role": "user", "content": user})
            r = c.chat.completions.create(model=self.model,
                                          temperature=0, messages=msgs)
            return r.choices[0].message.content or ""
        if self.name == "gemini":
            import google.generativeai as genai
            genai.configure()
            model = genai.GenerativeModel(self.model, system_instruction=system)
            return model.generate_content(user, generation_config={
                "temperature": 0}).text or ""
        if self.name == "groq":
            import requests
            msgs = []
            if system:
                msgs.append({"role": "system", "content": system})
            msgs.append({"role": "user", "content": user})
            last = None
            for attempt in range(6):
                try:
                    r = requests.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization":
                                 f"Bearer {os.environ['GROQ_API_KEY']}"},
                        json={"model": self.model, "temperature": 0,
                              "max_tokens": 4096, "messages": msgs},
                        timeout=600)
                    if r.status_code == 429:
                        last = f"429 rate limit"
                        time.sleep(30 * (attempt + 1))
                        continue
                    r.raise_for_status()
                    return (r.json()["choices"][0]["message"]["content"]
                            or "")
                except Exception as e:
                    last = e
                    time.sleep(10 * (attempt + 1))
            raise RuntimeError(f"groq gagal setelah 6 percobaan: {last}")
        raise ValueError(f"provider tak dikenal: {self.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", choices=["b1", "b2", "enip"], required=True)
    ap.add_argument("--provider", choices=list(DEFAULT_MODEL), required=True)
    ap.add_argument("--model", default=None)
    ap.add_argument("--ids", default=None,
                    help="daftar id dipisah koma; default: semua 20")
    ap.add_argument("--force", action="store_true",
                    help="timpa file output yang sudah ada")
    a = ap.parse_args()
    load_env()
    key = {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY",
           "gemini": "GEMINI_API_KEY", "groq": "GROQ_API_KEY"}[a.provider]
    if not os.environ.get(key):
        sys.exit(f"Belum ada {key} di environment — ekspor dulu.")
    prov = Provider(a.provider, a.model or DEFAULT_MODEL[a.provider])
    meta = json.loads((CORPUS / "metadata.json").read_text(encoding="utf-8"))
    ids = a.ids.split(",") if a.ids else [m["id"] for m in meta["corpus"]]
    outdir = RUNS / a.condition
    outdir.mkdir(parents=True, exist_ok=True)
    logpath = RUNS / "run_log.json"
    prev = json.loads(logpath.read_text()) if logpath.exists() else []
    for item in meta["corpus"]:
        if item["id"] not in ids:
            continue
        outfile = outdir / f"{item['id']}.md"
        if outfile.exists() and not a.force:
            print(f"  [resume] {item['id']} sudah ada — dilewati (--force utk ulang)",
                  flush=True)
            continue
        text = (CORPUS / "texts" / f"{item['id']}.txt").read_text(encoding="utf-8")
        user = f"{INSTRUCTION}\n\nNaskah (gaya: {item['style']}):\n\n{text}"
        if a.condition == "enip":
            system = build_enip_system()
        elif a.condition == "b2":
            system = (ROOT / "prompts" / "system-prompt.md").read_text(encoding="utf-8")
        else:
            system = None
        print(f"  [{a.condition}] {item['id']} → {prov.model} …", flush=True)
        out = prov.complete(system, user)
        outfile.write_text(out, encoding="utf-8")
        prev.append({"condition": a.condition, "id": item["id"], "provider": prov.name,
                     "model": prov.model, "temperature": 0,
                     "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                     "prompt_hash": hashlib.sha256(
                         (system or "")[:500].encode()).hexdigest()[:12]})
        logpath.write_text(json.dumps(prev, ensure_ascii=False, indent=2),
                           encoding="utf-8")
        time.sleep(1)
    print(f"Selesai: output di runs/{a.condition}/ (log di-run_log). "
          f"Total entri log: {len(prev)}")


if __name__ == "__main__":
    main()