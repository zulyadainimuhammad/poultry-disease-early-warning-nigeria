# WAHIS Validation Checkpoint

## Project
**Machine Learning-Based Early Warning System for Poultry Disease Outbreaks in Nigeria**

## Checkpoint date
2026-10-06

## Status
WAHIS acquisition, audit and structural validation completed to the point required before geographic integration.

## Evidence established

- Raw WAHIS export: 1,180 records and 19 source columns.
- Exact duplicate rows: 0.
- Records span 2005–2025.
- Numeric `New outbreaks` observations in this export begin in 2020.
- The usable export is semester-based: `Jan-Jun` and `Jul-Dec`.
- The 2020–2025 candidate subset contains 444 records with numeric `New outbreaks` and known administrative geography.
- Four diseases have numeric outbreak observations in the candidate period:
  - Newcastle disease virus (infection)
  - Infectious bursal disease (Gumboro disease)
  - Fowl typhoid
  - Avian infectious bronchitis
- 735 records contain `New outbreaks = -`.
- `-` is treated as missing, not zero.
- Missing `New outbreaks` can coexist with cases, deaths and other disease-activity measures.
- Multiple source records can occur within the same Administrative Division × Semester × Disease.
- Event and outbreak identifiers in this export are not usable for distinguishing individual records because they are reported as `-`.
- Numeric conversion validation produced no negative converted values for the checked epidemiological fields.
- The 444-row outbreak-count subset is an exploratory candidate table, not yet the final modelling panel.
- Missing geography–time–disease combinations must not automatically be assigned zero.

## Methodological decision

The project will not treat a missing outbreak-count field as confirmed disease absence. The final early-warning target will be defined after the WAHIS analytical panel and reporting structure are formally documented.

Quantitative fields such as outbreaks, cases and deaths will not be blindly summed across source records simply because they share the same geography, semester and disease.

## Next stage

**Stage 8 — Administrative Boundaries**

The next dataset acquisition will establish a standard geographic reference layer for Nigerian administrative divisions. Climate and environmental datasets will be integrated only after the geographic layer has been validated.

## Reproducibility

The detailed validation workflow is documented in:

`notebooks/03_WAHIS_Analytical_Table.ipynb`

Raw WAHIS data remains excluded from the public repository through the project's data-handling rules.
