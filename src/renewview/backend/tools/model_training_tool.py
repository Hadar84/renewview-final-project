"""Model Training Tool — trains RF and GB classifiers, tunes the best.

Compares Random Forest vs Gradient Boosting by macro F1,
tunes the winner with GridSearchCV, and saves the best model.
"""

import json
from pathlib import Path
from typing import Type

import joblib
import numpy as np
import pandas as pd
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GridSearchCV

from renewview.config.settings import DATA_DIR, MODELS_DIR, RANDOM_STATE, REPORTS_DIR


class ModelTrainingInput(BaseModel):
    """Input schema for model training tool."""

    features_dir: str = Field(
        default=str(DATA_DIR / "features"),
        description="Directory containing X_train.csv, y_train.csv, etc.",
    )


class ModelTrainingTool(BaseTool):
    """Train RF and GB classifiers, compare, tune the best, and save."""

    name: str = "model_training"
    description: str = (
        "Trains Random Forest and Gradient Boosting classifiers on the "
        "prepared features. Compares by macro F1-score, tunes the winner "
        "with GridSearchCV, and saves the best model to models/best_model.joblib."
    )
    args_schema: Type[BaseModel] = ModelTrainingInput

    def _run(self, features_dir: str = "") -> str:
        features_dir = Path(features_dir) if features_dir else DATA_DIR / "features"

        # ── Load data ─────────────────────────────────────────
        X_train = pd.read_csv(features_dir / "X_train.csv")
        y_train = pd.read_csv(features_dir / "y_train.csv").squeeze()
        X_val = pd.read_csv(features_dir / "X_val.csv")
        y_val = pd.read_csv(features_dir / "y_val.csv").squeeze()

        # ── Train baseline models ─────────────────────────────
        models = {
            "RandomForest": RandomForestClassifier(
                n_estimators=100, random_state=RANDOM_STATE
            ),
            "GradientBoosting": GradientBoostingClassifier(
                n_estimators=100, random_state=RANDOM_STATE
            ),
        }

        results = {}
        for name, model in models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_val)
            results[name] = {
                "accuracy": round(accuracy_score(y_val, y_pred), 4),
                "precision_macro": round(
                    precision_score(y_val, y_pred, average="macro", zero_division=0), 4
                ),
                "recall_macro": round(
                    recall_score(y_val, y_pred, average="macro", zero_division=0), 4
                ),
                "f1_macro": round(
                    f1_score(y_val, y_pred, average="macro", zero_division=0), 4
                ),
            }

        # ── Select best by macro F1 ──────────────────────────
        best_name = max(results, key=lambda k: results[k]["f1_macro"])

        # ── Tune with GridSearchCV ────────────────────────────
        if best_name == "RandomForest":
            param_grid = {
                "n_estimators": [100, 200],
                "max_depth": [10, 20, None],
            }
            base_model = RandomForestClassifier(random_state=RANDOM_STATE)
        else:
            param_grid = {
                "n_estimators": [100, 200],
                "learning_rate": [0.05, 0.1],
            }
            base_model = GradientBoostingClassifier(random_state=RANDOM_STATE)

        grid = GridSearchCV(
            base_model,
            param_grid,
            cv=3,
            scoring="f1_macro",
            n_jobs=-1,
            refit=True,
        )
        grid.fit(X_train, y_train)
        best_model = grid.best_estimator_

        # Evaluate tuned model on validation set
        y_pred_tuned = best_model.predict(X_val)
        tuned_metrics = {
            "accuracy": round(accuracy_score(y_val, y_pred_tuned), 4),
            "precision_macro": round(
                precision_score(y_val, y_pred_tuned, average="macro", zero_division=0),
                4,
            ),
            "recall_macro": round(
                recall_score(y_val, y_pred_tuned, average="macro", zero_division=0), 4
            ),
            "f1_macro": round(
                f1_score(y_val, y_pred_tuned, average="macro", zero_division=0), 4
            ),
        }

        # ── Save model and results ────────────────────────────
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(best_model, MODELS_DIR / "best_model.joblib")

        training_results = {
            "baseline_comparison": results,
            "best_baseline": best_name,
            "tuning": {
                "model": best_name,
                "best_params": grid.best_params_,
                "best_cv_f1_macro": round(grid.best_score_, 4),
            },
            "tuned_validation_metrics": tuned_metrics,
        }
        (MODELS_DIR / "training_results.json").write_text(
            json.dumps(training_results, indent=2)
        )

        # ── Save comparison report ────────────────────────────
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        report_lines = [
            "# Model Comparison Report\n",
            "## Baseline Comparison (Validation Set)\n",
            "| Model | Accuracy | Precision | Recall | F1 (macro) |",
            "|-------|----------|-----------|--------|------------|",
        ]
        for name, metrics in results.items():
            marker = " **" if name == best_name else ""
            report_lines.append(
                f"| {name}{marker} | {metrics['accuracy']} | "
                f"{metrics['precision_macro']} | {metrics['recall_macro']} | "
                f"{metrics['f1_macro']} |"
            )
        report_lines.extend([
            "",
            f"**Selected model:** {best_name} (highest macro F1)\n",
            "## Hyperparameter Tuning (GridSearchCV, 3-fold)\n",
            f"- Search space: `{param_grid}`",
            f"- Best params: `{grid.best_params_}`",
            f"- Best CV F1 (macro): {grid.best_score_:.4f}\n",
            "## Tuned Model — Validation Metrics\n",
            f"- Accuracy: {tuned_metrics['accuracy']}",
            f"- Precision (macro): {tuned_metrics['precision_macro']}",
            f"- Recall (macro): {tuned_metrics['recall_macro']}",
            f"- F1 (macro): {tuned_metrics['f1_macro']}\n",
            "## Classification Report\n",
            "```",
            classification_report(y_val, y_pred_tuned, zero_division=0),
            "```\n",
            f"**Model saved to:** `{MODELS_DIR / 'best_model.joblib'}`",
        ])
        (REPORTS_DIR / "model_comparison_report.md").write_text(
            "\n".join(report_lines)
        )

        output = {
            "status": "SUCCESS",
            "best_model": best_name,
            "best_params": grid.best_params_,
            "best_cv_f1_macro": round(grid.best_score_, 4),
            "tuned_validation_metrics": tuned_metrics,
            "baseline_comparison": results,
            "files_saved": [
                str(MODELS_DIR / "best_model.joblib"),
                str(MODELS_DIR / "training_results.json"),
                str(REPORTS_DIR / "model_comparison_report.md"),
            ],
        }
        return json.dumps(output, indent=2)
