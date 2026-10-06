import sys

import click

from . import match, parse, report


@click.group()
def main():
    """Reconcile a bank export against a ledger export."""


@main.command()
@click.option("--bank", required=True, type=click.Path(exists=True))
@click.option("--ledger", required=True, type=click.Path(exists=True))
@click.option("--format", "fmt", type=click.Choice(["text", "json"]), default="text")
def reconcile(bank, ledger, fmt):
    try:
        b = parse.read(bank, source="bank")
        l = parse.read(ledger, source="ledger")
    except parse.UnknownFormat as exc:
        click.echo(f"error: unrecognised CSV layout - {exc}", err=True)
        sys.exit(2)

    result = match.reconcile(b, l)
    render = report.as_json if fmt == "json" else report.as_text
    click.echo(render(*result))
    sys.exit(1 if (result[1] or result[2]) else 0)
