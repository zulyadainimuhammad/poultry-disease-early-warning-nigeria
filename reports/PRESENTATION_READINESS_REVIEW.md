# Presentation Readiness Review — 25 November 2026

## Scope of this review

This review checks the current research claims, saved evaluation artefacts, period alignment and deployment claims before public presentation. It does not retrain the Random Forest or claim a new independent validation result.

## Confirmed project implementation

- WAHIS surveillance source export: 1,180 rows and 19 columns.
- The audited source period spans 2005–2025 and includes 39 administrative divisions.
- There are 445 modelling-eligible records with numeric observed outbreak counts; 735 rows have unavailable outbreak-count values.
- Available climate data include ERA5-Land files for 2019–2025.
- Administrative reference layer: geoBoundaries Nigeria ADM1.
- Frozen evaluation dataset: 445 observations, 27 predictors and one target.
- Selected estimator: RandomForestRegressor, 300 trees, random_state 42.
- Saved model bundle, production schema and metadata are present.
- Batch and single-record inference checks are documented in Notebook 08.
- GitHub Actions main-branch run #52 (9 November 2026) was successful at the time of review.

## Corrections made in this branch

1. Regenerated temporal_period_values.csv row-by-row from the frozen evaluation dataset using year * 2 + (semester_order - 1).
2. Updated Notebook 09 to validate row-level temporal alignment before constructing chronological folds.
3. Removed a superseded evaluation block that depended on the stale period vector and displayed conflicting MAE/RMSE values.
4. Corrected the model's training-period metadata to the actual calendar range 2020 Jan-Jun through 2025 Jul-Dec.
5. Added explicit metadata that this experiment is retrospective/end-of-semester estimation, that its eight folds were used in model selection, and that it has no untouched independent final holdout.
6. Clarified in README that the current model does not establish pre-semester forecasting, a binary outbreak/no-outbreak classifier, live alerting or veterinary diagnosis.

## Authoritative evaluation figures

The committed final rolling-origin evaluation artefacts report:

| Measure | Result |
|---|---:|
| Validation folds | 8 |
| Validation periods | 2022 Jan-Jun to 2025 Jul-Dec |
| Out-of-sample predictions | 302 |
| Mean fold MAE | 6.515 |
| Mean fold RMSE | 11.594 |
| Pooled MAE | 6.415 |
| Pooled RMSE | 13.207 |
| Pooled median absolute error | 3.218 |
| Mean signed error | +3.252 |

MAE and RMSE are expressed in reported outbreak-count units. Positive mean signed error indicates an average tendency to overpredict. Errors are much larger for the high-count group (29 records; MAE 25.085) than the low-count group (196 records; MAE 3.369).

## Four methodological points and their disposition

### 1. Forecast timing

**Disposition: clarified, not modelled differently in this presentation-day correction.**

The climate inputs describe the same semester as the target. The current experiment is retrospective/end-of-semester estimation. It is not a pre-semester forecast. A prospective system requires lagged climate observations or climate forecasts available before the warning period, a declared warning horizon, and a new evaluation.

### 2. Independent validation

**Disposition: transparently documented; new holdout cannot be created from already-used periods.**

The eight rolling-origin folds were used during model selection and the saved evaluation. They are valid chronological development/validation evidence, but they are not an untouched independent final test set. A defensible final holdout requires later surveillance data or a new external dataset, with the protocol frozen before evaluation.

### 3. Baseline comparison

**Disposition: no unsupported superiority claim.**

A matched same-fold comparison was added and executed by GitHub Actions run #53. On 272 identical validation rows where the previous-three-available-period mean was available, the historical mean baseline MAE was **4.832**, while Random Forest MAE on the same 272 rows was **6.581**. The baseline performed better on MAE by 1.749 outbreak-count units. On 243 identical rows where previous-available-period count was available, the baseline MAE was **5.000** versus Random Forest **6.614**. Random Forest did beat the previous-three-period maximum baseline on 272 matched rows (MAE **6.581** vs **7.044**). Therefore, do not claim Random Forest is best overall; the simple mean baseline is stronger on MAE in the matched sample. All these folds were used in model development/selection; this is not independent final testing.

### 4. Documentation and metric consistency

**Disposition: corrected in this branch.**

Notebook 09 previously contained an earlier evaluation block whose temporal period file did not align with the frozen evaluation dataset and whose metrics conflicted with the later authoritative evaluation. The stale block has been removed. The temporal period file is now regenerated directly from year and semester order and validated row-by-row. The committed evaluation summary remains the source of reported final metrics.

## Additional caveats to state verbally

- All 445 numeric target observations are positive; unavailable outbreak-count records are not negative labels. The model is a regression of observed reported counts, not a classifier for outbreak absence.
- Historical lag features are made by shifting the previous available row within each administrative-division/disease series. When there are unreported gaps, a feature named previous semester may refer to the previous available reporting period rather than the immediately adjacent semester. This should be gap-audited and refactored before prospective deployment.
- Historical geographic results describe reported surveillance activity, not predicted future disease risk or true disease prevalence.
- An inference function and saved pipeline are present, but the repository does not demonstrate a deployed public API, dashboard or live alerting service.

## Recommended next technical phase after the presentation

1. Rebuild gap-aware historical lags on a complete temporal grid, retaining missingness separately from zero.
2. Run a matched rolling-origin comparison of Random Forest and historical baselines on identical fold records.
3. Freeze the modelling protocol and evaluate against a later, untouched surveillance period or independent data source.
4. For prospective warning, redesign the input timing so every predictor is available before the forecast target period.
5. Add prediction intervals/uncertainty and domain review before field use.
6. Only then package a dashboard or API with monitoring and veterinary/government stakeholder oversight.


## Matched baseline comparison results (CI run #53)

| Same-fold comparison | Matched rows | Random Forest MAE | Historical baseline MAE | Better MAE |
|---|---:|---:|---:|---|
| Previous available-period count | 243 | 6.614 | 5.000 | Historical baseline |
| Mean of previous three available periods | 272 | 6.581 | 4.832 | Historical baseline |
| Maximum of previous three available periods | 272 | 6.581 | 7.044 | Random Forest |

The comparison script and workflow are now part of the presentation-readiness PR. GitHub Actions run #53 completed successfully, including unit tests, matched comparisons, and artifact upload.
