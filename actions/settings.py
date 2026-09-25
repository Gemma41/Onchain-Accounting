# -*- coding: utf-8 -*-
"""Settings action — configuration overview for Onchain Accounting."""

from pathlib import Path

from rich.table import Table
from rich.panel import Panel
from rich import box

from service.ui import console, print_info, print_warning


def action_settings():
    """Display setup instructions: config.json sections and examples."""
    table = Table(
        show_header=True,
        header_style="bold bright_yellow",
        border_style="bright_yellow",
        box=box.ROUNDED,
        title="[bold bright_yellow] ◈ CONFIGURATION ◈ [/]",
        title_style="bright_yellow",
    )
    table.add_column("Setting", style="bright_yellow")
    table.add_column("Description", style="dim")
    table.add_column("Example", style="bright_black")

    table.add_row('accounting.cost_basis_method', 'Lot matching method', 'fifo / lifo / hifo')
    table.add_row('accounting.fiat_currency', 'Reporting currency', 'USD / EUR / GBP')
    table.add_row('accounting.short_term_days', 'Short/long-term boundary', '365')
    table.add_row('accounting.include_fees_in_basis', 'Fold fees into basis', 'true')
    table.add_row('import.csv_directory', 'CSV drop folder', './imports')
    table.add_row('import.exchange_apis', 'Exchange API credentials', 'binance / coinbase / kraken')
    table.add_row('pricing.source', 'Fiat rate provider', 'coingecko')
    table.add_row('reports.default_format', 'Export format', 'csv / pdf / json')
    table.add_row('database.url', 'Ledger storage DSN', 'sqlite:///data/ledger.db')

    panel = Panel(
        table,
        title="[bold bright_yellow] Onchain Accounting Settings [/]",
        border_style="bright_yellow",
        box=box.DOUBLE,
    )

    console.print()
    console.print(panel)

    base_dir = Path(__file__).parent.parent
    config_path = base_dir / "config.json"

    console.print()
    console.print("[dim]Configuration files:[/]")
    console.print(f"  [bright_yellow]config.json[/]  → {config_path}")
    console.print()
    print_info('Everything is stored locally in SQLite — back up data/ledger.db before migrating.')
    print_info('Exchange API keys need read-only permissions only.')
    print_warning("Keep API keys and secrets secure. Never commit config.json to version control.")
    print_info("Edit config files with any text editor (e.g. VS Code, Notepad).")
