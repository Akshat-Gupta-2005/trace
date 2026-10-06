# ledgerkit

Reconcile a bank CSV export against a ledger CSV and report what does not match.

```bash
pip install -e .
ledgerkit reconcile --bank statements/oct.csv --ledger books/oct.csv
```

Matching is fuzzy on date (±3 days) and exact on amount. Anything unmatched on
either side is reported.
