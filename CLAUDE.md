# CLAUDE.md — Instructions for Claude Code

> Read this file and BUILD_GUIDE.md before making any changes.

## Project

**RenewView** — Multi-Agent AI System for Solar Energy Land Viability Assessment (Southern Europe).  
Final project for AI Development course, Hebrew University 2026, Dr. Zvi Ben Ami.  
Author: Hadar Wigelman Zamoscinski.

## Architecture — STRICT separation

```
src/renewview/
├── config/settings.py              ← ALL constants, thresholds, tariffs. Never hardcode.
├── backend/
│   ├── gates/elimination_gates.py  ← G1–G4 pre-ML hard filters (runs BEFORE classifier)
│   ├── tools/                      ← CrewAI custom tools (NASA POWER, OSM, haversine)
│   ├── crews/
│   │   ├── land_intelligence_crew/ ← Crew 1: data ingestion → cleaning → EDA → contract
│   │   └── prediction_crew/        ← Crew 2: validate → features → train → eval + model card
│   └── services/
│       ├── prediction_service.py   ← Bridge between backend and frontend
│       └── energy_calculator.py    ← kWh + € revenue formulas
├── flow.py                         ← CrewAI Flow: Crew 1 → validation gate → Crew 2
├── main.py                         ← Entry point
└── frontend/
    ├── app.py                      ← Streamlit entry
    ├── components/                 ← UI components (site_inputs, results_display)
    └── assets/i18n.py              ← Translations: EN / PT / ES / EL
```

**Rules:**
- Frontend NEVER imports crews, tools, or agents. It only imports from `backend/services/`.
- Backend can run headless: `crewai flow kickoff` works without Streamlit.
- All thresholds and constants live in `config/settings.py`. Import them, don't duplicate.
- Each tool file contains exactly one tool class.
- Crews wire agents to tasks — they don't contain business logic.

## Key business rules

### Elimination Gates (G1–G4) — pre-ML, non-negotiable
| Gate | Condition | Result |
|------|-----------|--------|
| G1 | Land is protected/wetland/flood_zone | → Not Viable |
| G2 | Grid distance > 8 km | → Not Viable |
| G3 | GHI < 3.5 kWh/m²/day | → Not Viable |
| G4 | Parcel < 2 ha (ground only) | → Redirect to rooftop |
| G4b | Parcel < 5 ha (ground only) | → Flag "small_commercial" |

"Not Viable" is assigned by gates. The ML classifier only predicts High/Medium/Low for sites that pass all gates.

### Energy formula
```
annual_kWh = GHI × 365 × area_m² × panel_efficiency(0.20) × performance_ratio(0.80)
revenue_€ = annual_kWh × feed_in_tariff(per country)
```

### Target variable
4 classes: High / Medium / Low / Not Viable.  
Classifier outputs 3 classes. Gates assign "Not Viable."

## Commands

```bash
# Install
uv sync

# Run full pipeline (both crews)
crewai flow kickoff

# Run frontend only
streamlit run src/renewview/frontend/app.py

# Run tests (no LLM needed)
python -m pytest tests/ -v

# Run a specific test file
python -m pytest tests/test_gates.py -v

# Visualize the flow
python -c "from renewview.flow import RenewViewFlow; RenewViewFlow().plot('flow')"
```

## Environment

- Python 3.10–3.13
- CrewAI 1.9.3 (Flow type project)
- Needs OPENAI_API_KEY in `.env` for crew execution
- NASA POWER API and OSM Overpass are free, no keys
- Package manager: uv (preferred) or pip

## Code conventions

- Type hints on all function signatures
- Google-style docstrings on public classes and functions
- `pathlib.Path` for file paths, never string concatenation
- Specific exception handling (no bare `except:`)
- Constants: `UPPER_SNAKE_CASE` in settings.py
- Classes: `PascalCase`
- Files: `snake_case`

## CrewAI conventions

- Agent configs: YAML files in `config/agents.yaml` (role, goal, backstory)
- Task configs: YAML files in `config/tasks.yaml` (description with numbered steps, expected_output)
- Crews use `Process.sequential` unless documented otherwise
- Custom tools: inherit `BaseTool`, define `name`, `description`, `args_schema` (Pydantic), implement `_run()`
- Flow uses `@start()`, `@listen()`, `@router()` decorators

## Session plan & current status

| Session | Status | Focus |
|---------|--------|-------|
| 1 | ✅ Done | Scaffold, architecture, all files created |
| 2 | 🔲 Next | Wire tools to produce real data, test APIs |
| 3 | 🔲 | Crew 1 end-to-end with real outputs |
| 4 | 🔲 | Crew 2 ML pipeline end-to-end |
| 5 | 🔲 | Streamlit polish, multi-language, demo prep |

## What to check before committing

1. Does `python -m pytest tests/ -v` pass?
2. Are all new constants in `settings.py` (not hardcoded)?
3. Does the frontend still only import from `services/`?
4. Is BUILD_GUIDE.md checklist updated if a feature is complete?
5. Commit message format: `type: description` (feat/fix/refactor/docs/test)

## Files you should read first

1. `CLAUDE.md` — you're here
2. `BUILD_GUIDE.md` — full proposal alignment checklist, architecture rules, energy formulas
3. `config/settings.py` — all constants and thresholds
4. `backend/gates/elimination_gates.py` — core business logic
5. `flow.py` — pipeline orchestration
