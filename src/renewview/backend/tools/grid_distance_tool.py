"""Grid Distance Calculator — haversine distance to nearest infrastructure."""

import json
import math
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class GridDistanceInput(BaseModel):
    latitude: float = Field(..., description="Latitude of the point to check")
    longitude: float = Field(..., description="Longitude of the point to check")
    reference_points: str = Field(
        ..., description='JSON array: [{"lat": 38.5, "lon": -8.2}, ...]'
    )


class GridDistanceCalculatorTool(BaseTool):
    """Calculate haversine distance to nearest solar infrastructure."""

    name: str = "grid_distance_calculator"
    description: str = (
        "Calculates haversine distance in km from a lat/lon to the nearest "
        "reference point (solar farm or substation)."
    )
    args_schema: Type[BaseModel] = GridDistanceInput

    @staticmethod
    def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371.0
        lat1_r, lon1_r = math.radians(lat1), math.radians(lon1)
        lat2_r, lon2_r = math.radians(lat2), math.radians(lon2)
        dlat, dlon = lat2_r - lat1_r, lon2_r - lon1_r
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def _run(self, latitude: float, longitude: float, reference_points: str) -> str:
        try:
            refs = json.loads(reference_points)
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON for reference_points"})
        if not refs:
            return json.dumps({"error": "No reference points provided"})

        min_dist, nearest = float("inf"), None
        for ref in refs:
            rlat = ref.get("lat") or ref.get("latitude")
            rlon = ref.get("lon") or ref.get("longitude")
            if rlat is None or rlon is None:
                continue
            d = self._haversine(latitude, longitude, rlat, rlon)
            if d < min_dist:
                min_dist, nearest = d, ref

        return json.dumps({
            "query_point": {"latitude": latitude, "longitude": longitude},
            "nearest_distance_km": round(min_dist, 2),
            "nearest_point": nearest,
            "total_reference_points": len(refs),
        }, indent=2)
