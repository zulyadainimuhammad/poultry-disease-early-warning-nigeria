"""Data ingestion helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_csv(path: str | Path) -> pd.DataFrame:
    """Read a CSV file using pandas."""
    return pd.read_csv(path)


def write_csv(df: pd.DataFrame, path: str | Path) -> None:
    """Write a dataframe to CSV, creating parent directories if required."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False)
