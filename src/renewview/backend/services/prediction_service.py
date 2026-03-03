"""Prediction Service — loads trained model and runs inference.

This is the bridge between the backend ML pipeline and the frontend.
The frontend imports ONLY this service, never touches crews or tools directly.
"""

from typing import Optional

import numpy as np
import pandas as pd

from renewview.backend.gates.elimination_gates import run_elimination_gates
from renewview.backend.services.energy_calculator import (
    estimate_annual_kwh,
    estimate_revenue_eur,
    feasibility_score,
    parcel_ha_to_m2,
)
from renewview.config.settings import MODELS_DIR, NOT_VIABLE_CLASS, TARGET_COUNTRIES


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
        dni: Optional[float] = None,
        temperature: Optional[float] = None,
        humidity: Optional[float] = None,
        wind_speed: Optional[float] = None,
        precipitation: Optional[float] = None,
        cloud_cover: Optional[float] = None,
        usable_m2: Optional[float] = None,
    ) -> dict:
        """Run full assessment: gates → model → energy → score.

        Args:
            latitude: Site latitude.
            longitude: Site longitude.
            country: Country name or code (e.g. "Portugal" or "PT").
            site_type: ground_parcel / commercial_rooftop / parking_structure.
            parcel_size_ha: Parcel size in hectares (ground) or 0 for rooftop.
            grid_distance_km: Distance to grid in km.
            land_status: Land classification string.
            ghi: GHI in kWh/m²/day (if None, will estimate by latitude).
            dni: DNI in kWh/m²/day (if None, defaults to ghi * 1.15).
            temperature: Temperature in Celsius (if None, defaults to 18).
            humidity: Relative humidity % (if None, defaults to 65).
            wind_speed: Wind speed m/s (if None, defaults to 3.0).
            precipitation: Precipitation mm/day (if None, defaults to 2.0).
            cloud_cover: Cloud cover % (if None, defaults to 40).
            usable_m2: Usable area in m² (for rooftop/parking).

        Returns:
            Dict with viability_class, score, annual_kwh, revenue_eur, reasoning.
        """
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
        viability_class = "Medium"

        if self._loaded:
            try:
                prediction, confidence = self._predict_with_model(
                    latitude=latitude,
                    longitude=longitude,
                    country=country,
                    site_type=site_type,
                    grid_distance_km=grid_distance_km,
                    ghi=ghi,
                    dni=dni if dni is not None else ghi * 1.15,
                    temperature=temperature if temperature is not None else 18.0,
                    humidity=humidity if humidity is not None else 65.0,
                    wind_speed=wind_speed if wind_speed is not None else 3.0,
                    precipitation=precipitation if precipitation is not None else 2.0,
                    cloud_cover=cloud_cover if cloud_cover is not None else 40.0,
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

    def _predict_with_model(
        self,
        latitude: float,
        longitude: float,
        country: str,
        site_type: str,
        grid_distance_km: float,
        ghi: float,
        dni: float,
        temperature: float,
        humidity: float,
        wind_speed: float,
        precipitation: float,
        cloud_cover: float,
    ) -> tuple[str, float]:
        """Run the ML model using the saved feature pipeline.

        Replicates the same transforms as FeatureEngineeringTool:
        derived features → drop lat/lon → one-hot encode → scale.

        Returns:
            (class_label, confidence) tuple.
        """
        pipeline = self._pipeline  # dict with scaler, feature_names, etc.
        scaler = pipeline["scaler"]
        feature_names = pipeline["feature_names"]
        cat_columns = pipeline["cat_columns"]

        # Resolve country code
        country_code = country
        for code, name in TARGET_COUNTRIES.items():
            if country.lower() in (code.lower(), name.lower()):
                country_code = code
                break

        # Determine latitude zone
        if latitude < 38:
            lat_zone = "south"
        elif latitude < 40:
            lat_zone = "middle"
        else:
            lat_zone = "north"

        # Map frontend site_type to training site_type
        training_site_type = "solar_farm" if site_type == "ground_parcel" else "sample_point"

        # Build raw feature row
        raw = {
            "ghi": ghi,
            "dni": dni,
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "precipitation": precipitation,
            "cloud_cover": cloud_cover,
            "nearest_solar_farm_km": 0.0,
            "nearest_substation_km": grid_distance_km,
            "solar_cloud_ratio": ghi / (cloud_cover + 1),
            "temp_humidity_index": temperature * (1 - humidity / 100),
            "grid_accessibility_score": 1 / (grid_distance_km + 1),
            "irradiance_consistency": dni / (ghi + 0.1),
        }

        # One-hot encode categoricals (match training column names)
        cat_values = {
            "country": country_code,
            "site_type": training_site_type,
            "latitude_zone": lat_zone,
        }
        for col in cat_columns:
            val = cat_values.get(col, "")
            for feat in feature_names:
                if feat.startswith(f"{col}_"):
                    raw[feat] = 1.0 if feat == f"{col}_{val}" else 0.0

        # Build DataFrame in exact feature order
        row = {fn: raw.get(fn, 0.0) for fn in feature_names}
        X = pd.DataFrame([row], columns=feature_names)

        # Scale
        X_scaled = pd.DataFrame(
            scaler.transform(X), columns=feature_names
        )

        prediction = self._model.predict(X_scaled)[0]
        probas = self._model.predict_proba(X_scaled)[0]
        confidence = float(max(probas))

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
