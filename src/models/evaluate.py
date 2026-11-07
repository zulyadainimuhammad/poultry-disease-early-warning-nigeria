"""Evaluation helpers."""

from __future__ import annotations

from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def classification_metrics(y_true, y_pred, y_score=None) -> dict[str, float]:
    """Calculate core classification metrics.

    When probability/score estimates are supplied, both ROC-AUC and PR-AUC
    are calculated.
    """
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(
            precision_score(y_true, y_pred, zero_division=0)
        ),
        "recall": float(
            recall_score(y_true, y_pred, zero_division=0)
        ),
        "f1": float(
            f1_score(y_true, y_pred, zero_division=0)
        ),
    }

    if y_score is not None:
        metrics["roc_auc"] = float(
            roc_auc_score(y_true, y_score)
        )
        metrics["pr_auc"] = float(
            average_precision_score(y_true, y_score)
        )

    return metrics


def confusion_matrix_values(y_true, y_pred) -> list[list[int]]:
    """Return the binary confusion matrix as [[TN, FP], [FN, TP]]."""
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])

    return matrix.astype(int).tolist()
