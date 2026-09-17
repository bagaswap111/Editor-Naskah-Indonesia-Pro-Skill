#!/usr/bin/env python3
"""Ablation study runner for ENIP.

Runs ENIP with specific components removed to isolate their contribution.
Conditions:
  - enip_full: existing ENIP (already done)
  - enip_no_puebi: SKILL.md without PUEBI reference
  - enip_no_style: SKILL.md without STYLE_GUIDE reference
  - enip_no_workflow: SKILL.md without WORKFLOW reference

Usage:
  python3 run_ablation.py --condition enip_no_puebi --provider groq
  python3 run_ablation.py --condition enip_no_puebi --provider groq --ids aca_01,aca_02
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
    "groq": "openai/gpt-oss-120b",
}

# Ablation conditions: which references to exclude
ABLATION_EXCLUDE = {
    "enip_no_puebi": ["PUEBI.md"],
    "enip_no_style": ["STYLE_GUIDE.md"],
    "enip_no_workflow": ["WORKFLOW.md"],
}


def load_env():
    envfile = ROOT / ".env"
    if not envfile.exists():
        return
    for line in envfile.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


def build_enip_system(exclude_files=None):
    """Build ENIP system prompt, optionally excluding specific reference files."""
    parts = [(SKILL / "SKILL.md").read_text(encoding="utf-8")]
    parts.append(f"\n\n===== PARAMETER SESI EKSPERIMEN =====\n{SESSION}")
    return "\n".join(parts)


def build_enip_system_ablation(condition):
    """Build ENIP system prompt for ablation study.
    
    For API-based ablation, we simulate reference removal by appending
    a note that specific references are not available. This approximates
    the effect of not loading those references during execution.
    """
    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    
    exclude = ABLATION_EXCLUDE.get(condition, [])
    
    # Build exclusion note
    exclusion_notes = []
    if "PUEBI.md" in exclude:
        exclusion_notes.append(
            "CATATAN ABLASI: Referensi PUEBI.md TIDAK tersedia. "
            "Jangan gunakan aturan PUEBI spesifik. Fokus pada struktur dan gaya."
        )
    if "STYLE_GUIDE.md" in exclude:
        exclusion_notes.append(
            "CATATAN ABLASI: Referensi STYLE_GUIDE.md TIDAK tersedia. "
            "Jangan gunakan gaya spesifik. Fokus pada mekanik dan struktur."
        )
    if "WORKFLOW.md" in exclude:
        exclusion_notes.append(
            "CATATAN ABLASI: Referensi WORKFLOW.md TIDAK tersedia. "
            "Jangan gunakan alur kerja 7 tahap. Edit langsung tanpa struktur tahapan."
        )
    
    parts = [skill_text]
    parts.append(f"\n\n===== PARAMETER SESI EKSPERIMEN =====\n{SESSION}")
    if exclusion_notes:
        parts.append("\n\n" + "\n".join(exclusion_notes))
    return "\n".join(parts)


class Provider:
    def __init__(self, name, model):
        self.name = name
        self.model = model

    def complete(self, system, user):
        import requests
        
        if self.name == "gemini":
            api_key = os.environ.get("GEMINI_API_KEY")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={api_key}"
            
            contents = [{"parts": [{"text": user}]}]
            body = {"contents": contents, "generationConfig": {"temperature": 0, "maxOutputTokens": 4096}}
            
            if system:
                body["systemInstruction"] = {"parts": [{"text": system}]}
            
            last = None
            for attempt in range(6):
                try:
                    r = requests.post(url, json=body, timeout=600)
                    if r.status_code == 429:
                        last = f"429 rate limit"
                        time.sleep(30 * (attempt + 1))
                        continue
                    r.raise_for_status()
                    data = r.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"] or ""
                except Exception as e:
                    last = e
                    time.sleep(10 * (attempt + 1))
            raise RuntimeError(f"gemini gagal setelah 6 percobaan: {last}")
        
        if self.name == "groq":
            msgs = []
            if system:
                msgs.append({"role": "system", "content": system})
            msgs.append({"role": "user", "content": user})
            last = None
            for attempt in range(6):
                try:
                    body = {"model": self.model, "temperature": 0,
                            "max_tokens": 3500, "messages": msgs}
                    if self.model.startswith("openai/gpt-oss"):
                        body["reasoning_effort"] = "low"
                    r = requests.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization":
                                 f"Bearer {os.environ['GROQ_API_KEY']}"},
                        json=body,
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
    ap = argparse.ArgumentParser(description="ENIP Ablation Study Runner")
    ap.add_argument("--condition", 
                    choices=list(ABLATION_EXCLUDE.keys()),
                    required=True)
    ap.add_argument("--provider", choices=list(DEFAULT_MODEL), default="groq")
    ap.add_argument("--model", default=None)
    ap.add_argument("--ids", default=None,
                    help="comma-separated IDs; default: all 10 injected")
    ap.add_argument("--force", action="store_true",
                    help="overwrite existing output files")
    a = ap.parse_args()
    
    load_env()
    key = {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY",
           "gemini": "GEMINI_API_KEY", "groq": "GROQ_API_KEY"}[a.provider]
    if not os.environ.get(key):
        sys.exit(f"Belum ada {key} di environment — ekspor dulu.")
    
    prov = Provider(a.provider, a.model or DEFAULT_MODEL[a.provider])
    meta = json.loads((CORPUS / "metadata.json").read_text(encoding="utf-8"))
    
    # Default: only injected manuscripts (have ground truth)
    injected_ids = [m["id"] for m in meta["corpus"] if m["variant"] == "injected"]
    ids = a.ids.split(",") if a.ids else injected_ids
    
    outdir = RUNS / a.condition
    outdir.mkdir(parents=True, exist_ok=True)
    logpath = RUNS / "run_log.json"
    prev = json.loads(logpath.read_text()) if logpath.exists() else []
    
    print(f"Ablation condition: {a.condition}")
    print(f"Excluding: {ABLATION_EXCLUDE[a.condition]}")
    print(f"Manuscripts: {len(ids)}")
    print(f"Model: {prov.model}")
    print()
    
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
        system = build_enip_system_ablation(a.condition)
        
        print(f"  [{a.condition}] {item['id']} → {prov.model} …", flush=True)
        out = prov.complete(system, user)
        outfile.write_text(out, encoding="utf-8")
        
        prev.append({
            "condition": a.condition, "id": item["id"], 
            "provider": prov.name, "model": prov.model, 
            "temperature": 0,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "prompt_hash": hashlib.sha256(
                (system or "")[:500].encode()).hexdigest()[:12],
            "ablation_excluded": ABLATION_EXCLUDE[a.condition]
        })
        logpath.write_text(json.dumps(prev, ensure_ascii=False, indent=2),
                           encoding="utf-8")
        time.sleep(1)
    
    print(f"\nSelesai: output di runs/{a.condition}/ (log di run_log.json). "
          f"Total entri log: {len(prev)}")


if __name__ == "__main__":
    main()
