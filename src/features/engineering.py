"""Feature engineering utilities.

Feature definitions will be expanded only after the validated target and
prediction horizon have been established.
"""

from __future__ import annotations

import pandas as pd


SEMESTER_ORDER = {
    "Jan-Jun": 1,
    "Jul-Dec": 2,
}


def _validate_semester(df: pd.DataFrame) -> None:
    """Validate that all semester values use the project's defined labels."""
    invalid = set(df["semester"].dropna().unique()) - set(SEMESTER_ORDER)

    if invalid:
        raise ValueError(
            f"Invalid semester values: {sorted(invalid)}. "
            f"Expected one of: {list(SEMESTER_ORDER)}"
        )


def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add chronological calendar features for semester-level observations.

    ``time_index`` increases monotonically across year/semester combinations:
    Jan-Jun = first semester and Jul-Dec = second semester.
    """
    required = {"year", "semester"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    out = df.copy()
    _validate_semester(out)

    out["_semester_order"] = out["semester"].map(SEMESTER_ORDER)

    out["time_index"] = (
        out["year"].astype(int) * 2
        + out["_semester_order"]
    )

    out = out.sort_values("time_index").reset_index(drop=True)
    out = out.drop(columns="_semester_order")

    return out


def add_outbreak_lag(
    df: pd.DataFrame,
    group_columns: list[str],
    periods: int = 1,
    value_column: str = "new_outbreaks",
) -> pd.DataFrame:
    """Create a lagged historical-outbreak feature within each geography/disease.

    Rows are ordered chronologically by year and semester before calculating
    the lag. Invalid semester labels are rejected rather than silently sorted.
    """
    if periods < 1:
        raise ValueError("periods must be at least 1")

    required = set(group_columns) | {"year", "semester", value_column}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    out = df.copy()
    _validate_semester(out)

    out["_semester_order"] = out["semester"].map(SEMESTER_ORDER)

    out = out.sort_values(
        group_columns + ["year", "_semester_order"]
    ).copy()

    lag_name = f"{value_column}_lag_{periods}"

    out[lag_name] = (
        out.groupby(group_columns, dropna=False)[value_column]
        .shift(periods)
    )

    out = out.drop(columns="_semester_order")

    return out
