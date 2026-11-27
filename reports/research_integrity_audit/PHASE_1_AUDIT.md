# Phase 1 — Research Integrity and Data Readiness Audit

**Project:** Machine Learning-Based Early Warning System for Poultry Disease Outbreaks in Nigeria  
**Audit date:** 27 November 2026  
**Repository baseline:** main at merge commit a3da039f2701a3d31caa5110879076f470b1ea06  
**Scope:** read-only review of the public repository, WAHIS quantitative extract, analytical panel logic, feature-engineering notebooks, model metadata/evaluation artefacts, dashboard code and third-party source documentation.

## Executive assessment

**Readiness: Needs revision before describing the current model as a prospective early-warning service.** The repository already contains a substantial research workflow and a functioning interactive dashboard. It is suitable to demonstrate as an exploratory surveillance analytics prototype, provided its limitations are visible. The main work required is not a new algorithm or a wholesale rewrite; it is to correct the time semantics of historical features, obtain a valid occurrence/absence target where possible, separate retrospective analysis from prospective forecasting, preserve source dimensions and formalise provenance and deployment checks.

The user-facing product should be developed as a Nigeria-focused animal-health intelligence layer that adds transparent reporting-quality analysis, state-level exploration, climate context and carefully validated forecasting to existing official surveillance information. It should not be positioned as a replacement for WOAH's WAHIS platform, which already offers dashboards, mapping and data extraction.

## 1. Source data profile

| Check | Observed result | Interpretation |
|---|---:|---|
| WAHIS quantitative source rows | 1,180 | One extract in data/raw/Quantitative data 2026-10-01.csv |
| Source columns | 19 | Includes year, semester, administrative division, disease, species, serotype and quantitative fields |
| Reporting years | 2005–2025 | 39 distinct six-month reporting labels are present; 2006 H1, 2006 H2 and 2007 H1 are absent |
| Source disease categories | 6 | Only four disease categories have numeric new-outbreak targets in the current model table |
| Base area–disease–semester groups | 739 | Grouping key used in the conservative EDA panel |
| Groups with more than one source row | 439 (59.4%) | Multi-row source structure is material and must remain documented |
| Group-size distribution | 300 single-row; 437 two-row; 2 three-row | Most groups require companion-row consolidation |
| Groups with an unambiguous numeric new-outbreak value | 445 (60.2%) | Numeric target availability at grouped level |
| Groups with no numeric new-outbreak value | 294 (39.8%) | Unavailable reporting, not confirmed absence |
| Exact duplicate source rows | 0 | No exact row duplicates found in this extract |
| Usable Event_id / Outbreak_id values | None | Both fields contain the '-' placeholder throughout this extract; they cannot identify or deduplicate events |

### 1.1 Geography and source dimensions

The raw extract contains 39 distinct administrative-division values when the blank value is included. It contains the Nigeria country-level aggregate, a blank geography, and the spelling variants Nasarawa/Nassarawa. The existing geographic-validation notebook explicitly maps Nassarawa to Nasarawa and Federal Capital Territory to the geoBoundaries label Abuja Federal Capital Territory, and excludes the Nigeria aggregate from an ADM1 join. After standardising the spelling variation and excluding country-level and blank geography, the surveillance panel represents 37 state-level areas (the 36 states plus the FCT).

The model evaluation dataset contains 445 target records: 444 have an ADM1 key and one has no ADM1 key. None is marked as a country-level record. The unlocated row should be excluded from any state-specific forecast or surfaced as an explicit unknown-geography record.

All source rows have Animal Category = Domestic. The Species field is populated as Birds in 735 raw rows and blank on the 445 rows where New outbreaks is numeric. At the base group level, 439 of the 445 target-bearing groups have a Birds value in a companion row; six groups have no non-missing species attribute. The Serotype/Subtype/Genotype field contains 920 blanks, 253 instances of not sampled and 7 instances of not typed. At grouped level, 147 groups have one non-missing serotype/subtype label and 592 have none; no group contains multiple distinct non-missing serotype values in this extract.

**Implication:** the four-field base key is useful for conservatively combining companion rows in this particular extract, but species, animal category and serotype/subtype should be retained as group attributes with ambiguity flags. They should not be silently discarded, and future extracts must be re-audited before assuming the same grain.

### 1.2 Repeated-measure handling

The current panel helper retains a numeric measure only where the group has at most one distinct non-missing value, rather than summing repeated source rows. This is appropriate as a conservative rule for companion rows. In this extract, New outbreaks has no conflicting repeated values. Other measures do have conflicts: Cases in 2 groups, Deaths in 2, Susceptible in 2 and Slaughtered in 1. The existing helper flags these measures as ambiguous and leaves the grouped value missing.

**Required improvement:** retain and expose these ambiguity counts in the dashboard and data-quality report. A dashboard card showing zero conflicting outbreak counts must not imply that every other quantitative measure is conflict-free.

## 2. Target semantics and missingness

The 445 numeric New outbreaks values are all positive: minimum 1, median 3, mean 6.84 and maximum 184. There are no zero-valued target examples in this extract. The remaining 735 raw rows (or 294 grouped observations) have no numeric value in New outbreaks.

WOAH's six-monthly reporting guidance distinguishes the qualitative occurrence/absence reporting (Part 1) from quantitative information for diseases reported present (Part 2). The guidance defines new outbreaks as outbreaks that started during the reporting period and excludes outbreaks that started earlier and continued. It also uses explicit no-information/absence codes in the qualitative reporting workflow. Therefore, a missing value in this quantitative extract cannot safely be relabelled as zero or as confirmed absence.

**High-priority finding:** the current supervised regression dataset contains positive reported counts only. It cannot train a reliable outbreak-occurrence classifier or learn the complete distinction between present, absent and unknown. Its count predictions are conditional on a numeric count being reported in the available quantitative extract.

**Recommended action:** obtain and integrate the corresponding six-monthly qualitative occurrence/absence information (or another authoritative source of confirmed zero periods). Create explicit status categories such as reported presence, confirmed absence, and unknown/not reported. Do not infer confirmed absence from a blank quantitative count. If qualitative data cannot be obtained, keep the model scope explicitly limited to estimating reported counts among observations with numeric targets.

## 3. Historical feature timing — material issue

The feature-engineering notebook constructs previous-semester history with group-wise shift(1), two-semesters-prior with shift(2), and rolling history over the previous three available rows within each ADM1–disease series. It checks only that the referenced row is earlier than the current row; it does not require the temporal index difference to equal one or two calendar semesters.

An independent check of the 1,180-row source grouped into 122 area–disease time series found 617 transitions between consecutive available rows. Of those, 190 (30.8%) are not adjacent calendar semesters. Some transitions span 32 half-year index units, meaning many intervening semesters are absent from that series.

**High-priority finding:** features labelled previous semester and two semesters prior can actually refer to an older available reporting record. Rolling three-row history can also span more than three calendar semesters. This changes the meaning of the feature and may make a forecast appear to have more recent history than it really does.

**Recommended action:** rebuild the lags using exact calendar keys: period t-1 for previous semester and t-2 for two semesters prior. If the exact period has no observed numeric value, leave the lag missing and add explicit availability/recency indicators. Calculate rolling history over the fixed calendar window t-3 to t-1, with the number of observed values in that window. Never silently substitute the previous available row for the immediately preceding semester.

## 4. Forecast timing and climate inputs

The saved model metadata identifies the current experiment as retrospective/end-of-semester estimation. The 27-feature model includes climate measurements from the same semester as the target. In the 445-row model evaluation dataset, 444 records have complete climate predictors and one does not.

These same-period climate variables are appropriate for retrospective association or end-of-period estimation, but they would not all be available before the forecast semester begins. The current experiment therefore does not demonstrate a prospective pre-semester early warning.

**Recommended action:** keep the current Random Forest experiment as a clearly labelled retrospective research baseline. Build a separate prospective experiment using only predictors available at forecast issue time. Candidate inputs include calendar-aligned lagged outbreak history, historical/lagged climate information and any seasonal climate forecast that is demonstrably available at the forecast issue date. Record the forecast issue date and feature availability rules for every fold.

## 5. Model evaluation and selection

The current model has 445 training observations, 27 features and eight chronological rolling-origin folds, producing 302 out-of-sample predictions. The saved metrics are pooled MAE 6.415, pooled RMSE 13.207, pooled median absolute error 3.218 and mean signed error approximately +3.252. The eight folds were also used during candidate model selection; they are development-stage estimates, not an untouched independent final test.

The matched baseline artefact reports the following comparisons:

| Matched comparison | Rows | Random Forest MAE | Baseline MAE | Lower MAE |
|---|---:|---:|---:|---|
| Previous available period | 243 | 6.614 | 5.000 | Historical baseline |
| Previous three available periods mean | 272 | 6.581 | 4.832 | Historical baseline |
| Previous three available periods maximum | 272 | 6.581 | 7.044 | Random Forest |

**High-priority finding:** the current Random Forest should not be presented as the best-performing model overall. The three-period historical mean outperformed it on the matched 272-row comparison. Random Forest beat the three-period maximum comparator, but that does not reverse the first result.

**Recommended action:** correct the lag semantics, build the prospective target and features, then compare all candidate models and baselines on identical time-based validation populations. Keep model selection separate from the final assessment. A truly independent prospective evaluation will require a later period not used for model development; the current extract's latest reporting year is 2025.

The existing notebook also identifies disease_frequency and adm1_disease_record_count as potentially time-leaky because they are computed across the available dataset. They are excluded from the safe candidate feature list and are absent from the final 27-feature model metadata. Preserve that exclusion unless they are rebuilt from training-period data only.

## 6. Data provenance, licensing and public release

The current public repository contains the WAHIS CSV, ERA5-Land yearly source files for 2019–2025 and the geoBoundaries Nigeria ADM1 GeoJSON. However, data/raw/README.md currently says raw WAHIS and third-party datasets are maintained outside the public repository and are not committed by default. That statement does not match the files currently tracked in the repository.

WOAH describes public-interface data as being made available to the public for analysis, interpretation and risk-based decision-making. The precise terms for redistributing this particular bulk export inside a public application or a future commercial service have not been conclusively established by this audit. This should be clarified and documented before commercialisation; retain clear source attribution in the meantime.

The ERA5-Land dataset page identifies the dataset as CC-BY and provides DOI 10.24381/cds.e2161bac. geoBoundaries identifies its country dataset licence as CC-BY 4.0 and requires attribution. The repository's MIT licence applies to the project code; it does not automatically relicense third-party source data.

**Recommended action:** replace the contradictory raw-data README with a source manifest that records provider, dataset title, retrieval/export date, query filters, temporal and geographic coverage, licence/terms, citation, version/checksum and whether public redistribution is authorised. Add a THIRD_PARTY_NOTICES file covering WOAH/WAHIS, Copernicus ERA5-Land and geoBoundaries.

## 7. Product positioning and dashboard quality

WOAH's WAHIS public interface already includes dashboards, mapping tools and extraction of officially validated animal-health information. The project should not be differentiated as merely another map of WAHIS data.

The stronger product proposition is a Nigeria-focused analytical layer that makes reporting coverage and uncertainty explicit, combines surveillance information with climate context, provides state/disease/semester drill-downs, and—after prospective validation—offers transparent forecasts that help animal-health professionals prioritise further investigation.

### Recommended bold visual design direction

Keep the existing navy/teal identity, but use a disciplined high-contrast palette rather than adding arbitrary colours:

- Deep navy for navigation and primary text.
- Teal for observed surveillance information.
- Blue for geographic and time-series exploration.
- Amber for unavailable/incomplete information and caution states.
- Coral for prediction errors and material warnings.
- A colour-blind-conscious fixed disease palette, with labels and symbols so colour is never the only distinction.

Every chart should support purposeful hover detail, click-to-inspect observations, zoom/reset, clear units and denominators, and a plain-language explanation beside the visual. The Nigeria map should support state selection and drill-down. Filters should clearly distinguish project-wide statistics from the selected view. The layout must adapt to phone and desktop screens, with readable type, keyboard support and WCAG 2.2 AA-oriented contrast and interaction checks.

### Product features to build after the data corrections

1. Interactive Nigeria ADM1 choropleth with validated boundary-name joins and state profiles.
2. Separate layers for observed reported counts and numeric reporting completeness; never label missing as zero.
3. Disease-specific temporal profiles, distributions and relationships, including climate views with timing caveats.
4. Calendar-aligned history diagnostics and a prospective forecast view only after model validation.
5. Clickable research explanations that show definition, calculation, denominator, source and limitations.
6. Mobile/responsive layout and a public share/QR flow after data-use and deployment checks.

## 8. Software and deployment readiness

The local application and current test suite have been exercised successfully by the project owner, and the merged main-branch GitHub Actions run completed successfully. However, the current GitHub workflow installs the repository-level requirements and runs the research tests; it does not separately install app/requirements.txt or perform a Streamlit application startup/smoke test.

**Recommended action:** add CI coverage for the dashboard-specific dependency file, Python compilation/import checks and a lightweight Streamlit startup test. Keep Python version aligned with the tested local environment for first deployment, and verify required data/artefact paths are present in the deployed repository.

## 9. Prioritised implementation order

| Priority | Work item | Acceptance evidence |
|---|---|---|
| P0 | Reconcile the source-data manifest and third-party attribution; confirm intended public/commercial reuse | Accurate repository documentation and explicit source-use decision |
| P1 | Retain species/serotype/category attributes and ambiguity diagnostics in the analytical panel | Tests showing companion rows are consolidated without summing conflicting values or dropping source attributes |
| P1 | Replace row-shift history with calendar-aligned lags and fixed calendar rolling windows | Tests for missing intervening periods, no silent carry-back and correct t-1/t-2 joins |
| P1 | Integrate authoritative presence/absence information or explicitly limit the target to observed positive counts | Labelled presence/absence/unknown dataset, or documented conditional-count scope |
| P1 | Create a genuinely prospective forecast dataset using only issue-time-available predictors | Leakage audit, temporal split and reproducible fold dataset |
| P1 | Re-evaluate baselines and candidate models, reserving a future/untouched evaluation period | Matched metrics and independent prospective evaluation plan |
| P2 | Add validated Nigeria map and state drill-down | Boundary join tests and visual verification of all 37 ADM1 areas |
| P2 | Upgrade visual design, chart interactions, explanations and mobile accessibility | Interaction test paths, narrow-screen screenshots and accessibility checks |
| P2 | Add dashboard smoke tests to CI and deploy publicly | GitHub checks pass and deployed URL works on desktop and mobile |

## 10. Decision

**Current product status:** suitable to show as an exploratory surveillance analytics prototype, with the model explicitly labelled retrospective and development-stage.  
**Not yet supported:** claims of validated pre-semester early-warning capability, confirmed zero-outbreak classification, population-adjusted state risk, or operational alert readiness.  
**Next action:** implement the P1 data-model and calendar-lag corrections on a dedicated development branch; do not retrain or replace the current saved model until the new target and feature specification is agreed and testable.

## Sources consulted

- WOAH, Disease Data Collection / WAHIS public data: https://www.woah.org/en/what-we-do/animal-health-and-welfare/disease-data-collection/
- WOAH, Six-monthly Report — Notification Procedure for Terrestrial Animals (2016 guidance; definitions of new outbreaks, total outbreaks, and quantitative/qualitative reporting): https://www.woah.org/fileadmin/Home/eng/Animal_Health_in_the_World/docs/pdf/Demonstration_guides/Semestrial_Terrestrial__A_Guidelines_2016.pdf
- WOAH WAHIS public interface: https://wahis.woah.org/
- Copernicus Climate Data Store, ERA5-Land hourly data, DOI 10.24381/cds.e2161bac and CC-BY licence: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land
- geoBoundaries country downloads, CC-BY 4.0 and attribution requirement: https://www.geoboundaries.org/countryDownloads.html
- Streamlit Community Cloud app dependency and repository structure guidance: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies