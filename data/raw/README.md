# Raw source data

This directory contains the source datasets currently used by the Poultry Disease Intelligence — Nigeria research repository.

## 1. WOAH / WAHIS quantitative poultry-disease extract

**File:** `Quantitative data 2026-10-01.csv`  
**Source:** World Organisation for Animal Health (WOAH), World Animal Health Information System (WAHIS) public interface: https://wahis.woah.org/

The reviewed CSV has 1,180 Nigeria records and 19 columns, covering source reporting years 2005–2025. It contains six poultry disease categories and six-month reporting periods. In this extract, the `New outbreaks` field has 445 numeric values, all positive, and 735 unavailable values. All 445 numeric values occur in 2020–2025.

**Important interpretation:**
- WAHIS six-monthly reporting separates qualitative occurrence information (Part 1) from quantitative information for diseases reported present (Part 2).
- The Part 1 occurrence status distinguishes disease present, absent, suspected and no information.
- The Part 2 `New outbreaks` measure counts outbreaks that started during the reporting period; it excludes outbreaks that started earlier and continued.
- A blank or dash in this quantitative export must not be automatically treated as confirmed absence. Obtain the matching Part 1 occurrence status before constructing an occurrence/absence target.
- Reported outbreak counts are not counts of individual infected birds.
- This file's Event_id and Outbreak_id fields are placeholder values in the reviewed extract and should not be used as unique event identifiers.

WOAH's public-interface data are made available for analysis, interpretation and risk-based decision-making. Before distributing this bulk extract inside a public or commercial service, document the exact extraction, attribution and applicable reuse conditions.

## 2. Copernicus ERA5-Land climate data

**Directory:** `climate/era5_land/`  
**Files:** one annual NetCDF file for each year 2019–2025:
- `2019/era5_land_nigeria_2019.nc`
- `2020/era5_land_nigeria_2020.nc`
- `2021/era5_land_nigeria_2021.nc`
- `2022/era5_land_nigeria_2022.nc`
- `2023/era5_land_nigeria_2023.nc`
- `2024/era5_land_nigeria_2024.nc`
- `2025/era5_land_nigeria_2025.nc`

**Source:** Copernicus Climate Change Service (C3S), ERA5-Land hourly data from 1950 to present. Dataset DOI: https://doi.org/10.24381/cds.e2161bac  
Dataset page: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land

The dataset page identifies a CC-BY licence. Retain Copernicus/C3S attribution and the DOI in all derived data products and public presentations. The ADM1/monthly/semester transformations must document variables, spatial aggregation, units, temporal aggregation and missing-coverage handling.

## 3. Nigeria ADM1 administrative boundaries

**File:** `geoBoundaries-NGA-ADM1.geojson`  
**Provider:** geoBoundaries; Nigeria first-level administrative boundaries.

The geoBoundaries API metadata currently identifies Nigeria ADM1 as boundary ID `NGA-ADM1-27671186`, source GRID3, represented year 2022, 37 administrative units and CC BY 4.0. Verify that the exact file tracked in this repository matches the cited release/version before relying on that metadata in a final data release.

API metadata: https://www.geoboundaries.org/api/current/gbOpen/NGA/ADM1/  
Country download page: https://www.geoboundaries.org/countryDownloads.html

Attribution to geoBoundaries is required. Preserve the source version, checksum and any approved name harmonisations used in the state-level join.

## Reproducibility metadata to record on each refresh

Record the exact source URL, download/export date (UTC), source version, query filters, disease/species/geographic scope, temporal range, filename, byte size, SHA-256 checksum, licence/terms URL, attribution text and transformations. Do not overwrite an old extract without retaining its provenance.
