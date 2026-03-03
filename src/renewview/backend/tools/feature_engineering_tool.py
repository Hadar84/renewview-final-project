"""Feature Engineering Tool — transforms clean data into ML-ready features.

Creates derived features, encodes categoricals, scales numerics,
and produces stratified train/val/test splits.
"""

import json
from pathlib import Path
from typing import Type

import joblib
import numpy as np
import pandas as pd
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from renewview.config.settings import (
    DATA_DIR,
    MODELS_DIR,
    RANDOM_STATE,
    REPORTS_DIR,
    TEST_SPLIT,
    TRAIN_SPLIT,
    VAL_SPLIT,
)


class FeatureEngineeringInput(BaseModel):
    """Input schema for feature engineering tool."""

    data_path: str = Field(
        default=str(DATA_DIR / "clean_solar_data.csv"),
        description="Path to the cleaned CSV dataset.",
    )


class FeatureEngineeringTool(BaseTool):
    """Transform cleaned solar data into ML-ready features with train/val/test splits."""

    name: str = "feature_engineering"
    description: str = (
        "Loads clean_solar_data.csv, creates derived features "
        "(solar_cloud_ratio, temp_humidity_index, grid_accessibility_score, "
        "irradiance_consistency), one-hot encodes categoricals, scales numerics, "
        "and saves stratified train/val/test splits."
    )
    args_schema: Type[BaseModel] = FeatureEngineeringInput

    def _run(self, data_path: str = "") -> str:
        data_path = data_path or str(DATA_DIR / "clean_solar_data.csv")

        df = pd.read_csv(data_path)

        # ── Separate target ───────────────────────────────────
        target_col = "viability_class"
        y = df[target_col]
        X = df.drop(columns=[target_col])

        # ── Derived features (per tasks.yaml spec) ────────────
        X["solar_cloud_ratio"] = X["ghi"] / (X["cloud_cover"] + 1)
        X["temp_humidity_index"] = X["temperature"] * (1 - X["humidity"] / 100)
        X["grid_accessibility_score"] = 1 / (X["nearest_substation_km"] + 1)
        X["irradiance_consistency"] = X["dni"] / (X["ghi"] + 0.1)

        # ── Drop non-feature columns ──────────────────────────
        drop_cols = ["latitude", "longitude"]
        X = X.drop(columns=[c for c in drop_cols if c in X.columns])

        # ── One-hot encode categoricals ───────────────────────
        cat_cols = ["country", "site_type", "latitude_zone"]
        X = pd.get_dummies(X, columns=cat_cols, drop_first=False, dtype=float)

        # ── Record feature names before scaling ───────────────
        feature_names = list(X.columns)

        # ── Stratified split: 70/15/15 ────────────────────────
        test_val_ratio = VAL_SPLIT + TEST_SPLIT  # 0.30
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y,
            test_size=test_val_ratio,
            stratify=y,
            random_state=RANDOM_STATE,
        )
        # Split the temp set into val and test (50/50 of 0.30 = 0.15 each)
        val_fraction = VAL_SPLIT / test_val_ratio
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp,
            test_size=1 - val_fraction,
            stratify=y_temp,
            random_state=RANDOM_STATE,
        )

        # ── Scale numeric features ────────────────────────────
        scaler = StandardScaler()
        X_train_scaled = pd.DataFrame(
            scaler.fit_transform(X_train), columns=feature_names, index=X_train.index
        )
        X_val_scaled = pd.DataFrame(
            scaler.transform(X_val), columns=feature_names, index=X_val.index
        )
        X_test_scaled = pd.DataFrame(
            scaler.transform(X_test), columns=feature_names, index=X_test.index
        )

        # ── Save splits ──────────────────────────────────────
        features_dir = DATA_DIR / "features"
        features_dir.mkdir(parents=True, exist_ok=True)

        X_train_scaled.to_csv(features_dir / "X_train.csv", index=False)
        X_val_scaled.to_csv(features_dir / "X_val.csv", index=False)
        X_test_scaled.to_csv(features_dir / "X_test.csv", index=False)
        y_train.to_csv(features_dir / "y_train.csv", index=False)
        y_val.to_csv(features_dir / "y_val.csv", index=False)
        y_test.to_csv(features_dir / "y_test.csv", index=False)

        # ── Save feature pipeline ─────────────────────────────
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        pipeline_artifact = {
            "scaler": scaler,
            "feature_names": feature_names,
            "cat_columns": cat_cols,
            "drop_columns": drop_cols,
            "target_column": target_col,
        }
        joblib.dump(pipeline_artifact, MODELS_DIR / "feature_pipeline.joblib")

        # ── Save report ───────────────────────────────────────
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        report_lines = [
            "# Feature Engineering Report\n",
            f"**Source:** `{data_path}`\n",
            f"**Total samples:** {len(df)}\n",
            "## Derived Features\n",
            "| Feature | Formula |",
            "|---------|---------|",
            "| solar_cloud_ratio | ghi / (cloud_cover + 1) |",
            "| temp_humidity_index | temperature * (1 - humidity/100) |",
            "| grid_accessibility_score | 1 / (nearest_substation_km + 1) |",
            "| irradiance_consistency | dni / (ghi + 0.1) |",
            "",
            "## Encoding",
            f"- One-hot encoded: {cat_cols}",
            f"- Dropped: {drop_cols}",
            f"- Final feature count: {len(feature_names)}",
            "",
            "## Split Sizes",
            f"- Train: {len(X_train)} ({len(X_train)/len(df)*100:.0f}%)",
            f"- Validation: {len(X_val)} ({len(X_val)/len(df)*100:.0f}%)",
            f"- Test: {len(X_test)} ({len(X_test)/len(df)*100:.0f}%)",
            "",
            "## Class Distribution",
            "| Split | " + " | ".join(sorted(y.unique())) + " |",
            "|-------|" + "|".join(["------"] * len(y.unique())) + "|",
            f"| Train | " + " | ".join(
                str(int((y_train == c).sum())) for c in sorted(y.unique())
            ) + " |",
            f"| Val   | " + " | ".join(
                str(int((y_val == c).sum())) for c in sorted(y.unique())
            ) + " |",
            f"| Test  | " + " | ".join(
                str(int((y_test == c).sum())) for c in sorted(y.unique())
            ) + " |",
            "",
            f"## Feature Names ({len(feature_names)} total)",
            "```",
            "\n".join(feature_names),
            "```",
        ]
        (REPORTS_DIR / "feature_engineering_report.md").write_text(
            "\n".join(report_lines)
        )

        result = {
            "status": "SUCCESS",
            "total_samples": len(df),
            "feature_count": len(feature_names),
            "train_size": len(X_train),
            "val_size": len(X_val),
            "test_size": len(X_test),
            "class_distribution": y.value_counts().to_dict(),
            "feature_names": feature_names,
            "files_saved": [
                str(features_dir / "X_train.csv"),
                str(features_dir / "X_val.csv"),
                str(features_dir / "X_test.csv"),
                str(features_dir / "y_train.csv"),
                str(features_dir / "y_val.csv"),
                str(features_dir / "y_test.csv"),
                str(MODELS_DIR / "feature_pipeline.joblib"),
                str(REPORTS_DIR / "feature_engineering_report.md"),
            ],
        }
        return json.dumps(result, indent=2)
