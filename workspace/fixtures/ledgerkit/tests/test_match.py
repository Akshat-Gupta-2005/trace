from datetime import date
from decimal import Decimal

from ledgerkit.match import reconcile
from ledgerkit.parse import Entry


def e(day, amount, text="x", source="bank", row=2):
    return Entry(date(2026, 8, day), text, Decimal(amount), source, row)


def test_exact_pair():
    matched, ub, ul = reconcile([e(10, "12.00")], [e(10, "12.00", source="ledger")])
    assert len(matched) == 1 and not ub and not ul


def test_inside_window():
    matched, ub, ul = reconcile([e(10, "12.00")], [e(13, "12.00", source="ledger")])
    assert len(matched) == 1


def test_outside_window():
    matched, ub, ul = reconcile([e(10, "12.00")], [e(14, "12.00", source="ledger")])
    assert not matched and len(ub) == 1 and len(ul) == 1


def test_amount_must_be_exact():
    matched, ub, ul = reconcile([e(10, "12.00")], [e(10, "12.01", source="ledger")])
    assert not matched


def test_one_ledger_entry_used_once():
    matched, ub, ul = reconcile(
        [e(10, "12.00"), e(11, "12.00")], [e(10, "12.00", source="ledger")]
    )
    assert len(matched) == 1 and len(ub) == 1
