$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Create the project environment first:"
    Write-Host "py -3.11 -m venv .venv"
    exit 1
}

. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dashboard.txt
streamlit run app/dashboard.py
