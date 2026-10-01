# LanguageTool Comparison — Result

**Generated**: 2026-10-01T13:49:29+00:00
**Endpoint**: `https://api.languagetool.org/v2` (probed 2026-10-01T13:49:27+00:00)

## Feasibility

- Languages exposed by LanguageTool: **34**
- Indonesian (`id`) supported: **NO**
- Direct `POST /check` with `language=id` → **HTTP 400 Bad Request**: `Error: 'id' is not a language code known to LanguageTool. Supported language codes are: ar, ast-ES, be-BY, br-FR, ca-ES,`
- LanguageTool does not ship Indonesian rules: 'id' is absent from the supported-language inventory and a check request with language=id is rejected. No manuscript-level run is possible; see RESULTS.md.

## Mechanical baseline: fix rate per PUEBI category (weighted)

| Kategori | input | B3 (hunspell) | ENIP | B1 | B2 | LanguageTool |
|---|---|---|---|---|---|---|
| E1 | 0.0 | - | 0.9722 | 0.9444 | 0.9444 | n/a (no id rules) |
| E2 | 0.0 | - | 0.9429 | 1.0 | 1.0 | n/a (no id rules) |
| E3 | 0.0 | - | 1.0 | 1.0 | 1.0 | n/a (no id rules) |
| E4 | 0.0 | - | 1.0 | 1.0 | 1.0 | n/a (no id rules) |
| E5 | 0.0 | - | 1.0 | 1.0 | 1.0 | n/a (no id rules) |
| E6 | 0.0 | - | 1.0 | 0.9412 | 1.0 | n/a (no id rules) |
| E7 | 0.0 | - | 1.0 | 1.0 | 1.0 | n/a (no id rules) |
| E8 | 0.0 | - | 1.0 | 1.0 | 1.0 | n/a (no id rules) |
| E9 | 0.0 | - | 0.7 | 0.9 | 0.7667 | n/a (no id rules) |
| E10 | 0.0 | - | 1.0 | 1.0 | 1.0 | n/a (no id rules) |

## Conclusion

LanguageTool cannot serve as an Indonesian GEC baseline: it publishes no Indonesian rules, so the only mechanical open-source baseline available for this corpus is the hunspell id-ID detector (B3), which flags errors without producing corrected text (fix rate not applicable). ENIP/B1/B2 remain the text-producing conditions.
