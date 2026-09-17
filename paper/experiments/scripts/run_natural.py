#!/usr/bin/env python3
"""Natural manuscript evaluation runner for ENIP.

Runs ENIP on natural (non-synthetic) manuscripts extracted from buku-kolaborasi-llm.
Selects 20 manuscripts balanced across styles for evaluation.

Usage:
  python3 run_natural.py --provider gemini --model gemini-3.5-flash-lite
  python3 run_natural.py --provider gemini --model gemini-3.5-flash-lite --ids bkl_01_01,bkl_03_01
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
NATURAL_CORPUS = CORPUS / "buku-kolaborasi-llm" / "texts"

SESSION = ("Parameter sesi: gaya sesuai gaya naskah (metadata.style), "
           "formalitas 5, panjang kalimat sedang, densitas terminologi "
           "sedang, frekuensi analogi sedang, mode Edit + Catatan, "
           "format referensi APA 7.")
INSTRUCTION = "Perbaiki naskah ini sesuai PUEBI."

DEFAULT_MODEL = {
    "gemini": "gemini-3.5-flash-lite",
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


def build_enip_system():
    parts = [(SKILL / "SKILL.md").read_text(encoding="utf-8")]
    parts.append(f"\n\n===== PARAMETER SESI EKSPERIMEN =====\n{SESSION}")
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
        raise ValueError(f"provider tak dikenal: {self.name}")


# Natural manuscript selection: 20 manuscripts balanced across styles
NATURAL_SELECTION = [
    # Popular-educational (5)
    "bkl_01_01", "bkl_03_01", "bkl_05_01", "bkl_07_01", "bkl_09_01",
    # Academic (5)
    "bkl_02_01", "bkl_04_01", "bkl_08_01", "bkl_10_01", "bkl_15_01",
    # Journalistic (5)
    "bkl_06_01", "bkl_12_01", "bkl_06_02", "bkl_12_02", "bkl_06_03",
    # Persuasive (5)
    "bkl_18_01", "bkl_19_01", "bkl_18_02", "bkl_19_02", "bkl_18_03",
]


def main():
    ap = argparse.ArgumentParser(description="ENIP Natural Manuscript Runner")
    ap.add_argument("--provider", choices=list(DEFAULT_MODEL), default="gemini")
    ap.add_argument("--model", default=None)
    ap.add_argument("--ids", default=None,
                    help="comma-separated IDs; default: 20 balanced selection")
    ap.add_argument("--force", action="store_true",
                    help="overwrite existing output files")
    a = ap.parse_args()
    
    load_env()
    key = {"gemini": "GEMINI_API_KEY"}[a.provider]
    if not os.environ.get(key):
        sys.exit(f"Belum ada {key} di environment — ekspor dulu.")
    
    prov = Provider(a.provider, a.model or DEFAULT_MODEL[a.provider])
    
    # Load metadata if available, otherwise use filename-based detection
    meta_path = CORPUS / "buku-kolaborasi-llm" / "metadata_natural.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        ids = a.ids.split(",") if a.ids else NATURAL_SELECTION
    else:
        # Fallback: discover from filenames
        ids = a.ids.split(",") if a.ids else NATURAL_SELECTION
    
    outdir = RUNS / "natural"
    outdir.mkdir(parents=True, exist_ok=True)
    logpath = RUNS / "natural_run_log.json"
    prev = json.loads(logpath.read_text()) if logpath.exists() else []
    
    print(f"Natural manuscript evaluation")
    print(f"Manuscripts: {len(ids)}")
    print(f"Model: {prov.model}")
    print()
    
    for manuscript_id in ids:
        textfile = NATURAL_CORPUS / f"{manuscript_id}.txt"
        if not textfile.exists():
            print(f"  [skip] {manuscript_id} — file not found")
            continue
        
        outfile = outdir / f"{manuscript_id}.md"
        if outfile.exists() and not a.force:
            print(f"  [resume] {manuscript_id} sudah ada — dilewati (--force utk ulang)",
                  flush=True)
            continue
        
        text = textfile.read_text(encoding="utf-8")
        user = f"{INSTRUCTION}\n\nNaskah:\n\n{text}"
        system = build_enip_system()
        
        print(f"  [natural] {manuscript_id} → {prov.model} …", flush=True)
        out = prov.complete(system, user)
        outfile.write_text(out, encoding="utf-8")
        
        prev.append({
            "condition": "natural", "id": manuscript_id, 
            "provider": prov.name, "model": prov.model, 
            "temperature": 0,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "prompt_hash": hashlib.sha256(
                (system or "")[:500].encode()).hexdigest()[:12]
        })
        logpath.write_text(json.dumps(prev, ensure_ascii=False, indent=2),
                           encoding="utf-8")
        time.sleep(1)
    
    print(f"\nSelesai: output di runs/natural/ (log di natural_run_log.json). "
          f"Total entri log: {len(prev)}")


if __name__ == "__main__":
    main()
