"""Prediction entry points."""

from __future__ import annotations


def predict(model, features):
    """Generate predictions using a fitted model."""
    return model.predict(features)
