# Data Provenance and Third-Party Source Manifest

**Project:** Poultry Disease Intelligence — Nigeria  
**Last reviewed:** 27 November 2026

This manifest records the third-party data sources currently present in or used by the repository. It is a working register; the owner should complete the exact extraction filters, retrieval timestamp, checksums and source-specific reuse decision from the original download records before a public/commercial release.

| Source | Repository asset / use | Temporal and spatial scope observed | Attribution / licence evidence | Release action |
|---|---|---|---|---|
| WOAH / WAHIS | data/raw/Quantitative data 2026-10-01.csv; poultry disease quantitative surveillance | Nigeria; 2005–2025; six-monthly reports; 1,180 rows in the reviewed extract | WOAH states that public-interface data are available to the public for analysis, interpretation and risk-based decision-making. The exact terms for redistributing this specific bulk export in a hosted or commercial application need a documented decision. | Attribute WOAH/WAHIS and record extraction filters/date; confirm bulk reuse and commercial-product conditions before commercialisation. |
| Copernicus Climate Change Service / ERA5-Land | data/raw/climate/era5_land/2019–2025; climate context and features | 2019–2025 source files; ERA5-Land is a gridded reanalysis with 0.1° x 0.1° grid spacing and hourly source resolution | Dataset page identifies CC-BY licence; DOI 10.24381/cds.e2161bac. | Include Copernicus/C3S attribution and DOI; document variables, aggregation, units, extraction date and spatial aggregation method. |
| geoBoundaries | data/raw/geoBoundaries-NGA-ADM1.geojson; state/ADM1 boundary reference | Nigeria ADM1 | geoBoundaries country dataset is CC-BY 4.0 and requires attribution. | Include geoBoundaries attribution and version/source link; document the explicit Nassarawa and FCT name mappings. |

## Repository consistency issue

The current data/raw/README.md says raw WAHIS and third-party datasets are not committed by default and are maintained outside the public repository. The repository currently tracks the WAHIS CSV, seven yearly ERA5-Land folders (2019–2025) and the Nigeria ADM1 GeoJSON. Update the README so that it accurately describes the files that are actually present and the conditions under which they may be reused.

## Required metadata to complete for each future refresh

- Provider and exact dataset title.
- Original download URL and access date/time (UTC).
- Export/query filters, disease scope, geography, reporting period and other parameters.
- File name, byte size and SHA-256 checksum.
- Provider version / update date and any change from the previous extract.
- Licence / terms URL and attribution text.
- Whether redistribution in a publicly hosted demo and commercial product has been checked.
- Transformations applied, source columns retained/dropped, and resulting analytical grain.
- Owner / reviewer and review date.

## Attribution text to retain in the application

**Animal-health surveillance:** Source: World Organisation for Animal Health (WOAH), World Animal Health Information System (WAHIS), quantitative poultry-disease data extract. The displayed information describes officially reported surveillance records and may be affected by reporting completeness.

**Climate:** Climate context derived from Copernicus Climate Change Service (C3S) ERA5-Land reanalysis, DOI 10.24381/cds.e2161bac. Add the dataset-specific attribution required by the current licence.

**Administrative boundaries:** Nigeria ADM1 boundaries from geoBoundaries, CC-BY 4.0. Attribution to geoBoundaries is required.

## Official references

- WOAH Disease Data Collection: https://www.woah.org/en/what-we-do/animal-health-and-welfare/disease-data-collection/
- WAHIS: https://wahis.woah.org/
- ERA5-Land: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land
- geoBoundaries: https://www.geoboundaries.org/countryDownloads.html