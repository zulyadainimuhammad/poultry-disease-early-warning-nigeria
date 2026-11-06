import pandas as pd
import pytest
from src.data.validation import validate_semester_values, validate_candidate_table
from src.data.panel import build_observed_panel


def test_semester_validation_accepts_wahis_values():
    validate_semester_values(pd.DataFrame({"semester": ["Jan-Jun", "Jul-Dec"]}))


def test_semester_validation_rejects_unknown_value():
    with pytest.raises(ValueError):
        validate_semester_values(pd.DataFrame({"semester": ["Q1"]}))


def test_observed_panel_does_not_fill_missing_combinations_or_zero():
    df = pd.DataFrame({
        "year": [2022, 2022], "semester": ["Jan-Jun", "Jan-Jun"],
        "administrative_division": ["Kano", "Kano"], "disease": ["Newcastle", "Newcastle"],
        "new_outbreaks": [2, None], "cases": [10, None],
    })
    panel = build_observed_panel(df)
    assert len(panel) == 1
    assert panel.loc[0, "source_record_count"] == 2
    assert panel.loc[0, "new_outbreaks"] == 2
    assert panel.loc[0, "cases"] == 10


def test_panel_marks_conflicting_counts_ambiguous():
    df = pd.DataFrame({
        "year": [2022, 2022], "semester": ["Jan-Jun", "Jan-Jun"],
        "administrative_division": ["Kano", "Kano"], "disease": ["Newcastle", "Newcastle"],
        "new_outbreaks": [2, 5],
    })
    panel = build_observed_panel(df)
    assert bool(panel.loc[0, "new_outbreaks_ambiguous"])
    assert pd.isna(panel.loc[0, "new_outbreaks"])


def test_candidate_table_validation_reports_counts():
    df = pd.DataFrame({
        "year": [2022], "semester": ["Jan-Jun"],
        "administrative_division": ["Kano"], "disease": ["Newcastle"], "new_outbreaks": [1],
    })
    stats = validate_candidate_table(df)
    assert stats["rows"] == 1
