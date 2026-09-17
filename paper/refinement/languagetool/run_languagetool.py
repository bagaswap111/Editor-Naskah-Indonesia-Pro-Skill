#!/usr/bin/env python3
"""
LanguageTool Comparison Script
Runs LanguageTool on manuscripts and compares with ENIP results.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

def run_languagetool(text: str, lang: str = "id") -> List[Dict]:
    """Run LanguageTool on text and return matches."""
    try:
        # Try using LanguageTool Python API first
        import language_tool_python
        tool = language_tool_python.LanguageTool(lang)
        matches = tool.check(text)
        tool.close()
        return [
            {
                "message": m.message,
                "offset": m.offset,
                "length": m.errorLength,
                "rule": m.ruleId,
                "category": m.category,
                "context": m.context,
                "suggestions": m.replacements[:3] if m.replacements else []
            }
            for m in matches
        ]
    except ImportError:
        pass
    
    # Fallback to command line
    try:
        result = subprocess.run(
            ["languagetool", "--json", "-l", lang],
            input=text,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("matches", [])
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Try Java LanguageTool
    try:
        result = subprocess.run(
            ["java", "-jar", "languagetool-commandline.jar", "--json", "-l", lang],
            input=text,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("matches", [])
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    return []

def categorize_matches(matches: List[Dict]) -> Dict[str, int]:
    """Categorize LanguageTool matches into PUEBI error categories."""
    categories = {
        "E1": 0,  # Comma before conjunction
        "E2": 0,  # Redundant comma
        "E3": 0,  # Serial comma
        "E4": 0,  # Quotation mark
        "E5": 0,  # Pleonasm
        "E6": 0,  # Redundant hyphen
        "E7": 0,  # Number formatting
        "E8": 0,  # Capitalization
        "E9": 0,  # Italic foreign words
        "E10": 0, # Repeated word
        "other": 0
    }
    
    for match in matches:
        rule = match.get("rule", "").lower()
        message = match.get("message", "").lower()
        
        if "comma" in rule or "comma" in message:
            if "conjunction" in message or "dan" in message or "atau" in message:
                categories["E1"] += 1
            elif "serial" in message or "list" in message:
                categories["E3"] += 1
            else:
                categories["E2"] += 1
        elif "capital" in rule or "capital" in message or "uppercase" in message:
            categories["E8"] += 1
        elif "repeat" in rule or "repeat" in message or "duplicate" in message:
            categories["E10"] += 1
        elif "hyphen" in rule or "hyphen" in message:
            categories["E6"] += 1
        elif "number" in rule or "number" in message:
            categories["E7"] += 1
        elif "quote" in rule or "quotation" in message:
            categories["E4"] += 1
        else:
            categories["other"] += 1
    
    return categories

def compare_with_enip(lt_results: Dict[str, int], enip_results: Dict[str, int]) -> Dict:
    """Compare LanguageTool results with ENIP results."""
    comparison = {}
    for category in set(list(lt_results.keys()) + list(enip_results.keys())):
        lt_count = lt_results.get(category, 0)
        enip_count = enip_results.get(category, 0)
        comparison[category] = {
            "languagetool": lt_count,
            "enip": enip_count,
            "difference": enip_count - lt_count
        }
    return comparison

def main():
    """Main function."""
    # Example usage
    texts = [
        "Ini adalah contoh teks untuk diuji.",
        "Dia pergi ke pasar, dan membeli buah.",
        "Mahasiswa harus memahami PUEBI dengan baik."
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"\n=== Teks {i} ===")
        print(f"Teks: {text}")
        
        matches = run_languagetool(text)
        print(f"Jumlah temuan: {len(matches)}")
        
        categories = categorize_matches(matches)
        print(f"Kategori: {json.dumps(categories, indent=2)}")
        
        for match in matches[:3]:  # Show first 3 matches
            print(f"  - {match.get('message', 'N/A')}")
            print(f"    Sugesti: {match.get('suggestions', [])}")

if __name__ == "__main__":
    main()
