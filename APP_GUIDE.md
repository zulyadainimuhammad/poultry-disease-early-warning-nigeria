# Poultry Disease Intelligence — Interactive Prototype

This is a local, interactive research-demonstration layer for the existing **Poultry Disease Early Warning System for Nigeria**. It strengthens the current research; it does not replace the original WAHIS, climate, geography or modelling work.

## What the prototype does

- Presents a polished overview of the WAHIS evidence.
- Filters the charts by disease, administrative area and reporting years.
- Lets the audience select chart marks and see the selected value/context.
- Provides an expandable plain-language explanation beneath each visual, including what it shows, how it is calculated and what it cannot prove.
- Covers disease and time trends, administrative comparisons, relationships between reported measures, model-performance evidence, data quality and a guided explanation of the research stages.
- Keeps missing outbreak counts distinct from confirmed zero counts.

## Recommended way to add it to the existing repository

Extract this ZIP into the root of your existing repository, preserving the folder structure. It adds the following files:

```text
.streamlit/config.toml
APP_GUIDE.md
RUN_DASHBOARD.ps1
app/dashboard.py
notebooks/02b_WAHIS_Exploratory_Data_Analysis.ipynb
requirements-dashboard.txt
src/data/eda.py
tests/test_eda_panel.py
```

The current repository already provides `src/data/cleaning.py`, `src/data/panel.py`, the raw WAHIS CSV and the model evaluation artefacts. The prototype expects those files to remain in their existing locations.

## Run on Windows PowerShell

From the repository root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dashboard.txt
streamlit run app/dashboard.py
```

Or, after creating `.venv`, run:

```powershell
.\RUN_DASHBOARD.ps1
```

The browser will open the local application. Use the left-hand filters to change disease, area and reporting-year range. Click points/bars on charts to inspect values, and expand **Understand this visual** to read the explanation.

## Exploratory Data Analysis notebook

Open `notebooks/02b_WAHIS_Exploratory_Data_Analysis.ipynb` in Jupyter from the repository root or run the notebook with the working directory set to the repository. It complements the dashboard with a reproducible EDA narrative: source structure, missingness, disease coverage, distributions, time trends, geographic comparisons, relationships and modelling-feature checks.

## Data and methodology safeguards

- The dashboard constructs a unique year × semester × administrative division × disease panel.
- Repeated source records are not blindly summed. A numeric measure is kept only when the group's non-missing values are unambiguous. Conflicting measures are flagged and withheld.
- For the new-outbreak count in this source, 445 groups have one observed numeric value; 294 groups remain unavailable.
- The 1,180 raw rows form 739 unique analytical groups. 439 groups contain multiple source rows. There are no exact duplicate source rows and no conflicting repeated `new_outbreaks` values; two groups have conflicting repeated `cases` values.
- Country-level `Nigeria` totals and the unspecified geography are excluded from state-level comparisons. The Nassarawa/Nasarawa spelling variant is harmonised for display.
- State rankings are sums of observed reported counts, not population-adjusted outbreak risk. Reporting intensity and completeness may differ.
- The current Random Forest experiment is retrospective/end-of-semester, and its eight validation folds were also used during model selection. The dashboard does not present it as a live or independently validated future alert service.

## Prototype limits

This first version uses the committed WAHIS extract and saved model-evaluation artefacts. It is not connected to a live surveillance feed. It does not provide veterinary diagnosis, farm-level risk scoring, automatic alerts or an independently validated next-semester forecast. A state map can be added after the geographic boundary join is rechecked inside the app.

## Local checks performed

- Python compilation passed for the app, data helpers and tests.
- Four focused tests passed for conservative grouping, ambiguity flags, missing-not-zero handling and Nasarawa name harmonisation.
- The EDA notebook's code cells compile.
- A live Streamlit browser render was not verified in the build environment because Streamlit was not installed and package installation could not reach the package index. Install the dashboard requirements on the Windows project machine and inspect the actual app before presenting it.
