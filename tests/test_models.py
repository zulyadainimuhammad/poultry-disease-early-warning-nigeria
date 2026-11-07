import pandas as pd
import pytest
from src.models.train import (
    fit_baseline,
    chronological_holdout,
    rolling_origin_splits,
)
from src.models.evaluate import classification_metrics, confusion_matrix_values


def test_baseline_fits_only_explicitly_labelled_rows():
    df = pd.DataFrame({
        "rainfall": [100.0, 120.0, 80.0, 110.0, 90.0, 130.0],
        "division": ["A", "A", "B", "B", "C", "C"],
        "target": [0, 1, 0, 1, 0, 1],
    })
    result = fit_baseline(df, "target", ["rainfall"], ["division"])
    assert result.training_rows == 6
    assert result.model.predict(df[["rainfall", "division"]]).shape == (6,)


def test_baseline_rejects_single_class_target():
    with pytest.raises(ValueError):
        fit_baseline(pd.DataFrame({"x": [1, 2, 3], "target": [0, 0, 0]}), "target", ["x"], [])


def test_baseline_rejects_non_binary_target():
    with pytest.raises(ValueError):
        fit_baseline(pd.DataFrame({"x": [1, 2, 3, 4], "target": [1, 1, 2, 2]}), "target", ["x"], [])


def test_chronological_holdout_uses_latest_periods_for_test():
    df = pd.DataFrame({"period": [1, 1, 2, 2, 3, 3, 4, 4], "target": [0, 1] * 4})
    train, test = chronological_holdout(df, "period", "target", 0.25)
    assert train["period"].max() == 3
    assert test["period"].min() == 4


def test_chronological_holdout_requires_multiple_periods():
    with pytest.raises(ValueError):
        chronological_holdout(pd.DataFrame({"period": [1, 1], "target": [0, 1]}), "period", "target")


def test_classification_metrics_include_pr_auc():
    metrics = classification_metrics([0, 0, 1, 1], [0, 1, 1, 1], [0.1, 0.6, 0.7, 0.9])
    assert metrics["recall"] == 1.0
    assert "pr_auc" in metrics
    assert confusion_matrix_values([0, 0, 1, 1], [0, 1, 1, 1]) == [[1, 1], [0, 2]]
def test_rolling_origin_uses_expanding_training_windows():
    """
    Check that each new fold expands the training window
    and moves the test period one step forward.
    """

    # Create a simple chronological dataset.
    #
    # There are two observations in each period.
    df = pd.DataFrame({
        "period": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
        "target": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    })

    # Create rolling-origin validation folds.
    splits = rolling_origin_splits(
        df,
        time_column="period",
        target_column="target",
        min_train_periods=2,
        test_periods=1,
    )

    # With five periods and two initial training periods,
    # we should obtain three validation folds:
    #
    # Fold 1 -> Train 1-2, Test 3
    # Fold 2 -> Train 1-3, Test 4
    # Fold 3 -> Train 1-4, Test 5
    assert len(splits) == 3

    # Extract the three folds.
    train1, test1 = splits[0]
    train2, test2 = splits[1]
    train3, test3 = splits[2]

    # Check Fold 1.
    assert train1["period"].max() == 2
    assert test1["period"].tolist() == [3, 3]

    # Check Fold 2.
    assert train2["period"].max() == 3
    assert test2["period"].tolist() == [4, 4]

    # Check Fold 3.
    assert train3["period"].max() == 4
    assert test3["period"].tolist() == [5, 5]


def test_rolling_origin_never_uses_future_periods_for_training():
    """
    Verify that no training fold contains observations
    from the future relative to its test set.
    """

    # Create six chronological periods.
    df = pd.DataFrame({
        "period": [1, 2, 3, 4, 5, 6],
        "target": [0, 1, 0, 1, 0, 1],
    })

    # Create rolling-origin folds.
    splits = rolling_origin_splits(
        df,
        time_column="period",
        target_column="target",
        min_train_periods=2,
        test_periods=1,
    )

    # Check every fold.
    for train, test in splits:

        # The latest training period must always be
        # earlier than the earliest test period.
        assert train["period"].max() < test["period"].min()


def test_rolling_origin_excludes_missing_targets():
    """
    Verify that observations with missing target values
    are excluded from both training and testing.

    Missing targets must NOT be converted into zero.
    """

    # Some target values are deliberately missing.
    df = pd.DataFrame({
        "period": [1, 1, 2, 2, 3, 3],
        "target": [0, None, 1, None, 0, 1],
    })

    # Create rolling-origin folds.
    splits = rolling_origin_splits(
        df,
        time_column="period",
        target_column="target",
        min_train_periods=2,
        test_periods=1,
    )

    # Check every fold.
    for train, test in splits:

        # Neither training nor test data should contain
        # missing target values.
        assert train["target"].notna().all()
        assert test["target"].notna().all()


def test_rolling_origin_requires_enough_periods():
    """
    Verify that the function rejects a dataset that does
    not contain enough chronological periods.
    """

    # Only two periods are available.
    #
    # We require:
    # 2 training periods + 1 test period = 3 periods.
    df = pd.DataFrame({
        "period": [1, 2],
        "target": [0, 1],
    })

    # The function should raise an error because
    # there are not enough periods.
    with pytest.raises(ValueError):
        rolling_origin_splits(
            df,
            time_column="period",
            target_column="target",
            min_train_periods=2,
            test_periods=1,
        )