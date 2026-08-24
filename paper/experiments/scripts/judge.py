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


def parse_duration(s):
    """Groq memakai durasi seperti '120ms', '1m26.4s', '1h10m'."""
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        pass
    total = 0.0
    for num, u in re.findall(r"(\d+(?:\.\d+)?)\s*(ms|s|m|h)", s):
        total += float(num) * {"ms": 0.001, "s": 1, "m": 60,
                               "h": 3600}[u]
    return total or None


_model_last = {}
_model_gate = threading.Lock()


def _reserve_slot(gkey):
    """Pesan satu slot waktu (atomik), lalu tidur sampai giliran itu."""
    interval = float(os.environ.get("JUDGE_MIN_INTERVAL", "32"))
    with _model_gate:
        now = time.time()
        start = max(_model_last.get(gkey, 0.0), now)
        _model_last[gkey] = start + interval
    wait = start - now
    if wait > 0:
        time.sleep(wait)


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
               # 2048 cukup untuk JSON; qwen thinking butuh ruang lebih
               "max_tokens": 3072 if "qwen" in model else 2048,
               "messages": messages}
    if model.startswith("openai/gpt-oss"):
        # model reasoning — token reasoning masuk completion
        payload["reasoning_effort"] = "low"
    gkey = (provider, model)
    _reserve_slot(gkey)
    last = None
    for attempt in range(8):
        r = requests.post(url, headers=headers, json=payload,
                          timeout=timeout)
        if r.status_code == 429:
            body = (r.text or "").lower()
            # kuota HARIAN: percuma diulang hari ini — gagal cepat,
            # putaran berikutnya (judge_loop) yang mengisi ulang
            if "tokens per day" in body or "tpd" in body or \
                    "exceeded your current quota" in body:
                raise RuntimeError(f"HARD_QUOTA {provider} {model}")
            last = "429"
            reset = parse_duration(
                r.headers.get("retry-after")
                or r.headers.get("x-ratelimit-reset-tokens"))
            time.sleep(min(max(reset or 20.0, 15.0), 90.0))
            continue
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"] or ""
    raise RuntimeError(f"{provider} 429 berulang: {last}")


def parse_json(text):
    # qwen3 hybrid-thinking menyisipkan <think>…</think> (bisa memuat
    # kurung kurawal) di dalam content — buang sebelum parsing.
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


def save_rows(rows):
    """Tulis scores.json dengan MERGE dari isi file saat ini.

    Beberapa proses juri (Groq & Gemini) bisa berjalan paralel pada
    file yang sama; tanpa merge, penulis cepat menimpa baris proses
    lain. Kunci unik: (condition, id, judge, trial).
    """
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
    os.replace(tmp, SCORES)  # atomik: pembaca tak pernah lihat file parsial


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
        try:
            rows = json.loads(SCORES.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print("PERINGATAN: scores.json tak terbaca — mulai kosong",
                  flush=True)
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
                    # simpan inkremental + merge: aman dihentikan kapan pun
                    save_rows(rows)
                    print(f"  [{cond}/{cid}] {jname} t={trial} → "
                          f"{sum(skor.values())/7:.1f} ({done}/{total})",
                          flush=True)
                return row
            except Exception as e:
                last = e
                if "HARD_QUOTA" in str(e):
                    break  # kuota harian habis — jangan buang waktu
                if "429" in str(e):
                    time.sleep(30 * (attempt + 1))
                else:
                    time.sleep(5 * (attempt + 1))
        with lock:
            print(f"  GAGAL ({last}) {cond}/{cid} {jname} t={trial}", flush=True)
        return None

    # TPM 8K free tier: antrean per model diselingi agar model lambat
    # (mis. TPD rolling) tidak menghambat model lain
    workers = int(os.environ.get("JUDGE_WORKERS",
                                 "6" if any(JUDGES[j]["provider"] == "groq"
                                            for j in judges) else 1))
    antrian = {j: [] for j in judges}
    for cond, cid, src, out, anon in tasks:
        for jname in judges:
            for trial in JUDGES[jname]["trials"]:
                antrian[jname].append((cond, cid, src, out, anon,
                                       jname, trial))
    jobs = []
    while any(antrian.values()):
        for jname in judges:
            if antrian[jname]:
                jobs.append(antrian[jname].pop(0))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futs = [pool.submit(judge_task, *job) for job in jobs]
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