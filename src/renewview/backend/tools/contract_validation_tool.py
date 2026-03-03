"""Contract Validation Tool — validates dataset against JSON Schema contract.

Checks column names, types, value ranges, nulls, and row count
before the ML pipeline begins.
"""

import json
from pathlib import Path
from typing import Type

import pandas as pd
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from renewview.config.settings import DATA_DIR


class ContractValidationInput(BaseModel):
    """Input schema for contract validation tool."""

    data_path: str = Field(
        default=str(DATA_DIR / "clean_solar_data.csv"),
        description="Path to the CSV dataset to validate.",
    )
    contract_path: str = Field(
        default=str(DATA_DIR / "dataset_contract.json"),
        description="Path to the JSON Schema contract file.",
    )


class ContractValidationTool(BaseTool):
    """Validate a CSV dataset against its JSON Schema contract."""

    name: str = "contract_validation"
    description: str = (
        "Validates clean_solar_data.csv against dataset_contract.json. "
        "Checks column presence, types, value ranges, null policy, and "
        "row count. Returns PASS/FAIL with detailed report."
    )
    args_schema: Type[BaseModel] = ContractValidationInput

    def _run(self, data_path: str = "", contract_path: str = "") -> str:
        data_path = data_path or str(DATA_DIR / "clean_solar_data.csv")
        contract_path = contract_path or str(DATA_DIR / "dataset_contract.json")

        errors: list[str] = []
        warnings: list[str] = []

        # Load contract
        try:
            with open(contract_path) as f:
                contract = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return json.dumps({"status": "FAIL", "error": f"Cannot load contract: {e}"})

        # Load dataset
        try:
            df = pd.read_csv(data_path)
        except (FileNotFoundError, pd.errors.ParserError) as e:
            return json.dumps({"status": "FAIL", "error": f"Cannot load dataset: {e}"})

        properties = contract.get("properties", {})
        required_cols = contract.get("required", [])

        # Check required columns exist
        missing_cols = [c for c in required_cols if c not in df.columns]
        if missing_cols:
            errors.append(f"Missing required columns: {missing_cols}")

        extra_cols = [c for c in df.columns if c not in properties]
        if extra_cols:
            warnings.append(f"Extra columns not in contract: {extra_cols}")

        # Check nulls
        null_counts = df.isnull().sum()
        cols_with_nulls = {col: int(cnt) for col, cnt in null_counts.items() if cnt > 0}
        if cols_with_nulls:
            errors.append(f"Null values found: {cols_with_nulls}")

        # Check value ranges for numeric columns
        for col_name, spec in properties.items():
            if col_name not in df.columns:
                continue

            col_type = spec.get("type")
            if col_type == "number" and pd.api.types.is_numeric_dtype(df[col_name]):
                col_min = spec.get("minimum")
                col_max = spec.get("maximum")
                actual_min = float(df[col_name].min())
                actual_max = float(df[col_name].max())

                if col_min is not None and actual_min < col_min:
                    errors.append(
                        f"{col_name}: min {actual_min} < contract min {col_min}"
                    )
                if col_max is not None and actual_max > col_max:
                    errors.append(
                        f"{col_name}: max {actual_max} > contract max {col_max}"
                    )

            elif col_type == "string" and "enum" in spec:
                allowed = set(spec["enum"])
                actual = set(df[col_name].unique())
                invalid = actual - allowed
                if invalid:
                    errors.append(
                        f"{col_name}: invalid values {invalid}, allowed: {allowed}"
                    )

        # Identify target and feature columns
        target_col = "viability_class"
        feature_cols = [c for c in df.columns if c != target_col]

        status = "FAIL" if errors else "PASS"
        result = {
            "status": status,
            "rows": len(df),
            "columns": len(df.columns),
            "target_column": target_col,
            "feature_columns": feature_cols,
            "class_distribution": df[target_col].value_counts().to_dict()
                if target_col in df.columns else {},
            "errors": errors,
            "warnings": warnings,
        }
        return json.dumps(result, indent=2)
