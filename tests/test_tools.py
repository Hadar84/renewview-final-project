"""Tests for custom tools — offline tests only (no API calls)."""

import json

from renewview.backend.tools.grid_distance_tool import GridDistanceCalculatorTool


def test_haversine_known_distance():
    """Lisbon to Porto is ~274 km."""
    tool = GridDistanceCalculatorTool()
    result = json.loads(tool._run(
        latitude=38.7223,
        longitude=-9.1393,
        reference_points=json.dumps([{"lat": 41.1579, "lon": -8.6291}]),
    ))
    # Should be approximately 274 km
    assert 270 < result["nearest_distance_km"] < 280


def test_haversine_same_point():
    tool = GridDistanceCalculatorTool()
    result = json.loads(tool._run(
        latitude=38.0, longitude=-8.0,
        reference_points=json.dumps([{"lat": 38.0, "lon": -8.0}]),
    ))
    assert result["nearest_distance_km"] == 0.0


def test_haversine_multiple_refs():
    tool = GridDistanceCalculatorTool()
    result = json.loads(tool._run(
        latitude=38.0, longitude=-8.0,
        reference_points=json.dumps([
            {"lat": 40.0, "lon": -8.0},  # ~222 km
            {"lat": 38.1, "lon": -8.0},  # ~11 km (closest)
            {"lat": 42.0, "lon": -8.0},  # ~445 km
        ]),
    ))
    assert result["nearest_distance_km"] < 15  # closest should be ~11 km


def test_invalid_json():
    tool = GridDistanceCalculatorTool()
    result = json.loads(tool._run(38.0, -8.0, "not valid json"))
    assert "error" in result


if __name__ == "__main__":
    for name, func in list(globals().items()):
        if name.startswith("test_"):
            try:
                func()
                print(f"  ✓ {name}")
            except AssertionError as e:
                print(f"  ✗ {name}: {e}")
    print("\nDone.")
