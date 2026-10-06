"""Pair bank entries against ledger entries.

Exact on amount, within WINDOW days on date. Greedy: entries are consumed in
date order and a consumed entry cannot match again.
"""

from datetime import timedelta

WINDOW = timedelta(days=3)


def reconcile(bank, ledger):
    remaining = sorted(ledger, key=lambda e: e.when)
    matched, unmatched_bank = [], []

    for b in sorted(bank, key=lambda e: e.when):
        hit = None
        for candidate in remaining:
            if candidate.amount != b.amount:
                continue
            if abs(candidate.when - b.when) <= WINDOW:
                hit = candidate
                break
        if hit is None:
            unmatched_bank.append(b)
        else:
            remaining.remove(hit)
            matched.append((b, hit))

    return matched, unmatched_bank, remaining
