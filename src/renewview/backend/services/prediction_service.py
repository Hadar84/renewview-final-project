"""Prediction Service — loads trained model and runs inference.

This is the bridge between the backend ML pipeline and the frontend.
The frontend imports ONLY this service, never touches crews or tools directly.
"""

from pathlib import Path
from typing import Optional

import pandas as pd

from renewview.backend.gates.elimination_gates import GateResult, run_elimination_gates
from renewview.backend.services.energy_calculator import (
    estimate_annual_kwh,
    estimate_revenue_eur,
    feasibility_score,
    parcel_ha_to_m2,
)
from renewview.config.settings import MODELS_DIR, NOT_VIABLE_CLASS


class PredictionService:
    """Loads the trained model and provides predictions to the frontend."""

    def __init__(self):
        self._model = None
        self._pipeline = None
        self._loaded = False

    def load_model(self) -> bool:
        """Attempt to load the trained model and feature pipeline.

        Returns:
            True if model loaded successfully, False otherwise.
        """
        model_path = MODELS_DIR / "best_model.joblib"
        pipeline_path = MODELS_DIR / "feature_pipeline.joblib"

        try:
            import joblib
            self._model = joblib.load(model_path)
            self._pipeline = joblib.load(pipeline_path)
            self._loaded = True
            return True
        except FileNotFoundError:
            self._loaded = False
            return False

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def assess_site(
        self,
        latitude: float,
        longitude: float,
        country: str,
        site_type: str,
        parcel_size_ha: float,
        grid_distance_km: float,
        land_status: str = "agricultural",
        ghi: Optional[float] = None,
        usable_m2: Optional[float] = None,
    ) -> dict:
        """Run full assessment: gates → model → energy → score.

        Args:
            latitude: Site latitude.
            longitude: Site longitude.
            country: Country name.
            site_type: ground_parcel / commercial_rooftop / parking_structure.
            parcel_size_ha: Parcel size in hectares (ground) or 0 for rooftop.
            grid_distance_km: Distance to grid in km.
            land_status: Land classification string.
            ghi: GHI in kWh/m²/day (if None, will use heuristic).
            usable_m2: Usable area in m² (for rooftop/parking).

        Returns:
            Dict with viability_class, score, annual_kwh, revenue_eur, reasoning.
        """
        # Default GHI estimate by latitude if not provided
        if ghi is None:
            ghi = self._estimate_ghi_by_latitude(latitude)

        # ── Step 1: Elimination Gates ───────────────────────
        gate_result = run_elimination_gates(
            land_status=land_status,
            grid_distance_km=grid_distance_km,
            ghi_kwh=ghi,
            parcel_size_ha=parcel_size_ha,
            site_type=site_type,
        )

        if not gate_result.passed:
            return {
                "viability_class": NOT_VIABLE_CLASS,
                "score": 0.0,
                "annual_kwh": 0,
                "revenue_eur": 0,
                "eliminated_by": gate_result.eliminated_by,
                "reason": gate_result.reason,
                "redirect_to": gate_result.redirect_to,
                "flags": gate_result.flags,
                "used_model": False,
            }

        # ── Step 2: ML Prediction (if model available) ──────
        model_confidence = 0.0
        viability_class = "Medium"  # default heuristic

        if self._loaded:
            try:
                prediction, confidence = self._predict_with_model(
                    latitude, longitude, country, site_type,
                    parcel_size_ha, grid_distance_km, ghi,
                )
                viability_class = prediction
                model_confidence = confidence
            except Exception:
                viability_class = self._heuristic_class(ghi, grid_distance_km)
        else:
            viability_class = self._heuristic_class(ghi, grid_distance_km)

        # ── Step 3: Energy Calculation ──────────────────────
        if usable_m2 and site_type != "ground_parcel":
            area_m2 = usable_m2
        else:
            area_m2 = parcel_ha_to_m2(parcel_size_ha)

        annual_kwh = estimate_annual_kwh(ghi, area_m2, site_type)
        revenue_eur = estimate_revenue_eur(annual_kwh, country)

        # ── Step 4: Feasibility Score ───────────────────────
        score = feasibility_score(ghi, grid_distance_km, parcel_size_ha, model_confidence)

        return {
            "viability_class": viability_class,
            "score": score,
            "annual_kwh": annual_kwh,
            "revenue_eur": revenue_eur,
            "ghi_used": ghi,
            "eliminated_by": None,
            "reason": None,
            "redirect_to": None,
            "flags": gate_result.flags,
            "used_model": self._loaded,
        }

    def _predict_with_model(self, lat, lon, country, site_type, size, grid_km, ghi):
        """Run the ML model. Returns (class_label, confidence)."""
        features = pd.DataFrame([{
            "latitude": lat,
            "longitude": lon,
            "ghi": ghi,
            "nearest_substation_km": grid_km,
            "parcel_size_ha": size,
        }])

        # Transform through feature pipeline
        features_transformed = self._pipeline.transform(features)
        prediction = self._model.predict(features_transformed)[0]
        probas = self._model.predict_proba(features_transformed)[0]
        confidence = max(probas)

        return prediction, confidence

    @staticmethod
    def _heuristic_class(ghi: float, grid_km: float) -> str:
        """Fallback heuristic when model isn't available."""
        if ghi >= 5.0 and grid_km <= 3:
            return "High"
        elif ghi >= 4.0 and grid_km <= 5:
            return "Medium"
        else:
            return "Low"

    @staticmethod
    def _estimate_ghi_by_latitude(lat: float) -> float:
        """Rough GHI estimate by latitude for Southern Europe."""
        if lat < 36:
            return 5.5
        elif lat < 38:
            return 5.0
        elif lat < 40:
            return 4.5
        elif lat < 42:
            return 4.0
        else:
            return 3.8
