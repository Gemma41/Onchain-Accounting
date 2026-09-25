# -*- coding: utf-8 -*-
"""Bot actions for Onchain Accounting — portfolio overview, transaction import, PnL, tax reports, cost basis, income and exports.

Realistic simulation layer with Rich output.
"""

import random
import time
from datetime import datetime

from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box

from service.ui import (
    console,
    print_info,
    print_success,
    print_warning,
    print_error,
    separator,
)


_ASSETS = [
    ("BTC", 67000.0), ("ETH", 3500.0), ("SOL", 150.0),
    ("BNB", 600.0), ("USDC", 1.0), ("POL", 0.7),
]

_METHODS = ["FIFO", "LIFO", "HIFO"]

_SOURCES = [
    ("binance.csv", "CSV"), ("coinbase.csv", "CSV"), ("kraken.csv", "CSV"),
    ("Binance API", "API"), ("On-chain sync", "RPC"), ("hardware wallet.csv", "CSV"),
]

_INCOME_KINDS = ["staking", "airdrop", "interest", "liquidity mining"]


def _money(v: float) -> str:
    return f"${v:,.2f}"


def _signed_money(v: float) -> str:
    color = "bright_green" if v >= 0 else "red"
    sign = "+" if v >= 0 else ""
    return f"[{color}]{sign}${v:,.2f}[/{color}]"


def _asset_rows():
    rows = []
    total = 0.0
    vals = []
    for sym, price in _ASSETS:
        qty = round(random.uniform(0.05, 40.0), 4)
        val = qty * price
        vals.append((sym, qty, price, val))
        total += val
    for sym, qty, price, val in vals:
        share = val / total * 100 if total else 0
        rows.append((sym, f"{qty:,.4f}", _money(price), _money(val), f"{share:.1f}%"))
    return rows, total


def _import_rows():
    out = []
    for name, kind in _SOURCES:
        imported = random.randint(40, 5200)
        dupes = random.randint(0, 90)
        status = "[bright_green]OK[/]" if random.random() > 0.08 else "[yellow]Partial[/]"
        out.append((name, kind, f"{imported:,}", str(dupes), status))
    return out


def _pnl_rows():
    out = []
    for period in ("Today", "7 days", "30 days", "YTD", "All time"):
        realized = random.uniform(-4000, 24000)
        unrealized = random.uniform(-9000, 42000)
        fees = random.uniform(12, 900)
        net = realized + unrealized - fees
        out.append((period, _signed_money(realized), _signed_money(unrealized),
                    f"-${fees:,.2f}", _signed_money(net)))
    return out


def _method_rows(cfg):
    acc = cfg.get("accounting", {})
    active = acc.get("cost_basis_method", "fifo").upper()
    out = []
    for m in _METHODS:
        st = random.uniform(1800, 12400)
        lt = random.uniform(400, 16800)
        income = random.uniform(200, 3200)
        liab = (st * 0.24) + (lt * 0.15) + (income * 0.22)
        mark = " ← active" if m == active else ""
        out.append((m + mark, _money(st), _money(lt), _money(income), _money(liab)))
    return out


def _lot_rows():
    out = []
    for i in range(random.randint(7, 12)):
        sym, price = random.choice(_ASSETS)
        qty = round(random.uniform(0.05, 8.0), 4)
        cost = price * random.uniform(0.4, 1.3)
        proceeds = qty * price
        gain = qty * (price - cost)
        days = random.randint(3, 900)
        term = "[bright_green]LONG[/]" if days > 365 else "[yellow]SHORT[/]"
        acquired = "202%d-%02d-%02d" % (random.randint(3, 6), random.randint(1, 12), random.randint(1, 28))
        out.append((acquired, sym, f"{qty:,.4f}", _money(cost), _signed_money(gain), term))
    return out


def _income_rows():
    out = []
    for _ in range(random.randint(6, 10)):
        kind = random.choice(_INCOME_KINDS)
        sym, price = random.choice(_ASSETS[:4])
        qty = round(random.uniform(0.01, 4.0), 4)
        usd = qty * price
        date = "2026-%02d-%02d" % (random.randint(1, 9), random.randint(1, 28))
        out.append((date, kind, f"{qty:,.4f} {sym}", _money(usd)))
    return out


def _export_rows(cfg):
    rep = cfg.get("reports", {})
    fmt = rep.get("default_format", "csv")
    out_dir = rep.get("output_directory", "./reports")
    fname = "tax_report_%s.%s" % (datetime.now().strftime("%Y"), fmt)
    return [
        ("Filename", fname),
        ("Format", fmt.upper()),
        ("Transactions", str(random.randint(400, 24000))),
        ("Size", f"{random.randint(48, 1500)} KB"),
        ("Path", f"{out_dir}/{fname}"),
    ]


def action_portfolio_overview(cfg: dict):
    """Aggregate balances across wallets, chains and exchanges (simulation)."""
    console.print()
    rows, total = _asset_rows()
    print_info('Aggregating wallets, exchange accounts and DeFi positions')
    separator()
    with Progress(
        SpinnerColumn(style="bright_yellow"),
        TextColumn("[bright_yellow]{task.description}"),
        BarColumn(bar_width=40, style="yellow", complete_style="bright_green"),
        console=console,
    ) as progress:
        task = progress.add_task('Aggregating portfolio...', total=3)
        for step_label in ['Reading local ledger database...', 'Refreshing fiat rates...', 'Valuing positions...']:
            progress.update(task, description=step_label)
            time.sleep(0.35)
            progress.advance(task)

    table = Table(
        show_header=True,
        header_style="bold bright_yellow",
        border_style="yellow",
        box=box.ROUNDED,
        title="[bold bright_yellow]  PORTFOLIO OVERVIEW  [/]",
    )
    table.add_column('Asset', style='bright_cyan')
    table.add_column('Quantity', justify='right', style='bright_white')
    table.add_column('Price', justify='right', style='dim')
    table.add_column('Value', justify='right', style='bright_green')
    table.add_column('Share', justify='right', style='yellow')

    for row in rows:
        table.add_row(*row)


    console.print()
    console.print(table)
    console.print()
    summary = Table(
        show_header=False,
        border_style="bright_yellow",
        box=box.ROUNDED,
    )
    summary.add_column("Metric", style="bright_yellow")
    summary.add_column("Value", justify="right", style="bright_white")
    summary.add_row('Total Value', f"${total:,.2f}")
    summary.add_row('Assets', str(len(rows)))
    summary.add_row('Wallets Tracked', str(random.randint(3, 12)))
    summary.add_row('Last Sync', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    console.print(Panel(summary, border_style="bright_yellow",
                        title="[bold bright_yellow]  NET WORTH  [/]"))
    console.print()
    print_info('All data stays local — encrypted at rest, never uploaded.')


def action_import_transactions(cfg: dict):
    """Import transactions from CSV, exchange APIs and on-chain (simulation)."""
    console.print()
    print_info('Sources: CSV drops in ./imports, exchange APIs, on-chain sync')
    separator()
    with Progress(
        SpinnerColumn(style="bright_yellow"),
        TextColumn("[bright_yellow]{task.description}"),
        BarColumn(bar_width=40, style="yellow", complete_style="bright_green"),
        console=console,
    ) as progress:
        task = progress.add_task('Importing transactions...', total=4)
        for step_label in ['Reading CSV files...',
         'Syncing exchange APIs...',
         'Fetching on-chain history...',
         'Deduplicating & matching transfers...']:
            progress.update(task, description=step_label)
            time.sleep(0.4)
            progress.advance(task)

    table = Table(
        show_header=True,
        header_style="bold bright_yellow",
        border_style="yellow",
        box=box.ROUNDED,
        title="[bold bright_yellow]  IMPORT RESULTS  [/]",
    )
    table.add_column('Source', style='bright_cyan')
    table.add_column('Type', style='dim')
    table.add_column('Imported', justify='right', style='bright_white')
    table.add_column('Duplicates', justify='right', style='dim')
    table.add_column('Status', justify='center')

    for row in _import_rows():
        table.add_row(*row)


    console.print()
    console.print(table)
    console.print()
    print_success('Import complete. Ledger is up to date.')
    print_info('Duplicate detection matches on tx hash + timestamp + amount.')


def action_pnl_report(cfg: dict):
    """Realized and unrealized profit/loss report (simulation)."""
    console.print()
    method = cfg.get("accounting", {}).get("cost_basis_method", "fifo").upper()
    print_info(f"Cost basis method: {method} · fees included in basis")
    separator()
    with Progress(
        SpinnerColumn(style="bright_yellow"),
        TextColumn("[bright_yellow]{task.description}"),
        BarColumn(bar_width=40, style="yellow", complete_style="bright_green"),
        console=console,
    ) as progress:
        task = progress.add_task('Computing PnL...', total=3)
        for step_label in ['Matching disposals to acquisition lots...',
         'Valuing open positions...',
         'Aggregating fees...']:
            progress.update(task, description=step_label)
            time.sleep(0.4)
            progress.advance(task)

    table = Table(
        show_header=True,
        header_style="bold bright_yellow",
        border_style="yellow",
        box=box.ROUNDED,
        title="[bold bright_yellow]  PROFIT & LOSS  [/]",
    )
    table.add_column('Period', style='bright_cyan')
    table.add_column('Realized', justify='right')
    table.add_column('Unrealized', justify='right')
    table.add_column('Fees', justify='right', style='dim')
    table.add_column('Net', justify='right', style='bold')

    for row in _pnl_rows():
        table.add_row(*row)


    console.print()
    console.print(table)
    console.print()
    print_info('Unrealized PnL uses the latest fiat rates; realized uses lot-matched basis.')


def action_tax_report(cfg: dict):
    """Capital gains tax report with method comparison (simulation)."""
    console.print()
    print_info('Comparing cost-basis methods on identical lot history')
    separator()
    with Progress(
        SpinnerColumn(style="bright_yellow"),
        TextColumn("[bright_yellow]{task.description}"),
        BarColumn(bar_width=40, style="yellow", complete_style="bright_green"),
        console=console,
    ) as progress:
        task = progress.add_task('Building tax report...', total=3)
        for step_label in ['Splitting short/long-term lots...',
         'Computing gains per method...',
         'Estimating liability...']:
            progress.update(task, description=step_label)
            time.sleep(0.4)
            progress.advance(task)

    table = Table(
        show_header=True,
        header_style="bold bright_yellow",
        border_style="yellow",
        box=box.ROUNDED,
        title="[bold bright_yellow]  TAX REPORT — METHOD COMPARISON  [/]",
    )
    table.add_column('Method', style='bright_cyan')
    table.add_column('ST Gains', justify='right', style='bright_white')
    table.add_column('LT Gains', justify='right', style='bright_white')
    table.add_column('Income', justify='right', style='dim')
    table.add_column('Est. Liability', justify='right', style='bold yellow')

    for row in _method_rows(cfg):
        table.add_row(*row)


    console.print()
    console.print(table)
    console.print()
    print_info('Rates shown are illustrative placeholders — set your jurisdiction rates in config.')
    print_info('Export a tax-ready CSV/PDF from the Export Reports menu.')


def action_cost_basis(cfg: dict):
    """Inspect open acquisition lots and method impact (simulation)."""
    console.print()
    print_info('Open lots after disposal matching (oldest-first for FIFO)')
    separator()
    with Progress(
        SpinnerColumn(style="bright_yellow"),
        TextColumn("[bright_yellow]{task.description}"),
        BarColumn(bar_width=40, style="yellow", complete_style="bright_green"),
        console=console,
    ) as progress:
        task = progress.add_task('Walking lots...', total=3)
        for step_label in ['Loading acquisition lots...',
         'Applying disposal matching...',
         'Marking short/long term...']:
            progress.update(task, description=step_label)
            time.sleep(0.35)
            progress.advance(task)

    table = Table(
        show_header=True,
        header_style="bold bright_yellow",
        border_style="yellow",
        box=box.ROUNDED,
        title="[bold bright_yellow]  OPEN LOTS  [/]",
    )
    table.add_column('Acquired', style='dim')
    table.add_column('Asset', style='bright_cyan')
    table.add_column('Qty', justify='right', style='bright_white')
    table.add_column('Basis / unit', justify='right', style='dim')
    table.add_column('Unrealized', justify='right')
    table.add_column('Term', justify='center')

    for row in _lot_rows():
        table.add_row(*row)


    console.print()
    console.print(table)
    console.print()
    print_info('Lots older than 365 days qualify as long-term in most jurisdictions.')


def action_income_staking(cfg: dict):
    """Income events: staking rewards, airdrops, interest (simulation)."""
    console.print()
    print_info('Income is valued at the fiat rate on the receipt date')
    separator()
    with Progress(
        SpinnerColumn(style="bright_yellow"),
        TextColumn("[bright_yellow]{task.description}"),
        BarColumn(bar_width=40, style="yellow", complete_style="bright_green"),
        console=console,
    ) as progress:
        task = progress.add_task('Collecting income events...', total=3)
        for step_label in ['Scanning staking rewards...',
         'Detecting airdrops...',
         'Valuing at receipt-date rates...']:
            progress.update(task, description=step_label)
            time.sleep(0.35)
            progress.advance(task)

    table = Table(
        show_header=True,
        header_style="bold bright_yellow",
        border_style="yellow",
        box=box.ROUNDED,
        title="[bold bright_yellow]  INCOME EVENTS  [/]",
    )
    table.add_column('Date', style='dim')
    table.add_column('Kind', style='bright_cyan')
    table.add_column('Amount', justify='right', style='bright_white')
    table.add_column('Value (USD)', justify='right', style='bright_green')

    for row in _income_rows():
        table.add_row(*row)


    console.print()
    console.print(table)
    console.print()
    print_info('Receipt-date valuation becomes the cost basis of the received asset.')


def action_export_reports(cfg: dict):
    """Export tax-ready reports (simulation)."""
    console.print()
    print_info('Preparing report export...')
    separator()
    with Progress(
        SpinnerColumn(style="bright_green"),
        TextColumn("[bright_green]{task.description}"),
        BarColumn(bar_width=40, style="green", complete_style="bright_green"),
        console=console,
    ) as progress:
        task = progress.add_task('Building report...', total=4)
        for step_label in ['Collecting ledger data...',
         'Rendering report layout...',
         'Writing file...',
         'Verifying output...']:
            progress.update(task, description=step_label)
            time.sleep(0.3)
            progress.advance(task)

    table = Table(
        show_header=True,
        header_style="bold bright_green",
        border_style="green",
        box=box.SIMPLE_HEAD,
        title="[bold bright_green]  EXPORT COMPLETE  [/]",
    )
    table.add_column('Property', style='bright_blue')
    table.add_column('Value', justify='right', style='bright_white')

    for row in _export_rows(cfg):
        table.add_row(*row)


    console.print()
    console.print(table)
    console.print()
    print_success('Report exported — ready for your accountant or tax software.')


__all__ = ['action_portfolio_overview',
 'action_import_transactions',
 'action_pnl_report',
 'action_tax_report',
 'action_cost_basis',
 'action_income_staking',
 'action_export_reports']
