#!/usr/bin/env python3
"""Fase C2 — juri kualitas untuk output editor B1/B2/ENIP.

Juri (K2, berbeda dari editor K1=openai/gpt-oss-120b):
  J1: qwen/qwen3.6-27b             (Groq)   — juri utama, trial 0 & 0.7
  J2: openai/gpt-oss-20b           (Groq)   — uji sensitivitas model lemah
  J3: gemini-3.5-flash             (Google) — uji sensitivitas lintas-penyedia

Penilaian ANONIM: juri hanya melihat "naskah asli" + "hasil editan" dengan
label acak (OUT-####) — kondisi B1/B2/ENIP tidak pernah disebut. Peta label
disimpan di metrics/judge_anon_map.json (seed tetap, reproducibel) sehingga
run ulang tidak mengubah label.

Idempotent: entri (condition, id, judge, trial) yang sudah ada di
metrics/scores.json dilewati — aman di-hentikan dan dilanjutkan.

Rubrik: 7 dimensi + aturan dari skill/enip-editor/references/QUALITY_METRICS.md
(skor 1-10; Mekanik 10 hanya bila nol kesalahan; Akurasi ≤8 bila ada
catatan belum ditindaklanjuti; justifikasi wajib untuk skor ≤6).

Usage:
  python3 scripts/judge.py                     # semua juri & trial
  python3 scripts/judge.py --judges J1,J3      # subset juri
  python3 scripts/judge.py --full              # mulai dari awal (abaikan scores.json)
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
SCORES = METRICS / "scores.json"
ANON_MAP = METRICS / "judge_anon_map.json"
ANON_MAP_SRC = METRICS / "judge_anon_map_source.json"

QUALITY = Path(__file__).resolve().parents[3] / "skill" / "enip-editor" / "references" / "QUALITY_METRICS.md"

DIMENSI = ["Kejelasan", "Koherensi", "Kedalaman", "Akurasi", "Gaya",
           "Mekanik", "Engagement"]

JUDGES = {
    "J1": {"provider": "groq", "model": "qwen/qwen3.6-27b",
           "trials": [0, 0.7]},
    # Deviasi #6/#7: llama-3.1-8b-instant decommissioned → gpt-oss-20b
    # (satu family dgn editor — dicatat sebagai keterbatasan)
    "J2": {"provider": "groq", "model": "openai/gpt-oss-20b",
           "trials": [0, 0.7]},
    "J3": {"provider": "gemini", "model": "gemini-3.5-flash", "trials": [0]},
}

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


def call(provider, model, messages, temperature, timeout=600):
    import requests
    if provider == "groq":
        url = "https://api.groq.com/openai/v1/chat/completions"
        key = os.environ["GROQ_API_KEY"]
    elif provider == "gemini":
        url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
        key = os.environ["GEMINI_API_KEY"]
    else:
        raise ValueError(f"juri tak dikenal: {provider}")
    headers = {"Authorization": f"Bearer {key}"}
    payload = {"model": model, "temperature": temperature,
               # 2048: total request (rubric+naskah+cap) aman di TPM 8K
               "max_tokens": 2048, "messages": messages}
    if model.startswith("openai/gpt-oss"):
        # model reasoning — token reasoning masuk completion
        payload["reasoning_effort"] = "low"
    last = None
    for attempt in range(8):
        r = requests.post(url, headers=headers, json=payload,
                          timeout=timeout)
        if r.status_code == 429:
            last = "429"
            wa = r.headers.get("retry-after")
            sleep_s = max(float(wa), 20.0) if wa else 30.0 * (attempt + 1)
            time.sleep(min(sleep_s, 300.0))
            continue
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"] or ""
    raise RuntimeError(f"{provider} 429 berulang: {last}")


def parse_json(text):
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"tidak ada JSON: {text[:300]!r}")
    return json.loads(text[start:end + 1])


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


def load(seed, conditions=("b1", "b2", "enip")):
    meta = json.loads((CORPUS / "metadata.json").read_text(encoding="utf-8"))
    ids = [m["id"] for m in meta["corpus"]]
    if ANON_MAP.exists():
        mapping = json.loads(ANON_MAP.read_text(encoding="utf-8"))
    else:
        rng = random.Random(seed)
        shuffled = ids[:]
        rng.shuffle(shuffled)
        mapping = {"seed": seed}
        for i, cid in enumerate(shuffled):
            mapping[cid] = f"OUT-{i+1:04d}"
        METRICS.mkdir(exist_ok=True)
        ANON_MAP.write_text(json.dumps(mapping, ensure_ascii=False, indent=2),
                            encoding="utf-8")
    tasks = []
    for cond in conditions:
        for cid in ids:
            src = (CORPUS / "texts" / f"{cid}.txt").read_text(encoding="utf-8")
            outp = RUNS / cond / f"{cid}.md"
            if not outp.exists():
                print(f"  (skip) {cond}/{cid} — output belum ada", flush=True)
                continue
            out = outp.read_text(encoding="utf-8")
            tasks.append((cond, cid, src, out, mapping[cid]))
    return tasks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--judges", default="J1,J2,J3")
    ap.add_argument("--seed", type=int, default=20260815)
    ap.add_argument("--full", action="store_true",
                    help="abaikan scores.json yang sudah ada (mulai ulang)")
    a = ap.parse_args()

    envfile = ROOT / ".env"
    if envfile.exists():
        for line in envfile.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

    tasks = load(a.seed)
    judges = a.judges.split(",")
    needed = {JUDGES[j]["provider"] for j in judges}
    if "groq" in needed and not os.environ["GROQ_API_KEY"]:
        sys.exit("GROQ_API_KEY tidak ditemukan (cek paper/experiments/.env)")
    if "gemini" in needed and not os.environ["GEMINI_API_KEY"]:
        sys.exit("GEMINI_API_KEY tidak ditemukan (cek paper/experiments/.env)")
    total = sum(len(tasks) * len(JUDGES[j]["trials"]) for j in judges)
    done = 0

    existing = set()
    rows = []
    if not a.full and SCORES.exists():
        rows = json.loads(SCORES.read_text(encoding="utf-8"))
        for row in rows:
            existing.add((row["condition"], row["id"], row["judge"],
                          row["trial"]))

    lock = threading.Lock()

    def judge_task(cond, cid, src, out, anon, jname, trial):
        nonlocal done
        if (cond, cid, jname, trial) in existing:
            return None
        j = JUDGES[jname]
        msgs = [{"role": "system", "content": SYSTEM},
                {"role": "user",
                 "content": TEMPLATE_USER.format(source=src, edited=out,
                                                 anon=anon)}]
        last = None
        for attempt in range(3):
            try:
                txt = call(j["provider"], j["model"], msgs, trial)
                skor, jus = norm_skor(parse_json(txt))
                row = {"condition": cond, "id": cid, "judge": jname,
                       "trial": trial, "provider": j["provider"],
                       "model": j["model"], "anon": anon, "skor": skor,
                       "justifikasi": jus,
                       "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")}
                with lock:
                    rows.append(row)
                    done += 1
                    print(f"  [{cond}/{cid}] {jname} t={trial} → "
                          f"{sum(skor.values())/7:.1f} ({done}/{total})",
                          flush=True)
                return row
            except Exception as e:
                last = e
                if "429" in str(e):
                    time.sleep(30 * (attempt + 1))
                else:
                    time.sleep(5 * (attempt + 1))
        with lock:
            print(f"  GAGAL ({last}) {cond}/{cid} {jname} t={trial}", flush=True)
        return None

    groq_futures = []
    workers = 1 if all(JUDGES[j]["provider"] == "gemini" for j in judges) else 4
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for cond, cid, src, out, anon in tasks:
            for jname in judges:
                for trial in JUDGES[jname]["trials"]:
                    f = pool.submit(judge_task, cond, cid, src, out, anon,
                                    jname, trial)
                    groq_futures.append(f)
                    if JUDGES[jname]["provider"] == "gemini":
                        f.result()
                        time.sleep(15)
        concurrent.futures.wait(groq_futures)

    METRICS.mkdir(exist_ok=True)
    SCORES.write_text(json.dumps(rows, ensure_ascii=False, indent=2),
                      encoding="utf-8")
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