"""Manual delivery CLI for the €29 RenewView residential solar report.

Run after a Lemon Squeezy order to produce a single customer PDF:

    python scripts/generate_report.py \\
        --name "Maria Silva" \\
        --email maria@example.pt \\
        --location "Faro, Portugal" \\
        --country Portugal \\
        --lat 37.0179 \\
        --lon -7.9304 \\
        --roof-area-m2 80 \\
        --orientation S \\
        --shading light

Run with no arguments for an interactive prompt that asks one field at a time.

Output: ``~/renewview-outputs/reports/customers/<slug>_<YYYY-MM-DD>.pdf``
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import Callable, Optional

from renewview.backend.services.prediction_service import PredictionService
from renewview.backend.services.report_generator import generate_report

VALID_ORIENTATIONS = ("S", "SE", "SW", "E", "W", "N", "NE", "NW")
VALID_SHADING = ("none", "light", "moderate", "heavy")
VALID_LANGS = ("en", "pt", "es", "el")

OUTPUT_ROOT = Path.home() / "renewview-outputs" / "reports" / "customers"


# ── helpers ─────────────────────────────────────────────────


def slugify(name: str) -> str:
    """Lowercase, spaces→hyphens, strip non-alphanumeric (keep hyphens).

    Empty result falls back to ``"customer"`` so we never produce a bare
    ``_<date>.pdf`` filename.
    """
    lowered = name.strip().lower()
    hyphenated = re.sub(r"\s+", "-", lowered)
    cleaned = re.sub(r"[^a-z0-9-]", "", hyphenated)
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")
    return cleaned or "customer"


def _prompt(
    label: str,
    *,
    required: bool = True,
    cast: Optional[Callable[[str], object]] = None,
    choices: Optional[tuple[str, ...]] = None,
    default: Optional[str] = None,
) -> Optional[object]:
    """Ask the user for one value. Re-asks on invalid input.

    Returns ``None`` only when ``required=False`` and the user enters blank.
    """
    hint = ""
    if choices:
        hint = f" [{'/'.join(choices)}]"
    if default is not None:
        hint += f" (default: {default})"
    elif not required:
        hint += " (optional, press Enter to skip)"

    while True:
        raw = input(f"{label}{hint}: ").strip()
        if not raw:
            if default is not None:
                raw = default
            elif not required:
                return None
            else:
                print("  → required, please enter a value.")
                continue
        if choices and raw.lower() not in [c.lower() for c in choices]:
            print(f"  → must be one of: {', '.join(choices)}")
            continue
        if cast is not None:
            try:
                return cast(raw)
            except (TypeError, ValueError):
                print(f"  → could not parse '{raw}', try again.")
                continue
        return raw


def interactive_collect() -> dict:
    """Collect all customer + site fields by asking one at a time."""
    print("RenewView — manual report generator")
    print("Enter customer + site details (Ctrl+C to abort).\n")
    return {
        "name": _prompt("Customer name"),
        "email": _prompt("Customer email"),
        "location": _prompt("Location (e.g. 'Faro, Portugal')"),
        "country": _prompt("Country", choices=("Portugal", "Spain", "Greece", "Italy")),
        "lat": _prompt("Latitude", cast=float),
        "lon": _prompt("Longitude", cast=float),
        "roof_area_m2": _prompt("Roof area in m²", cast=float),
        "orientation": _prompt("Roof orientation", choices=VALID_ORIENTATIONS),
        "shading": _prompt("Shading level", choices=VALID_SHADING),
        "ghi": _prompt(
            "GHI in kWh/m²/day", required=False, cast=float
        ),
        "lang": _prompt("Language", choices=VALID_LANGS, default="en"),
    }


def parse_cli_args(argv: list[str]) -> dict:
    """Parse argparse flags. Errors exit via argparse (clean message, no trace)."""
    parser = argparse.ArgumentParser(
        prog="generate_report.py",
        description="Generate a €29 RenewView residential solar PDF for one customer.",
    )
    parser.add_argument("--name", required=True, help="Customer name")
    parser.add_argument("--email", required=True, help="Customer email")
    parser.add_argument("--location", required=True, help="Free-text location (e.g. 'Faro, Portugal')")
    parser.add_argument(
        "--country",
        required=True,
        choices=["Portugal", "Spain", "Greece", "Italy"],
        help="Country (used by the assessment engine)",
    )
    parser.add_argument("--lat", required=True, type=float, help="Latitude")
    parser.add_argument("--lon", required=True, type=float, help="Longitude")
    parser.add_argument(
        "--roof-area-m2", required=True, type=float, dest="roof_area_m2",
        help="Usable roof area in m²",
    )
    parser.add_argument(
        "--orientation", required=True, choices=list(VALID_ORIENTATIONS),
        help="Roof orientation",
    )
    parser.add_argument(
        "--shading", required=True, choices=list(VALID_SHADING),
        help="Shading level",
    )
    parser.add_argument(
        "--ghi", type=float, default=None,
        help="GHI in kWh/m²/day (default: estimated from latitude)",
    )
    parser.add_argument(
        "--lang", choices=list(VALID_LANGS), default="en",
        help="Report language (default: en)",
    )
    return vars(parser.parse_args(argv))


def build_output_path(name: str, today: Optional[date] = None) -> Path:
    today = today or date.today()
    return OUTPUT_ROOT / f"{slugify(name)}_{today.isoformat()}.pdf"


def run_assessment(inputs: dict) -> dict:
    """Call PredictionService.assess_site for the residential branch.

    Returns the assessment dict shaped for ``generate_report``.
    """
    service = PredictionService()
    return service.assess_site(
        latitude=float(inputs["lat"]),
        longitude=float(inputs["lon"]),
        country=inputs["country"],
        site_type="residential_roof",
        parcel_size_ha=0.0,
        grid_distance_km=0.0,
        ghi=inputs.get("ghi"),
        roof_area_m2=float(inputs["roof_area_m2"]),
        orientation=inputs["orientation"],
        shading=inputs["shading"],
    )


def main(argv: Optional[list[str]] = None) -> int:
    argv = sys.argv[1:] if argv is None else argv

    try:
        inputs = interactive_collect() if not argv else parse_cli_args(argv)
    except KeyboardInterrupt:
        print("\nAborted.")
        return 130
    except EOFError:
        print("\nNo input received. Aborted.")
        return 1

    try:
        assessment = run_assessment(inputs)
    except (TypeError, ValueError, KeyError) as exc:
        print(f"Error: could not run assessment — {exc}")
        return 1
    except Exception as exc:  # noqa: BLE001 — surface a friendly message
        print(f"Error: assessment failed — {exc}")
        return 1

    customer = {
        "name": inputs["name"],
        "email": inputs["email"],
        "location": inputs["location"],
    }
    out_path = build_output_path(inputs["name"])

    try:
        generate_report(assessment, customer, out_path, lang=inputs.get("lang", "en"))
    except RuntimeError as exc:
        print(f"Error: PDF generation failed — {exc}")
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"Error: could not write PDF — {exc}")
        return 1

    abs_path = out_path.resolve()
    print()
    print(f"PDF written: {abs_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
