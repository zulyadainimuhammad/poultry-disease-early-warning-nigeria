@'
# Raw Data

This directory contains the source datasets used by the Poultry Disease Early Warning System for Nigeria.

## 1. WAHIS quantitative disease data

File:

`Quantitative data 2026-10-01.csv`

Source:

World Organisation for Animal Health (WOAH), World Animal Health Information System (WAHIS).

The dataset contains the quantitative animal-health surveillance data used in the disease-outbreak analysis and modelling workflow.

WAHIS:
https://wahis.woah.org/

## 2. ERA5-Land climate data

Directory:

`climate/era5_land/`

Annual ERA5-Land files covering 2019–2025 are included in this repository.

Source:

Copernicus Climate Data Store (CDS), ERA5-Land.

Dataset:
https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land

ERA5-Land is distributed under a CC-BY licence. Appropriate attribution should be retained when using or redistributing the data.

## 3. Administrative boundaries

File:

`geoBoundaries-NGA-ADM1.geojson`

This file contains Nigeria administrative-level boundary data used for geographic validation and historical administrative analysis.

## Data organisation

```text
data/raw/
├── Quantitative data 2026-10-01.csv
├── geoBoundaries-NGA-ADM1.geojson
├── climate/
│   └── era5_land/
│       ├── 2019/
│       ├── 2020/
│       ├── 2021/
│       ├── 2022/
│       ├── 2023/
│       ├── 2024/
│       └── 2025/
└── README.md