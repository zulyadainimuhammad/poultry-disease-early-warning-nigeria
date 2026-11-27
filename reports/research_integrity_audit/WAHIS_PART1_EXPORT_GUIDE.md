# WAHIS Six-Monthly Occurrence-Status Export Guide

## Purpose

Obtain the qualitative disease occurrence-status data needed to distinguish reported presence, confirmed absence, suspected status and no information from the quantitative WAHIS extract already used by this project.

**Do not derive absence from a blank quantitative count.** WOAH describes six-monthly reports as two parts: Part 1 is qualitative occurrence information and Part 2 is quantitative information for diseases reported present.

## Public WAHIS route inspected

1. Open https://wahis.woah.org/ (public interface).
2. Open **Reports** in the top navigation.
3. Select **Six-monthly reports**.
4. In the report-list filter panel, choose **Nigeria** under Country/Territory.
5. The public view inspected on 27 November 2026 displayed an **Export all (59)** button. The number may change as WAHIS updates.
6. Use **Export all** to download the original Excel workbook (.xlsx). Do not edit or resave the original export before archiving it.
7. The inspected listing showed report records from 2022–2025 and included both terrestrial and aquatic report entries. WOAH describes the public WAHIS interface as containing validated data since 2005, so the current listing view does not establish that 2005–2021 reports are unavailable. Older report access must be investigated separately.

## What to preserve in the export

Keep all columns and all report rows in the original workbook. Do not filter the downloaded file before providing it for audit.

Inspect for fields such as country; report year and semester; animal/report type (terrestrial or aquatic); disease; animal category (domestic or wildlife); species (birds); production type (poultry or non-poultry, where applicable); occurrence code and full status description; geographic level or administrative division; report identifier; and submission/update date.

Occurrence status can include disease present, disease limited to one or more zones, infection/infestation, disease absent, suspected, no information and never reported. Preserve the source wording and code; do not collapse categories before analysis.

## Initial analytical scope

For comparison with the current quantitative extract, identify terrestrial report entries, domestic animal category, birds species, poultry production type where that field exists, all relevant disease rows, all available years and both semesters. Preserve both country-level and administrative-area status where available.

Do not assume qualitative Part 1 status has the same geographic grain as quantitative Part 2 records. Some occurrence codes may be reported at country level, while quantitative information can be reported monthly or by first administrative division. Design the join only after inspecting the actual workbook columns and row structure.

## After download

1. Keep the original .xlsx unchanged.
2. Record the download date (UTC), public WAHIS page/filter used and workbook filename.
3. Upload the original workbook for schema and matching checks.
4. Do not replace or delete the current quantitative extract.
5. Keep unmatched or ambiguous report rows as explicit review cases.

## Matching protocol after workbook inspection

- Standardise country and semester labels without changing original source values.
- Map exact disease labels using an explicit reviewed mapping table.
- Match species, animal category and production type before combining status with quantitative data.
- Match geography only where the source supplies compatible geographic detail.
- Retain report identifiers and original rows for traceability.
- Require documented join cardinality and test for unexpected row multiplication.
- Preserve status categories as distinct values.
- Leave quantitative counts missing where the status is no information or quantitative information was not supplied.
- Do not treat disease absent as a zero numeric new-outbreak count unless the source definition and target specification justify that transformation for the intended task.

## Official WOAH references

- WAHIS public interface: https://wahis.woah.org/
- WOAH Disease Data Collection: https://www.woah.org/en/what-we-do/animal-health-and-welfare/disease-data-collection/
- WOAH Six-Monthly Report — Notification Procedure for Terrestrial Animals (2016): https://www.woah.org/fileadmin/Home/eng/Animal_Health_in_the_World/docs/pdf/Demonstration_guides/Semestrial_Terrestrial__A_Guidelines_2016.pdf
- WAHIS glossary of reporting terms: https://rr-asia.woah.org/en/wahis-reporting-glossary/

## Current status

**Public interface and export control located. Excel workbook not yet downloaded or analysed.** No occurrence-status label has been joined to the 1,180-row quantitative extract.