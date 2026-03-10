# 🌞 RenewView — Solar Energy Land Viability Assessment

**Final Project — Hebrew University AI Development Course 2026**

RenewView is a multi-agent AI tool that assesses the solar energy viability of land parcels in Southern Europe (Portugal, Spain, Greece, Italy). Users enter a property address, draw their parcel on a map, and receive an AI-powered feasibility report with energy estimates and revenue projections.

---

## Live Demo

Run locally at `http://localhost:8501` — see setup instructions below.

---

## Features

- **3-step assessment flow**: Pre-qualification → Site Details → Feasibility Report
- **Address search**: Geocoding via Nominatim (OpenStreetMap)
- **Interactive parcel drawing**: Draw polygon on map, auto-calculates area in m²
- **Auto-detection**: Grid distance (OSM Overpass API) and terrain type (Open-Elevation API)
- **Live climate data**: NASA POWER API fetches real GHI, DNI, temperature, humidity
- **ML prediction**: Random Forest + Gradient Boosting ensemble
- **4-gate elimination system**: Protected land, grid distance, solar irradiance, parcel size
- **Multi-language**: English, Portuguese, Spanish, Greek
- **Dark solar-tech theme**: Consistent green-on-dark UI

---

## Architecture

```
User Input (Streamlit)
       │
       ▼
Crew 1 — Land Intelligence
  ├── Ingestion Agent      ← NASA POWER API + OSM Solar Farms
  ├── Cleaning Agent       ← Schema validation + guardrails
  ├── EDA Agent            ← Feature analysis
  └── Contract Agent       ← Structured output
       │
       ▼
Validation Gate (schema check)
       │
       ▼
Elimination Gates G1–G4
  ├── G1: Protected/wetland land status
  ├── G2: Grid distance > 8 km
  ├── G3: GHI < 3.5 kWh/m²/day
  └── G4: Parcel size < 2 ha (ground-mount)
       │
       ▼
Crew 2 — Prediction
  ├── Validator Agent
  ├── Feature Engineering Agent
  ├── Model Training Agent     ← RandomForest + GradientBoosting
  └── Evaluation Agent
       │
       ▼
Results (Streamlit)
  ├── Viability score (SVG gauge)
  ├── Estimated annual kWh
  ├── Estimated annual revenue (€)
  └── Gate pass details
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Multi-agent orchestration | CrewAI with Flows |
| ML pipeline | Scikit-learn (RandomForest, GradientBoosting) |
| Frontend | Streamlit |
| Map & drawing | Folium + streamlit-folium + Shapely |
| Climate data | NASA POWER API |
| Location data | OpenStreetMap Overpass API + Nominatim |
| Language | Python 3.12 |

---

## Setup

### Prerequisites
- WSL (Windows) or Linux/macOS
- Python 3.12
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/Hadar84/renewview-final-project
cd renewview-final-project

# Create virtual environment (use Linux filesystem, not NTFS)
python3.12 -m venv ~/renewview-venv
source ~/renewview-venv/bin/activate

# Install dependencies
pip install -e .

# Create output directory
mkdir -p ~/renewview-outputs
```

### Running the App

```bash
source ~/renewview-venv/bin/activate
streamlit run src/renewview/frontend/app.py
```

Open `http://localhost:8501` in your browser.

### Running Tests

```bash
source ~/renewview-venv/bin/activate
python -m pytest tests/ -v
```

All 40 tests should pass.

---

## File Structure

```
src/renewview/
├── main.py                          # Entry point
├── flow.py                          # CrewAI Flow orchestration
├── config/
│   └── settings.py                  # Constants and API endpoints
├── backend/
│   ├── gates/
│   │   └── elimination_gates.py     # G1–G4 hard filters
│   ├── tools/
│   │   ├── nasa_power.py            # NASA POWER API tool
│   │   ├── osm_solar.py             # OSM solar farms tool
│   │   ├── grid_distance.py         # Grid distance calculator
│   │   ├── contract_validation.py   # Schema validation tool
│   │   ├── feature_engineering.py   # ML feature engineering
│   │   ├── model_training.py        # Model training tool
│   │   └── model_evaluation.py      # Model evaluation tool
│   ├── crews/
│   │   ├── land_intelligence_crew/  # Crew 1: data ingestion & EDA
│   │   └── prediction_crew/         # Crew 2: ML prediction
│   └── services/
│       ├── prediction_service.py    # Prediction orchestration
│       └── energy_calculator.py     # kWh & revenue estimation
└── frontend/
    ├── app.py                       # Main Streamlit app (3-step flow)
    ├── components/
    │   ├── site_inputs.py           # Step 2: location + map + inputs
    │   └── results_display.py       # Step 3: report rendering
    ├── pages/
    │   └── about.py                 # About tab content
    └── assets/
        ├── i18n.py                  # Translations (EN/PT/ES/EL)
        └── styles.py                # HTML/CSS components
```

---

## Data

- **Training data**: 205 rows from Portugal, Greece, and Spain
- **Italy**: Frequently times out on OSM queries — limited representation
- **Features**: GHI, DNI, temperature, humidity, wind speed, precipitation, cloud cover, grid distance, parcel size, terrain type, land status, site type

---

## Model Card

| Property | Value |
|----------|-------|
| Model | RandomForest + GradientBoosting ensemble |
| Training samples | 205 |
| Test F1 score | 1.0 |
| Countries | Portugal, Spain, Greece |

**⚠️ Important caveat on F1 = 1.0**: The training dataset contains linearly separable classes — viable vs. non-viable sites have clearly distinct feature profiles in the current dataset. This produces perfect accuracy on the test split but does **not** reflect real-world generalization. The model should be considered a proof-of-concept classifier. A production system would require a larger, more diverse dataset with marginal cases.

---

## Known Limitations

- Grid distance auto-detection fails in rural areas where OSM lacks substation data — user can set manually
- Italy data is sparse due to OSM API timeouts
- Revenue estimates use simplified feed-in tariff assumptions
- Model accuracy is inflated due to linearly separable training data (see Model Card above)
- Not suitable for professional investment decisions — preliminary screening only

---

## Technical Notes

- **venv location**: `~/renewview-venv` (Linux filesystem — NTFS causes permission errors)
- **Output files**: `~/renewview-outputs/` (same reason)
- **Git setup**: Uses separate `.git` dir at `~/renewview-git` with worktree pointing to Windows mount
- **CrewAI output_file bug**: Use callback-based file saving instead of `output_file` parameter

---

## Course Context

Built for the Hebrew University AI Development Course 2026 as a final project demonstrating:
- Multi-agent AI architecture with CrewAI Flows
- Real API integration (NASA, OpenStreetMap)
- End-to-end ML pipeline
- Production-quality Streamlit frontend
