import pandas as pd
from src.data.cleaning import clean_wahis, build_outbreak_candidate_table


def test_cleaning_standardises_columns_and_preserves_missing():
    raw = pd.DataFrame({
        "Year": ["2022", "2022"], "Semester": ["Jan-Jun", "Jul-Dec"],
        "Administrative Division": ["Kano", "Kano"], "Disease": ["Newcastle", "Newcastle"],
        "New outbreaks": ["-", "2"],
    })
    cleaned = clean_wahis(raw)
    assert pd.isna(cleaned.loc[0, "new_outbreaks"])
    assert cleaned.loc[1, "new_outbreaks"] == 2
    assert cleaned.loc[0, "year"] == 2022


def test_candidate_table_uses_only_numeric_reported_values():
    df = pd.DataFrame({
        "new_outbreaks": [None, 0, 3],
        "administrative_division": ["Kano", "Kano", None],
    })
    result = build_outbreak_candidate_table(df)
    assert len(result) == 1
    assert result.iloc[0]["reported_outbreak"] == 0
