"""Render a reconciliation result as text or JSON."""

import json


def as_text(matched, unmatched_bank, unmatched_ledger):
    lines = [f"matched: {len(matched)}"]
    if unmatched_bank:
        lines.append(f"\nonly in bank ({len(unmatched_bank)}):")
        for e in unmatched_bank:
            lines.append(f"  row {e.row:>4}  {e.when}  {e.amount:>10}  {e.text}")
    if unmatched_ledger:
        lines.append(f"\nonly in ledger ({len(unmatched_ledger)}):")
        for e in unmatched_ledger:
            lines.append(f"  row {e.row:>4}  {e.when}  {e.amount:>10}  {e.text}")
    return "\n".join(lines)


def as_json(matched, unmatched_bank, unmatched_ledger):
    def shape(e):
        return {"row": e.row, "when": str(e.when), "amount": str(e.amount), "text": e.text}

    return json.dumps(
        {
            "matched": [[shape(a), shape(b)] for a, b in matched],
            "only_in_bank": [shape(e) for e in unmatched_bank],
            "only_in_ledger": [shape(e) for e in unmatched_ledger],
        },
        indent=2,
    )
