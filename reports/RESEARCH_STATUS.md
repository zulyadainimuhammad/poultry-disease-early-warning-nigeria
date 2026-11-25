# Research status — 25 November 2026

The research workflow is completed through model development, rolling-origin temporal evaluation, explainability and saved model artefacts.

## Current model scope
The Random Forest estimates reported outbreak counts in an end-of-semester retrospective scenario. Climate features refer to the same semester as the target, so this is not a pre-semester forecast or live outbreak alert.

## Evaluation evidence
- 445 eligible observed-count records.
- 27 predictors.
- Eight chronological rolling-origin folds.
- 302 out-of-sample predictions across 2022 Jan-Jun to 2025 Jul-Dec.
- Pooled MAE 6.415; pooled RMSE 13.207; pooled median absolute error 3.218.
- Mean signed error approximately +3.252 (overall overprediction tendency).

The folds were used during model development/selection, so an untouched independent final holdout is not available. See reports/PRESENTATION_READINESS_REVIEW.md for the presentation corrections and validation caveats.

## Implemented artefacts
- WAHIS audit, cleaning and analytical notebooks.
- ADM1 boundary validation and climate integration.
- Feature engineering and model comparison.
- Saved Random Forest pipeline, metadata and production schema.
- Rolling-origin fold metrics, predictions, evaluation summary and feature-importance artefacts.
- Notebook inference checks and automated CI.

## Outstanding before operational use
- Gap-aware lag feature refactor and re-evaluation.
- Matched baseline comparison on identical rows and folds.
- Independent validation on later or external surveillance observations.
- Prospective feature timing for a true pre-semester warning horizon.
- Uncertainty estimation, monitoring and domain expert review.
- Deployment as a separately tested API/dashboard.
