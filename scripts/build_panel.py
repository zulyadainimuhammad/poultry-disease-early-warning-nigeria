"""Build a conservative observed WAHIS panel from a local CSV export."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
from src.data.cleaning import clean_wahis
from src.data.panel import build_observed_panel
from src.data.validation import validate_semester_values, validate_no_exact_duplicates


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to the private/local WAHIS CSV export")
    parser.add_argument("--output", default="data/processed/wahis_observed_panel.csv")
    args = parser.parse_args()
    source = Path(args.input)
    if not source.is_file():
        raise FileNotFoundError(f"Input CSV not found: {source}")
    raw = pd.read_csv(source)
    validate_no_exact_duplicates(raw)
    clean = clean_wahis(raw)
    validate_semester_values(clean)
    panel = build_observed_panel(clean)
    destination = Path(args.output)
    if not destination.is_absolute():
        destination = ROOT / destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(destination, index=False)
    print(f"Raw rows: {len(raw):,}")
    print(f"Observed panel rows: {len(panel):,}")
    print(f"Output: {destination}")
    print("Note: absent keys and missing measures remain unlabelled; no zeros were imputed.")


if __name__ == "__main__":
    main()
