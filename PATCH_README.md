# Poultry Disease Dashboard V2.2 — tab isolation and Geography repair

## Why this patch is needed

The reported traceback is raised in `render_geography()` when the state-detail table sorts on `temporal_period` after the display-column subset has removed it. Since Streamlit tabs execute all tab bodies by default, the exception in Geography also prevents Relationships, Model performance, Data quality, How it works, and Share / QR from rendering. This is one shared crash, not six separate failures.

## What this patch changes

1. Keeps the Geography data fix: `prepare_state_detail_records()` sorts by the numeric `temporal_period` key before dropping it from the visible table.
2. Makes tabs stateful and lazy with `on_change="rerun"`, and renders only the selected tab using each tab's `.open` property. A problem in one section will no longer take down every other tab.
3. Includes the Geography helper and regression test.

## Apply

1. Stop Streamlit with Ctrl+C.
2. Extract this ZIP into the root of `poultry-disease-early-warning-nigeria`.
3. Replace the three files when Windows asks.
4. Ensure the dashboard dependencies include Streamlit 1.55 or later. The user's current installation is 1.67.0, which supports stateful tabs.
5. Run `python -m pytest -q`.
6. Start with `python -m streamlit run app/dashboard.py`.

This patch does not alter raw data, notebooks, saved model artefacts, or `main`.
