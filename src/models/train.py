"""Baseline modelling utilities.

Only explicitly labelled rows are trainable. The module does not infer disease
absence from missing surveillance records. Use a chronological holdout when a
validated time index is available.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


@dataclass
class TrainingResult:
    model: Pipeline
    feature_columns: list[str]
    target_column: str
    training_rows: int


def build_baseline_pipeline(numeric_features: list[str], categorical_features: list[str]) -> Pipeline:
    """Create a reproducible logistic-regression baseline pipeline."""
    transformers = []
    if numeric_features:
        numeric = Pipeline([
            ("imputer", SimpleImputer(strategy="median", add_indicator=True)),
            ("scaler", StandardScaler()),
        ])
        transformers.append(("numeric", numeric, numeric_features))
    if categorical_features:
        categorical = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ])
        transformers.append(("categorical", categorical, categorical_features))
    if not transformers:
        raise ValueError("At least one numeric or categorical feature is required.")
    prep = ColumnTransformer(transformers, remainder="drop")
    return Pipeline([
        ("preprocess", prep),
        ("classifier", LogisticRegression(
            max_iter=2000, class_weight="balanced", random_state=42
        )),
    ])


def fit_baseline(
    df: pd.DataFrame,
    target_column: str,
    numeric_features: list[str],
    categorical_features: list[str],
) -> TrainingResult:
    """Fit a baseline on explicitly labelled rows; reject invalid target data."""
    features = numeric_features + categorical_features
    if not features:
        raise ValueError("At least one feature is required.")
    missing = set(features + [target_column]).difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    labelled = df.dropna(subset=[target_column]).copy()
    if labelled.empty:
        raise ValueError("No labelled rows available; do not infer labels from missing reports.")
    y = labelled[target_column]
    if y.nunique() != 2:
        raise ValueError("Binary baseline requires exactly two observed target classes.")
    if set(pd.Series(y.unique()).tolist()) != {0, 1}:
        raise ValueError("Target must be explicitly encoded as binary 0/1.")
    X = labelled[features]
    pipeline = build_baseline_pipeline(numeric_features, categorical_features)
    pipeline.fit(X, y)
    return TrainingResult(pipeline, features, target_column, len(labelled))


def save_model(result: TrainingResult, path: str | Path) -> None:
    """Persist model and metadata with joblib."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({
        "model": result.model,
        "feature_columns": result.feature_columns,
        "target_column": result.target_column,
        "training_rows": result.training_rows,
    }, destination)


def load_model(path: str | Path) -> dict:
    """Load a model bundle previously written by save_model."""
    return joblib.load(path)
