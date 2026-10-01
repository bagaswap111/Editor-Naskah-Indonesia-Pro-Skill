#!/usr/bin/env python3
"""
Run LanguageTool on the evaluation manuscripts.

Feasibility-first design: LanguageTool's language inventory is probed before
any manuscript is sent. If Indonesian (`id`) is not offered, the run records
the evidence (language codes + HTTP error from an `id` check) and stops, so the
negative result is reproducible instead of silently producing empty counts.

Usage:
    python run_languagetool.py [--manuscripts DIR] [--out DIR] [--base-url URL]
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_BASE_URL = "https://api.languagetool.org/v2"
HERE = Path(__file__).resolve().parent
DEFAULT_MANUSCRIPTS = HERE.parent / "human_eval" / "manuscripts"
DEFAULT_OUT = HERE / "results"

CATEGORIES = {
    "E1": 0,   # koma sebelum konjungsi
    "E2": 0,   # koma berlebih
    "E3": 0,   # serial comma
    "E4": 0,   # tanda kutip
    "E5": 0,   # pleonasme
    "E6": 0,   # hubung berlebih
    "E7": 0,   # penulisan angka
    "E8": 0,   # kapitalisasi
    "E9": 0,   # kata asing bermiring
    "E10": 0,  # kata berulang
    "other": 0,
}


def http_json(url: str, data: Optional[Dict] = None, timeout: int = 30):
    """GET or POST form-encoded JSON; returns (payload, http_error)."""
    if data is None:
        req = urllib.request.Request(url, headers={"User-Agent": "enip-refinement/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8")), None
        except urllib.error.HTTPError as e:
            return None, {"status": e.code, "reason": e.reason, "body": e.read().decode("utf-8", "replace")[:500]}
        except Exception as e:  # noqa: BLE001 - network failures must not crash the run
            return None, {"status": None, "reason": str(e), "body": ""}
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(
        url, data=encoded, headers={"Content-Type": "application/x-www-form-urlencoded",
                                    "User-Agent": "enip-refinement/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        return None, {"status": e.code, "reason": e.reason, "body": e.read().decode("utf-8", "replace")[:500]}
    except Exception as e:  # noqa: BLE001
        return None, {"status": None, "reason": str(e), "body": ""}


def probe_languages(base_url: str):
    payload, err = http_json(f"{base_url}/languages")
    if err:
        return None, err
    codes = sorted({lang.get("code", "") for lang in payload})
    return codes, None


def supports_indonesian(codes: List[str]) -> bool:
    return any(c == "id" or c.startswith("id-") for c in codes)


def categorize(matches: List[Dict]) -> Dict[str, int]:
    """Map LanguageTool matches onto the PUEBI E1-E10 taxonomy used by the paper."""
    cats = dict(CATEGORIES)
    for m in matches:
        rule = (m.get("rule", {}).get("id", "") + " " + m.get("rule", {}).get("description", "")).lower()
        msg = (m.get("message", "") + " " + m.get("shortMessage", "")).lower()
        text = f"{rule} {msg}"
        if "comma" in text or "comma" in msg:
            if "conjunction" in text or "dan" in text or "atau" in text:
                cats["E1"] += 1
            elif "serial" in text or "list" in text:
                cats["E3"] += 1
            else:
                cats["E2"] += 1
        elif "capital" in text or "uppercase" in text:
            cats["E8"] += 1
        elif "repeat" in text or "duplicate" in text or "double" in text:
            cats["E10"] += 1
        elif "hyphen" in text or "dash" in text:
            cats["E6"] += 1
        elif "number" in text or "digit" in text:
            cats["E7"] += 1
        elif "quote" in text or "quotation" in text:
            cats["E4"] += 1
        else:
            cats["other"] += 1
    return cats


def check_text(base_url: str, text: str, lang: str = "id"):
    return http_json(f"{base_url}/check", data={"text": text, "language": lang})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manuscripts", type=Path, default=DEFAULT_MANUSCRIPTS)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    codes, err = probe_languages(args.base_url)
    record = {
        "tool": "LanguageTool",
        "endpoint": args.base_url,
        "probed_at": stamp,
        "indonesian_supported": False,
        "language_codes": codes or [],
        "probe_error": err,
        "manuscripts": [],
        "notes": [],
    }

    if codes is None:
        record["notes"].append(f"Language inventory probe failed: {err}")
        (args.out / "languagetool_results.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        print("LanguageTool language inventory unreachable:", err, file=sys.stderr)
        return 2

    record["indonesian_supported"] = supports_indonesian(codes)
    print(f"LanguageTool languages: {len(codes)} | Indonesian ('id') supported: {record['indonesian_supported']}")

    if not record["indonesian_supported"]:
        probe_payload, probe_err = check_text(
            args.base_url, "Dia pergi ke pasar, dan membeli buah.", lang="id")
        record["id_check_probe"] = {
            "payload": probe_payload,
            "error": probe_err,
            "interpretation": "HTTP 400 = language 'id' rejected by LanguageTool" if probe_err and probe_err.get("status") == 400 else "unexpected response",
        }
        record["notes"].append(
            "LanguageTool does not ship Indonesian rules: 'id' is absent from the "
            "supported-language inventory and a check request with language=id is rejected. "
            "No manuscript-level run is possible; see RESULTS.md.")
        (args.out / "languagetool_results.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        print("Indonesian not supported -> wrote evidence, skipping manuscript run.")
        return 0

    files = sorted(args.manuscripts.glob("*.txt"))
    if not files:
        record["notes"].append(f"No manuscripts found in {args.manuscripts}")
    for path in files:
        text = path.read_text(encoding="utf-8")
        payload, check_err = check_text(args.base_url, text)
        entry = {"manuscript": path.stem, "chars": len(text)}
        if check_err:
            entry["error"] = check_err
        else:
            matches = payload.get("matches", [])
            entry["matches"] = len(matches)
            entry["categories"] = categorize(matches)
        record["manuscripts"].append(entry)
        print(f"  {path.name}: {entry.get('matches', 'ERROR')}")

    (args.out / "languagetool_results.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {args.out / 'languagetool_results.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
