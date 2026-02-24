"""Elimination Gates — Pre-ML filters per proposal Section 3.

Sites that fail any gate are classified as "Not Viable" or rerouted
WITHOUT going through the ML classifier. This is a hard business rule.
"""

from dataclasses import dataclass
from typing import Optional

from renewview.config.settings import (
    GATE_G1_EXCLUDED_LAND,
    GATE_G2_MAX_GRID_DISTANCE_KM,
    GATE_G3_MIN_GHI_KWH,
    GATE_G4_MIN_PARCEL_HA_GROUND,
    GATE_G4_SMALL_COMMERCIAL_HA,
)


@dataclass
class GateResult:
    """Result from running a site through elimination gates."""

    passed: bool
    eliminated_by: Optional[str] = None  # e.g., "G1", "G2", "G3"
    reason: Optional[str] = None
    redirect_to: Optional[str] = None  # e.g., "rooftop_assessment"
    flags: list[str] = None

    def __post_init__(self):
        if self.flags is None:
            self.flags = []


def run_elimination_gates(
    land_status: str,
    grid_distance_km: float,
    ghi_kwh: float,
    parcel_size_ha: float,
    site_type: str,
) -> GateResult:
    """Run all 4 elimination gates on a site.

    Args:
        land_status: Land classification (e.g., "agricultural", "wetland", "protected").
        grid_distance_km: Distance to nearest grid connection in km.
        ghi_kwh: Global Horizontal Irradiance in kWh/m²/day.
        parcel_size_ha: Parcel size in hectares.
        site_type: One of "ground_parcel", "commercial_rooftop", "parking_structure".

    Returns:
        GateResult with pass/fail status and reasoning.
    """
    flags = []

    # ── G1: Protected or wetland land → Eliminated ──────────
    if land_status.lower() in GATE_G1_EXCLUDED_LAND:
        return GateResult(
            passed=False,
            eliminated_by="G1",
            reason=f"Land classified as '{land_status}' — protected/restricted zone. "
                   f"Solar development not permitted.",
        )

    # ── G2: Grid distance > 8 km → Eliminated ──────────────
    if grid_distance_km > GATE_G2_MAX_GRID_DISTANCE_KM:
        return GateResult(
            passed=False,
            eliminated_by="G2",
            reason=f"Grid distance {grid_distance_km:.1f} km exceeds {GATE_G2_MAX_GRID_DISTANCE_KM} km "
                   f"maximum — connection costs likely prohibitive.",
        )

    # ── G3: Irradiance < 3.5 kWh/m²/day → Eliminated ──────
    if ghi_kwh < GATE_G3_MIN_GHI_KWH:
        return GateResult(
            passed=False,
            eliminated_by="G3",
            reason=f"Solar irradiance {ghi_kwh:.2f} kWh/m²/day is below {GATE_G3_MIN_GHI_KWH} "
                   f"minimum threshold — insufficient solar resource.",
        )

    # ── G4: Parcel size routing (ground parcels only) ───────
    if site_type == "ground_parcel":
        if parcel_size_ha < GATE_G4_MIN_PARCEL_HA_GROUND:
            return GateResult(
                passed=False,
                eliminated_by="G4",
                reason=f"Parcel {parcel_size_ha:.1f} ha is below {GATE_G4_MIN_PARCEL_HA_GROUND} ha "
                       f"minimum for ground-mount — consider rooftop installation instead.",
                redirect_to="rooftop_assessment",
            )

        if parcel_size_ha < GATE_G4_SMALL_COMMERCIAL_HA:
            flags.append("small_commercial")

    # ── All gates passed ────────────────────────────────────
    return GateResult(passed=True, flags=flags)
