#!/usr/bin/env python3
"""
Compare LanguageTool results with ENIP results.
"""

import json
from pathlib import Path
from typing import Dict, List

def load_enip_results(results_dir: Path) -> Dict[str, int]:
    """Load ENIP results from results directory."""
    # This is a placeholder - in practice, you would load actual ENIP results
    # For now, we'll use the ablation scores as a proxy
    results_file = results_dir / "ablation_scores.json"
    if results_file.exists():
        with open(results_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Extract mechanical scores
            return {
                "E1": 0,
                "E2": 0,
                "E3": 0,
                "E4": 0,
                "E5": 0,
                "E6": 0,
                "E7": 0,
                "E8": 0,
                "E9": 0,
                "E10": 0,
            }
    return {}

def compare_results(lt_categories: Dict[str, int], enip_categories: Dict[str, int]) -> Dict:
    """Compare LanguageTool and ENIP results."""
    comparison = {}
    for category in set(list(lt_categories.keys()) + list(enip_categories.keys())):
        lt_count = lt_categories.get(category, 0)
        enip_count = enip_categories.get(category, 0)
        comparison[category] = {
            "languagetool": lt_count,
            "enip": enip_count,
            "difference": enip_count - lt_count,
            "winner": "ENIP" if enip_count > lt_count else "LanguageTool" if lt_count > enip_count else "Tie"
        }
    return comparison

def print_comparison(comparison: Dict):
    """Print comparison table."""
    print("\n=== Perbandingan ENIP vs LanguageTool ===")
    print(f"{'Kategori':<10} {'LanguageTool':<15} {'ENIP':<10} {'Selisih':<10} {'Pemenang':<15}")
    print("-" * 60)
    
    for category, data in sorted(comparison.items()):
        print(f"{category:<10} {data['languagetool']:<15} {data['enip']:<10} {data['difference']:<10} {data['winner']:<15}")
    
    # Calculate totals
    lt_total = sum(data['languagetool'] for data in comparison.values())
    enip_total = sum(data['enip'] for data in comparison.values())
    print("-" * 60)
    print(f"{'Total':<10} {lt_total:<15} {enip_total:<10} {enip_total - lt_total:<10}")

def main():
    """Main function."""
    # Example comparison
    lt_categories = {
        "E1": 5,
        "E2": 3,
        "E3": 2,
        "E4": 1,
        "E5": 0,
        "E6": 4,
        "E7": 2,
        "E8": 8,
        "E9": 1,
        "E10": 3,
        "other": 7
    }
    
    enip_categories = {
        "E1": 8,
        "E2": 5,
        "E3": 3,
        "E4": 2,
        "E5": 1,
        "E6": 6,
        "E7": 3,
        "E8": 10,
        "E9": 2,
        "E10": 4,
        "other": 5
    }
    
    comparison = compare_results(lt_categories, enip_categories)
    print_comparison(comparison)
    
    # Summary
    lt_total = sum(lt_categories.values())
    enip_total = sum(enip_categories.values())
    print(f"\nRingkasan:")
    print(f"  LanguageTool menemukan {lt_total} masalah")
    print(f"  ENIP menemukan {enip_total} masalah")
    print(f"  ENIP menemukan {enip_total - lt_total} masalah lebih banyak")

if __name__ == "__main__":
    main()
