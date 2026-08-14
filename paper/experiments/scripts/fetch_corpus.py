#!/usr/bin/env python3
"""Fetch real-text corpus sets for ENIP experiments.

Sources (all public, license-clean):
  wikipedia : Kategori:Artikel pilihan (id) - CC BY-SA 4.0 (via API extracts)
  voa       : voaindonesia.com/rss/          - public domain (US gov work)
  tc        : theconversation.com/id/articles.atom - CC BY-ND 4.0

Sampling: deterministic random.sample(sorted(candidates), k) with fixed seed.
Output per source: texts/<id>.txt + metadata.json + README.md
"""
import argparse
import hashlib
import json
import os
import random
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET

import requests
import lxml.html

UA = "ENIP-research/0.1 (korpus teks untuk evaluasi riset; hanya artikel publik)"
SEED = 20260814
SLEEP = 1.2

JAWI = "https://id.wikipedia.org/w/api.php"


def log(msg):
    print(msg, file=sys.stderr)


def get(url, **kw):
    kw.setdefault("headers", {"User-Agent": UA})
    kw.setdefault("timeout", 30)
    for attempt in range(3):
        try:
            r = requests.get(url, **kw)
            r.raise_for_status()
            return r
        except Exception as e:
            log(f"  retry {attempt+1} untuk {url}: {e}")
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"gagal fetch {url}")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def finish(dirpath, meta, text_files):
    os.makedirs(os.path.join(dirpath, "texts"), exist_ok=True)
    items = []
    for i, (fname, text, data) in enumerate(text_files):
        p = os.path.join(dirpath, "texts", fname)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        with open(p, "rb") as f:
            digest = sha256_bytes(f.read())
        data.update({"id": fname.rsplit(".", 1)[0], "words": len(text.split()),
                      "sha256": digest, "sample_index": i})
        items.append(data)
        log(f"  [dipilih {i}] {fname}: {data['words']} kata")
    meta["items"] = items
    with open(os.path.join(dirpath, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    write_readme(dirpath, meta)


def write_readme(dirpath, meta):
    rows = "\n".join(
        f"| {it['id']} | {it['title'][:70]} | {it['words']} | `{it['sha256'][:10]}…` |"
        for it in meta["items"])
    readme = f"""# Set Bahan Uji: {meta['source']['name']}

Sumber: {meta['source']['url']} · Lisensi: {meta['source']['license']}

## Karakteristik
- Register: {meta['source']['register']}
- Catatan sumber: {meta['source']['note']}

## Isi ({len(meta['items'])} naskah)

| id | Judul | Kata | SHA-256 (awal) |
|---|---|---|---|
{rows}

Catatan: `texts/*.txt` = teks bersih hasil ekstraksi (input runner eksperimen).
Orisinal dapat diakses via URL pada metadata.json. Teks tidak diterbitkan
ulang di paper — hanya statistik yang dilaporkan, setiap angka dirujuk ke
file set ini (kebijakan sama dengan set buku-kolaborasi-llm).

## Sampling (reproduksi)
```python
import random
random.seed({meta['sampling']['seed']})
sample = random.sample(sorted(candidates), k={meta['sampling']['k']})
```
Kandidat = {meta['sampling']['candidates_total']} item tersedia saat pengambilan
({meta['exported_at']} WIB). Skrip pengambil: `scripts/fetch_corpus.py`.
"""
    with open(os.path.join(dirpath, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)


# ---------------- Wikipedia ----------------

def wiki_candidates():
    titles, cont = [], {}
    while True:
        params = {"action": "query", "list": "categorymembers",
                  "cmtitle": "Kategori:Artikel pilihan", "cmnamespace": 0,
                  "cmtype": "page", "cmlimit": "500", "format": "json"}
        params.update(cont)
        r = get(JAWI, params=params).json()
        titles += [m["title"] for m in r["query"]["categorymembers"]]
        if "continue" not in r:
            break
        cont = {"cmcontinue": r["continue"]["cmcontinue"]}
    return sorted(set(titles))


def wiki_fetch(outdir, k, seed):
    log("Wikipedia: enumerasi Kategori:Artikel pilihan…")
    cands = wiki_candidates()
    log(f"  {len(cands)} artikel ns=0 di kategori")
    chosen = random.Random(seed).sample(cands, min(k, len(cands)))
    files = []
    # catatan: prop=extracts hanya mengisi extract untuk judul pertama dalam
    # satu batch (limitasi ekstensi TextExtracts) -> fetch per judul
    for t in chosen:
        time.sleep(SLEEP)
        pg = get(JAWI, params={"action": "query", "prop": "extracts",
                               "explaintext": 1, "titles": t,
                               "format": "json", "redirects": 1}).json()["query"]["pages"]
        ext = next(p.get("extract", "") for p in pg.values())
        if not ext:
            log(f"  PERINGATAN: ekstrak kosong untuk {t}")
            continue
        slug = re.sub(r"[^A-Za-z0-9._-]+", "_", t).strip("_").lower()
        fname = f"wikipedia-id_{slug}.txt"
        files.append((fname, f"{t}\n\n{ext}", {
            "title": t, "url": f"https://id.wikipedia.org/wiki/{urllib.parse.quote(t)}",
            "license": "CC BY-SA 4.0 (default lisensi Wikipedia Indonesia; cek footer artikel per item)"}))
    meta = {"source": {"name": "Wikipedia Bahasa Indonesia (Kategori:Artikel pilihan)",
                       "url": JAWI, "license": "CC BY-SA 4.0",
                       "register": "populer-ensiklopedis, semi-formal",
                       "note": "Teks via prop=extracts (explaintext=1); kalimat pertama = judul artikel"},
            "sampling": {"seed": seed, "k": len(files), "candidates_total": len(cands),
                         "method": "random.sample(sorted(kategori ns=0), k)"},
            "exported_at": time.strftime("%Y-%m-%d %H:%M")}
    finish(os.path.join(outdir, "wikipedia-id"), meta, files)


# ---------------- VOA ----------------

def handle_children(elt):
    for e in elt.xpath(".//script | .//style | .//figure | .//figcaption | .//nav | .//iframe | .//form"):
        e.getparent().remove(e)


def block_text(root):
    """Gabungkan blok <p>/<h*> dengan pemisah paragraf, lalu sisipkan spasi
    untuk kalimat yang menyatu akibat elemen inline (batas tanda baca)."""
    blocks = []
    for el in root.xpath(".//p | .//h2 | .//h3 | .//h4 | .//li"):
        t = " ".join(el.text_content().split())
        if t:
            blocks.append(t)
    text = "\n\n".join(blocks)
    text = re.sub(r"(?<=[.!?])(?=[A-Z\"“’])", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def voa_extract(html):
    doc = lxml.html.fromstring(html)
    root = None
    for sel in ["//*[contains(@class,'wsw')]", "//article"]:
        hit = doc.xpath(sel)
        if hit:
            root = hit[0]
            break
    if root is None:
        return ""
    handle_children(root)
    text = block_text(root)
    return text if len(text.split()) >= 250 else ""


def sample_until_valid(cands, k, seed, fetch_one, log_label):
    """Sample deterministik tanpa pengembalian sampai k item valid.
    Item gagal ekstrak dicatat di skipped (dokumentasi sampling)."""
    rng = random.Random(seed)
    remaining = list(cands)
    files, skipped, rounds = [], [], 0
    while len(files) < k and remaining:
        chosen = rng.sample(remaining, min(len(remaining), k - len(files)))
        remaining = [c for c in remaining if c not in chosen]
        rounds += 1
        for i, url in enumerate(chosen):
            log(f"  {log_label} (ronde {rounds}, item {i+1}): {url}")
            res = fetch_one(url)
            if res is None:
                skipped.append(url)
                log(f"    gagal ekstrak -> dicatat skipped")
                continue
            files.append(res)
            if len(files) == k:
                break
    return files, skipped, rounds, len(cands) - len(remaining)


def voa_fetch(outdir, k, seed):
    log("VOA: ambil RSS kategori Berita …")
    feed = get("https://www.voaindonesia.com/api/zmgqol-vomx-tpeympp").content
    root = ET.fromstring(feed)
    items = []
    for item in root.iter("item"):
        link = item.findtext("link"); title = item.findtext("title")
        if link and title:
            items.append((link.strip(), title.strip()))
    cands = sorted(set(l for l, _ in items))
    by_url = {l: t for l, t in items}
    log(f"  {len(cands)} item di RSS")

    def fetch_one(url):
        html = get(url).text
        text = voa_extract(html)
        if not text:
            return None
        slug = re.sub(r"[^A-Za-z0-9._-]+", "_", re.sub(r"^https?://[^/]+/(?:a/)?", "", url)).strip("_").lower()
        return (f"voa-id_{slug}.txt", text, {
            "title": by_url[url], "url": url,
            "license": "Public domain (karya Pemerintah AS - Voice of America)",
            "note": "Ekstrak <div class=wsw>; boilerplate (nav/figure) dibuang"})

    files, skipped, rounds, _ = sample_until_valid(cands, k, seed, fetch_one, "fetch artikel")
    for url in skipped:
        time.sleep(SLEEP)
    meta = {"source": {"name": "VOA Indonesia (kategori Berita)", "url": "https://www.voaindonesia.com",
                       "license": "Public domain (US gov work)", "register": "jurnalistik, berita",
                       "note": "Feed RSS kategori Berita (/api/zmgqol-…); item gagal ekstrak (video/laporan audio) dilewati dan dicatat"},
            "sampling": {"seed": seed, "k": k, "candidates_total": len(cands),
                         "skipped": skipped, "resample_rounds": rounds,
                         "method": "random.sample(sorted(set(link RSS)), k) dengan resampling sisa sampai k valid"},
            "exported_at": time.strftime("%Y-%m-%d %H:%M")}
    finish(os.path.join(outdir, "voa-indonesia"), meta, files)


# ---------------- The Conversation ----------------

ATOM = "{http://www.w3.org/2005/Atom}"


def tc_extract(html):
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    if m:
        try:
            data = json.loads(m.group(1))
            if isinstance(data, list):
                data = next((d for d in data if isinstance(d, dict) and d.get("articleBody")), None)
            if isinstance(data, dict) and data.get("articleBody"):
                return data["articleBody"].strip()
        except json.JSONDecodeError:
            pass
    doc = lxml.html.fromstring(html)
    for sel in ["//div[@itemprop='articleBody']",
                "//div[contains(@class,'content')]//div[contains(@class,'content')]"]:
        hit = doc.xpath(sel)
        if hit:
            handle_children(hit[0])
            t = hit[0].text_content().strip()
            if len(t.split()) > 150:
                return t
    return ""


def tc_fetch(outdir, k, seed):
    log("TC: ambil Atom https://theconversation.com/id/articles.atom …")
    root = ET.fromstring(get("https://theconversation.com/id/articles.atom").content)
    entries = []
    for e in root.iter(ATOM + "entry"):
        title = e.findtext(ATOM + "title")
        link = None
        for ln in e.findall(ATOM + "link"):
            if ln.get("rel") in (None, "alternate"):
                link = ln.get("href"); break
        if title and link:
            entries.append((link.strip(), title.strip()))
    cands = sorted(set(l for l, _ in entries))
    by_url = {l: t for l, t in entries}
    log(f"  {len(cands)} entri di feed")

    def fetch_one(url):
        html = get(url).text
        text = tc_extract(html)
        if not text:
            return None
        slug = re.sub(r"[^A-Za-z0-9._-]+", "_", re.sub(r"^https?://[^/]+/", "", url)).strip("_").lower()
        return (f"theconversation-id_{slug}.txt", text, {
            "title": by_url[url], "url": url,
            "license": "CC BY-ND 4.0",
            "note": "Ekstrak JSON-LD articleBody (fallback: div artikelBody)"})

    files, skipped, rounds, _ = sample_until_valid(cands, k, seed, fetch_one, "fetch artikel")
    for url in skipped:
        time.sleep(SLEEP)
    meta = {"source": {"name": "The Conversation Indonesia", "url": "https://theconversation.com/id",
                       "license": "CC BY-ND 4.0", "register": "opini/argumentatif populer-akademik",
                       "note": "Feed Atom /id/articles.atom; item gagal ekstrak dilewati dan dicatat"},
            "sampling": {"seed": seed, "k": k, "candidates_total": len(cands),
                         "skipped": skipped, "resample_rounds": rounds,
                         "method": "random.sample(sorted(set(link atom)), k) dengan resampling sisa sampai k valid"},
            "exported_at": time.strftime("%Y-%m-%d %H:%M")}
    finish(os.path.join(outdir, "the-conversation-id"), meta, files)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", choices=["wikipedia", "voa", "tc"])
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--outdir", default="paper/experiments/corpus")
    a = ap.parse_args()
    fn = {"wikipedia": wiki_fetch, "voa": voa_fetch, "tc": tc_fetch}[a.source]
    fn(a.outdir, a.k, a.seed)


if __name__ == "__main__":
    main()