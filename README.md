# Machine Learning-Based Early Warning System for Poultry Disease Outbreaks in Nigeria

## Project Overview

This repository contains the research implementation for:

**Machine Learning-Based Early Warning System for Poultry Disease Outbreaks in Nigeria**

The project investigates whether climatic and environmental variables, combined with historical poultry disease records, can be used to predict poultry disease outbreak risk in Nigeria.

This is an individual six-week data science fellowship research project. The analytical scope will remain evidence-driven: disease selection, prediction target, geographical granularity, modelling period, and final feature set will be determined after systematic inspection and validation of the available data.

## Core Research Question

> Can climatic and environmental variables, combined with historical poultry disease records, be used to predict poultry disease outbreak risk in Nigeria?

## Supporting Questions

1. What temporal and geographic patterns are present in reported poultry disease records?
2. Which climate and environmental variables are associated with changes in reported outbreak patterns?
3. How accurately can machine learning models predict outbreak risk?
4. Which features contribute most to model predictions?
5. How can model outputs be communicated as interpretable geographic risk information?

## Aim

To develop and evaluate a machine learning framework for predicting poultry disease outbreak risk in Nigeria using historical disease, climate, environmental, and geographic data.

## Objectives

- Identify and integrate relevant disease, climate, environmental, and geographic datasets.
- Characterise temporal and geographic patterns in reported poultry disease.
- Engineer appropriate temporal, climate, environmental, and historical-disease features.
- Develop and compare suitable statistical and machine learning baselines/models.
- Evaluate predictive performance using metrics appropriate for the data and class balance.
- Apply model explainability techniques to understand predictive features.
- Develop a prototype risk visualisation for communicating model outputs.

## Current Data

The initial disease dataset is a WAHIS export covering Nigerian poultry disease records.

Current audit findings from the supplied export:
- 1,180 raw records
- 19 columns
- Years represented: 2005–2025
- 6 poultry disease categories
- 39 administrative divisions represented
- 444 candidate records with numeric reported outbreak counts and known administrative geography
- Candidate numeric-outbreak records occur in 2020–2025
- The WAHIS temporal structure is semester-based (January–June and July–December)

The current analytical design is therefore being validated around **Administrative Division × Semester × Disease** before climate integration and modelling.

### Important data interpretation rule

A missing or non-reported outbreak value must not automatically be interpreted as zero disease occurrence. In particular, **no reported outbreak is not equivalent to confirmed disease absence**.

## Data Sources

The project will document and version the provenance of each external dataset used, including where applicable:
- World Organisation for Animal Health (WOAH) World Animal Health Information System (WAHIS)
- Climate datasets such as ERA5, NASA POWER, or CHIRPS, subject to data suitability and availability
- Environmental and geographic datasets
- Relevant Nigerian agricultural or poultry population data where justified

Raw external data will not be committed to this public repository unless redistribution and licensing conditions have been checked.

## Methodological Workflow

1. Data sourcing and provenance
2. Data inspection and audit
3. Data cleaning
4. Analytical-table construction and validation
5. Exploratory data analysis
6. Climate/environment integration
7. Feature engineering and leakage checks
8. Baseline modelling
9. Machine learning model development
10. Model evaluation and calibration where appropriate
11. Explainability
12. Risk visualisation
13. Research reporting and reproducibility

A genuine early-warning setup requires predictors to be available before the prediction period. Lagged climate variables and historical disease activity will therefore be considered where supported by the data.

## Candidate Modelling Approach

Models will be selected based on the validated target and data structure rather than complexity alone. Potential approaches include:
- Logistic regression as a baseline for binary occurrence
- Random Forest
- XGBoost
- LightGBM where justified and available
- Temporal/deep-learning approaches only if the data volume and temporal structure support them

Potential evaluation metrics include:
- Precision
- Recall
- F1-score
- ROC-AUC
- PR-AUC
- Confusion matrix
- Calibration measures where appropriate

Accuracy alone will not be treated as sufficient for imbalanced outcomes.

## Repository Structure

```
poultry-disease-early-warning-nigeria/
├── data/
│   ├── raw/
│   │   └── README.md
│   ├── interim/
│   │   └── README.md
│   └── processed/
│       └── README.md
├── notebooks/
│   ├── 01_WAHIS_Data_Audit.ipynb
│   ├── 02_WAHIS_Data_Cleaning.ipynb
│   ├── 03_WAHIS_Analytical_Table.ipynb
│   ├── 04_Climate_Data_Exploration.ipynb
│   ├── 05_Data_Integration.ipynb
│   ├── 06_Feature_Engineering.ipynb
│   ├── 07_Baseline_Model.ipynb
│   ├── 08_Machine_Learning_Models.ipynb
│   ├── 09_Model_Evaluation.ipynb
│   └── 10_Explainability_and_Risk_Mapping.ipynb
├── src/
│   ├── data/
│   ├── features/
│   └── models/
├── tests/
├── configs/
├── models/
├── reports/
│   ├── figures/
│   └── tables/
├── .github/
│   └── workflows/
├── .gitignore
├── README.md
├── requirements.txt
├── LICENSE
└── CITATION.cff
```

## Reproducibility

The project is being built as a reproducible research workflow rather than a single exploratory notebook. Data provenance, cleaning rules, validation checks, modelling assumptions, and evaluation decisions will be documented as the work progresses.

## Limitations to Track

Important limitations will be documented rather than hidden, including:
- reporting coverage and surveillance differences across locations and periods
- diagnostic and reporting availability
- changes in reporting practices over time
- incomplete administrative detail in source data
- class imbalance
- uncertainty associated with unreported or missing observations
- data leakage risk when constructing early-warning features

## Project Status

**Phase:** Repository and data-validation setup

**Next research step:** Validate the WAHIS analytical table at Administrative Division × Semester × Disease level and finalise the prediction target from the observed data structure.

## Citation

When the study is formally published, this repository will be updated with the final bibliographic citation and research DOI where applicable.
