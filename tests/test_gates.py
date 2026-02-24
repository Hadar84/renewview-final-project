"""Tests for elimination gates — no LLM needed."""

from renewview.backend.gates.elimination_gates import run_elimination_gates


def test_g1_wetland_eliminated():
    result = run_elimination_gates("wetland", 5.0, 5.0, 10.0, "ground_parcel")
    assert not result.passed
    assert result.eliminated_by == "G1"


def test_g1_protected_eliminated():
    result = run_elimination_gates("protected", 3.0, 5.5, 20.0, "ground_parcel")
    assert not result.passed
    assert result.eliminated_by == "G1"


def test_g2_far_grid_eliminated():
    result = run_elimination_gates("agricultural", 15.0, 5.0, 10.0, "ground_parcel")
    assert not result.passed
    assert result.eliminated_by == "G2"


def test_g2_boundary_passes():
    result = run_elimination_gates("agricultural", 8.0, 5.0, 10.0, "ground_parcel")
    assert result.passed  # exactly 8 km is NOT > 8


def test_g3_low_irradiance_eliminated():
    result = run_elimination_gates("agricultural", 5.0, 2.5, 10.0, "ground_parcel")
    assert not result.passed
    assert result.eliminated_by == "G3"


def test_g4_tiny_parcel_redirect():
    result = run_elimination_gates("agricultural", 5.0, 5.0, 1.5, "ground_parcel")
    assert not result.passed
    assert result.eliminated_by == "G4"
    assert result.redirect_to == "rooftop_assessment"


def test_g4_small_commercial_flag():
    result = run_elimination_gates("agricultural", 5.0, 5.0, 3.0, "ground_parcel")
    assert result.passed
    assert "small_commercial" in result.flags


def test_g4_rooftop_skips_parcel_check():
    """Rooftops should skip parcel size gates."""
    result = run_elimination_gates("commercial", 2.0, 5.0, 0.5, "commercial_rooftop")
    assert result.passed  # 0.5 ha rooftop should not be blocked by G4


def test_all_gates_pass():
    result = run_elimination_gates("agricultural", 3.0, 5.5, 20.0, "ground_parcel")
    assert result.passed
    assert result.eliminated_by is None
    assert result.flags == []


if __name__ == "__main__":
    for name, func in list(globals().items()):
        if name.startswith("test_"):
            try:
                func()
                print(f"  ✓ {name}")
            except AssertionError as e:
                print(f"  ✗ {name}: {e}")
    print("\nDone.")
