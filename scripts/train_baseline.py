"""Train and evaluate a baseline using a chronological holdout.

The input must contain a researcher-validated binary target (0/1) and a time
column. This tool never turns missing WAHIS reports into negative examples.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
from src.models.train import chronological_holdout, fit_baseline, save_model
from src.models.evaluate import classification_metrics, confusion_matrix_values


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="CSV containing validated features and labels")
    parser.add_argument("--target", required=True, help="Explicit binary target encoded as 0/1")
    parser.add_argument("--time-column", required=True, help="Numeric or sortable time index")
    parser.add_argument("--numeric", default="", help="Comma-separated numeric feature columns")
    parser.add_argument("--categorical", default="", help="Comma-separated categorical feature columns")
    parser.add_argument("--test-size", type=float, default=0.2, help="Fraction of distinct later periods held out")
    parser.add_argument("--output", default="models/baseline.joblib")
    args = parser.parse_args()

    source = Path(args.input)
    if not source.is_file():
        raise FileNotFoundError(source)
    numeric = [x.strip() for x in args.numeric.split(",") if x.strip()]
    categorical = [x.strip() for x in args.categorical.split(",") if x.strip()]
    data = pd.read_csv(source)
    train_df, test_df = chronological_holdout(data, args.time_column, args.target, args.test_size)
    result = fit_baseline(train_df, args.target, numeric, categorical)
    features = result.feature_columns
    predictions = result.model.predict(test_df[features])
    scores = result.model.predict_proba(test_df[features])[:, 1]
    metrics = classification_metrics(test_df[args.target], predictions, scores)
    save_model(result, args.output)

    print(f"Training rows: {result.training_rows}")
    print(f"Test rows: {len(test_df)}")
    print(f"Test time range: {test_df[args.time_column].min()} to {test_df[args.time_column].max()}")
    print(f"Metrics: {metrics}")
    print(f"Confusion matrix [TN, FP; FN, TP]: {confusion_matrix_values(test_df[args.target], predictions)}")
    print(f"Model saved: {args.output}")
    print("Research caution: review label validity, surveillance bias, spatial leakage and calibration before interpreting risk.")


if __name__ == "__main__":
    main()
