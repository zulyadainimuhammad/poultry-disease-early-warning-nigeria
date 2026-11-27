# WAHIS Six-Monthly Occurrence-Status Acquisition Guide

## Purpose

Obtain the disease-level occurrence-status information needed to distinguish reported presence, confirmed absence, suspected status and no information from the quantitative WAHIS extract already used by this project.

**Do not derive absence from a blank quantitative count.** WOAH's six-monthly reporting procedure separates Part 1 qualitative occurrence information from Part 2 quantitative information for diseases reported present.

## 1. What the uploaded CSV contains

The project owner uploaded `SMR_2026-11-27_05-54.csv`, exported from the public Nigeria Six-monthly Reports register. It is a report catalogue, not the disease-level occurrence dataset.

- 59 Nigeria report-register entries, all marked Validated.
- 42 terrestrial reports: exactly one First-semester and one Second-semester report for every year 2005–2025.
- 17 aquatic reports, in addition to the terrestrial reports.
- The final source column was named `undefined`; its values are `report_info_id` values used in the public report-review URL.
- Report IDs alone are not unique across animal types; the report-info identifier is unique within this register export.

The cleaned index `WAHIS_Nigeria_SMR_Report_Register_Clean.csv` renames the fields, preserves the original report IDs and report-info IDs, and constructs report-review links. It is an index only; it does not contain disease status rows.

## 2. Public report navigation

1. Open https://wahis.woah.org/.
2. Open **Reports → Six-monthly reports**.
3. Filter Country/Territory to **Nigeria**.
4. Use **Export all** to download the report-register CSV.
5. Use each terrestrial row's report ID and report-info ID to open the individual review page.

Example inspected report: Nigeria, Terrestrial, First semester 2025, Report ID `SMR_175738`, report-info ID `126754`.

`https://wahis.woah.org/#/smr-review/175738?reportInfoId=126754&fromPage=smr-management-url`

The inspected 2025 report page exposed sections for Disease situation, Quantitative data, Surveillance and control measures, and Animal population. A public **Download PDF** control was visible. The disease-level status and quantitative data must be extracted from this individual report, not from the register CSV.

A historical 2005 First-semester detail route was tested using Report ID `13426` and report-info ID `17478`. The page shell loaded but the report-specific content and PDF control were not visible in that browser check. This is a rendering/retrieval limitation in the check, not evidence that the underlying historical report does not exist.

## 3. Possible public preview endpoint for automated retrieval

An independent open-source project documents the public WAHIS preview route:

`https://wahis.woah.org/smr/pi/report/{report_id}?format=preview`

Its six-monthly ingestion script calls this route for each report and then transforms the response into structured summary and detail tables. The summary includes disease status (present/absent/unreported) and case counts by country, disease and taxa; the detail output contains finer temporal and/or spatial case data where available.

Reference implementation (independent, non-WOAH code):

- Repository: https://github.com/ecohealthalliance/wahis
- Six-monthly ingestion script: https://github.com/ecohealthalliance/wahis/blob/master/inst/processing_scripts/process_six_month_reports.R

**Current retrieval status:** testing the preview endpoint for the 2025 First-semester Nigeria report returned HTTP 503 during this audit. The endpoint path and transformation approach are therefore a promising lead, not a successfully completed extraction. Do not build a production ingestion job around it until response availability, schema, rate limits and terms have been verified.

## 4. Acquisition sequence

1. Preserve the original report-register CSV unchanged.
2. Use the cleaned report index to select the 42 terrestrial reports for 2005–2025.
3. Test the preview endpoint first on one recent report and one historical report. Record HTTP status, content type, response shape and any API errors.
4. If the preview route works, retrieve reports in small batches with polite rate limits and retry/backoff; retain the raw response for every report.
5. If the preview route is unavailable, use the individual report-review page's public PDF download for a small sample, verify PDF text/table extraction, and then decide whether to retrieve the remaining reports by PDF or seek a supported bulk API route from WOAH.
6. Keep the original report responses/PDFs and a report-level extraction log. Never overwrite original source files.

## 5. What to preserve from the report detail

Keep all report rows and columns before filtering. Inspect and preserve:

- Country, report ID, report-info ID, report year and semester.
- Report status, report date and validation date.
- Animal type (terrestrial / aquatic).
- Disease name and the exact source disease label.
- Occurrence code and full occurrence-status description.
- Animal category (domestic / wildlife), species and production type where available.
- Geographic level and administrative division / zone where available.
- All quantitative fields, units and the report's denominator/population context.
- Source identifiers and row-level provenance.

Occurrence status may include disease present, disease limited to one or more zones, disease suspected, disease absent, no information and never reported. Preserve the exact status and code; do not collapse categories before analysis.

## 6. Matching protocol

- Standardise country, year and semester labels without overwriting original values.
- Map disease names using a reviewed explicit crosswalk; preserve unmatched source labels.
- Match animal type, category, species and production type before combining report status with quantitative rows.
- Match geography only where the source provides compatible geographic detail. Do not assume Part 1 and Part 2 use the same geographic grain.
- Retain report ID and report-info ID for lineage.
- Enforce expected join cardinality and test for row multiplication.
- Preserve present, absent, suspected, limited-to-zones, no-information and never-reported as separate statuses.
- Do not infer confirmed absence from a blank Part 2 quantitative count.
- Do not convert an occurrence status into a numeric new-outbreak count without checking the official data definition and modelling target.

## Official references

- WAHIS public interface: https://wahis.woah.org/
- WOAH Disease Data Collection: https://www.woah.org/en/what-we-do/animal-health-and-welfare/disease-data-collection/
- WOAH Six-Monthly Report — Notification Procedure for Terrestrial Animals (2016): https://www.woah.org/fileadmin/Home/eng/Animal_Health_in_the_World/docs/pdf/Demonstration_guides/Semestrial_Terrestrial__A_Guidelines_2016.pdf
- WAHIS reporting glossary: https://rr-asia.woah.org/en/wahis-reporting-glossary/

## Current status

**The 59-row report register has been downloaded and audited. The underlying disease-level Part 1 occurrence records have not yet been retrieved or joined.** The preview API returned HTTP 503 in the latest check. The next technical step is to test the public preview API again or validate PDF extraction on a sample report.