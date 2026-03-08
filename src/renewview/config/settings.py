"""RenewView — Central configuration.

All thresholds, tariffs, and constants live here.
Never hardcode values in business logic — import from this module.
"""

from pathlib import Path

# ── Paths ───────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[3]  # renewview/

# Output dirs live on the Linux filesystem to avoid NTFS permission issues.
# Copy to the project folder when needed: cp -r ~/renewview-outputs/* data/
_OUTPUT_ROOT = Path.home() / "renewview-outputs"
DATA_DIR = _OUTPUT_ROOT / "data"
MODELS_DIR = _OUTPUT_ROOT / "models"
REPORTS_DIR = _OUTPUT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# ── Elimination Gate Thresholds (Proposal Section 3) ────────
GATE_G1_EXCLUDED_LAND = {"wetland", "protected", "flood_zone", "national_park"}
GATE_G2_MAX_GRID_DISTANCE_KM = 8.0
GATE_G3_MIN_GHI_KWH = 3.5  # kWh/m²/day
GATE_G4_MIN_PARCEL_HA_GROUND = 2.0  # below → redirect to rooftop
GATE_G4_SMALL_COMMERCIAL_HA = 5.0  # below → flag as small commercial

# ── Grid Distance Scoring ───────────────────────────────────
GRID_DISTANCE_FAVORABLE_KM = 3.0
GRID_DISTANCE_MODERATE_KM = 8.0

# ── Target Classes ──────────────────────────────────────────
VIABILITY_CLASSES = ["High", "Medium", "Low"]  # classifier output
NOT_VIABLE_CLASS = "Not Viable"  # assigned by elimination gates only
ALL_CLASSES = VIABILITY_CLASSES + [NOT_VIABLE_CLASS]

# ── Energy Calculation (Proposal Section 4) ─────────────────
PANEL_EFFICIENCY = 0.20  # standard crystalline silicon 2024
PERFORMANCE_RATIO = 0.80  # inverter + wiring + temperature + soiling losses
GROUND_COVERAGE_RATIO = 0.50  # fraction of parcel usable for panels (ground-mount)
ROOFTOP_COVERAGE_RATIO = 0.70  # rooftop/parking typically higher coverage

# ── Feed-in Tariffs (€/kWh, approximate 2024) ──────────────
FEED_IN_TARIFFS = {
    "Portugal": 0.065,
    "Spain": 0.060,
    "Greece": 0.070,
    "Italy": 0.075,
}

# ── Target Regions ──────────────────────────────────────────
TARGET_COUNTRIES = {
    "PT": "Portugal",
    "ES": "Spain",
    "GR": "Greece",
    "IT": "Italy",
}

# ── Site Types ──────────────────────────────────────────────
SITE_TYPES = ["ground_parcel", "commercial_rooftop", "parking_structure"]

# ── NASA POWER API Parameters ──────────────────────────────
NASA_POWER_PARAMS = (
    "ALLSKY_SFC_SW_DWN,"  # GHI
    "ALLSKY_SFC_SW_DNI,"  # DNI
    "T2M,"                # Temperature 2m
    "RH2M,"               # Relative Humidity 2m
    "WS2M,"               # Wind Speed 2m
    "PRECTOTCORR,"        # Precipitation
    "CLOUD_AMT"           # Cloud Cover
)

# ── OSM Overpass Bounding Boxes (south, west, north, east) ──
OSM_COUNTRY_BBOXES = {
    "PT": (36.9, -9.5, 42.2, -6.1),
    "ES": (36.0, -9.3, 43.8, 4.3),
    "GR": (34.8, 19.3, 41.8, 29.7),
    "IT": (36.6, 6.6, 47.1, 18.5),
}

# ── Nominatim Geocoding (frontend address search) ────────────
NOMINATIM_USER_AGENT = "renewview-solar-assessment/0.1"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_TIMEOUT = 10

# ── Overpass API (substation lookup for grid distance) ───────
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OVERPASS_TIMEOUT = 15
SUBSTATION_SEARCH_RADII_KM = [50, 100]

# ── Open-Elevation API (terrain detection) ───────────────────
OPEN_ELEVATION_URL = "https://api.open-elevation.com/api/v1/lookup"
OPEN_ELEVATION_TIMEOUT = 10
ELEVATION_GRID_STEP_DEG = 0.05
TERRAIN_VARIANCE_FLAT = 20       # variance < 20m → "flat"
TERRAIN_VARIANCE_HILLY = 100     # variance 20–100m → "hilly", >100m → "mountainous"
TERRAIN_COUNTRY_FALLBACK = {
    "Portugal": "hilly",
    "Spain": "hilly",
    "Greece": "hilly",
    "Italy": "mountainous",
}

# ── Map Display ──────────────────────────────────────────────
MAP_DEFAULT_ZOOM = 11
MAP_DRAW_ZOOM = 15
MAP_TILE_PROVIDER = "cartodbdark_matter"

# ── Model Training ──────────────────────────────────────────
TRAIN_SPLIT = 0.70
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15
RANDOM_STATE = 42
