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

---

# Launch handoff — read this before touching launch work

> This section is the single source of truth for shipping the paid product. It exists so any
> future session has full context without the author re-explaining. Keep it updated as tasks close.

## Product being launched

The **€29 RenewView residential solar report** — a one-page PDF that tells a homeowner whether
their roof is worth going solar, with kWp sizing, annual kWh, € savings, and payback.

- **Storefront / payment:** Lemon Squeezy (hosted checkout, no card handling on our side).
- **Live app:** Streamlit Cloud (auto-deploys from `main`). The app sells the report; the report
  itself is generated and delivered by hand for now (see manual-delivery model below).

## The three remaining launch tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1 | **Map fix** — Step 2 map renders near-black on dark CARTO tiles | ✅ Done (commit `0aece03`) | Switched to Esri World Imagery satellite tiles via `MAP_TILE_PROVIDER` / `MAP_TILE_ATTR` in `settings.py`. Customers can now see their roof. |
| 2 | **€1 test transaction** | 🔲 To do | Put a temporary €1 variant live in Lemon Squeezy, buy it end-to-end with a real card, confirm the order webhook/email arrives, then run the manual delivery flow against that order. Remove/disable the €1 variant before public launch. Goal: prove checkout → notification → delivery works before real money. |
| 3 | **Launch posts** | 🔲 To do | Publish the launch announcements (the homeowner-facing posts driving traffic to the Lemon Squeezy checkout). Go live only after task 2 passes. |

## Manual-delivery model (first ~10 orders)

Delivery is **deliberately manual** until ~10 orders prove demand. Do NOT build automated
fulfilment before then — it is wasted work if the offer doesn't sell.

Per order, the loop is:
1. Lemon Squeezy emails the order (name, email, and whatever roof details the customer provided).
2. Run the delivery CLI:
   ```bash
   python scripts/generate_report.py \
       --name "Maria Silva" --email maria@example.pt \
       --location "Faro, Portugal" --country Portugal \
       --lat 37.0179 --lon -7.9304 \
       --roof-area-m2 80 --orientation S --shading light
   ```
   Or run it with no arguments for an interactive one-field-at-a-time prompt.
3. Output PDF lands at `~/renewview-outputs/reports/customers/<slug>_<YYYY-MM-DD>.pdf`.
4. Email the PDF back to the customer manually.

Notes:
- The CLI uses the same backend `PredictionService` + `report_generator` as the app, so the
  numbers match what the customer saw on screen.
- Revisit automation only after ~10 delivered orders.

## Resume protocol — how a future session picks up

1. Read `CLAUDE.md` (this file), then `BUILD_GUIDE.md`.
2. Check the launch-tasks table above for the next 🔲 task, and `git log --oneline -10` for what
   actually shipped since this was written.
3. Before changing anything, run `python -m pytest tests/ -v` (needs deps installed: `uv sync`,
   or `pip install` the project; without them, ML/PDF tests fail on missing `joblib`/`crewai`/
   `reportlab` — that's an env gap, not a regression).
4. Honor the architecture rules above: constants in `settings.py`, frontend imports only from
   `services/`, commit format `type: description`.
5. After finishing a launch task, flip its row to ✅ with the commit hash and push to `main`
   (Streamlit Cloud auto-deploys).
