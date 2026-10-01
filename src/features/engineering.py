"""Feature engineering utilities.

Feature definitions will be expanded only after the validated target and
prediction horizon have been established.
"""

from __future__ import annotations

import pandas as pd


def add_outbreak_lag(
    df: pd.DataFrame,
    group_columns: list[str],
    periods: int = 1,
    value_column: str = "new_outbreaks",
) -> pd.DataFrame:
    """Create a lagged historical-outbreak feature within each geography/disease."""
    out = df.sort_values(group_columns + ["year", "semester"]).copy()
    lag_name = f"{value_column}_lag_{periods}"
    out[lag_name] = out.groupby(group_columns, dropna=False)[value_column].shift(periods)
    return out
