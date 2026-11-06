"""Conservative WAHIS panel construction helpers."""
from __future__ import annotations
import pandas as pd

KEY_COLUMNS = ["year", "semester", "administrative_division", "disease"]
MEASURE_COLUMNS = ["new_outbreaks", "cases", "deaths", "killed_and_disposed_of", "slaughtered", "vaccinated", "susceptible"]


def build_observed_panel(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate observed keys conservatively; never infer unreported absence.

    Distinct non-null measurements within a key are considered ambiguous.
    A single observed value is retained even when other source records are null.
    Multiple distinct values are not summed because source records may not be
    independent additive observations.
    """
    missing = set(KEY_COLUMNS).difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    work = df.copy()
    for col in MEASURE_COLUMNS:
        if col in work.columns:
            work[col] = pd.to_numeric(work[col], errors="coerce")
    grouped = work.groupby(KEY_COLUMNS, dropna=False, observed=True)
    result = grouped.size().rename("source_record_count").to_frame()
    for col in MEASURE_COLUMNS:
        if col not in work.columns:
            continue
        stats = grouped[col].agg(["count", "nunique", "first"])
        result[f"{col}_non_missing_count"] = stats["count"]
        result[f"{col}_ambiguous"] = stats["nunique"].gt(1)
        result[col] = stats["first"].where(stats["nunique"].le(1))
    return result.reset_index()
