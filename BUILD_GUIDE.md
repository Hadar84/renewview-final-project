# RenewView — Build Guide & Architecture Rules

> This document defines the rules, guardrails, and conventions for building RenewView.
> Every contributor (human or AI) must follow these before writing or modifying code.

---

## 1 — Architecture Principles

### Frontend / Backend Separation
```
src/renewview/
├── backend/    ← CrewAI agents, tools, services, ML pipeline. NO Streamlit here.
└── frontend/   ← Streamlit pages, components, UI logic. NO ML/CrewAI here.
```

**Rule:** The frontend calls backend services through `backend/services/`. It never imports
crews, tools, or agents directly. This means the backend can run headless (`crewai flow kickoff`)
and the frontend can run independently (`streamlit run`).

### Single Responsibility
- **1 file = 1 purpose.** An agent file defines agents. A tool file defines one tool.
- **Crews don't contain business logic.** They wire agents → tasks → process. That's it.
- **Tools are pure functions with API wrappers.** No side effects beyond the API call.
- **Services bridge backend → frontend.** They load models, run predictions, format results.

### File Naming Convention
- `snake_case` for all Python files and directories
- YAML configs: `agents.yaml`, `tasks.yaml` (CrewAI convention)
- Constants: `UPPER_SNAKE_CASE`
- Classes: `PascalCase`

---

## 2 — Proposal Alignment Checklist

Every feature below maps to the submitted proposal. Check each before considering the project complete.

### Data & Features
- [ ] NASA POWER API: GHI, DNI, temperature, humidity, wind speed, precipitation, cloud cover
- [ ] OpenStreetMap: confirmed solar farm locations (labels) + substation coordinates
- [ ] Grid distance: auto-computed via haversine (<3 km favorable, 3–8 km moderate, >8 km negative)
- [ ] User inputs: site type, parcel size (ha), terrain, land class, wetland/flood/protected status
- [ ] Latitude zone as feature

### Elimination Gates (Pre-ML) — CRITICAL
These run BEFORE the classifier. Sites that fail are eliminated or rerouted, never classified.

| Gate | Rule | Action |
|------|------|--------|
| G1 | Protected or wetland land | → Eliminated ("Not Viable") |
| G2 | Grid distance > 8 km | → Eliminated ("Not Viable") |
| G3 | Irradiance < 3.5 kWh/m²/day | → Eliminated ("Not Viable") |
| G4 | Parcel < 2 ha | → Redirect to rooftop assessment |
| G4b | Parcel < 5 ha (ground) | → Flag as "small commercial" |

### Target Variable
- **4 classes:** High / Medium / Low / Not Viable
- Not Viable is assigned by elimination gates, NOT by the classifier
- The classifier only sees sites that passed all gates → predicts High/Medium/Low

### Outputs (per proposal Section 4)
- [ ] Feasibility score: 0–100%
- [ ] Risk class: High / Medium / Low / Not Viable
- [ ] Estimated annual kWh: `irradiance × area × panel_efficiency`
- [ ] Projected € revenue: `annual_kWh × feed_in_tariff_per_country`
- [ ] "Connect with Regional Installer" prompt for Medium/High results

### Crew 1 — Land Intelligence
- [ ] Data Ingestion Agent (NASA POWER + OSM)
- [ ] Cleaning, Validation & Label Construction Agent
- [ ] EDA & Regional Pattern Analysis Agent
- [ ] Dataset Contract Generator Agent
- [ ] Outputs: `clean_data.csv`, `eda_report.html`, `dataset_contract.json`

### Crew 2 — Feasibility Prediction
- [ ] Contract Validator Agent (FIRST in crew — validates handoff)
- [ ] Feature Engineering Agent
- [ ] Model Training Agent (Random Forest vs. Gradient Boosting)
- [ ] Evaluation & Model Card Agent
- [ ] Outputs: `model.pkl`, `evaluation_report.md`, `model_card.md`

### Streamlit Frontend
- [ ] Multi-language UI: EN / PT / ES / EL
- [ ] Adaptive inputs per site type (ground/rooftop/parking)
- [ ] Ground: terrain, grid distance, wetland status, parcel size (ha)
- [ ] Rooftop/Parking: usable m², skip terrain
- [ ] Results: score, class, annual kWh, € revenue
- [ ] "Connect with Regional Installer" for Medium/High

### Ethics (proposal Section 3)
- [ ] Acknowledge bias toward data-rich regions
- [ ] False positive risk on marginal sites
- [ ] Agricultural land conversion trade-offs

---

## 3 — Code Quality Rules

### Python
- Type hints on all function signatures
- Docstrings on all public classes and functions (Google style)
- No bare `except:` — always catch specific exceptions
- `pathlib.Path` over string concatenation for file paths
- Constants in `config/settings.py`, never hardcoded in logic

### CrewAI Specific
- Agent backstories must be specific and actionable, not generic
- Task descriptions must include numbered steps and explicit output paths
- Task `expected_output` must describe format, location, and validation criteria
- Tool `args_schema` must use Pydantic models with Field descriptions
- Crews use `Process.sequential` unless there's a documented reason for hierarchical

### Testing
- Every custom tool must have a standalone test that runs without an LLM
- Elimination gates must have unit tests for each threshold
- The energy calculation formula must have tests with known values

### Git
- Commit messages: `type: description` (e.g., `feat: add NASA POWER tool`, `fix: gate G2 threshold`)
- Branch per session: `session-1/scaffold`, `session-2/tools`, etc.
- Never commit `.env`, `data/`, `models/` (these are in `.gitignore`)

---

## 4 — Energy Calculation Reference

```
Annual kWh = GHI (kWh/m²/day) × 365 × area_m² × panel_efficiency × performance_ratio

Where:
  panel_efficiency = 0.20 (standard crystalline silicon, 2024)
  performance_ratio = 0.80 (accounts for inverter loss, wiring, temperature, soiling)
  area_m² = parcel_ha × 10000 × ground_coverage_ratio (typically 0.4–0.6 for ground-mount)

Revenue (€/year) = annual_kWh × feed_in_tariff

Feed-in tariffs (approximate, 2024):
  Portugal: €0.065/kWh
  Spain:    €0.060/kWh
  Greece:   €0.070/kWh
  Italy:    €0.075/kWh
```

---

## 5 — Development Workflow

### With Claude Code (recommended)
```bash
cd renewview
claude                         # opens Claude Code in the project
# Ask: "Read BUILD_GUIDE.md then implement session 2 tools"
```

### Without Claude Code
```bash
crewai flow kickoff            # run full pipeline
streamlit run src/renewview/frontend/app.py  # run UI separately
```

### Session Plan
| Session | Focus | Key Files |
|---------|-------|-----------|
| 1 ✅ | Scaffold + architecture | All structure files |
| 2 | Custom tools (NASA, OSM, haversine) + elimination gates | `backend/tools/`, `backend/gates/` |
| 3 | Crew 1 wiring — agents produce real outputs | `backend/crews/land_intelligence_crew/` |
| 4 | Crew 2 wiring — ML pipeline runs end to end | `backend/crews/prediction_crew/` |
| 5 | Streamlit app + multi-language + demo prep | `frontend/` |

---

## 6 — File Inventory

When complete, the project should contain exactly these files:

```
renewview/
├── pyproject.toml
├── .env.example
├── .gitignore
├── README.md
├── BUILD_GUIDE.md                              ← this file
├── src/renewview/
│   ├── __init__.py
│   ├── main.py                                 ← entry point
│   ├── flow.py                                 ← Flow orchestration
│   ├── config/
│   │   └── settings.py                         ← constants, thresholds, tariffs
│   ├── backend/
│   │   ├── crews/
│   │   │   ├── land_intelligence_crew/
│   │   │   │   ├── config/agents.yaml
│   │   │   │   ├── config/tasks.yaml
│   │   │   │   └── land_intelligence_crew.py
│   │   │   └── prediction_crew/
│   │   │       ├── config/agents.yaml
│   │   │       ├── config/tasks.yaml
│   │   │       └── prediction_crew.py
│   │   ├── tools/
│   │   │   ├── nasa_power_tool.py
│   │   │   ├── osm_solar_tool.py
│   │   │   └── grid_distance_tool.py
│   │   ├── gates/
│   │   │   └── elimination_gates.py            ← G1–G4 pre-ML filters
│   │   └── services/
│   │       ├── prediction_service.py           ← model loading + inference
│   │       └── energy_calculator.py            ← kWh + € revenue
│   └── frontend/
│       ├── app.py                              ← Streamlit main
│       ├── pages/
│       │   ├── assessment.py                   ← input form + results
│       │   └── about.py                        ← project info + ethics
│       ├── components/
│       │   ├── site_inputs.py                  ← adaptive input forms
│       │   └── results_display.py              ← score/class/kWh/revenue cards
│       └── assets/
│           └── i18n.py                         ← EN/PT/ES/EL translations
├── data/                                       ← generated (gitignored)
├── models/                                     ← generated (gitignored)
├── reports/                                    ← generated (gitignored)
└── tests/
    ├── test_gates.py
    ├── test_tools.py
    └── test_energy_calculator.py
```
