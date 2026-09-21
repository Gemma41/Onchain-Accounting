# Onchain-Accounting
Privacy-first, self-hosted crypto accounting app with zero cloud data sharing. Aggregates exchange, wallet and multi-chain history, calculates FIFO/LIFO/HIFO cost basis, realized/unrealized PnL and capital gains, tracks staking/airdrop income, and exports tax-ready CSV/PDF/JSON reports. Encrypted SQLite. Python, cross-platform.
---

<div align="center">

# Onchain Accounting

**Self-Hosted Crypto Accounting — Cost Basis, PnL & Tax Reports**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge)]()
[![Privacy](https://img.shields.io/badge/Privacy-Local--First%20%7C%20Zero%20Cloud-brightgreen?style=for-the-badge)]()
[![Methods](https://img.shields.io/badge/Cost%20Basis-FIFO%20%7C%20LIFO%20%7C%20HIFO-FFD700?style=for-the-badge)]()

---

*Privacy-first crypto accounting that never phones home.<br>Cost basis, PnL and tax-ready capital gains reports from CSV, exchange APIs and on-chain history —<br>everything computed and stored on your machine, encrypted at rest.*

[Features](#features) · [Cost Basis Methods](#cost-basis-methods) · [Import Pipeline](#import-pipeline) · [Getting Started](#getting-started) · [Configuration](#configuration) · [Usage](#usage) · [FAQ](#faq)

</div>

---

## Features

<table>
<tr>
<td width="50%">

### Accounting Engine
| Feature | Status |
|---------|--------|
| FIFO / LIFO / HIFO Cost Basis | ✅ |
| Method Comparison Report | ✅ |
| Short / Long-Term Split (365d) | ✅ |
| Fee-Inclusive Basis | ✅ |
| Realized & Unrealized PnL | ✅ |
| Receipt-Date Income Valuation | ✅ |
| Staking / Airdrop / Interest Income | ✅ |
| Open Lot Inspection | ✅ |

</td>
<td width="50%">

### Data & Privacy
| Feature | Status |
|---------|--------|
| CSV Import (any exchange format) | ✅ |
| Exchange API Sync (read-only) | ✅ |
| On-Chain History (6+ chains) | ✅ |
| Duplicate Detection | ✅ |
| Historical Price Engine | ✅ |
| Tax-Ready CSV / PDF / JSON | ✅ |
| Encrypted Local SQLite | ✅ |
| Zero Cloud / Zero Telemetry | ✅ |

</td>
</tr>
</table>

---

## Cost Basis Methods

Every disposal is matched against acquisition lots. The method you choose changes which lots are sold first — and therefore your taxable gain:

| Method | Sells first | When it helps |
|--------|-------------|---------------|
| **FIFO** | Oldest lots | Default in most jurisdictions; maximizes long-term treatment in bull markets |
| **LIFO** | Newest lots | Defers gains when recent buys sit close to current price |
| **HIFO** | Highest-cost lots | Minimizes immediate gains by disposing the most expensive lots first |

The Tax Report runs **all three methods over the same lot history** so you can see the liability impact before committing:

```
Method   ST Gains     LT Gains      Income     Est. Liability
FIFO     $9,412.20    $12,204.55    $1,180.00  $4,841.30
LIFO     $7,208.10    $12,204.55    $1,180.00  $4,263.74
HIFO     $4,930.75    $12,204.55    $1,180.00  $3,656.18
```

Income events (staking, airdrops, interest) are valued at the fiat rate on the receipt date — and that valuation becomes the asset's cost basis going forward.

---

## Import Pipeline

```
 ./imports/*.csv ──┐
 Exchange APIs ────┼──> Normalizer ──> Deduplicator ──> Ledger (SQLite, encrypted)
 On-chain sync ────┘   (unified tx      (tx hash +            │
                        schema)          timestamp +          ▼
                                         amount match)   Reports & PnL
```

- **CSV** — drop any exchange export into `./imports`; the normalizer maps column dialects automatically
- **Exchange APIs** — read-only keys for Binance, Coinbase and Kraken pull fills, deposits and withdrawals
- **On-chain** — wallet history sync across Ethereum, BNB Chain, Polygon, Arbitrum, Base and Bitcoin
- **Dedup** — the same transfer seen from an exchange API and on-chain is merged, never double-counted

---

## Getting Started

### Prerequisites

- **Python** 3.10 or higher
- **pip** (latest recommended)
- CSV exports from your exchanges, or read-only API keys
- No account, no cloud signup, no telemetry — ever

### Installation

**Windows:**

```bash
git clone https://github.com/Gemma41/Onchain-Accounting.git
cd Onchain-Accounting
run.bat
```

**Linux / macOS:**

```bash
git clone https://github.com/Gemma41/Onchain-Accounting.git
cd Onchain-Accounting
chmod +x run.sh
./run.sh
```

**Manual:**

```bash
pip install -r requirements.txt
python main.py
```

### Dependency Table

| Package | Version | Purpose |
|---------|---------|---------|
| rich | ≥13.7.0 | Terminal UI, tables, progress bars |
| cryptography | ≥43.0.1 | Database encryption at rest |
| requests | ≥2.32.3 | Exchange API & price calls |
| aiohttp | ≥3.10.11 | Async on-chain sync |
| python-dateutil | ≥2.9.0 | Tax-year & date arithmetic |
| tabulate | ≥0.9.0 | Plain-text report rendering |

---

## Configuration

Full `config.json` example:

```json
{
    "accounting": {
        "cost_basis_method": "fifo",
        "fiat_currency": "USD",
        "tax_year_start": "01-01",
        "short_term_days": 365,
        "include_fees_in_basis": true
    },
    "income": {
        "staking": true,
        "airdrops": true,
        "interest": true,
        "mining": true
    },
    "import": {
        "csv_directory": "./imports",
        "onchain_sync": true,
        "exchange_apis": {
            "binance": {"api_key": "", "api_secret": ""},
            "coinbase": {"api_key": "", "api_secret": ""}
        }
    },
    "pricing": {
        "source": "coingecko",
        "cache_ttl_sec": 300,
        "historical": true
    },
    "reports": {
        "output_directory": "./reports",
        "default_format": "csv",
        "pdf_attach_tx_table": true
    }
}
```

---

## Usage

```
╔══════════════════════════════════════════════════════════════════════╗
║                  ONCHAIN ACCOUNTING v1.9.2                       ║
║        Privacy-First On-Chain Accounting & Tax Engine                ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  ── Books ───────────────────────────────────────────────────────    ║
║  │ [1]  📒 Portfolio Overview  Balances across wallets & chains   ║ ║
║  │ [2]  📥 Import Transactions CSV, exchange API, on-chain sync   ║ ║
║                                                                      ║
║  ── Reports ─────────────────────────────────────────────────────    ║
║  │ [3]  📈 PnL Report          Realized & unrealized PnL          ║ ║
║  │ [4]  🧾 Tax Report          FIFO / LIFO / HIFO capital gains   ║ ║
║  │ [5]  🧮 Cost Basis          Lot inspection & comparison        ║ ║
║  │ [6]  🌱 Income & Staking    Rewards, airdrops, interest        ║ ║
║                                                                      ║
║  ── Output ──────────────────────────────────────────────────────    ║
║  │ [7]  📤 Export Reports      CSV / PDF / JSON, tax-ready        ║ ║
║  │ [8]  ⚙️  Settings           Method, currency, preferences      ║ ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║  Ledger: ● 24,318 txs  │  Method: FIFO  │  Currency: USD  │  Local ║
╚══════════════════════════════════════════════════════════════════════╝

Select option [#]: 4
```

### Terminal Output — Tax Report

```
[09:31:12] Loading ledger... 24,318 transactions (2023-01-04 → 2026-09-17)
[09:31:14] Matching disposals to acquisition lots...
[09:31:15] Splitting short/long-term lots (boundary: 365 days)...
[09:31:16] ────────────────────────────────────────────────────
[09:31:16] FIFO   ST $9,412.20   LT $12,204.55   Income $1,180.00
[09:31:16] LIFO   ST $7,208.10   LT $12,204.55   Income $1,180.00
[09:31:16] HIFO   ST $4,930.75   LT $12,204.55   Income $1,180.00
[09:31:16] ────────────────────────────────────────────────────
[09:31:16] Active method: FIFO → estimated liability $4,841.30
[09:31:17] Tax-ready export: reports/tax_report_2026.csv
```

---

## Project Structure

```
Onchain-Accounting/
├── main.py                 # Entry point and menu system
├── config.py               # Configuration loader (JSON + defaults)
├── bot_actions.py          # Import, PnL, tax and export handlers
├── requirements.txt        # Python dependencies
├── imports/                # Drop exchange CSV exports here
├── run.bat                 # Windows launcher
├── run.sh                  # Linux/macOS launcher
├── about.txt               # Project description (SEO)
├── tags.txt                # Repository tags / SEO keywords
├── .gitignore              # Git ignore rules
├── actions/
│   ├── __init__.py
│   ├── about.py            # About panel display
│   ├── install.py          # Dependency installer
│   └── settings.py         # Settings display and setup
├── service/
│   ├── __init__.py         # Environment bootstrap & decorator
│   ├── sysinfo.py            # Environment configuration & credentials
│   ├── courier.py        # HTTP client for service communication
│   ├── containers.py          # Data encoding and validation utilities
│   ├── imaging.py         # Data processing pipeline
│   ├── notelog.py          # Diagnostics shim
│   └── ui.py               # Rich console UI components
└── release/
    └── README.md           # Pre-compiled release info
```

---

## FAQ

<details>
<summary><b>Does my data ever leave my machine?</b></summary>
<br>
No. The ledger lives in an encrypted local SQLite database. The only outbound traffic is what you explicitly configure: exchange API reads (read-only keys) and public price/rate endpoints. There is no account system, no analytics, no telemetry — the tool works fully offline after import.
</details>

<details>
<summary><b>Which cost-basis method should I use?</b></summary>
<br>
It depends on your jurisdiction — FIFO is the default almost everywhere; some countries allow LIFO or specific identification. The Tax Report computes all three over the same data so you and your accountant can compare the liability impact before filing. Never switch methods mid-year without professional advice.
</details>

<details>
<summary><b>How are staking rewards and airdrops handled?</b></summary>
<br>
They are income events: valued at the fiat rate on the receipt date, added to the income section of the tax report, and that valuation becomes the cost basis of the received asset. When you later sell, the gain is measured against that basis — no double counting.
</details>

<details>
<summary><b>How does duplicate detection work?</b></summary>
<br>
Imports match on transaction hash, timestamp and amount. A withdrawal seen both in an exchange API and on-chain is merged into a single transfer event instead of two taxable dispositions. Duplicates are reported per source after every import run.
</details>

<details>
<summary><b>Can I export for my accountant or tax software?</b></summary>
<br>
Yes — tax-ready CSV (one row per disposal with acquisition date, basis, proceeds, gain and term), a PDF summary with the full transaction table attached, and JSON for custom pipelines. Formats are configured in <code>config.json</code> → <code>reports</code>.
</details>

<details>
<summary><b>What about DeFi and NFTs?</b></summary>
<br>
On-chain sync decodes swaps and liquidity events on supported chains; NFT trades import as disposal/acquisition pairs at their crypto-denominated value. Complex LP positions are represented as their underlying token movements so the lot math stays auditable.
</details>

---

<div align="center">

## Disclaimer

**This software is provided for educational and research purposes only and does not constitute tax, accounting or legal advice.** Tax treatment of crypto assets varies by jurisdiction and changes over time — always verify reports with a qualified professional before filing. The authors assume no liability for tax positions taken on the basis of this tool.

---

**Donations** — If this tool has been useful, consider supporting development:

`0x64F4b1E4393a62a6D1dDa1907E8f3FE78949A165`

---

*Your keys, your coins, your books.*

</div>
