# -*- coding: utf-8 -*-
"""About action — project info, features, requirements for Onchain Accounting."""

from rich.table import Table
from rich.panel import Panel
from rich import box

from service.ui import console


def action_about():
    """Display project info: overview, features, requirements."""
    features_table = Table(
        show_header=True,
        header_style="bold bright_yellow",
        border_style="bright_yellow",
        box=box.SIMPLE,
        title="[bold bright_yellow] ◈ FEATURES ◈ [/]",
        title_style="bright_yellow",
    )
    features_table.add_column("Feature", style="bright_yellow")
    features_table.add_column("Status", justify="center", style="bright_green")

    for feat in [
        'Self-hosted, privacy-first crypto accounting',
        'FIFO / LIFO / HIFO cost basis with method comparison',
        'Realized & unrealized PnL per period',
        'Capital gains split: short-term vs long-term',
        'Income events: staking, airdrops, interest, mining',
        'CSV import + exchange API sync + on-chain history',
        'Duplicate detection (tx hash + timestamp + amount)',
        'Receipt-date fiat valuation for income',
        'Historical price engine with caching',
        'Tax-ready CSV / PDF / JSON export',
        'Encrypted local database — zero cloud, zero telemetry',
        'Cross-platform (Windows/Linux/macOS)',
    ]:
        features_table.add_row(feat, "✓")

    setup_table = Table(
        show_header=True,
        header_style="bold bright_yellow",
        border_style="bright_yellow",
        box=box.MINIMAL_HEAVY_HEAD,
        title="[bold bright_yellow] ◈ REQUIREMENTS & SETUP ◈ [/]",
        title_style="bright_yellow",
    )
    setup_table.add_column("Item", style="bright_yellow")
    setup_table.add_column("Note", style="dim")
    setup_table.add_row('Python', '3.10 or higher')
    setup_table.add_row('pip', 'Latest version recommended')
    setup_table.add_row('Libraries', 'rich, cryptography, requests, aiohttp, python-dateutil, tabulate')
    setup_table.add_row('Install', 'pip install -r requirements.txt')
    setup_table.add_row('Run', 'python main.py')
    setup_table.add_row('Data', 'CSV drops in ./imports or exchange API keys')
    setup_table.add_row('Storage', 'Local SQLite — nothing leaves your machine')

    console.print()
    console.print(Panel(features_table, border_style="bright_yellow", box=box.ROUNDED))
    console.print()
    console.print(Panel(setup_table, border_style="bright_yellow", box=box.ROUNDED))
    console.print()
    console.print(
        "[dim]Onchain Accounting — self-hosted crypto ledger. Pick your cost-basis method in config.json → accounting.cost_basis_method.[/]"
    )
    console.print()
    console.print("[dim]Contact:[/] [bright_blue]0x64F4b1E4393a62a6D1dDa1907E8f3FE78949A165[/] (ETH/EVM)")
    console.print()
