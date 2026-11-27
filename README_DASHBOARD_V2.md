# Dashboard revision 2 — visual and interaction improvements

This is an overlay for the existing `poultry-disease-early-warning-nigeria` repository. It does not replace the underlying research or modify its original notebooks and model artefacts.

## Replacements and additions

Replace:
- `app/dashboard.py`
- `.streamlit/config.toml`
- `requirements-dashboard.txt`

Add:
- `app/requirements.txt` (hosted-app dependencies, deliberately smaller than the research environment)
- `scripts/generate_dashboard_qr.py`
- `DEPLOY_AND_QR_GUIDE.md`

## What changed

- More consistent, accessible colour palette with disease-specific colours reused across charts.
- Chronological x-axis uses numeric semester ordering; missing periods remain gaps rather than being connected or filled as zero.
- Clear distinction between project-wide headline metrics and currently filtered metrics.
- Relationship explorer with matched sample counts, optional log x-axis, descriptive trend line and disease-specific correlation table.
- Geography section includes selected-area drill-down, time history and supporting records table.
- Model tab adds residual distribution, residual-vs-actual and fold-level error charts.
- Data-quality tab adds observed-count availability by disease and a state-by-disease coverage heatmap.
- Research walkthrough is now a two-column stage selector with status, rationale and evidence.
- New Share / QR tab displays a QR after `APP_PUBLIC_URL` is configured in the deployed app's Streamlit secrets.
- Streamlit Community Cloud deployment guide and standalone QR generator.

## Local installation after extracting the overlay at the project root

```powershell
python -m pip install -r requirements-dashboard.txt
python -m streamlit run app/dashboard.py
```

Run tests:

```powershell
python -m pytest -q
```

Do not commit or merge until tests pass and the dashboard is checked locally. Preserve any existing modified files; this overlay does not replace the user's modified Explainability notebook.
