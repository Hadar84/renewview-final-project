"""Model Evaluation Tool — evaluates the trained model and produces reports.

Generates classification report, confusion matrix, feature importance,
ROC curves, evaluation report, and model card.
"""

import json
from pathlib import Path
from typing import Type

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.preprocessing import label_binarize

from renewview.config.settings import DATA_DIR, FIGURES_DIR, MODELS_DIR, REPORTS_DIR


class ModelEvaluationInput(BaseModel):
    """Input schema for model evaluation tool."""

    model_path: str = Field(
        default=str(MODELS_DIR / "best_model.joblib"),
        description="Path to the trained model (.joblib).",
    )
    features_dir: str = Field(
        default=str(DATA_DIR / "features"),
        description="Directory containing X_test.csv and y_test.csv.",
    )


class ModelEvaluationTool(BaseTool):
    """Evaluate the trained model and produce reports, figures, and model card."""

    name: str = "model_evaluation"
    description: str = (
        "Evaluates the best trained model on the held-out test set. "
        "Generates confusion matrix, feature importance, ROC curves, "
        "a final evaluation report, and a model card."
    )
    args_schema: Type[BaseModel] = ModelEvaluationInput

    def _run(self, model_path: str = "", features_dir: str = "") -> str:
        model_path = Path(model_path) if model_path else MODELS_DIR / "best_model.joblib"
        features_dir = Path(features_dir) if features_dir else DATA_DIR / "features"

        # ── Load model and test data ──────────────────────────
        model = joblib.load(model_path)
        X_test = pd.read_csv(features_dir / "X_test.csv")
        y_test = pd.read_csv(features_dir / "y_test.csv").squeeze()

        classes = sorted(y_test.unique())
        y_pred = model.predict(X_test)

        # ── Metrics ───────────────────────────────────────────
        metrics = {
            "accuracy": round(accuracy_score(y_test, y_pred), 4),
            "precision_macro": round(
                precision_score(y_test, y_pred, average="macro", zero_division=0), 4
            ),
            "recall_macro": round(
                recall_score(y_test, y_pred, average="macro", zero_division=0), 4
            ),
            "f1_macro": round(
                f1_score(y_test, y_pred, average="macro", zero_division=0), 4
            ),
        }
        report_text = classification_report(
            y_test, y_pred, zero_division=0
        )

        # ── Figures ───────────────────────────────────────────
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)

        # Confusion matrix
        fig_cm, ax_cm = plt.subplots(figsize=(6, 5))
        ConfusionMatrixDisplay.from_predictions(
            y_test, y_pred, display_labels=classes, ax=ax_cm, cmap="Blues"
        )
        ax_cm.set_title("Confusion Matrix — Test Set")
        fig_cm.tight_layout()
        fig_cm.savefig(FIGURES_DIR / "confusion_matrix.png", dpi=150)
        plt.close(fig_cm)

        # Feature importance
        fig_fi, ax_fi = plt.subplots(figsize=(8, 6))
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            feature_names = X_test.columns
            sorted_idx = np.argsort(importances)[-15:]  # top 15
            ax_fi.barh(
                [feature_names[i] for i in sorted_idx],
                importances[sorted_idx],
                color="steelblue",
            )
            ax_fi.set_xlabel("Feature Importance")
            ax_fi.set_title("Top 15 Feature Importances")
        fig_fi.tight_layout()
        fig_fi.savefig(FIGURES_DIR / "feature_importance.png", dpi=150)
        plt.close(fig_fi)

        # ROC curves (one-vs-rest)
        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_test)
            y_test_bin = label_binarize(y_test, classes=classes)

            fig_roc, ax_roc = plt.subplots(figsize=(7, 6))
            for i, cls in enumerate(classes):
                if y_test_bin.shape[1] > 1:
                    RocCurveDisplay.from_predictions(
                        y_test_bin[:, i], y_proba[:, i],
                        name=cls, ax=ax_roc,
                    )
                else:
                    # Binary case: use column 0 directly
                    RocCurveDisplay.from_predictions(
                        y_test_bin.ravel(), y_proba[:, 1],
                        name="Positive class", ax=ax_roc,
                    )
                    break
            ax_roc.set_title("ROC Curves (One-vs-Rest)")
            ax_roc.plot([0, 1], [0, 1], "k--", alpha=0.3)
            fig_roc.tight_layout()
            fig_roc.savefig(FIGURES_DIR / "roc_curves.png", dpi=150)
            plt.close(fig_roc)

        # ── Feature importance data for report ────────────────
        top_features = []
        if hasattr(model, "feature_importances_"):
            sorted_idx_all = np.argsort(importances)[::-1]
            for idx in sorted_idx_all[:10]:
                top_features.append({
                    "feature": X_test.columns[idx],
                    "importance": round(float(importances[idx]), 4),
                })

        # ── Evaluation report ─────────────────────────────────
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        eval_lines = [
            "# Final Evaluation Report\n",
            f"**Model:** `{model_path.name}`",
            f"**Test samples:** {len(X_test)}\n",
            "## Test Set Metrics\n",
            f"- Accuracy: {metrics['accuracy']}",
            f"- Precision (macro): {metrics['precision_macro']}",
            f"- Recall (macro): {metrics['recall_macro']}",
            f"- F1 (macro): {metrics['f1_macro']}\n",
            "## Classification Report\n",
            "```",
            report_text,
            "```\n",
            "## Figures\n",
            "- `figures/confusion_matrix.png`",
            "- `figures/feature_importance.png`",
            "- `figures/roc_curves.png`\n",
            "## Top 10 Features\n",
            "| Rank | Feature | Importance |",
            "|------|---------|------------|",
        ]
        for i, feat in enumerate(top_features, 1):
            eval_lines.append(
                f"| {i} | {feat['feature']} | {feat['importance']} |"
            )
        eval_lines.extend([
            "",
            "## Business Interpretation\n",
            "- **High viability:** Site has strong solar resource and good grid access. "
            "Recommended for development.\n",
            "- **Low viability:** Marginal solar resource or poor infrastructure. "
            "Higher investment risk.\n",
            "- **False positive risk:** A site wrongly classified as High may lead to "
            "wasted consultant visits and feasibility studies.\n",
            "- **False negative risk:** A viable site classified as Low represents a "
            "missed renewable energy opportunity.",
        ])
        (REPORTS_DIR / "final_evaluation_report.md").write_text(
            "\n".join(eval_lines)
        )

        # ── Model card ────────────────────────────────────────
        model_type = type(model).__name__
        card_lines = [
            "# Model Card — RenewView Solar Viability Classifier\n",
            "## Model Details\n",
            f"- **Model type:** {model_type}",
            f"- **Framework:** scikit-learn",
            f"- **Version:** 1.0",
            f"- **Date:** 2026-03\n",
            "## Intended Use\n",
            "- **Primary use:** Classify solar energy site viability as High or Low "
            "for sites in Southern Europe (Portugal, Spain, Greece) that pass "
            "elimination gates.",
            "- **Intended users:** Renewable energy consultants, land assessment "
            "analysts, Streamlit app end-users.",
            "- **Out of scope:** Sites outside Southern Europe; sites that fail "
            "elimination gates (those are pre-classified as Not Viable).\n",
            "## Training Data\n",
            "- **Source:** NASA POWER API (solar irradiance, climate) + "
            "OpenStreetMap (confirmed solar farm locations, substations).",
            "- **Countries:** Portugal, Spain, Greece.",
            "- **Size:** ~100 samples after cleaning and deduplication.",
            "- **Target:** viability_class (High/Low). "
            "Not Viable is assigned by elimination gates, not this model.\n",
            "## Performance\n",
            f"- Accuracy: {metrics['accuracy']}",
            f"- F1 (macro): {metrics['f1_macro']}",
            f"- Precision (macro): {metrics['precision_macro']}",
            f"- Recall (macro): {metrics['recall_macro']}\n",
            "## Limitations\n",
            "- **Small dataset:** ~100 samples limits generalization. "
            "Performance may degrade on unseen regions.",
            "- **Data-rich region bias:** Portugal and Greece have more confirmed "
            "solar farms in OSM than less-documented areas.",
            "- **No Medium class:** Current data distribution only produced "
            "High and Low labels. Medium sites are not represented.\n",
            "## Ethical Considerations\n",
            "- **Agricultural land conversion:** High viability scores on "
            "agricultural land may encourage conversion to solar farms, "
            "with food security trade-offs.",
            "- **False positive impact:** Overestimating viability could lead "
            "to wasted investment on marginal sites.",
            "- **Regional equity:** Under-documented regions may receive "
            "systematically lower scores due to data gaps, not actual "
            "unsuitability.",
        ]
        (REPORTS_DIR / "model_card.md").write_text("\n".join(card_lines))

        output = {
            "status": "SUCCESS",
            "test_metrics": metrics,
            "top_features": top_features,
            "figures_saved": [
                str(FIGURES_DIR / "confusion_matrix.png"),
                str(FIGURES_DIR / "feature_importance.png"),
                str(FIGURES_DIR / "roc_curves.png"),
            ],
            "reports_saved": [
                str(REPORTS_DIR / "final_evaluation_report.md"),
                str(REPORTS_DIR / "model_card.md"),
            ],
        }
        return json.dumps(output, indent=2)
