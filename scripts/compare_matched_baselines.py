"""Matched rolling-origin comparison of Random Forest and historical baselines.

This script uses the frozen 445-row model-evaluation dataset and identical
chronological folds for every model. Historical baselines are compared with
the Random Forest on the exact same rows for which each baseline is available.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
EVALUATION_DIR = ROOT / "artifacts" / "evaluation"
MODEL_DIR = ROOT / "artifacts" / "final_model"

BASELINES = {
    "previous_semester_outbreak_count": "Previous available reporting period",
    "outbreak_history_mean_3": "Mean of previous three available reporting periods",
    "outbreak_history_max_3": "Maximum of previous three available reporting periods",
}


def metrics(y_true: pd.Series, y_pred: pd.Series | np.ndarray) -> dict[str, float]:
    return {
        "n": int(len(y_true)),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "median_absolute_error": float(median_absolute_error(y_true, y_pred)),
    }


def main() -> None:
    data_path = EVALUATION_DIR / "model_evaluation_dataset.csv"
    metadata_path = MODEL_DIR / "model_metadata.json"
    if not data_path.is_file() or not metadata_path.is_file():
        raise FileNotFoundError("Frozen evaluation dataset or model metadata is missing.")

    frame = pd.read_csv(data_path)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    feature_columns = metadata["features"]
    target_column = metadata["target_column"]
    required = feature_columns + [target_column, "year", "semester_order"]
    missing = sorted(set(required).difference(frame.columns))
    if missing:
        raise ValueError(f"Evaluation dataset is missing columns: {missing}")
    if len(frame) != 445:
        raise ValueError(f"Expected 445 frozen records, found {len(frame)}")

    # Recompute time from source columns; do not rely on a detached time file.
    frame["temporal_period"] = (
        pd.to_numeric(frame["year"], errors="raise").astype(int) * 2
        + pd.to_numeric(frame["semester_order"], errors="raise").astype(int)
        - 1
    )
    frame = frame.sort_values(["temporal_period"]).reset_index(drop=True)

    validation_periods = [int(x) for x in metadata["validation"]["validation_periods"]]
    preprocessor = ColumnTransformer(
        [("numeric", SimpleImputer(strategy="median"), feature_columns)],
        remainder="drop",
    )
    model = Pipeline([
        ("preprocess", preprocessor),
        ("model", RandomForestRegressor(
            n_estimators=300,
            random_state=42,
            n_jobs=-1,
        )),
    ])

    fold_predictions: list[pd.DataFrame] = []
    fold_rows: list[dict[str, float | int]] = []

    for fold, period in enumerate(validation_periods, start=1):
        train = frame.loc[frame["temporal_period"] < period].copy()
        test = frame.loc[frame["temporal_period"] == period].copy()
        if train.empty or test.empty:
            raise ValueError(f"Fold {fold} (period {period}) has empty train/test data.")

        fitted = Pipeline([
            ("preprocess", ColumnTransformer(
                [("numeric", SimpleImputer(strategy="median"), feature_columns)],
                remainder="drop",
            )),
            ("model", RandomForestRegressor(
                n_estimators=300,
                random_state=42,
                n_jobs=-1,
            )),
        ])
        fitted.fit(train[feature_columns], train[target_column])
        predictions = fitted.predict(test[feature_columns])

        part = test[["temporal_period", target_column]].copy()
        part["fold"] = fold
        part["dataset_row_index"] = test.index
        part["random_forest_prediction"] = predictions
        for column in BASELINES:
            part[column] = test[column].to_numpy()
        fold_predictions.append(part)

        fold_rows.append({
            "fold": fold,
            "period": period,
            "training_rows": len(train),
            "validation_rows": len(test),
            **metrics(test[target_column], predictions),
        })

    oos = pd.concat(fold_predictions, ignore_index=True)
    target = oos[target_column]
    rf_pred = oos["random_forest_prediction"]
    summary = {
        "evaluation": {
            "method": "same eight rolling-origin folds used in model development",
            "independent_final_holdout": False,
            "folds": len(validation_periods),
            "out_of_sample_predictions": len(oos),
            "validation_periods": validation_periods,
            "random_forest_all_rows": metrics(target, rf_pred),
        },
        "matched_comparisons": {},
        "fold_metrics": fold_rows,
    }

    for column, label in BASELINES.items():
        common = oos[column].notna()
        if not common.any():
            continue
        rf_common = oos.loc[common, "random_forest_prediction"]
        actual_common = oos.loc[common, target_column]
        baseline_common = oos.loc[common, column]
        summary["matched_comparisons"][column] = {
            "baseline_label": label,
            "matched_rows": int(common.sum()),
            "random_forest_on_same_rows": metrics(actual_common, rf_common),
            "historical_baseline": metrics(actual_common, baseline_common),
            "mae_difference_rf_minus_baseline": float(
                mean_absolute_error(actual_common, rf_common)
                - mean_absolute_error(actual_common, baseline_common)
            ),
        }

    output_json = EVALUATION_DIR / "matched_baseline_comparison.json"
    output_csv = EVALUATION_DIR / "matched_baseline_oos_predictions.csv"
    output_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    oos.to_csv(output_csv, index=False)

    print(json.dumps(summary, indent=2))
    print(f"Saved: {output_json}")
    print(f"Saved: {output_csv}")


if __name__ == "__main__":
    main()
