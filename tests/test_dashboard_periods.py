import pandas as pd

from src.data.eda import complete_reporting_periods


def test_reporting_periods_are_chronological_and_gap_stays_missing():
    observed = pd.DataFrame(
        {
            "temporal_period": [4040, 4042, 4043],
            "new_outbreaks": [3, 7, 4],
        }
    )
    result = complete_reporting_periods(observed, 2020, 2021)
    assert result["period_label"].tolist() == [
        "Jan–Jun 2020", "Jul–Dec 2020", "Jan–Jun 2021", "Jul–Dec 2021"
    ]
    assert result.loc[result["temporal_period"].eq(4041), "new_outbreaks"].isna().all()
    assert result.loc[result["temporal_period"].eq(4042), "new_outbreaks"].iloc[0] == 7


def test_grouped_periods_preserve_disease_series_and_missing_periods():
    observed = pd.DataFrame(
        {
            "temporal_period": [4040, 4041, 4040],
            "disease": ["Newcastle", "Newcastle", "Fowl typhoid"],
            "new_outbreaks": [5, 2, 3],
        }
    )
    result = complete_reporting_periods(observed, 2020, 2020, "disease")
    assert len(result) == 4
    missing = result.loc[
        result["disease"].eq("Fowl typhoid") & result["temporal_period"].eq(4041),
        "new_outbreaks",
    ]
    assert missing.isna().all()
    assert result.loc[result["disease"].eq("Newcastle"), "new_outbreaks"].tolist() == [5, 2]
