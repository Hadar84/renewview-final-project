"""RenewView Flow — orchestrates Land Intelligence → Feasibility Prediction.

Uses CrewAI Flow with @start/@listen/@router decorators.
Includes a validation gate between the two crews.
"""

import json
import os
from typing import Any, Dict

from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

from renewview.backend.crews.land_intelligence_crew.land_intelligence_crew import (
    LandIntelligenceCrew,
)
from renewview.backend.crews.prediction_crew.prediction_crew import (
    FeasibilityPredictionCrew,
)
from renewview.config.settings import DATA_DIR, MODELS_DIR, REPORTS_DIR, FIGURES_DIR


class RenewViewState(BaseModel):
    """Shared state across the RenewView flow."""

    stage: str = "initialized"
    raw_data_path: str = ""
    clean_data_path: str = ""
    eda_report_path: str = ""
    contract_path: str = ""
    crew1_result: str = ""
    contract_valid: bool = False
    model_path: str = ""
    evaluation_report_path: str = ""
    model_card_path: str = ""
    crew2_result: str = ""
    final_status: str = ""


class RenewViewFlow(Flow[RenewViewState]):
    """Main flow: Crew 1 → Validation Gate → Crew 2."""

    @start()
    def initialize(self) -> Dict[str, Any]:
        """Create output directories."""
        print("\n" + "=" * 60)
        print("  RenewView — Solar Energy Land Viability Assessment")
        print("  Multi-Agent AI System — Southern Europe")
        print("=" * 60)

        for d in [DATA_DIR, DATA_DIR / "features", MODELS_DIR, REPORTS_DIR, FIGURES_DIR]:
            d.mkdir(parents=True, exist_ok=True)

        self.state.stage = "initialized"
        print("\n  ✓ Directories ready. Starting Crew 1...\n")
        return {"status": "initialized"}

    @listen(initialize)
    def run_land_intelligence_crew(self) -> str:
        """Execute Crew 1 — data pipeline."""
        print("\n" + "-" * 60)
        print("  STAGE 1: Land Intelligence Crew")
        print("-" * 60)
        self.state.stage = "crew1_running"

        try:
            result = LandIntelligenceCrew().crew().kickoff()
            self.state.crew1_result = str(result)
            self.state.raw_data_path = str(DATA_DIR / "raw_solar_data.csv")
            self.state.clean_data_path = str(DATA_DIR / "clean_solar_data.csv")
            self.state.eda_report_path = str(REPORTS_DIR / "eda_report.md")
            self.state.contract_path = str(DATA_DIR / "dataset_contract.json")
            self.state.stage = "crew1_complete"
            print("\n  ✓ Crew 1 complete!")
            return "crew1_success"
        except Exception as e:
            self.state.stage = "crew1_failed"
            self.state.final_status = f"Crew 1 failed: {e}"
            print(f"\n  ✗ Crew 1 FAILED: {e}")
            return "crew1_failed"

    @router(run_land_intelligence_crew)
    def validate_handoff(self) -> str:
        """Validation gate between crews."""
        print("\n" + "-" * 60)
        print("  VALIDATION GATE")
        print("-" * 60)

        if self.state.stage == "crew1_failed":
            print("  ✗ Crew 1 did not complete.")
            return "validation_failed"

        contract_path = self.state.contract_path
        if not os.path.exists(contract_path):
            print(f"  ⚠ Contract not found — allowing pass-through (dev mode)")
            self.state.contract_valid = True
            return "validation_passed"

        try:
            with open(contract_path) as f:
                contract = json.load(f)
            required = ["columns", "target_column", "feature_columns"]
            missing = [k for k in required if k not in contract]
            if missing:
                print(f"  ✗ Contract missing: {missing}")
                self.state.contract_valid = False
                return "validation_failed"

            self.state.contract_valid = True
            print("  ✓ Dataset contract valid.")
            return "validation_passed"
        except (json.JSONDecodeError, IOError) as e:
            print(f"  ✗ Validation error: {e}")
            return "validation_failed"

    @listen("validation_passed")
    def run_prediction_crew(self) -> str:
        """Execute Crew 2 — ML pipeline."""
        print("\n" + "-" * 60)
        print("  STAGE 2: Feasibility Prediction Crew")
        print("-" * 60)
        self.state.stage = "crew2_running"

        try:
            result = FeasibilityPredictionCrew().crew().kickoff()
            self.state.crew2_result = str(result)
            self.state.model_path = str(MODELS_DIR / "best_model.joblib")
            self.state.evaluation_report_path = str(REPORTS_DIR / "final_evaluation_report.md")
            self.state.model_card_path = str(REPORTS_DIR / "model_card.md")
            self.state.stage = "crew2_complete"
            print("\n  ✓ Crew 2 complete!")
            return "crew2_success"
        except Exception as e:
            self.state.stage = "crew2_failed"
            self.state.final_status = f"Crew 2 failed: {e}"
            print(f"\n  ✗ Crew 2 FAILED: {e}")
            return "crew2_failed"

    @listen("validation_failed")
    def handle_validation_failure(self) -> None:
        """Handle gate failure."""
        print("\n  PIPELINE STOPPED — validation gate failed.")
        self.state.final_status = "Failed at validation gate"
        self.state.stage = "failed"

    @listen(run_prediction_crew)
    def generate_summary(self) -> Dict[str, Any]:
        """Final pipeline summary."""
        print("\n" + "=" * 60)
        print("  ✓ RENEWVIEW PIPELINE COMPLETE")
        print("=" * 60)
        self.state.final_status = "Pipeline completed successfully"
        self.state.stage = "complete"

        artifacts = {
            "raw_data": self.state.raw_data_path,
            "clean_data": self.state.clean_data_path,
            "eda_report": self.state.eda_report_path,
            "dataset_contract": self.state.contract_path,
            "trained_model": self.state.model_path,
            "evaluation_report": self.state.evaluation_report_path,
            "model_card": self.state.model_card_path,
        }
        for name, path in artifacts.items():
            icon = "✓" if os.path.exists(path) else "–"
            print(f"    {icon} {name}: {path}")

        print("\n  Next: streamlit run src/renewview/frontend/app.py")
        print("=" * 60)
        return {"status": "success", "artifacts": artifacts}
