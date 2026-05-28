"""Tests for residential roof site type — kWp, kWh, savings, PAE+S, gates, service."""

from renewview.backend.gates.elimination_gates import run_residential_roof_gates
from renewview.backend.services.energy_calculator import (
    feasibility_score_residential,
    residential_annual_kwh,
    residential_annual_savings_eur,
    residential_net_savings_25yr_eur,
    residential_payback_years,
    residential_system_kwp,
)
from renewview.backend.services.prediction_service import PredictionService


# ── System size (kWp) ────────────────────────────────────────


def test_kwp_south_unshaded():
    # 80 m² * 0.18 * 1.0 * 1.0 = 14.4 kWp
    assert residential_system_kwp(80, "S", "none") == 14.4


def test_kwp_north_derate():
    # 80 * 0.18 * 0.6 * 1.0 = 8.64
    assert residential_system_kwp(80, "N", "none") == 8.64


def test_kwp_heavy_shading_derate():
    # 80 * 0.18 * 1.0 * 0.5 = 7.2
    assert residential_system_kwp(80, "S", "heavy") == 7.2


def test_kwp_orientation_case_insensitive():
    assert residential_system_kwp(50, "se", "light") == residential_system_kwp(50, "SE", "LIGHT")


def test_kwp_zero_area():
    assert residential_system_kwp(0, "S", "none") == 0.0


# ── Annual kWh ───────────────────────────────────────────────


def test_annual_kwh_formula():
    # 5 kWp * 5 GHI * 365 * 0.85 = 7,756.25
    assert residential_annual_kwh(5.0, 5.0) == 7756.25


def test_annual_kwh_zero_system():
    assert residential_annual_kwh(0.0, 5.0) == 0.0


# ── Annual savings (€) ───────────────────────────────────────


def test_annual_savings_at_022_rate():
    # 7756 kWh * 0.22 = 1706.32
    assert residential_annual_savings_eur(7756) == 1706.32


# ── Payback period ──────────────────────────────────────────


def test_payback_basic():
    # 5 kWp * 1200 = 6000 install; 1500 €/yr → 4.0 years
    assert residential_payback_years(5.0, 1500.0) == 4.0


def test_payback_rounds_to_1_decimal():
    # 4 kWp * 1200 = 4800; 1300 €/yr → 3.6923... → 3.7
    assert residential_payback_years(4.0, 1300.0) == 3.7


# ── 25-year net savings ─────────────────────────────────────


def test_net_savings_25yr_basic():
    # 5 kWp * 1200 = 6000; 1500 * 25 = 37500; 37500 - 6000 = 31500
    assert residential_net_savings_25yr_eur(5.0, 1500.0) == 31500


def test_net_savings_25yr_rounds_to_int():
    # 3 kWp * 1200 = 3600; 1200.40 * 25 = 30010.0; 30010 - 3600 = 26410
    result = residential_net_savings_25yr_eur(3.0, 1200.40)
    assert result == 26410
    assert isinstance(result, int)


# ── Roof gates ───────────────────────────────────────────────


def test_roof_gate_g1_north_fails():
    r = run_residential_roof_gates("N", "none", 5.0, 5.0)
    assert not r.passed
    assert r.eliminated_by == "G1"


def test_roof_gate_g2_heavy_shading_fails():
    r = run_residential_roof_gates("S", "heavy", 5.0, 5.0)
    assert not r.passed
    assert r.eliminated_by == "G2"


def test_roof_gate_g3_low_ghi_fails():
    r = run_residential_roof_gates("S", "none", 3.0, 5.0)
    assert not r.passed
    assert r.eliminated_by == "G3"


def test_roof_gate_g4_undersized_fails():
    r = run_residential_roof_gates("S", "none", 5.0, 0.5)
    assert not r.passed
    assert r.eliminated_by == "G4"


def test_roof_gate_g4_oversized_fails():
    r = run_residential_roof_gates("S", "none", 5.0, 20.0)
    assert not r.passed
    assert r.eliminated_by == "G4"


def test_roof_gates_happy_path_passes():
    r = run_residential_roof_gates("S", "none", 5.0, 5.0)
    assert r.passed
    assert r.eliminated_by is None


# ── Score ────────────────────────────────────────────────────


def test_score_residential_sunny_south():
    score = feasibility_score_residential(5.5, 8.0, "S", "none")
    assert score > 80


def test_score_residential_marginal():
    score = feasibility_score_residential(3.5, 1.5, "E", "moderate")
    assert score < 50


# ── PredictionService end-to-end (no model needed) ───────────


def test_assess_residential_happy_pt():
    svc = PredictionService()  # do not load model — residential bypasses it
    r = svc.assess_site(
        latitude=37.0, longitude=-8.0, country="Portugal",
        site_type="residential_roof",
        parcel_size_ha=0.0, grid_distance_km=0.0,
        ghi=5.5,
        roof_area_m2=80, orientation="S", shading="none",
    )
    assert r["viability_class"] in ("High", "Medium")
    assert r["site_type"] == "residential_roof"
    assert r["used_model"] is False
    assert r["annual_kwh"] > 0
    assert r["revenue_eur"] > 0   # holds savings for residential
    assert r["kwp"] > 0
    assert r["payback_years"] > 0
    assert r["net_savings_25yr_eur"] > 0


def test_assess_residential_not_viable_north():
    svc = PredictionService()
    r = svc.assess_site(
        latitude=37.0, longitude=-8.0, country="Portugal",
        site_type="residential_roof",
        parcel_size_ha=0.0, grid_distance_km=0.0,
        ghi=5.5,
        roof_area_m2=80, orientation="N", shading="none",
    )
    assert r["viability_class"] == "Not Viable"
    assert r["eliminated_by"] == "G1"
    assert r["site_type"] == "residential_roof"


def test_assess_residential_not_viable_heavy_shading():
    svc = PredictionService()
    r = svc.assess_site(
        latitude=37.0, longitude=-8.0, country="Portugal",
        site_type="residential_roof",
        parcel_size_ha=0.0, grid_distance_km=0.0,
        ghi=5.5,
        roof_area_m2=80, orientation="S", shading="heavy",
    )
    assert r["viability_class"] == "Not Viable"
    assert r["eliminated_by"] == "G2"


if __name__ == "__main__":
    for name, func in list(globals().items()):
        if name.startswith("test_"):
            try:
                func()
                print(f"  ✓ {name}")
            except AssertionError as e:
                print(f"  ✗ {name}: {e}")
    print("\nDone.")
