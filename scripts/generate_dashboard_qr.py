"""Generate a printable QR code for the deployed public dashboard."""
from __future__ import annotations

import argparse
from pathlib import Path

import qrcode


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Full public dashboard URL, e.g. https://your-app.streamlit.app")
    parser.add_argument("--output", default="artifacts/dashboard_qr.png", help="Output PNG path")
    args = parser.parse_args()

    if not args.url.startswith("https://"):
        parser.error("Provide the full public HTTPS URL, not localhost.")

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=12,
        border=4,
    )
    qr.add_data(args.url)
    qr.make(fit=True)
    image = qr.make_image(fill_color="#102A43", back_color="white")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    print(f"QR code saved to: {output.resolve()}")
    print(f"Encoded URL: {args.url}")


if __name__ == "__main__":
    main()
