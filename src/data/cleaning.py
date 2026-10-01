"""Cleaning utilities for WAHIS poultry disease data."""

from __future__ import annotations

import pandas as pd

MISSING_MARKERS = {"-", "—", "", "NA", "N/A", "na", "n/a", "null", "None"}

NUMERIC_COLUMNS = [
    "new_outbreaks",
    "susceptible",
    "cases",
    "killed_and_disposed_of",
    "slaughtered",
    "deaths",
    "vaccinated",
]

COLUMN_MAP = {
    "Year": "year",
    "Semester": "semester",
    "World region": "world_region",
    "Country": "country",
    "Administrative Division": "administrative_division",
    "Disease": "disease",
    "Serotype/Subtype/Genotype": "serotype_subtype_genotype",
    "Animal Category": "animal_category",
    "Event_id": "event_id",
    "Species": "species",
    "Outbreak_id": "outbreak_id",
    "New outbreaks": "new_outbreaks",
    "Susceptible": "susceptible",
    "Measuring units": "measuring_units",
    "Cases": "cases",
    "Killed and disposed of": "killed_and_disposed_of",
    "Slaughtered": "slaughtered",
    "Deaths": "deaths",
    "Vaccinated": "vaccinated",
}


def standardise_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename known WAHIS columns to stable snake_case names."""
    return df.rename(columns=COLUMN_MAP).copy()


def replace_missing_markers(df: pd.DataFrame) -> pd.DataFrame:
    """Convert WAHIS missing-value markers to pandas NA."""
    out = df.copy()
    for col in out.select_dtypes(include=["object", "string"]).columns:
        out[col] = out[col].replace(list(MISSING_MARKERS), pd.NA)
    return out


def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert known quantitative fields to numeric values."""
    out = df.copy()
    for col in NUMERIC_COLUMNS:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    if "year" in out.columns:
        out["year"] = pd.to_numeric(out["year"], errors="coerce").astype("Int64")
    return out


def clean_wahis(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the initial reproducible WAHIS cleaning rules."""
    out = standardise_columns(df)
    out = replace_missing_markers(out)

    for col in out.select_dtypes(include=["object", "string"]).columns:
        out[col] = out[col].astype("string").str.strip()

    out = convert_numeric_columns(out)

    if {"year", "semester"}.issubset(out.columns):
        out["period"] = (
            out["year"].astype("string") + " | " + out["semester"].astype("string")
        )

    return out


def build_outbreak_candidate_table(df: pd.DataFrame) -> pd.DataFrame:
    """Select rows suitable for initial outbreak-target validation.

    This does not assert disease absence where an outbreak value is missing.
    """
    required = {"new_outbreaks", "administrative_division"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    mask = df["new_outbreaks"].notna() & df["administrative_division"].notna()
    out = df.loc[mask].copy()
    out["reported_outbreak"] = (out["new_outbreaks"] > 0).astype("int8")
    return out
