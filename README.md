# ☀️ RenewView

**Multi-Agent AI System for Solar Energy Land Viability & Investment Decision Intelligence — Southern Europe**

Final Project — AI Development & Collaboration — Hebrew University 2026 — Dr. Zvi Ben Ami  
**Hadar Wigelman Zamoscinski**

---

## Problem

The EU targets 700 GW solar by 2030, but SolarPower Europe's 2025 report warns this goal is at risk. Landowners across Southern Europe have no data-driven way to assess land viability before spending thousands on consultants. Existing platforms are manual intake funnels with no predictive scoring.

## Solution

A CrewAI-powered pre-screening decision gate that predicts solar feasibility, classifies risk tiers, estimates energy output & revenue, and connects viable sites to regional installers.

## Architecture

```
RenewView Flow
│
├── Crew 1: Land Intelligence (Sequential, 4 agents)
│   ├── Data Ingestion          → NASA POWER API + OpenStreetMap
│   ├── Cleaning & Labels       → Validation + label construction
│   ├── EDA                     → Regional pattern analysis
│   └── Dataset Contract        → Schema + handoff validation
│       → clean_data.csv • eda_report.md • dataset_contract.json
│
├── ── Validation Gate ──       → Contract check before ML
│
├── Elimination Gates (G1–G4)   → Pre-ML hard filters
│   G1: Protected/wetland       → Not Viable
│   G2: Grid > 8 km            → Not Viable
│   G3: GHI < 3.5 kWh/m²/day  → Not Viable
│   G4: Parcel < 2 ha          → Redirect to rooftop
│
├── Crew 2: Feasibility Prediction (Sequential, 4 agents)
│   ├── Contract Validator      → Validates handoff
│   ├── Feature Engineering     → Derived features + splits
│   ├── Model Training          → Random Forest vs Gradient Boosting
│   └── Evaluation & Model Card → Metrics + ethics documentation
│       → model.pkl • evaluation_report.md • model_card.md
│
└── Streamlit Frontend
    ├── Multi-language (EN/PT/ES/EL)
    ├── Adaptive inputs (ground / rooftop / parking)
    └── Output: score, class, kWh, € revenue, installer link
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | CrewAI Flow (2 crews, 8 agents) |
| Solar Data | NASA POWER API (free) |
| Infrastructure Data | OpenStreetMap Overpass API (free) |
| ML | Scikit-Learn (RF, GB) |
| Frontend | Streamlit |
| Data Processing | Pandas, Matplotlib, Seaborn |

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/renewview.git
cd renewview

# Install
uv sync                    # or: pip install -e .

# Configure
cp .env.example .env       # add your OpenAI key

# Run pipeline (both crews)
crewai flow kickoff

# Run frontend separately
streamlit run src/renewview/frontend/app.py

# Run tests (no LLM needed)
python -m pytest tests/ -v
```

## Project Structure

```
renewview/
├── pyproject.toml
├── BUILD_GUIDE.md              ← architecture rules & guardrails
├── README.md
├── src/renewview/
│   ├── main.py                 ← entry point
│   ├── flow.py                 ← Flow orchestration
│   ├── config/settings.py      ← all constants & thresholds
│   ├── backend/
│   │   ├── crews/              ← 2 crews (4 + 4 agents)
│   │   ├── tools/              ← NASA, OSM, haversine
│   │   ├── gates/              ← G1–G4 elimination gates
│   │   └── services/           ← prediction + energy calc
│   └── frontend/
│       ├── app.py              ← Streamlit main
│       ├── components/         ← adaptive inputs, results
│       └── assets/i18n.py      ← 4-language translations
└── tests/                      ← gates, tools, energy calc
```

## Ethics & Limitations

- Bias toward data-rich regions (Spain, Italy have more OSM data)
- False positive risk on marginal sites
- Agricultural land conversion trade-offs
- This is a preliminary screening tool — always consult a professional

## License

Academic project — Hebrew University 2026.
