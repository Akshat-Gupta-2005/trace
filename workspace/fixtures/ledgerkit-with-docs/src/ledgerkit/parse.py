"""CSV readers. Bank exports and ledger exports have different column names."""

import csv
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from dateutil import parser as dateparser

BANK_COLUMNS = {"Date", "Description", "Amount"}
LEDGER_COLUMNS = {"posted_on", "memo", "value"}


@dataclass(frozen=True)
class Entry:
    when: date
    text: str
    amount: Decimal
    source: str
    row: int


class UnknownFormat(Exception):
    pass


def read(path, source):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        cols = set(reader.fieldnames or [])
        if BANK_COLUMNS <= cols:
            keys = ("Date", "Description", "Amount")
        elif LEDGER_COLUMNS <= cols:
            keys = ("posted_on", "memo", "value")
        else:
            raise UnknownFormat(f"{path}: columns {sorted(cols)}")
        out = []
        for i, row in enumerate(reader, start=2):
            out.append(
                Entry(
                    when=dateparser.parse(row[keys[0]]).date(),
                    text=row[keys[1]].strip(),
                    amount=Decimal(row[keys[2]].replace(",", "")),
                    source=source,
                    row=i,
                )
            )
        return out
