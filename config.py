# -*- coding: utf-8 -*-
"""Configuration loader for Onchain Accounting — JSON config + defaults."""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"

_DEFAULTS = {'accounting': {'cost_basis_method': 'fifo',
                    'fiat_currency': 'USD',
                    'tax_year_start': '01-01',
                    'short_term_days': 365,
                    'include_fees_in_basis': True},
     'income': {'staking': True, 'airdrops': True, 'interest': True, 'mining': True},
     'import': {'csv_directory': './imports',
                'onchain_sync': True,
                'exchange_apis': {'binance': {'api_key': '', 'api_secret': ''},
                                  'coinbase': {'api_key': '', 'api_secret': ''},
                                  'kraken': {'api_key': '', 'api_secret': ''}}},
     'chains': {'ethereum': True,
                'bsc': True,
                'polygon': True,
                'arbitrum': True,
                'base': True,
                'bitcoin': True,
                'solana': False},
     'pricing': {'source': 'coingecko', 'cache_ttl_sec': 300, 'historical': True},
     'reports': {'output_directory': './reports',
                 'default_format': 'csv',
                 'pdf_attach_tx_table': True},
     'database': {'url': 'sqlite:///data/ledger.db'}}


def load_config() -> dict:
    """Load configuration from config.json, merging with defaults."""
    cfg = dict(_DEFAULTS)
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
            _deep_merge(cfg, user_cfg)
        except (json.JSONDecodeError, OSError):
            pass
    return cfg


def _deep_merge(base: dict, override: dict):
    """Recursively merge override into base dict."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def save_config(cfg: dict):
    """Persist configuration to config.json."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
