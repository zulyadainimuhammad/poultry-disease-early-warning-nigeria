"""Validation checks for the poultry disease analytical table."""

from __future__ import annotations

import pandas as pd


def require_columns(df: pd.DataFrame, columns: list[str]) -> None:
    missing = set(columns).difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def validate_semester_values(df: pd.DataFrame) -> None:
    """Ensure semester labels remain within the expected WAHIS structure."""
    if "semester" not in df.columns:
        raise ValueError("Column 'semester' is required.")
    allowed = {"Jan-Jun", "Jul-Dec"}
    observed = set(df["semester"].dropna().astype(str).unique())
    invalid = observed.difference(allowed)
    if invalid:
        raise ValueError(f"Unexpected semester values: {sorted(invalid)}")


def validate_no_exact_duplicates(df: pd.DataFrame) -> None:
    duplicates = int(df.duplicated().sum())
    if duplicates:
        raise ValueError(f"Found {duplicates} exact duplicate rows.")


def validate_candidate_table(df: pd.DataFrame) -> dict[str, int]:
    """Return compact validation statistics without assuming missing means zero."""
    require_columns(
        df,
        ["year", "semester", "administrative_division", "disease", "new_outbreaks"],
    )
    return {
        "rows": len(df),
        "years": int(df["year"].nunique(dropna=True)),
        "administrative_divisions": int(
            df["administrative_division"].nunique(dropna=True)
        ),
        "diseases": int(df["disease"].nunique(dropna=True)),
        "missing_outbreak_values": int(df["new_outbreaks"].isna().sum()),
    }
