#!/usr/bin/env python3
"""Extract natural manuscripts from buku-kolaborasi-llm for ENIP corpus expansion.

Selects sub-babs from different chapters, extracts body text (skipping headers),
and segments into 400-600 word passages. Outputs to corpus/buku-kolaborasi-llm/texts/.

Usage:
  python3 extract_natural_corpus.py --extract
  python3 extract_natural_corpus.py --list
"""
import argparse
import json
import os
import re
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUKU_ROOT = Path("/Users/bagaskorosaputro/Documents/GithubDesktop/buku-kolaborasi-llm/konten")
CORPUS_DIR = ROOT / "corpus" / "buku-kolaborasi-llm"
TEXTS_DIR = CORPUS_DIR / "texts"
METADATA_FILE = CORPUS_DIR / "metadata_natural.json"

SEED = 20260917
TARGET_WORDS = (400, 600)

# Selected sub-babs: 2 per chapter for diversity
SELECTIONS = [
    # Jilid 1
    ("jilid-1", "bab-01-model", "sub-bab-1.md", "pop", "populer-edukatif", "Evolusi Transformer ke Lokal"),
    ("jilid-1", "bab-01-model", "sub-bab-3.md", "aca", "akademis", "Arsitektur Attention dan Positional Encoding"),
    ("jilid-1", "bab-02-hardware", "sub-bab-2.md", "pop", "populer-edukatif", "Komparasi GPU untuk Inferensi LLM"),
    ("jilid-1", "bab-02-hardware", "sub-bab-5.md", "aca", "akademis", "Analisis Bandwidth Memory HBM vs GDDR"),
    ("jilid-1", "bab-03-software", "sub-bab-1.md", "pop", "populer-edukatif", "Software Gateway dan Interface"),
    ("jilid-1", "bab-03-software", "sub-bab-4.md", "jur", "jurnalistik", "Perbandingan Framework Inferensi"),
    ("jilid-1", "bab-04-otomasi-agent", "sub-bab-1.md", "pop", "populer-edukatif", "Agentic AI dan Otomasi Sistem"),
    ("jilid-1", "bab-04-otomasi-agent", "sub-bab-3.md", "aca", "akademis", "Arsitektur Agent dan Tool Use"),
    # Jilid 2
    ("jilid-2", "bab-05-inference", "sub-bab-1.md", "pop", "populer-edukatif", "High-Performance Inference Engines"),
    ("jilid-2", "bab-05-inference", "sub-bab-4.md", "aca", "akademis", "Optimasi KV-Cache dan Quantization"),
    ("jilid-2", "bab-06-home", "sub-bab-1.md", "pop", "populer-edukatif", "Implementasi Skala 1: Home Assistance"),
    ("jilid-2", "bab-06-home", "sub-bab-3.md", "jur", "jurnalistik", "Studi Kasus: Smart Home dengan LLM Lokal"),
    ("jilid-2", "bab-07-small", "sub-bab-1.md", "pop", "populer-edukatif", "Implementasi Skala 2: Small Office"),
    ("jilid-2", "bab-08-general", "sub-bab-1.md", "pop", "populer-edukatif", "Implementasi Skala 3: General Office"),
    ("jilid-2", "bab-08-general", "sub-bab-4.md", "aca", "akademis", "Arsitektur Enterprise untuk LLM"),
    ("jilid-2", "bab-09-integrasi", "sub-bab-1.md", "pop", "populer-edukatif", "Integrasi Ekosistem Otomasi"),
    ("jilid-2", "bab-09-integrasi", "sub-bab-3.md", "aca", "akademis", "Pipeline Data dan ETL untuk LLM"),
    ("jilid-2", "bab-10-etika", "sub-bab-1.md", "per", "persuasif-argumentatif", "Etika, Keamanan & Masa Depan"),
    ("jilid-2", "bab-10-etika", "sub-bab-4.md", "per", "persuasif-argumentatif", "Dampak Sosial dan Kesenjangan Digital"),
    ("jilid-2", "bab-10-etika", "sub-bab-7.md", "sas", "sastrawi", "Refleksi Filosofis tentang Kecerdasan Buatan"),
]


def extract_body_text(filepath):
    """Extract body text from markdown, skipping headers and metadata."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove YAML frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # Remove markdown headers (##, ###, etc.) but keep their text
    lines = content.split('\n')
    body_lines = []
    in_code_block = False
    
    for line in lines:
        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        
        if in_code_block:
            continue
        
        # Skip empty lines at the start
        if not body_lines and not line.strip():
            continue
        
        # Skip section headers (## N. Tujuan Sub-Bab, etc.)
        if re.match(r'^#{1,3}\s+\d+\.', line.strip()):
            continue
        
        # Skip standalone headers that are just numbers
        if re.match(r'^#{1,3}\s+\d+\s*$', line.strip()):
            continue
        
        # Skip "---" separators
        if line.strip() == '---':
            continue
        
        # Skip blockquotes (title/subtitle)
        if line.strip().startswith('>'):
            continue
        
        # Skip bullet lists that look like learning objectives
        if re.match(r'^\s*-\s+(Menjelaskan|Memahami|Mengidentifikasi|Memproyeksikan|Menghitung|Membandingkan|Memilih|Menganalisis|Merancang|Mengimplementasikan)', line.strip()):
            continue
        
        body_lines.append(line)
    
    # Join and clean
    text = '\n'.join(body_lines)
    
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    
    # Remove markdown formatting for plain text
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)  # italic
    text = re.sub(r'`([^`]+)`', r'\1', text)  # inline code
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # links
    
    return text


def segment_text(text, min_words=400, max_words=600):
    """Segment text into passages of target word count."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    segments = []
    current_segment = []
    current_words = 0
    
    for para in paragraphs:
        para_words = len(para.split())
        
        if current_words + para_words > max_words and current_segment:
            segments.append('\n\n'.join(current_segment))
            current_segment = [para]
            current_words = para_words
        else:
            current_segment.append(para)
            current_words += para_words
    
    if current_segment:
        segments.append('\n\n'.join(current_segment))
    
    # Filter by minimum word count
    return [s for s in segments if len(s.split()) >= min_words]


def main():
    parser = argparse.ArgumentParser(description="Extract natural corpus from buku-kolaborasi-llm")
    parser.add_argument("--extract", action="store_true", help="Extract manuscripts")
    parser.add_argument("--list", action="store_true", help="List available selections")
    args = parser.parse_args()
    
    if args.list:
        print(f"{'ID':<35} {'Style':<6} {'Audience':<25} {'Title'}")
        print("-" * 120)
        for i, (jilid, bab, subbab, style, audience, title) in enumerate(SELECTIONS):
            uid = f"bkl_{i+1:02d}"
            print(f"{uid:<35} {style:<6} {audience:<25} {title}")
        print(f"\nTotal: {len(SELECTIONS)} selections")
        return
    
    if args.extract:
        TEXTS_DIR.mkdir(parents=True, exist_ok=True)
        
        metadata = []
        manifest = []
        
        for i, (jilid, bab, subbab, style, audience, title) in enumerate(SELECTIONS):
            uid = f"bkl_{i+1:02d}"
            src = BUKU_ROOT / jilid / bab / subbab
            
            if not src.exists():
                print(f"  SKIP {uid}: {src} not found")
                continue
            
            body = extract_body_text(src)
            segments = segment_text(body, *TARGET_WORDS)
            
            for j, seg in enumerate(segments):
                seg_id = f"{uid}_{j+1:02d}"
                out_file = TEXTS_DIR / f"{seg_id}.txt"
                
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(seg)
                
                word_count = len(seg.split())
                entry = {
                    "id": seg_id,
                    "source_id": uid,
                    "title": title,
                    "style": style,
                    "audience": audience,
                    "source_file": f"{jilid}/{bab}/{subbab}",
                    "words": word_count,
                    "variant": "natural",
                    "segment_index": j,
                    "total_segments": len(segments),
                }
                metadata.append(entry)
                manifest.append(f"{seg_id}: {word_count} words ({style}) — {title} [seg {j+1}/{len(segments)}]")
                
                print(f"  {seg_id}: {word_count} words ({style}) — {title} [seg {j+1}/{len(segments)}]")
        
        # Write metadata
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "seed": SEED,
                "source": "buku-kolaborasi-llm",
                "license": "fair use (research)",
                "n_segments": len(metadata),
                "n_sources": len(SELECTIONS),
                "corpus": metadata,
            }, f, indent=2, ensure_ascii=False)
        
        # Write manifest
        manifest_file = CORPUS_DIR / "MANIFEST.md"
        with open(manifest_file, "w", encoding="utf-8") as f:
            f.write("# Natural Corpus: Buku Kolaborasi LLM\n\n")
            f.write(f"Source: buku-kolaborasi-llm (local files)\n")
            f.write(f"License: fair use (research)\n")
            f.write(f"Segments: {len(metadata)} from {len(SELECTIONS)} chapters\n")
            f.write(f"Target words per segment: {TARGET_WORDS[0]}-{TARGET_WORDS[1]}\n\n")
            f.write("## Segments\n\n")
            for line in manifest:
                f.write(f"- {line}\n")
        
        total_words = sum(e["words"] for e in metadata)
        print(f"\nExtracted {len(metadata)} segments ({total_words} total words) from {len(SELECTIONS)} sources")
        print(f"Metadata: {METADATA_FILE}")
        print(f"Manifest: {manifest_file}")


if __name__ == "__main__":
    main()
