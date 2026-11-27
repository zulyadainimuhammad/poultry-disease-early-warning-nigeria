import pandas as pd

from src.data.eda import build_eda_panel
from src.data.cleaning import clean_wahis


def _raw(rows):
    return pd.DataFrame(rows, columns=[
        "Year", "Semester", "World region", "Country", "Administrative Division",
        "Disease", "Serotype/Subtype/Genotype", "Animal Category", "Event_id", "Species",
        "Outbreak_id", "New outbreaks", "Susceptible", "Measuring units", "Cases",
        "Killed and disposed of", "Slaughtered", "Deaths", "Vaccinated",
    ])


def test_build_eda_panel_retains_one_observed_outbreak_count_from_companion_rows():
    raw = _raw([
        [2024, "Jan-Jun 2024", "Africa", "Nigeria", "Kano", "Newcastle", "", "Domestic", "-", "Birds", "-", "4", "100", "Animal", "20", "0", "0", "2", "50"],
        [2024, "Jan-Jun 2024", "Africa", "Nigeria", "Kano", "Newcastle", "", "Domestic", "-", "Birds", "-", "-", "-", "Animal", "-", "-", "-", "-", "-"],
    ])
    panel = build_eda_panel(clean_wahis(raw))
    assert len(panel) == 1
    assert panel.loc[0, "source_record_count"] == 2
    assert panel.loc[0, "new_outbreaks"] == 4
    assert not bool(panel.loc[0, "new_outbreaks_ambiguous"])


def test_conflicting_repeated_measure_is_flagged_and_not_summed():
    raw = _raw([
        [2024, "Jan-Jun 2024", "Africa", "Nigeria", "Kano", "Newcastle", "", "Domestic", "-", "Birds", "-", "4", "100", "Animal", "20", "0", "0", "2", "50"],
        [2024, "Jan-Jun 2024", "Africa", "Nigeria", "Kano", "Newcastle", "", "Domestic", "-", "Birds", "-", "-", "100", "Animal", "25", "0", "0", "2", "50"],
    ])
    panel = build_eda_panel(clean_wahis(raw))
    assert panel.loc[0, "new_outbreaks"] == 4
    assert pd.isna(panel.loc[0, "cases"])
    assert bool(panel.loc[0, "cases_ambiguous"])


def test_unavailable_outbreak_count_remains_missing_not_zero():
    raw = _raw([
        [2024, "Jul-Dec 2024", "Africa", "Nigeria", "Kano", "Newcastle", "", "Domestic", "-", "Birds", "-", "-", "100", "Animal", "20", "0", "0", "2", "50"],
    ])
    panel = build_eda_panel(clean_wahis(raw))
    assert len(panel) == 1
    assert pd.isna(panel.loc[0, "new_outbreaks"])
    assert not bool(panel.loc[0, "outbreak_count_available"])
    assert panel.loc[0, "temporal_period"] == 4049


def test_nasarawa_name_variant_is_normalised_for_area_comparisons():
    raw = _raw([
        [2024, "Jan-Jun 2024", "Africa", "Nigeria", "Nassarawa", "Newcastle", "", "Domestic", "-", "Birds", "-", "2", "100", "Animal", "20", "0", "0", "2", "50"],
        [2024, "Jan-Jun 2024", "Africa", "Nigeria", "Nasarawa", "Newcastle", "", "Domestic", "-", "Birds", "-", "3", "100", "Animal", "25", "0", "0", "2", "50"],
    ])
    panel = build_eda_panel(clean_wahis(raw))
    assert set(panel["admin_display"].dropna()) == {"Nasarawa"}

def test_prepare_state_detail_records_sorts_before_hiding_period_key():
    from src.data.eda import prepare_state_detail_records

    detail = pd.DataFrame(
        {
            "admin_display": ["Kaduna", "Kaduna", "Kaduna"],
            "disease": ["Newcastle", "Fowl typhoid", "Newcastle"],
            "period_label": ["Jul-Dec 2021", "Jan-Jun 2021", "Jan-Jun 2021"],
            "temporal_period": [4043, 4042, 4042],
            "new_outbreaks": [8, 3, 5],
            "cases": [20, 9, 14],
        }
    )

    result = prepare_state_detail_records(detail)

    assert result["period_label"].tolist() == ["Jan-Jun 2021", "Jan-Jun 2021", "Jul-Dec 2021"]
    assert result["new_outbreaks"].tolist() == [3, 5, 8]
    assert "temporal_period" not in result.columns

