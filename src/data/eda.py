"""Source-aware helpers for the WAHIS exploratory dashboard.

The dashboard operates at one row per year × semester × administrative
area × disease. Repeated source rows are not blindly summed: a measure is
retained only when the group contains at most one distinct non-missing value.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from src.data.cleaning import clean_wahis
from src.data.panel import build_observed_panel

RAW_COLUMNS = {
    "Year", "Semester", "Administrative Division", "Disease", "New outbreaks"
}
ADMIN_RENAMES = {
    "Nassarawa": "Nasarawa",
    "Federal Capital Territory": "Federal Capital Territory",
}


def load_wahis_source(path: str | Path) -> pd.DataFrame:
    """Read and clean the raw quantitative WAHIS extract."""
    source_path = Path(path)
    if not source_path.is_file():
        raise FileNotFoundError(
            f"WAHIS source file not found: {source_path}. "
            "Run the dashboard from the repository root and check data/raw/."
        )
    raw = pd.read_csv(source_path, dtype="string")
    missing = RAW_COLUMNS.difference(raw.columns)
    if missing:
        raise ValueError(f"Raw WAHIS file is missing expected columns: {sorted(missing)}")
    return clean_wahis(raw)


def build_eda_panel(cleaned: pd.DataFrame) -> pd.DataFrame:
    """Build a conservative state/disease/semester panel for exploration.

    This is an exploratory panel, not automatically the final forecasting
    dataset. Conflicting non-null values are marked ambiguous and left null.
    Missing outbreak reports are never changed to zero.
    """
    panel = build_observed_panel(cleaned)
    panel["year"] = pd.to_numeric(panel["year"], errors="coerce").astype("Int64")
    panel["semester_half"] = (
        panel["semester"].astype("string").str.extract(r"^(Jan-Jun|Jul-Dec)", expand=False)
    )
    panel["semester_order"] = panel["semester_half"].map({"Jan-Jun": 1, "Jul-Dec": 2}).astype("Int64")
    panel["temporal_period"] = (
        panel["year"].astype("Float64") * 2 + (panel["semester_order"].astype("Float64") - 1)
    ).astype("Int64")
    panel["period_label"] = panel["semester"].astype("string")
    panel["admin_raw"] = panel["administrative_division"].astype("string")
    panel["admin_display"] = panel["admin_raw"].replace(ADMIN_RENAMES)
    panel["geography_scope"] = "State / administrative division"
    panel.loc[panel["admin_raw"].eq("Nigeria"), "geography_scope"] = "Country aggregate"
    panel.loc[panel["admin_raw"].isna(), "geography_scope"] = "Unspecified geography"
    panel["outbreak_count_available"] = panel["new_outbreaks"].notna()
    panel["is_state_level"] = panel["admin_raw"].notna() & panel["admin_raw"].ne("Nigeria")
    panel["outbreak_magnitude"] = pd.cut(
        panel["new_outbreaks"],
        bins=[0, 5, 20, float("inf")],
        labels=["Low (1–5)", "Moderate (6–20)", "High (>20)"],
        include_lowest=True,
    )
    return panel.sort_values(["temporal_period", "admin_display", "disease"], na_position="last").reset_index(drop=True)


def source_quality_summary(raw: pd.DataFrame, panel: pd.DataFrame) -> dict[str, int | float]:
    """Return transparent row-level and grouped-level quality statistics."""
    raw_new = pd.to_numeric(raw["new_outbreaks"], errors="coerce")
    multirow = panel["source_record_count"].gt(1)
    return {
        "raw_rows": int(len(raw)),
        "raw_observed_outbreak_rows": int(raw_new.notna().sum()),
        "raw_unavailable_outbreak_rows": int(raw_new.isna().sum()),
        "panel_groups": int(len(panel)),
        "panel_observed_outbreak_groups": int(panel["new_outbreaks"].notna().sum()),
        "panel_unavailable_outbreak_groups": int(panel["new_outbreaks"].isna().sum()),
        "multirow_groups": int(multirow.sum()),
        "conflicting_outbreak_groups": int(panel["new_outbreaks_ambiguous"].sum()),
        "conflicting_cases_groups": int(panel["cases_ambiguous"].sum()) if "cases_ambiguous" in panel else 0,
        "exact_duplicate_rows": int(raw.duplicated().sum()),
        "raw_diseases": int(raw["disease"].nunique(dropna=True)),
        "raw_admin_labels": int(raw["administrative_division"].nunique(dropna=True)),
        "state_admin_areas_after_name_standardisation": int(
            panel.loc[panel["is_state_level"], "admin_display"].nunique(dropna=True)
        ),
        "year_min": int(pd.to_numeric(raw["year"], errors="coerce").min()),
        "year_max": int(pd.to_numeric(raw["year"], errors="coerce").max()),
    }


def state_level_panel(panel: pd.DataFrame) -> pd.DataFrame:
    """Exclude country totals and unknown geography from state comparisons."""
    return panel.loc[panel["is_state_level"]].copy()


def aggregate_observed_counts(
    panel: pd.DataFrame,
    dimensions: Iterable[str],
) -> pd.DataFrame:
    """Sum observed group counts only, retaining missing-only groups as NA.

    The input should already be at the unique state × disease × semester grain.
    This sum describes available reported counts, not complete national burden.
    """
    dims = list(dimensions)
    work = panel.loc[panel["new_outbreaks"].notna()].copy()
    if work.empty:
        return pd.DataFrame(columns=dims + ["reported_outbreaks", "observed_groups"])
    return (
        work.groupby(dims, dropna=False, observed=True)["new_outbreaks"]
        .agg(reported_outbreaks="sum", observed_groups="count")
        .reset_index()
    )


def complete_reporting_periods(
    observed: pd.DataFrame,
    start_year: int,
    end_year: int,
    group_column: str | None = None,
) -> pd.DataFrame:
    """Return a chronological semester series with missing observations left as NA.

    The index is ``year * 2 + (semester_order - 1)``. This ensures Jan-Jun
    precedes Jul-Dec and that absent reporting periods remain gaps rather than
    being silently replaced with zero.
    """
    if start_year > end_year:
        raise ValueError("start_year must be less than or equal to end_year")
    required = {"temporal_period", "new_outbreaks"}
    if group_column:
        required.add(group_column)
    missing = required.difference(observed.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    periods = [year * 2 + offset for year in range(start_year, end_year + 1) for offset in (0, 1)]
    result = pd.DataFrame({"temporal_period": periods})
    if group_column:
        groups = sorted(observed[group_column].dropna().unique().tolist())
        result = pd.MultiIndex.from_product(
            [periods, groups], names=["temporal_period", group_column]
        ).to_frame(index=False)
        values = (
            observed.groupby(["temporal_period", group_column], as_index=False)["new_outbreaks"]
            .sum(min_count=1)
        )
        result = result.merge(values, how="left", on=["temporal_period", group_column])
    else:
        values = observed.groupby("temporal_period", as_index=False)["new_outbreaks"].sum(min_count=1)
        result = result.merge(values, how="left", on="temporal_period")

    result["year"] = result["temporal_period"] // 2
    result["semester_half"] = (result["temporal_period"] % 2).map({0: "Jan–Jun", 1: "Jul–Dec"})
    result["period_label"] = result["semester_half"] + " " + result["year"].astype(str)
    sort_columns = ["temporal_period"] + ([group_column] if group_column else [])
    return result.sort_values(sort_columns).reset_index(drop=True)

def prepare_state_detail_records(detail: pd.DataFrame) -> pd.DataFrame:
    """Return chronological, presentation-ready records for a state drill-down.

    Sort using the internal numeric period key before selecting display columns.
    The numeric key is intentionally not required in the visible table.
    """
    required = {"temporal_period", "disease"}
    missing = required.difference(detail.columns)
    if missing:
        raise ValueError(f"State detail is missing required columns: {sorted(missing)}")

    display_columns = [
        "admin_display", "disease", "period_label", "new_outbreaks",
        "cases", "deaths", "vaccinated", "susceptible",
    ]
    available_columns = [column for column in display_columns if column in detail.columns]
    return (
        detail.sort_values(["temporal_period", "disease"])[available_columns]
        .reset_index(drop=True)
    )

