# DECISIONS — ledgerkit

Append-only record of choices made and problems solved.
Current state lives in 3_features.md.

## Decisions log

| Date | Decision | Why |
|---|---|---|
| 2026-07-09 | `Decimal` for all amounts, never `float` | A 0.01 discrepancy is the entire product. `float` made `12.00` and `11.999999999999998` unequal on the second real file we tried. Rejected: rounding floats at comparison time, which just moves the threshold problem. |
| 2026-07-14 | Sniff CSV layout from the column set, not from a `--format` flag | Bookkeepers do not know which export they have. Rejected: requiring the flag, which turns a support question into a support ticket. |
| 2026-07-21 | Date window fixed at 3 days | Covers Fri→Mon settlement, the only lag seen in 3 months of real data. Rejected: making it configurable before we had evidence anyone needed it. |

## Problems faced and fixed

### P1 — Excel exports failed to parse on the first column *(2026-07-11, tooling)*

**Symptom:** `KeyError: 'Date'` on every file exported from Excel, while the same
data saved from LibreOffice parsed fine. `reader.fieldnames` showed
`['﻿Date', 'Description', 'Amount']`.

**Root cause:** Excel writes a UTF-8 BOM; `csv.DictReader` treats it as part of the
first header name.

**Fix:** open with `encoding="utf-8-sig"` (`src/ledgerkit/parse.py:26`).

**Verified:** re-parsed the three Excel exports that had failed; all three now
return the expected row counts. Reverting to `utf-8` reproduces the `KeyError`.

**Generalises to:** when only one column misbehaves and it is the first one,
suspect an encoding mark before suspecting the parser.

## Open decisions

### OD1 — Should reconcile emit machine-readable output as well as text?

**Blocks:** nothing yet. It blocks the accounting-package import work if that ever
starts, and it is cheap now and expensive once someone is scraping the text output.

**Options:**

| Option | Costs | Buys you |
|---|---|---|
| Text only | Anyone automating it parses our human output, which we then cannot change | One format to maintain |
| Add `--format json` | A second renderer, and a shape we are then committed to | Automation without screen-scraping |

**Leaning:** add it, but not until something actually needs it.

**What would settle it:** the first person who asks to pipe the output into
anything.

**Raised:** 2026-07-22.
