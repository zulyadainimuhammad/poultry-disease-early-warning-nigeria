# Data Provenance and Third-Party Source Manifest

**Project:** Poultry Disease Intelligence — Nigeria  
**Last reviewed:** 27 November 2026

This manifest records the third-party data sources currently present in or used by the repository. It is a working register; the owner should complete the exact extraction filters, retrieval timestamp, checksums and source-specific reuse decision from the original download records before a public/commercial release.

| Source | Repository asset / use | Temporal and spatial scope observed | Attribution / licence evidence | Release action |
|---|---|---|---|---|
| WOAH / WAHIS | data/raw/Quantitative data 2026-10-01.csv; poultry disease quantitative surveillance | Nigeria; 2005–2025 source-row span; quantitative `New outbreaks` values occur only in 2020–2025; 1,180 rows in the reviewed extract | WOAH says official public-interface data are made available without restriction for analysis, interpretation and risk-based decision-making. The specific bulk export's record-level extraction filters and any separate redistribution terms were not present in the repository. The related six-monthly reporting guidance separates qualitative occurrence status (Part 1) from quantitative data for diseases reported present (Part 2). | Attribute WOAH/WAHIS; record extraction filters and date; retrieve/join Part 1 occurrence status where available; document the applicable public-display and commercial-use terms before product launch. |
| Copernicus Climate Change Service / ERA5-Land | data/raw/climate/era5_land/2019–2025; climate context and features | 2019–2025 source files; ERA5-Land is a gridded reanalysis with 0.1° x 0.1° grid spacing and hourly source resolution | Dataset page identifies CC-BY licence; DOI 10.24381/cds.e2161bac. | Include Copernicus/C3S attribution and DOI; document variables, aggregation, units, extraction date and spatial aggregation method. |
| geoBoundaries / GRID3 | data/raw/geoBoundaries-NGA-ADM1.geojson; state/ADM1 boundary reference | Nigeria ADM1; boundary reference year 2022; 37 administrative units | The geoBoundaries API record for NGA ADM1 reports boundaryID `NGA-ADM1-27671186`, source GRID3 and licence CC BY 4.0. Confirm the repository file checksum/version matches the referenced release before publication. | Attribute geoBoundaries and GRID3 source; link the source page; record the boundary ID, represented year and file checksum; document explicit Nassarawa and FCT name mappings. |

## Repository consistency issue

The current data/raw/README.md says raw WAHIS and third-party datasets are not committed by default and are maintained outside the public repository. The repository currently tracks the WAHIS CSV, seven yearly ERA5-Land folders (2019–2025) and the Nigeria ADM1 GeoJSON. In addition, data/processed/README.md contains a block of raw-source documentation under the wrong heading/path, rather than documenting processed outputs. Update both README files so that paths, content and data-use conditions match the actual repository. The public-interface WAHIS data page says public data are available without restriction for analysis, interpretation and risk-based decision-making; the precise terms applicable to this extracted dataset and onward commercial redistribution should be documented rather than guessed.

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
- geoBoundaries Nigeria ADM1 API metadata: https://www.geoboundaries.org/api/current/gbOpen/NGA/ADM1/
- geoBoundaries country downloads: https://www.geoboundaries.org/countryDownloads.html
- WOAH six-monthly reporting guidance: https://www.woah.org/fileadmin/Home/eng/Animal_Health_in_the_World/docs/pdf/Demonstration_guides/Semestrial_Terrestrial__A_Guidelines_2016.pdf