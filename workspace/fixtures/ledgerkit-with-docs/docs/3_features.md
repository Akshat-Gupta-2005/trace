# FEATURES — ledgerkit

Living document. Updated at the end of every working session, as part of the work.
Reasoning and history live in 4_decisions.md.

**Last updated:** 2026-07-28 — matching engine landed; greedy pairing passes its
tests. Next: output formatting.

## Status legend

| Status     | Meaning                                   |
|------------|-------------------------------------------|
| `Planned`  | Agreed, not started                       |
| `Building` | In progress right now                     |
| `Done`     | Implemented AND verified                  |
| `Cut`      | Deliberately dropped — see 4_decisions.md |

Stars mean: worth explaining in a code review.

## Code map

    src/ledgerkit/
      cli.py      click entry point, wires parse -> match -> output
      parse.py    reads both CSV layouts into Entry records
      match.py    greedy amount-exact / date-fuzzy pairing
    tests/
      test_match.py   pairing behaviour

**Not yet built**

- JSON output for machine consumers
- any report rendering at all — `cli.py` currently prints raw tuples
- `--window` flag to override the 3-day date tolerance

## Features

### Input

| Feature | Status | What it does | Lives in | Star |
|---|---|---|---|---|
| Two CSV layouts | `Building` | Sniffs bank (`Date`/`Description`/`Amount`) vs ledger (`posted_on`/`memo`/`value`) column sets | `src/ledgerkit/parse.py` | |
| BOM tolerance | `Done` | Opens with `utf-8-sig`, so Excel exports parse | `src/ledgerkit/parse.py` | |
| Unknown layout is an error | `Done` | Raises `UnknownFormat` naming the columns it saw, rather than guessing | `src/ledgerkit/parse.py` | ★ |

### Matching

| Feature | Status | What it does | Lives in | Star |
|---|---|---|---|---|
| Amount-exact pairing | `Done` | `Decimal` comparison, never float | `src/ledgerkit/match.py` | ★ |
| 3-day date window | `Done` | `WINDOW = timedelta(days=3)`, covers weekend settlement lag | `src/ledgerkit/match.py` | |
| One ledger row used once | `Done` | Matched candidates are removed from the pool | `src/ledgerkit/match.py` | ★ |

### Deferred and cut

| Feature | Status | Note |
|---|---|---|
| Fuzzy description matching | `Cut` | Amount+date was enough on the 3 real months tested; text matching added false pairs |

## Current state / measured results

3 tests passing.

    pytest -q

## Open items

- [ ] decide the output format story
- [ ] add `--window` flag
- [ ] check behaviour on an empty ledger file
