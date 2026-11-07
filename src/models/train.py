"""Baseline modelling utilities.

Only explicitly labelled rows are trainable. Missing surveillance reports are
not negative labels. Evaluation should use a chronological holdout.
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


def chronological_holdout(
    df: pd.DataFrame, time_column: str, target_column: str, test_size: float = 0.2
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split labelled data using later time periods as the test set."""
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")
    missing = {time_column, target_column}.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    labelled = df.dropna(subset=[target_column, time_column]).copy()
    periods = sorted(labelled[time_column].unique())
    if len(periods) < 2:
        raise ValueError("At least two distinct time periods are required.")
    n_test = max(1, int(round(len(periods) * test_size)))
    n_test = min(n_test, len(periods) - 1)
    cutoff = periods[-n_test]
    train = labelled[labelled[time_column] < cutoff].copy()
    test = labelled[labelled[time_column] >= cutoff].copy()
    if train.empty or test.empty:
        raise ValueError("Chronological split produced an empty partition.")
    return train, test


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
        ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)),
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
    pipeline = build_baseline_pipeline(numeric_features, categorical_features)
    pipeline.fit(labelled[features], y)
    return TrainingResult(pipeline, features, target_column, len(labelled))

def rolling_origin_splits(
    df: pd.DataFrame,
    time_column: str,
    target_column: str,
    min_train_periods: int = 2,
    test_periods: int = 1,
) -> list[tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Create expanding-window chronological train/test splits.

    Rolling-origin validation is designed for time-dependent data.
    Instead of randomly splitting the dataset, each validation fold
    trains on earlier periods and tests on a later period.

    Example:

        Periods: 2020, 2021, 2022, 2023, 2024

        Fold 1:
            Train -> 2020, 2021
            Test  -> 2022

        Fold 2:
            Train -> 2020, 2021, 2022
            Test  -> 2023

        Fold 3:
            Train -> 2020, 2021, 2022, 2023
            Test  -> 2024

    Important methodological rules:

    1. Only rows with an observed target are used.
       Missing targets are NOT treated as negative labels.

    2. Training data always comes from periods before
       the test period.

    3. The training window expands as we move forward
       through time.

    4. No future observations are allowed to leak into
       an earlier training fold.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe containing the time and target columns.

    time_column : str
        Name of the chronological time/period column.

    target_column : str
        Name of the binary target column.

    min_train_periods : int, default=2
        Minimum number of chronological periods required
        for the first training window.

    test_periods : int, default=1
        Number of chronological periods used for each
        validation/test window.

    Returns
    -------
    list[tuple[pd.DataFrame, pd.DataFrame]]
        A list of (train, test) dataframe pairs.

    Raises
    ------
    ValueError
        If the input is invalid or there are not enough
        time periods to create at least one fold.
    """

    # ---------------------------------------------------------
    # 1. Validate the minimum training-window size
    # ---------------------------------------------------------
    if min_train_periods < 1:
        raise ValueError(
            "min_train_periods must be at least 1."
        )

    # ---------------------------------------------------------
    # 2. Validate the number of test periods
    # ---------------------------------------------------------
    if test_periods < 1:
        raise ValueError(
            "test_periods must be at least 1."
        )

    # ---------------------------------------------------------
    # 3. Make sure the required columns exist
    # ---------------------------------------------------------
    missing = {
        time_column,
        target_column,
    }.difference(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    # ---------------------------------------------------------
    # 4. Keep only explicitly labelled observations
    #
    # Missing target values are NOT interpreted as zero.
    # This is important for the WAHIS surveillance data because
    # an unreported observation does not necessarily mean
    # that no disease outbreak occurred.
    # ---------------------------------------------------------
    labelled = df.dropna(
        subset=[target_column, time_column]
    ).copy()

    # ---------------------------------------------------------
    # 5. Identify the unique chronological periods
    #
    # sorted() ensures that the validation process moves
    # forward through time rather than using a random order.
    # ---------------------------------------------------------
    periods = sorted(
        labelled[time_column].unique()
    )

    # ---------------------------------------------------------
    # 6. Check that enough periods exist
    #
    # Example:
    # min_train_periods = 2
    # test_periods = 1
    #
    # We need at least:
    # 2 training periods + 1 test period = 3 periods
    # ---------------------------------------------------------
    if len(periods) < min_train_periods + test_periods:
        raise ValueError(
            "Not enough distinct time periods for "
            "rolling-origin validation."
        )

    # ---------------------------------------------------------
    # 7. Create the expanding training/test windows
    # ---------------------------------------------------------
    splits = []

    for train_end in range(
        min_train_periods,
        len(periods) - test_periods + 1,
    ):
        # ---------------------------------------------
        # Training periods:
        # start from the earliest period and expand
        # the training window at every fold.
        # ---------------------------------------------
        train_periods = periods[:train_end]

        # ---------------------------------------------
        # Test periods:
        # immediately follow the training periods.
        # ---------------------------------------------
        test_periods_values = periods[
            train_end:train_end + test_periods
        ]

        # ---------------------------------------------
        # Select the actual observations belonging
        # to the training periods.
        # ---------------------------------------------
        train = labelled[
            labelled[time_column].isin(train_periods)
        ].copy()

        # ---------------------------------------------
        # Select the actual observations belonging
        # to the test periods.
        # ---------------------------------------------
        test = labelled[
            labelled[time_column].isin(test_periods_values)
        ].copy()

        # ---------------------------------------------
        # Safety check:
        # never return an empty training or test fold.
        # ---------------------------------------------
        if train.empty or test.empty:
            continue

        # ---------------------------------------------
        # Store this fold.
        # ---------------------------------------------
        splits.append(
            (train, test)
        )

    # ---------------------------------------------------------
    # 8. Final safety check
    # ---------------------------------------------------------
    if not splits:
        raise ValueError(
            "Rolling-origin validation produced "
            "no valid folds."
        )

    # ---------------------------------------------------------
    # 9. Return all chronological folds
    # ---------------------------------------------------------
    return splits

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
