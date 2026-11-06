"""Train a baseline on a researcher-validated, explicitly labelled CSV.

This command intentionally requires an explicit target column. It does not
convert unreported surveillance records into negative examples.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
from sklearn.metrics import classification_report
from src.models.train import fit_baseline, save_model


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="CSV with researcher-validated labels")
    parser.add_argument("--target", required=True, help="Explicit binary target column encoded 0/1")
    parser.add_argument("--numeric", default="", help="Comma-separated numeric feature columns")
    parser.add_argument("--categorical", default="", help="Comma-separated categorical feature columns")
    parser.add_argument("--output", default="models/baseline.joblib")
    args = parser.parse_args()

    path = Path(args.input)
    if not path.is_file():
        raise FileNotFoundError(path)
    numeric = [x.strip() for x in args.numeric.split(",") if x.strip()]
    categorical = [x.strip() for x in args.categorical.split(",") if x.strip()]
    frame = pd.read_csv(path)
    result = fit_baseline(frame, args.target, numeric, categorical)
    save_model(result, args.output)
    print(f"Fitted rows: {result.training_rows}")
    print(f"Features: {result.feature_columns}")
    print(f"Model saved: {args.output}")
    print("WARNING: this is a fitted baseline, not a validated early-warning result.")
    print("Use a chronological holdout and surveillance-bias review before reporting performance.")


if __name__ == "__main__":
    main()
