import pandas as pd
import pytest
from src.models.train import fit_baseline
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
    df = pd.DataFrame({"x": [1, 2, 3], "target": [0, 0, 0]})
    with pytest.raises(ValueError):
        fit_baseline(df, "target", ["x"], [])


def test_classification_metrics_include_pr_auc():
    metrics = classification_metrics([0, 0, 1, 1], [0, 1, 1, 1], [0.1, 0.6, 0.7, 0.9])
    assert metrics["recall"] == 1.0
    assert "pr_auc" in metrics
    assert confusion_matrix_values([0, 0, 1, 1], [0, 1, 1, 1]) == [[1, 1], [0, 2]]
