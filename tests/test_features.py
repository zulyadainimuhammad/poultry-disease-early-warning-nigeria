import pandas as pd
import pytest
from src.features.engineering import add_outbreak_lag, add_calendar_features


def test_calendar_features_follow_semester_order():
    df = pd.DataFrame({"year": [2022, 2021], "semester": ["Jan-Jun", "Jul-Dec"]})
    result = add_calendar_features(df)
    assert result.sort_values("time_index")["semester"].tolist() == ["Jul-Dec", "Jan-Jun"]


def test_lag_is_grouped_and_time_ordered():
    df = pd.DataFrame({
        "division": ["Kano", "Kano", "Kano"], "year": [2022, 2021, 2022],
        "semester": ["Jan-Jun", "Jul-Dec", "Jul-Dec"], "new_outbreaks": [3, 1, 4],
    })
    result = add_outbreak_lag(df, ["division"])
    row = result[(result.year == 2022) & (result.semester == "Jul-Dec")].iloc[0]
    assert row["new_outbreaks_lag_1"] == 3


def test_lag_rejects_invalid_semester():
    df = pd.DataFrame({"division": ["Kano"], "year": [2022], "semester": ["Q1"], "new_outbreaks": [1]})
    with pytest.raises(ValueError):
        add_outbreak_lag(df, ["division"])
