# Project docs config

    PROJECT_NAME   = ledgerkit
    PROJECT_GOAL   = A CLI that reconciles a bank CSV export against a ledger CSV and reports what does not match, for bookkeepers closing a month.
    AUDIENCE       = teammates picking this up, and future me
    STACK          = Python 3.11, click, python-dateutil, pytest, hatchling
    DOC_LOCATION   = docs/
    STAR_LABEL     = worth explaining in a code review
    RUNTIME_SHAPE  = a single CLI, no services — `pip install -e .` then `ledgerkit reconcile`
    CONTRACT_KIND  = CLI flags and exit codes
    DOC_SET        = 3_features.md, 4_decisions.md
