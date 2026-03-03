"""Tests for Crew 2 ML pipeline tools — no LLM needed.

Runs the full pipeline: contract validation → feature engineering →
model training → model evaluation on the real Crew 1 output data.
"""

import json
from pathlib import Path

import pandas as pd
import pytest

from renewview.config.settings import DATA_DIR, FIGURES_DIR, MODELS_DIR, REPORTS_DIR


# ── Contract Validation ──────────────────────────────────────


class TestContractValidation:
    """Tests for the contract validation tool."""

    def test_valid_dataset_passes(self):
        from renewview.backend.tools.contract_validation_tool import ContractValidationTool

        tool = ContractValidationTool()
        result = json.loads(tool._run())
        assert result["status"] == "PASS", f"Validation failed: {result['errors']}"
        assert result["rows"] > 0
        assert result["target_column"] == "viability_class"
        assert len(result["feature_columns"]) > 0

    def test_missing_file_fails(self, tmp_path):
        from renewview.backend.tools.contract_validation_tool import ContractValidationTool

        tool = ContractValidationTool()
        result = json.loads(tool._run(data_path=str(tmp_path / "nonexistent.csv")))
        assert result["status"] == "FAIL"

    def test_bad_contract_fails(self, tmp_path):
        from renewview.backend.tools.contract_validation_tool import ContractValidationTool

        tool = ContractValidationTool()
        bad_json = tmp_path / "bad.json"
        bad_json.write_text("{not valid json")
        result = json.loads(tool._run(contract_path=str(bad_json)))
        assert result["status"] == "FAIL"


# ── Feature Engineering ──────────────────────────────────────


class TestFeatureEngineering:
    """Tests for the feature engineering tool."""

    def test_feature_engineering_produces_splits(self):
        from renewview.backend.tools.feature_engineering_tool import FeatureEngineeringTool

        tool = FeatureEngineeringTool()
        result = json.loads(tool._run())
        assert result["status"] == "SUCCESS"
        assert result["feature_count"] > 0
        assert result["train_size"] > 0
        assert result["val_size"] > 0
        assert result["test_size"] > 0

    def test_split_files_exist(self):
        features_dir = DATA_DIR / "features"
        for name in ["X_train.csv", "X_val.csv", "X_test.csv",
                      "y_train.csv", "y_val.csv", "y_test.csv"]:
            path = features_dir / name
            assert path.exists(), f"Missing: {path}"
            df = pd.read_csv(path)
            assert len(df) > 0, f"Empty: {path}"

    def test_pipeline_artifact_saved(self):
        import joblib

        pipeline_path = MODELS_DIR / "feature_pipeline.joblib"
        assert pipeline_path.exists()
        pipeline = joblib.load(pipeline_path)
        assert "scaler" in pipeline
        assert "feature_names" in pipeline
        assert "cat_columns" in pipeline

    def test_derived_features_present(self):
        X_train = pd.read_csv(DATA_DIR / "features" / "X_train.csv")
        expected = [
            "solar_cloud_ratio",
            "temp_humidity_index",
            "grid_accessibility_score",
            "irradiance_consistency",
        ]
        for feat in expected:
            assert feat in X_train.columns, f"Missing derived feature: {feat}"

    def test_split_proportions(self):
        X_train = pd.read_csv(DATA_DIR / "features" / "X_train.csv")
        X_val = pd.read_csv(DATA_DIR / "features" / "X_val.csv")
        X_test = pd.read_csv(DATA_DIR / "features" / "X_test.csv")
        total = len(X_train) + len(X_val) + len(X_test)
        train_ratio = len(X_train) / total
        # Allow +/- 5% tolerance for small datasets
        assert 0.60 <= train_ratio <= 0.80, f"Train ratio {train_ratio:.2f} out of range"


# ── Model Training ───────────────────────────────────────────


class TestModelTraining:
    """Tests for the model training tool."""

    def test_model_training_succeeds(self):
        from renewview.backend.tools.model_training_tool import ModelTrainingTool

        tool = ModelTrainingTool()
        result = json.loads(tool._run())
        assert result["status"] == "SUCCESS"
        assert result["best_model"] in ("RandomForest", "GradientBoosting")
        assert result["best_cv_f1_macro"] > 0

    def test_model_file_saved(self):
        assert (MODELS_DIR / "best_model.joblib").exists()

    def test_training_results_json(self):
        results_path = MODELS_DIR / "training_results.json"
        assert results_path.exists()
        results = json.loads(results_path.read_text())
        assert "baseline_comparison" in results
        assert "tuning" in results
        assert "tuned_validation_metrics" in results

    def test_comparison_report_saved(self):
        assert (REPORTS_DIR / "model_comparison_report.md").exists()


# ── Model Evaluation ─────────────────────────────────────────


class TestModelEvaluation:
    """Tests for the model evaluation tool."""

    def test_model_evaluation_succeeds(self):
        from renewview.backend.tools.model_evaluation_tool import ModelEvaluationTool

        tool = ModelEvaluationTool()
        result = json.loads(tool._run())
        assert result["status"] == "SUCCESS"
        assert result["test_metrics"]["accuracy"] > 0
        assert len(result["top_features"]) > 0

    def test_figures_generated(self):
        for fig in ["confusion_matrix.png", "feature_importance.png", "roc_curves.png"]:
            path = FIGURES_DIR / fig
            assert path.exists(), f"Missing figure: {path}"
            assert path.stat().st_size > 0, f"Empty figure: {path}"

    def test_evaluation_report_saved(self):
        assert (REPORTS_DIR / "final_evaluation_report.md").exists()

    def test_model_card_saved(self):
        path = REPORTS_DIR / "model_card.md"
        assert path.exists()
        content = path.read_text()
        assert "Intended Use" in content
        assert "Limitations" in content
        assert "Ethical Considerations" in content


# ── Integration: Prediction Service ──────────────────────────


class TestPredictionServiceIntegration:
    """Tests that PredictionService works with the trained model."""

    def test_load_model(self):
        from renewview.backend.services.prediction_service import PredictionService

        svc = PredictionService()
        loaded = svc.load_model()
        assert loaded, "Model failed to load"
        assert svc.is_loaded

    def test_assess_viable_site(self):
        from renewview.backend.services.prediction_service import PredictionService

        svc = PredictionService()
        svc.load_model()
        result = svc.assess_site(
            latitude=38.0,
            longitude=-8.0,
            country="Portugal",
            site_type="ground_parcel",
            parcel_size_ha=10.0,
            grid_distance_km=3.0,
            ghi=5.0,
        )
        assert result["viability_class"] in ("High", "Medium", "Low")
        assert result["annual_kwh"] > 0
        assert result["revenue_eur"] > 0
        assert result["used_model"] is True

    def test_assess_eliminated_site(self):
        from renewview.backend.services.prediction_service import PredictionService

        svc = PredictionService()
        svc.load_model()
        result = svc.assess_site(
            latitude=38.0,
            longitude=-8.0,
            country="Portugal",
            site_type="ground_parcel",
            parcel_size_ha=10.0,
            grid_distance_km=3.0,
            ghi=5.0,
            land_status="wetland",
        )
        assert result["viability_class"] == "Not Viable"
        assert result["used_model"] is False
