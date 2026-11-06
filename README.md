# Machine Learning-Based Early Warning System for Poultry Disease Outbreaks in Nigeria

**Research focus:** Evidence-led analysis of poultry disease surveillance data, climate and environmental context, and potential early-warning indicators in Nigeria.

**Repository owner:** Zulyadaini Muhammad Aminu  
**Status:** Reproducible data-engineering and validation workflow under development. A validated predictive model and operational alert system have **not** yet been established.

## 1. Research problem

Poultry disease outbreaks threaten animal health, farm livelihoods, food supply and the resilience of Nigeria's poultry value chain. This project investigates whether historical disease surveillance records, combined with suitable climate, environmental and geographic data, can support earlier identification of elevated outbreak risk.

The project is guided by one question:

> Can available poultry disease surveillance, climate and environmental data support reliable, geographically meaningful early-warning signals in Nigeria?

The analysis will be evidence-driven. The disease scope, prediction horizon, geographic unit, target definition and final feature set must be justified from the coverage and quality of the available data.

## 2. Current data evidence and limitations

The initial source is a WOAH/WAHIS quantitative export supplied for this research. The audit recorded:

- 1,180 raw source records and 19 columns;
- reporting years 2005–2025;
- semester reporting periods (Jan-Jun and Jul-Dec);
- 39 administrative divisions in the export;
- 444 candidate rows with numeric reported outbreak counts and known administrative geography;
- numeric outbreak-count observations in the export beginning in 2020;
- four disease categories with numeric outbreak observations in the candidate period.

These are source-export audit findings, not estimates of national disease incidence. The 444 candidate rows are not a balanced training panel.

### Non-negotiable interpretation rules

1. A WAHIS dash (-) is treated as missing, not zero.
2. A missing report is not evidence that disease was absent.
3. An unobserved geography-period-disease combination is not automatically added as a negative example.
4. Multiple source rows for a key are not blindly summed. They may describe different reporting records or measures.
5. A predictive target must be defined and justified before model training.
6. Predictors must be available at the intended warning time. Future information and post-outbreak measurements must not leak into the model.

Raw surveillance data is excluded from this public repository. Keep the original export locally in data/raw/ and check the applicable data-use and redistribution terms before sharing it.

## 3. Implemented components

- WAHIS column standardisation and missing-marker handling.
- Numeric conversion that preserves missing values.
- Candidate extraction for rows with numeric outbreak counts and known geography.
- Semester validation and duplicate checks.
- Conservative observed-panel construction at Administrative Division × Semester × Disease.
- Ambiguity flags where multiple distinct quantitative values occur within one panel key.
- Semester calendar features and grouped lag-feature utilities.
- A logistic-regression baseline pipeline requiring an explicitly validated binary target.
- Chronological holdout splitting and classification metrics including precision, recall, F1, ROC-AUC and PR-AUC where defined.
- Command-line scripts for building the observed panel and training a baseline.
- Automated tests and GitHub Actions test workflow.

## 4. Repository layout

~~~text
configs/                 Project configuration
data/raw/                Local source exports (not committed)
data/interim/            Local intermediate datasets (not committed)
data/processed/          Local validated outputs (not committed)
notebooks/               Research notebooks and analysis sequence
src/data/                Ingestion, cleaning, validation and panel construction
src/features/            Time and lag feature engineering
src/models/               Baseline training, prediction and evaluation
scripts/                  Reproducible command-line entry points
tests/                    Unit and regression tests
reports/                  Research checkpoints and generated report locations
models/                   Locally saved model artefacts (not committed)
~~~

## 5. Local setup

Python 3.11 is the supported development version.

### Windows PowerShell

~~~powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q
~~~

### macOS / Linux

~~~bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q
~~~

## 6. Build the observed WAHIS panel

Place the authorised source export in the local data/raw/ directory. Then run:

~~~bash
python scripts/build_panel.py --input "data/raw/your_wahis_export.csv"
~~~

The default output is data/processed/wahis_observed_panel.csv. The script validates the semester labels and duplicate rows, standardises fields and constructs only observed geography-period-disease keys. It does not fill unobserved keys or impute missing outbreak counts as zero.

## 7. Train a baseline only after target validation

The training command requires a researcher-defined binary target encoded as 0/1 and a time column. The input should contain only features available before the forecast period.

~~~bash
python scripts/train_baseline.py \
  --input data/processed/researcher_validated_model_table.csv \
  --target validated_target \
  --time-column time_index \
  --numeric lagged_outbreak_measure,rainfall_lagged \
  --categorical administrative_division,disease \
  --test-size 0.2
~~~

The later time periods are reserved for testing. The example feature names are illustrative only; do not use a feature unless its provenance, timing, units and availability have been checked. The target must not be created by treating missing WAHIS reports as negative events.

The script saves a fitted baseline bundle under models/baseline.joblib and reports holdout metrics. A fitted model is not automatically a valid early-warning system. Report performance only after checking label quality, temporal separation, geographic leakage, surveillance bias, class balance and calibration.

## 8. Planned research stages

1. Complete WAHIS data audit and source documentation.
2. Validate administrative geography and boundaries.
3. Acquire and document climate/environmental data at defensible spatial and temporal resolutions.
4. Integrate data only after geographic and time alignment checks.
5. Define an outcome and warning horizon that the surveillance data can support.
6. Engineer only predictors available before the warning period.
7. Compare simple baselines with suitable machine-learning models.
8. Evaluate with chronological and, where data permits, geographic holdouts.
9. Explain model behaviour and quantify uncertainty.
10. Build a prototype risk communication interface only if the underlying model is sufficiently validated.
11. Document limitations and obtain domain-expert feedback.

## 9. Research integrity and limitations

The source data may reflect differences in surveillance intensity, reporting completeness, diagnostic capacity, administrative coverage and changes in reporting practice. These factors can create apparent geographic or temporal patterns unrelated to true disease risk.

Until suitable negative observations, reporting denominators or a defensible outcome definition are available, the work may support descriptive surveillance analysis rather than supervised outbreak prediction. Climate association is not, by itself, proof of causation. Any future risk scores must be labelled as research outputs, not veterinary diagnosis or official outbreak alerts.

## 10. Current status

**Completed:** Initial WAHIS structural audit; cleaning and validation utilities; conservative observed-panel builder; feature utilities; baseline modelling/evaluation utilities; unit-test coverage and reproducible command-line entry points.

**Not yet completed:** Publicly reproducible execution against the private WAHIS export; validated geographic-boundary linkage; climate/environment integration; final target and forecast horizon; empirically evaluated model; explainability report; risk map; deployed dashboard or alerting service.

The next practical input required to move from engineering to empirical modelling is the original WAHIS CSV export, plus the documentation/licensing details for the intended climate and geographic datasets.
