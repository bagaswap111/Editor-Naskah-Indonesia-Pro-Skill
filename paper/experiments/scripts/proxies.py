#!/usr/bin/env python3
"""C4 — Proksi koherensi deterministik (proxies.py).

Per naskah (per kondisi):
  - variansi panjang kalimat (std & cv, target sedang & terkontrol)
  - rasio konjungsi unik / konjungsi total (variasi transisi)
  - repetisi leksikal: 10 kata isi paling sering / total kata

Kondisi 'input' = baseline teks asli. Output: metrics/proxies.json
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
RUNS = ROOT / "runs"
METRICS = ROOT / "metrics"

KONJUNGSI = re.compile(
    r"\b(tetapi|melainkan|sedangkan|namun|walaupun|meskipun|karena|sebab|"
    r"oleh karena itu|dengan demikian|sementara itu|selain itu|kemudian|"
    r"lalu|akhirnya|sehingga|maka|atau|dan|serta|adapun|sedangkan)\b",
    re.IGNORECASE)


def sentences(text):
    parts = re.split(r"(?<=[.!?…])\s+", text.strip())
    return [p for p in parts if len(p.split()) > 1]


def stats(text):
    sents = sentences(text)
    lengths = [len(s.split()) for s in sents]
    mean = sum(lengths) / len(lengths) if lengths else 0
    var = sum((x - mean) ** 2 for x in lengths) / len(lengths) if lengths else 0
    std = var ** 0.5
    words = re.findall(r"[A-Za-zÀ-ÿ]+", text.lower())
    kw = [w for w in words if len(w) > 3]
    conj_all = KONJUNGSI.findall(text)
    top10 = Counter(kw).most_common(10)
    return {
        "n_sentences": len(sents),
        "sent_len_mean": round(mean, 2),
        "sent_len_std": round(std, 2),
        "sent_len_cv": round(std / mean, 3) if mean else None,
        "conj_unique": len(set(c.lower() for c in conj_all)),
        "conj_total": len(conj_all),
        "conj_variety_ratio": round(len(set(c.lower() for c in conj_all)) / len(conj_all), 3) if conj_all else None,
        "lexical_top10_share": round(sum(n for _, n in top10) / len(kw), 4) if kw else None,
        "top10_words": [f"{w}:{n}" for w, n in top10],
    }


def main():
    meta = json.loads((CORPUS / "metadata.json").read_text(encoding="utf-8"))
    out = {}
    for cond in ["input"]:
        per = {}
        for item in meta["corpus"]:
            tid = item["id"]
            text = (CORPUS / "texts" / f"{tid}.txt").read_text(encoding="utf-8")
            per[tid] = stats(text)
        out[cond] = per
    (METRICS / "proxies.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    ms = [v["sent_len_cv"] for v in out["input"].values() if v["sent_len_cv"]]
    print(f"Proksi input (baseline) untuk {len(out['input'])} naskah:")
    print(f"  CV panjang kalimat: mean {sum(ms)/len(ms):.3f}")
    print("  Lihat metrics/proxies.json untuk rincian per naskah.")


if __name__ == "__main__":
    main()