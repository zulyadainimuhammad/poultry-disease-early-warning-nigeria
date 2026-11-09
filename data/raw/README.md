from pathlib import Path

readme_path = PROJECT_ROOT / "README.md"

readme_content = """# Poultry Disease Early Warning System for Nigeria

**Research and decision-support project for modelling reported poultry disease outbreak activity using surveillance history and climate-related features.**

**Repository owner:** Zulyadaini Muhammad Aminu  
**Status:** Completed reproducible modelling and evaluation workflow with a validated temporal machine-learning model and production-ready model artefacts.

---

## 1. Project Overview

Poultry disease outbreaks can affect animal health, farmer livelihoods, food production and the resilience of Nigeria's poultry value chain.

This project develops a data-driven early-warning component for poultry disease surveillance in Nigeria. It combines historical reported outbreak information with temporal, disease-history and climate-related features to estimate future reported outbreak counts.

The system is designed as a **decision-support and early-warning component**, not as a disease diagnostic system or a replacement for veterinary surveillance and field investigation.

The project follows an evidence-led workflow covering:

1. WAHIS data auditing
2. Data cleaning and validation
3. Analytical-table construction
4. Administrative boundary validation
5. Climate-data exploration
6. Data integration
7. Feature engineering
8. Baseline modelling
9. Machine-learning model development
10. Formal temporal evaluation
11. Explainability and historical risk/activity analysis
12. Production model and schema validation

---

## 2. Research Problem

The central question is:

> Can historical poultry disease surveillance information, combined with temporal, disease-history and climate-related features, support useful early-warning estimates of reported outbreak activity in Nigeria?

The project focuses on **reported surveillance activity**. A reported outbreak count is not equivalent to true disease prevalence or total disease incidence because surveillance coverage, reporting behaviour and data availability can influence observed records.

---

## 3. Data and Evidence

The project uses poultry disease surveillance information derived from the WOAH/WAHIS quantitative export available for this research, together with integrated climate/environmental information.

The source audit identified:

- 1,180 raw source records
- 19 source columns
- reporting years covering 2005–2025
- semester reporting periods
- administrative geographic information
- numeric reported outbreak-count observations
- multiple poultry disease categories
- climate-related variables integrated for modelling where available

The modelling dataset was constructed conservatively from observations that met the project's eligibility rules.

### Important interpretation rules

1. A WAHIS dash (`-`) is treated as missing rather than zero.
2. A missing report is not interpreted as evidence that disease was absent.
3. An unobserved geography-period-disease combination is not automatically treated as a negative example.
4. Future information is not used to construct predictors for historical validation periods.
5. Historical outbreak information is used only through features available within the temporal modelling framework.
6. Model outputs represent predicted reported outbreak counts, not confirmed disease diagnoses.

Raw surveillance data are not redistributed through this repository where data-use restrictions apply.

---

## 4. Repository Workflow

The project is organised into the following notebooks:

### Notebook 01 — WAHIS Data Audit

Audits the raw surveillance export, including:

- schema and column inspection
- missingness
- temporal coverage
- administrative coverage
- disease categories
- numeric outbreak-count availability
- data-quality issues

### Notebook 02 — WAHIS Data Cleaning

Performs conservative cleaning and standardisation while preserving missing values and the meaning of the source data.

### Notebook 03 — WAHIS Analytical Table

Constructs the analytical surveillance table used by subsequent modelling and analysis.

### Notebook 03b — Administrative Boundaries Validation

Validates and standardises administrative geographic information used for historical geographic analysis.

### Notebook 04 — Climate Data Exploration

Explores climate/environmental data and evaluates temporal coverage and variable availability.

### Notebook 05 — Data Integration

Integrates surveillance and climate information while preserving temporal alignment and missing-data information.

### Notebook 06 — Feature Engineering

Creates temporal, disease-history, climate and data-availability features for modelling.

### Notebook 07 — Baseline Model

Establishes baseline modelling and provides a reference point before the final machine-learning models.

### Notebook 08 — Machine Learning Models

Develops and compares:

- Random Forest
- Gradient Boosting
- Ridge Regression

Model selection uses **rolling-origin temporal validation** rather than random train/test splitting.

### Notebook 09 — Model Evaluation

Provides the formal out-of-sample evaluation, error analysis, feature-importance analysis and model integrity checks.

### Notebook 10 — Explainability and Risk Mapping

Interprets the selected model and analyses historical administrative/geographic outbreak activity without presenting historical reporting activity as true disease prevalence.

---

## 5. Machine-Learning Methodology

### Candidate models

Three regression models were evaluated:

- Random Forest Regressor
- Gradient Boosting Regressor
- Ridge Regression

All candidate models use the same temporal validation framework.

### Temporal validation

Random train/test splitting was deliberately avoided because it could allow future information to influence model evaluation.

The final evaluation uses:

**Rolling-origin temporal validation with 8 chronological validation folds.**

Each validation fold predicts a later temporal period using only observations available before that period.

The final validation periods are encoded as:

- 4044
- 4045
- 4046
- 4047
- 4048
- 4049
- 4050
- 4051

The evaluation produced **302 out-of-sample predictions**.

---

## 6. Final Model

The selected model is a:

**Random Forest Regressor**

The Random Forest was selected because it provided the strongest overall performance and stability across the chronological validation folds.

The final production pipeline was trained using **445 eligible historical observations**.

The production pipeline includes:

- numeric feature handling
- median imputation
- Random Forest regression
- deterministic random state
- reproducible prediction behaviour

The final model uses **27 predictor features**.

---

## 7. Model Performance

The authoritative out-of-sample evaluation results are:

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

The mean fold metrics represent performance across the chronological validation folds, while the pooled metrics aggregate all out-of-sample predictions.

### Interpretation

The model demonstrates **moderate predictive performance** under chronological out-of-sample evaluation.

However, performance varies across time. The model also shows a tendency toward overprediction in the evaluated out-of-sample predictions.

Therefore, the results support the model as a **decision-support/early-warning component**, but not as a standalone operational disease-alert system.

---

## 8. Error Analysis

The formal evaluation identified several important characteristics.

### Overall error

Across the 302 out-of-sample predictions:

- pooled MAE = 6.415
- pooled RMSE = 13.207
- pooled median absolute error = 3.218
- mean signed error = approximately +3.252

The positive signed error indicates an overall tendency toward overprediction.

### Error and outbreak magnitude

Prediction error tends to increase as observed outbreak counts become larger.

The magnitude analysis showed:

| Observed magnitude | Records | MAE |
|---|---:|---:|
| Low: 1–5 | 196 | 3.369 |
| Moderate: 6–20 | 77 | 7.136 |
| High: >20 | 29 | 25.085 |

The high-magnitude group contains relatively few observations, so these results should be interpreted cautiously.

---

## 9. Explainability

Feature-importance analysis indicates that historical outbreak information is the dominant source of predictive signal.

The strongest predictors include:

1. `previous_semester_outbreak_count`
2. `outbreak_history_mean_3`
3. `outbreak_history_max_3`
4. `two_semesters_prior_outbreak_count`
5. `semester_total_precipitation_mm`
6. `disease_code`
7. `dewpoint_c`
8. `semester_mean_wind_component_magnitude_ms`

Out-of-sample permutation importance similarly indicates that recent outbreak-history variables contribute substantially to model performance.

This finding should not be interpreted as proof of causality. Feature importance describes predictive contribution within this modelling framework; it does not establish that a variable causes disease outbreaks.

---

## 10. Historical Geographic Analysis

The project also analyses the geographic distribution of reported surveillance activity.

The administrative analysis identified **37 state-level administrative divisions** after standardisation.

Historical reporting/activity is not uniform across administrative areas.

The highest reported activity in the analytical data includes locations such as:

- Jigawa
- Kaduna
- Osun
- Kogi
- Akwa Ibom
- Benue
- Niger
- Gombe
- Bayelsa
- Kwara

These rankings describe **reported surveillance activity in the available dataset**, not true disease prevalence or geographic disease risk.

Differences can arise from disease occurrence, surveillance intensity, reporting completeness, administrative practices and other data-generation processes.

---

## 11. Production Model Artefacts

The repository contains production-oriented model artefacts under:

```text
artifacts/final_model/