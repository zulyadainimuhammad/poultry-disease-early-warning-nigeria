# Poultry Disease Early Warning System for Nigeria

**Research and decision-support project for modelling reported poultry disease outbreak activity using surveillance history and climate-related features.**

**Repository owner:** Zulyadaini Muhammad Aminu  
**Status:** Completed reproducible modelling and evaluation workflow with a validated temporal machine-learning model and production-ready model artefacts.

## 1. Project Overview

This project develops a data-driven early-warning component for poultry disease surveillance in Nigeria. It combines historical reported outbreak information with temporal, disease-history and climate-related features to estimate future reported outbreak counts.

The system is designed as a **decision-support and early-warning component**, not as a disease diagnostic system and not as a replacement for veterinary surveillance or field investigation.

The workflow covers:

1. WAHIS data auditing
2. Data cleaning and validation
3. Analytical-table construction
4. Administrative-boundary validation
5. Climate-data exploration
6. Data integration
7. Feature engineering
8. Baseline modelling
9. Machine-learning model development
10. Formal temporal evaluation
11. Explainability and historical geographic analysis
12. Production model and schema validation

## 2. Research Problem

The central question is:

> Can historical poultry disease surveillance information, combined with temporal, disease-history and climate-related features, support useful early-warning estimates of reported outbreak activity in Nigeria?

The project focuses on **reported surveillance activity**. Reported outbreak counts are not equivalent to true disease prevalence or total disease incidence because surveillance coverage, reporting behaviour, diagnostic capacity and data availability can influence observed records.

## 3. Data and Evidence

The project uses a WOAH/WAHIS quantitative export available for this research together with integrated climate/environmental information.

The source audit identified:

- 1,180 raw source records
- 19 source columns
- reporting years covering 2005–2025
- semester reporting periods
- administrative geographic information
- numeric reported outbreak-count observations
- multiple poultry disease categories
- climate-related variables integrated for modelling where available

Important interpretation rules:

1. A WAHIS dash (-) is treated as missing rather than zero.
2. A missing report is not evidence that disease was absent.
3. An unobserved geography-period-disease combination is not automatically treated as a negative example.
4. Future information is not used to construct predictors for historical validation periods.
5. Model outputs represent predicted reported outbreak counts, not confirmed disease diagnoses.

Raw surveillance data are not redistributed through this repository where data-use restrictions apply.

## 4. Repository Workflow

| Notebook | Purpose |
|---|---|
| 01_WAHIS_Data_Audit.ipynb | Source audit, coverage, missingness and data-quality assessment |
| 02_WAHIS_Data_Cleaning.ipynb | Conservative cleaning and standardisation |
| 03_WAHIS_Analytical_Table.ipynb | Construction of the analytical surveillance table |
| 03b_Administrative_Boundaries_Validation.ipynb | Administrative geography validation and standardisation |
| 04_Climate_Data_Exploration.ipynb | Climate/environmental data exploration |
| 05_Data_Integration.ipynb | Temporal and data-source integration |
| 06_Feature_Engineering.ipynb | Temporal, outbreak-history and climate feature engineering |
| 07_Baseline_Model.ipynb | Baseline modelling |
| 08_Machine_Learning_Models.ipynb | Candidate regression models and rolling-origin validation |
| 09_Model_Evaluation.ipynb | Formal OOS evaluation, error analysis and explainability |
| 10_Explainability_and_Risk_Mapping.ipynb | Model interpretation and historical geographic activity analysis |

## 5. Machine-Learning Methodology

Three regression models were evaluated:

- Random Forest Regressor
- Gradient Boosting Regressor
- Ridge Regression

Random train/test splitting was deliberately avoided. The final evaluation uses **rolling-origin temporal validation with 8 chronological folds** so that each validation period is predicted using information available before that period.

The formal evaluation produced **302 out-of-sample predictions**.

The final model was trained on **445 eligible historical observations** and uses **27 predictor features**.

## 6. Final Model

The selected model is a **Random Forest Regressor**.

The production pipeline uses median imputation for numeric predictors and a Random Forest with:

- 300 trees
- random_state = 42
- parallel execution

The saved model was reloaded successfully and reproduced the same predictions as the in-memory trained pipeline.

## 7. Model Performance

Authoritative out-of-sample results:

| Metric | Result |
|---|---:|
| Validation method | Rolling-origin temporal validation |
| Validation folds | 8 |
| Out-of-sample predictions | 302 |
| Mean fold MAE | 6.515 |
| Mean fold RMSE | 11.594 |
| Pooled MAE | 6.415 |
| Pooled RMSE | 13.207 |
| Pooled median absolute error | 3.218 |

The model demonstrates **moderate predictive performance** under chronological out-of-sample evaluation. Performance varies across time, and the evaluated predictions show an overall tendency toward overprediction.

These results support the model as a **decision-support/early-warning component**, not as a standalone operational disease-alert or diagnostic system.

## 8. Error Analysis

Across the 302 out-of-sample predictions:

- pooled MAE = 6.415
- pooled RMSE = 13.207
- pooled median absolute error = 3.218
- mean signed error = approximately +3.252

Error tends to increase with observed outbreak magnitude.

| Observed magnitude | Records | MAE |
|---|---:|---:|
| Low: 1–5 | 196 | 3.369 |
| Moderate: 6–20 | 77 | 7.136 |
| High: >20 | 29 | 25.085 |

The high-magnitude group is relatively small and should therefore be interpreted cautiously.

## 9. Explainability

Recent outbreak-history variables dominate the predictive signal. Important predictors include:

1. previous_semester_outbreak_count
2. outbreak_history_mean_3
3. outbreak_history_max_3
4. two_semesters_prior_outbreak_count
5. semester_total_precipitation_mm
6. disease_code
7. dewpoint_c
8. semester_mean_wind_component_magnitude_ms

Feature importance describes predictive contribution within this model; it does **not** establish causality.

## 10. Historical Geographic Analysis

The administrative analysis identified **37 state-level administrative divisions** after standardisation.

Reported surveillance activity is not uniform across administrative areas. Higher reported activity in the analytical data includes Jigawa, Kaduna, Osun, Kogi, Akwa Ibom, Benue, Niger, Gombe, Bayelsa and Kwara.

These rankings describe **reported surveillance activity in the available dataset**, not true disease prevalence or geographic disease risk. Differences can reflect disease occurrence, surveillance intensity, reporting completeness, administrative practices and other data-generation processes.

## 11. Production Artefacts

Production-oriented model artefacts are stored in:

artifacts/final_model/

Key files:

- random_forest_pipeline.joblib
- model_metadata.json
- production_schema.json

Formal evaluation artefacts are stored in:

artifacts/evaluation/

including:

- rolling_origin_evaluation_summary.json
- rolling_origin_fold_metrics.csv
- rolling_origin_oos_predictions.csv
- random_forest_feature_importance.csv
- random_forest_oos_permutation_importance.csv
- model_evaluation_dataset.csv
- temporal_period_values.csv

## 12. Production Inference

The project includes a production inference interface that validates:

- input type
- required model features
- prediction finiteness
- non-negative predictions

This provides a foundation for a future API, dashboard or monitoring service.

## 13. Limitations

### Surveillance and reporting bias
The model predicts reported surveillance activity rather than unobserved true disease incidence.

### Limited sample size
The final modelling dataset contains 445 eligible observations and 302 formal out-of-sample predictions.

### Temporal variability
Performance varies between historical validation periods, and future periods may behave differently.

### Prediction error
The model can produce substantial errors, especially for larger outbreak counts.

### Climate interpretation
Climate variables contribute predictive information in this modelling framework, but the project does not establish causal relationships between climate variables and disease outbreaks.

### Geographic interpretation
Historical reporting/activity patterns should not be interpreted as direct disease-risk maps.

### Operational deployment
The current model is a validated research and decision-support component. Prospective validation, monitoring, uncertainty estimation and domain oversight are required before operational deployment.

## 14. Reproducibility and Quality Assurance

The project includes checks covering:

- notebook execution
- data-processing consistency
- reference validation
- knowledge-base validation
- automated tests
- model artefact integrity
- production schema consistency
- evaluation metric consistency
- prediction reproducibility

The project test suite contains **57 tests**, all of which passed during the completed validation workflow.

## 15. Future Work

Recommended next steps include:

- prospective validation using newly reported surveillance data
- improved geographic modelling
- additional environmental and epidemiological variables
- uncertainty estimation and prediction intervals
- calibration and operational threshold selection
- model/data drift monitoring
- external validation with independent surveillance sources
- dashboard/API integration
- veterinary and animal-health stakeholder review

## 16. Conclusion

This project demonstrates a reproducible machine-learning workflow for estimating reported poultry disease outbreak activity in Nigeria.

The final Random Forest achieved a mean fold MAE of **6.515** and mean fold RMSE of **11.594** under eight rolling-origin temporal validation folds, with **302 out-of-sample predictions**.

The strongest predictive signals came primarily from recent outbreak history, while selected climate variables also contributed to prediction.

The evidence supports the feasibility of using historical surveillance and environmental information as part of a **poultry disease early-warning and decision-support system**. The model should complement, rather than replace, veterinary surveillance and field investigation.

## Author

**Zulyadaini Muhammad Aminu**

Data Analyst | Business Intelligence | Data Science | Machine Learning

Kano, Nigeria
