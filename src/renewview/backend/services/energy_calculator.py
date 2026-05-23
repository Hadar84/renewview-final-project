"""Energy Calculator — kWh and € revenue estimation per proposal Section 4.

Formula: Annual kWh = GHI × 365 × area_m² × panel_efficiency × performance_ratio
Revenue: annual_kWh × country feed-in tariff
"""

from renewview.config.settings import (
    FEED_IN_TARIFFS,
    GROUND_COVERAGE_RATIO,
    PANEL_EFFICIENCY,
    PAES_ELIGIBLE_COUNTRY,
    PAES_MAX_KWP,
    PAES_MIN_KWP,
    PAES_SUBSIDY_CAP_EUR,
    PAES_SUBSIDY_RATE,
    PERFORMANCE_RATIO,
    RESIDENTIAL_INSTALL_COST_PER_KWP,
    RESIDENTIAL_KWH_RATE_EUR,
    ROOF_KWP_PER_M2,
    ROOF_ORIENTATION_DERATE,
    ROOF_SHADING_DERATE,
    ROOF_SYSTEM_PERFORMANCE_RATIO,
    ROOFTOP_COVERAGE_RATIO,
)


def estimate_annual_kwh(
    ghi_kwh_m2_day: float,
    area_m2: float,
    site_type: str = "ground_parcel",
) -> float:
    """Estimate annual energy production in kWh.

    Args:
        ghi_kwh_m2_day: Global Horizontal Irradiance (kWh/m²/day).
        area_m2: Total site area in m². For ground parcels, pass ha × 10000.
        site_type: "ground_parcel", "commercial_rooftop", or "parking_structure".

    Returns:
        Estimated annual kWh production.
    """
    coverage = (
        ROOFTOP_COVERAGE_RATIO
        if site_type in ("commercial_rooftop", "parking_structure")
        else GROUND_COVERAGE_RATIO
    )

    usable_area = area_m2 * coverage
    annual_kwh = ghi_kwh_m2_day * 365 * usable_area * PANEL_EFFICIENCY * PERFORMANCE_RATIO
    return round(annual_kwh, 2)


def estimate_revenue_eur(annual_kwh: float, country: str) -> float:
    """Estimate annual revenue in euros.

    Args:
        annual_kwh: Annual energy production in kWh.
        country: Country name (Portugal, Spain, Greece, Italy).

    Returns:
        Estimated annual revenue in €.
    """
    tariff = FEED_IN_TARIFFS.get(country, 0.065)  # default to Portugal
    return round(annual_kwh * tariff, 2)


def parcel_ha_to_m2(parcel_ha: float) -> float:
    """Convert hectares to square meters."""
    return parcel_ha * 10_000


def feasibility_score(
    ghi: float,
    grid_distance_km: float,
    parcel_size_ha: float,
    model_confidence: float = 0.0,
) -> float:
    """Compute 0–100% feasibility score combining model + heuristics.

    Weighted formula:
      40% model confidence
      30% irradiance quality (GHI normalized to 3.5–6.5 range)
      20% grid proximity (inverse distance, capped at 8 km)
      10% site scale (log-scaled parcel size)

    Args:
        ghi: Global Horizontal Irradiance (kWh/m²/day).
        grid_distance_km: Distance to nearest grid connection.
        parcel_size_ha: Parcel size in hectares.
        model_confidence: ML model prediction confidence (0–1).

    Returns:
        Feasibility score 0–100%.
    """
    import math

    # Normalize GHI: 3.5 = 0%, 6.5 = 100%
    ghi_score = max(0, min(1, (ghi - 3.5) / 3.0))

    # Grid proximity: 0 km = 100%, 8 km = 0%
    grid_score = max(0, 1 - (grid_distance_km / 8.0))

    # Parcel scale: log-scaled, 2 ha = ~30%, 50 ha = ~100%
    scale_score = max(0, min(1, math.log10(max(parcel_size_ha, 0.1)) / math.log10(50)))

    score = (
        0.40 * model_confidence
        + 0.30 * ghi_score
        + 0.20 * grid_score
        + 0.10 * scale_score
    )

    return round(score * 100, 1)


# ── Residential Roof Calculations ───────────────────────────


def residential_system_kwp(
    roof_area_m2: float,
    orientation: str,
    shading: str,
) -> float:
    """Estimate installable PV system size for a residential roof.

    Args:
        roof_area_m2: Usable roof area in m².
        orientation: One of S, SE, SW, E, W, N.
        shading: One of none, light, moderate, heavy.

    Returns:
        Estimated system size in kWp (clamped to >= 0).
    """
    orient_factor = ROOF_ORIENTATION_DERATE.get(orientation.upper(), 0.85)
    shade_factor = ROOF_SHADING_DERATE.get(shading.lower(), 0.75)
    raw_kwp = roof_area_m2 * ROOF_KWP_PER_M2 * orient_factor * shade_factor
    return round(max(0.0, raw_kwp), 2)


def residential_annual_kwh(kwp: float, ghi_kwh_m2_day: float) -> float:
    """Annual production for a residential rooftop system.

    kWh = kWp * GHI * 365 * performance_ratio
    """
    return round(kwp * ghi_kwh_m2_day * 365 * ROOF_SYSTEM_PERFORMANCE_RATIO, 2)


def residential_annual_savings_eur(annual_kwh: float) -> float:
    """Annual € savings on retail electricity for a residential system."""
    return round(annual_kwh * RESIDENTIAL_KWH_RATE_EUR, 2)


def paes_subsidy_estimate(kwp: float, country: str) -> dict:
    """Estimate Portugal PAE+S subsidy eligibility and amount.

    Eligible only when country == Portugal and 1.5 <= kWp <= 10.
    Subsidy = min(€3,000, system_cost * 0.85) where system_cost = kWp * €1,200.
    """
    system_cost = round(kwp * RESIDENTIAL_INSTALL_COST_PER_KWP, 2)
    if country != PAES_ELIGIBLE_COUNTRY:
        return {"eligible": False, "amount_eur": 0.0, "system_cost_eur": system_cost}
    if kwp < PAES_MIN_KWP or kwp > PAES_MAX_KWP:
        return {"eligible": False, "amount_eur": 0.0, "system_cost_eur": system_cost}
    amount = min(PAES_SUBSIDY_CAP_EUR, system_cost * PAES_SUBSIDY_RATE)
    return {"eligible": True, "amount_eur": round(amount, 2), "system_cost_eur": system_cost}


def feasibility_score_residential(
    ghi: float,
    kwp: float,
    orientation: str,
    shading: str,
) -> float:
    """0–100% feasibility score for a residential roof.

    Weights: 30% GHI quality, 30% orientation, 30% shading, 10% kWp scale.
    """
    ghi_score = max(0.0, min(1.0, (ghi - 3.5) / 3.0))
    orient_score = max(
        0.0,
        (ROOF_ORIENTATION_DERATE.get(orientation.upper(), 0.6) - 0.6) / 0.4,
    )
    shade_score = max(
        0.0,
        (ROOF_SHADING_DERATE.get(shading.lower(), 0.5) - 0.5) / 0.5,
    )
    kwp_score = max(0.0, min(1.0, (kwp - 1.5) / 8.5))
    score = (
        0.30 * ghi_score
        + 0.30 * orient_score
        + 0.30 * shade_score
        + 0.10 * kwp_score
    )
    return round(score * 100, 1)
