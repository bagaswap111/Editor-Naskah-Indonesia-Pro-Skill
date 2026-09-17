#!/usr/bin/env python3
"""Ablation judge — Gemini-only version for ablation study evaluation.

Judges ablation outputs (enip_no_puebi, enip_no_style, enip_no_workflow)
using Gemini 3.5 Flash Lite as the single judge.

Usage:
  python3 judge_ablation.py
  python3 judge_ablation.py --full  # restart from scratch
"""
import argparse
import concurrent.futures
import json
import os
import random
import re
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "metrics"
RUNS = ROOT / "runs"
CORPUS = ROOT / "corpus"
SCORES = METRICS / "ablation_scores.json"
QUALITY = Path(__file__).resolve().parents[3] / "skill" / "enip-editor" / "references" / "QUALITY_METRICS.md"

DIMENSI = ["Kejelasan", "Koherensi", "Kedalaman", "Akurasi", "Gaya",
           "Mekanik", "Engagement"]

JUDGE = {"provider": "gemini", "model": "gemini-3.5-flash-lite"}

RUBRIC = QUALITY.read_text(encoding="utf-8")

SYSTEM = (
    "Anda adalah juri kualitas naskah bahasa Indonesia. Anda menilai HASIL "
    "EDITAN terhadap naskah aslinya.\n\n"
    "Rubrik (dari QUALITY_METRICS.md):\n\n" + RUBRIC + "\n\n" +
    "Aturan penilaian:\n"
    "1. Skor setiap dimensi 1-10 (integer).\n"
    "2. Skor Mekanik 10 HANYA jika benar-benar nol kesalahan PUEBI.\n"
    "3. Jika hasil editan memuat catatan yang belum ditindaklanjuti\n"
    "   (mis. '[Sumber?]', 'perlu verifikasi'), skor Akurasi maksimal 8.\n"
    "4. Sertakan justifikasi SATU kalimat untuk setiap dimensi berskor <=6.\n"
    "5. Skor tidak boleh 'kompensasi silang' antar dimensi.\n\n"
    "Keluarkan HANYA satu objek JSON tanpa teks lain:\n"
    '{"skor":{"Kejelasan":8,"Koherensi":8,"Kedalaman":7,"Akurasi":8,'
    '"Gaya":8,"Mekanik":9,"Engagement":7},'
    '"justifikasi":{"<nm_dimensi>":"satu kalimat"}}'
)

TEMPLATE_USER = (
    "Naskah asli:\n\n{source}\n\n"
    "Hasil editan (anonim, ID {anon}):\n\n{edited}\n\n"
    "Beri penilaian 7 dimensi sesuai rubrik. Keluarkan JSON."
)

ABLATION_CONDITIONS = ["enip_no_puebi", "enip_no_style", "enip_no_workflow"]


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


def call_gemini(messages, temperature, timeout=600):
    import requests
    api_key = os.environ.get("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{JUDGE['model']}:generateContent?key={api_key}"
    
    # Extract system and user messages
    system_text = ""
    user_text = ""
    for msg in messages:
        if msg["role"] == "system":
            system_text = msg["content"]
        elif msg["role"] == "user":
            user_text = msg["content"]
    
    body = {
        "contents": [{"parts": [{"text": user_text}]}],
        "generationConfig": {"temperature": temperature, "maxOutputTokens": 2048}
    }
    if system_text:
        body["systemInstruction"] = {"parts": [{"text": system_text}]}
    
    last = None
    for attempt in range(6):
        try:
            r = requests.post(url, json=body, timeout=timeout)
            if r.status_code == 429:
                last = "429 rate limit"
                time.sleep(30 * (attempt + 1))
                continue
            r.raise_for_status()
            data = r.json()
            return data["candidates"][0]["content"]["parts"][0]["text"] or ""
        except Exception as e:
            last = e
            time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"gemini gagal setelah 6 percobaan: {last}")


def parse_json(text):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M)
    dec = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch != "{":
            continue
        try:
            obj, _end = dec.raw_decode(text[i:])
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    raise ValueError(f"tidak ada JSON: {text[:300]!r}")


def norm_skor(obj):
    raw = obj.get("skor", obj)
    skor = {}
    for d in DIMENSI:
        v = raw.get(d)
        if isinstance(v, (int, float)):
            skor[d] = int(round(v))
        else:
            raise ValueError(f"skor {d} bukan angka: {v!r}")
    jus = obj.get("justifikasi", {}) or {}
    return skor, {str(k): str(v) for k, v in jus.items()}


def load_tasks(seed):
    meta = json.loads((CORPUS / "metadata.json").read_text(encoding="utf-8"))
    ids = [m["id"] for m in meta["corpus"]]
    
    # Create anon mapping
    rng = random.Random(seed)
    shuffled = ids[:]
    rng.shuffle(shuffled)
    mapping = {"seed": seed}
    for i, cid in enumerate(shuffled):
        mapping[cid] = f"OUT-{i+1:04d}"
    METRICS.mkdir(exist_ok=True)
    (METRICS / "ablation_anon_map.json").write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    
    tasks = []
    for cond in ABLATION_CONDITIONS:
        for cid in ids:
            src = (CORPUS / "texts" / f"{cid}.txt").read_text(encoding="utf-8")
            outp = RUNS / cond / f"{cid}.md"
            if not outp.exists():
                print(f"  (skip) {cond}/{cid} — output belum ada", flush=True)
                continue
            out = outp.read_text(encoding="utf-8")
            tasks.append((cond, cid, src, out, mapping[cid]))
    return tasks


def save_rows(rows):
    merged = {}
    if SCORES.exists():
        try:
            for row in json.loads(SCORES.read_text(encoding="utf-8")):
                merged[(row["condition"], row["id"], row["judge"],
                        row["trial"])] = row
        except (json.JSONDecodeError, KeyError):
            pass
    for row in rows:
        merged[(row["condition"], row["id"], row["judge"],
                row["trial"])] = row
    tmp = SCORES.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(list(merged.values()),
                              ensure_ascii=False, indent=2),
                   encoding="utf-8")
    os.replace(tmp, SCORES)


def main():
    ap = argparse.ArgumentParser(description="Ablation Judge (Gemini-only)")
    ap.add_argument("--seed", type=int, default=20260815)
    ap.add_argument("--full", action="store_true",
                    help="restart from scratch")
    a = ap.parse_args()
    
    load_env()
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY tidak ditemukan")
    
    tasks = load_tasks(a.seed)
    print(f"Tasks to judge: {len(tasks)}")
    
    existing = set()
    rows = []
    if not a.full and SCORES.exists():
        try:
            rows = json.loads(SCORES.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
        for row in rows:
            existing.add((row["condition"], row["id"], row["judge"],
                          row["trial"]))
    
    lock = threading.Lock()
    done = [0]
    total = len(tasks)
    
    def judge_task(cond, cid, src, out, anon):
        key = (cond, cid, "J1", 0)
        if key in existing:
            return None
        
        msgs = [{"role": "system", "content": SYSTEM},
                {"role": "user",
                 "content": TEMPLATE_USER.format(source=src, edited=out,
                                                 anon=anon)}]
        try:
            txt = call_gemini(msgs, temperature=0)
            skor, jus = norm_skor(parse_json(txt))
            row = {"condition": cond, "id": cid, "judge": "J1",
                   "trial": 0, "provider": "gemini",
                   "model": JUDGE["model"], "anon": anon, "skor": skor,
                   "justifikasi": jus,
                   "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")}
            with lock:
                rows.append(row)
                done[0] += 1
                save_rows(rows)
                print(f"  [{cond}/{cid}] J1 t=0 → "
                      f"{sum(skor.values())/7:.1f} ({done[0]}/{total})",
                      flush=True)
            return row
        except Exception as e:
            print(f"  GAGAL ({e}) {cond}/{cid}", flush=True)
            return None
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        futs = [pool.submit(judge_task, *job) for job in tasks]
        concurrent.futures.wait(futs)
    
    METRICS.mkdir(exist_ok=True)
    save_rows(rows)
    rows = json.loads(SCORES.read_text(encoding="utf-8"))
    by_cond = {}
    for r in rows:
        by_cond.setdefault(r["condition"], []).append(r)
    print("\nSelesai. Entri total:", len(rows))
    for cond, rs in sorted(by_cond.items()):
        mean = (sum(r["skor"][d] for r in rs for d in DIMENSI)
                / (len(rs) * 7)) if rs else 0
        print(f"  {cond}: {len(rs)} penilaian, rata-rata {mean:.2f}")


if __name__ == "__main__":
    main()
