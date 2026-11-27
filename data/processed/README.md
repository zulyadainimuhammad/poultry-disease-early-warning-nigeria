# Processed and interim data

This directory is intended for derived outputs created from the source datasets under `data/raw/`. Generated CSVs are not necessarily committed to the public repository; the notebooks or scripts that create them, their inputs, and their transformation rules must be documented.

## Processed WAHIS outputs

The research notebooks refer to these generated files:

- `wahis_analytical_table.csv` — cleaned WAHIS records with stable analytical identifiers and explicit observation-status fields.
- `wahis_administrative_boundary_lookup.csv` — explicit mapping from WAHIS administrative labels to validated ADM1 boundary names, with country-level records kept separate.
- `wahis_climate_integrated.csv` — WAHIS analytical records joined to state-level semester climate summaries using ADM1 + year + semester.
- `wahis_modelling_features.csv` — engineered temporal, geographic, disease, historical-outbreak and climate fields for modelling.

## Interim climate outputs

The climate notebooks refer to:

- `climate/adm1_monthly_climate_2019_2025.csv`
- `climate/adm1_semester_climate_2019_2025.csv`
- `climate/climate_quality_audit.csv`
- `newcastle_climate_integration.csv`

**Reproducibility status:** the current public repository contains the annual ERA5-Land NetCDF source files, but the reviewed climate notebook loads and audits these prepared interim CSVs rather than generating them from the raw NetCDF inputs. A tested raw-to-ADM1-monthly/semester processing script still needs to be added before the climate feature pipeline can be reproduced from a fresh clone.

## Data-quality rules

- Keep unavailable values as missing; do not convert them to zero.
- Distinguish WAHIS Part 1 occurrence status from Part 2 quantitative counts.
- Use conservative, measure-specific consolidation for companion WAHIS rows; retain ambiguity flags where repeated numeric values conflict.
- Preserve species, serotype/subtype and animal-category attributes and document when any of them affect analytical grain.
- Validate ADM1 + year + semester climate keys as unique before a many-to-one join.
- Preserve original WAHIS record identifiers and confirm row-count/record-identity preservation after integration.

Generated files should be accompanied by source-manifest entries and reproducible scripts or notebook cells. The current repository audit and data-source register are in `reports/research_integrity_audit/`.
