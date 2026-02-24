"""Tests for energy calculator — known-value verification."""

from renewview.backend.services.energy_calculator import (
    estimate_annual_kwh,
    estimate_revenue_eur,
    feasibility_score,
    parcel_ha_to_m2,
)


def test_parcel_conversion():
    assert parcel_ha_to_m2(1.0) == 10_000
    assert parcel_ha_to_m2(5.0) == 50_000


def test_annual_kwh_ground():
    """5 kWh/m²/day, 10 ha ground parcel."""
    # 5 * 365 * 100000 * 0.5 (coverage) * 0.20 * 0.80 = 14,600,000
    kwh = estimate_annual_kwh(5.0, 100_000, "ground_parcel")
    assert abs(kwh - 14_600_000) < 1


def test_annual_kwh_rooftop():
    """5 kWh/m²/day, 1000 m² rooftop."""
    # 5 * 365 * 1000 * 0.7 (coverage) * 0.20 * 0.80 = 204,400
    kwh = estimate_annual_kwh(5.0, 1_000, "commercial_rooftop")
    assert abs(kwh - 204_400) < 1


def test_revenue_portugal():
    revenue = estimate_revenue_eur(1_000_000, "Portugal")
    assert revenue == 65_000.0  # 1M kWh * 0.065


def test_revenue_italy():
    revenue = estimate_revenue_eur(1_000_000, "Italy")
    assert revenue == 75_000.0  # 1M kWh * 0.075


def test_feasibility_score_range():
    score = feasibility_score(5.0, 3.0, 10.0, 0.8)
    assert 0 <= score <= 100


def test_feasibility_score_high():
    """High GHI, close grid, large parcel, high confidence → high score."""
    score = feasibility_score(6.5, 0.5, 50.0, 0.95)
    assert score > 80


def test_feasibility_score_low():
    """Low GHI, far grid, small parcel, no model → low score."""
    score = feasibility_score(3.5, 7.5, 2.0, 0.0)
    assert score < 30


if __name__ == "__main__":
    for name, func in list(globals().items()):
        if name.startswith("test_"):
            try:
                func()
                print(f"  ✓ {name}")
            except AssertionError as e:
                print(f"  ✗ {name}: {e}")
    print("\nDone.")
