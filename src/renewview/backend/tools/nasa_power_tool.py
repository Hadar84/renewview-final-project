"""NASA POWER API Tool — fetches solar irradiance and climate data.

Free API, no key required. Docs: https://power.larc.nasa.gov/docs/services/api/
"""

import json
from typing import Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from renewview.config.settings import NASA_POWER_PARAMS


class NASAPowerInput(BaseModel):
    """Input schema for NASA POWER API tool."""

    latitude: float = Field(..., description="Latitude (-90 to 90)")
    longitude: float = Field(..., description="Longitude (-180 to 180)")
    start_year: int = Field(default=2020, description="Start year (default: 2020)")
    end_year: int = Field(default=2023, description="End year (default: 2023)")


class NASAPowerTool(BaseTool):
    """Fetch solar irradiance and climate data from NASA POWER API."""

    name: str = "nasa_power_solar_data"
    description: str = (
        "Fetches solar irradiance and climate data from NASA POWER API "
        "for a given lat/lon. Returns GHI, DNI, temperature, humidity, "
        "wind speed, precipitation, cloud cover as annual averages."
    )
    args_schema: Type[BaseModel] = NASAPowerInput

    def _run(self, latitude: float, longitude: float,
             start_year: int = 2020, end_year: int = 2023) -> str:
        url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
        params = {
            "parameters": NASA_POWER_PARAMS,
            "community": "RE",
            "longitude": longitude,
            "latitude": latitude,
            "start": start_year,
            "end": end_year,
            "format": "JSON",
        }
        try:
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            p = data.get("properties", {}).get("parameter", {})
            result = {
                "latitude": latitude,
                "longitude": longitude,
                "ghi_kwh_m2_day": p.get("ALLSKY_SFC_SW_DWN", {}).get("ANN"),
                "dni_kwh_m2_day": p.get("ALLSKY_SFC_SW_DNI", {}).get("ANN"),
                "temperature_c": p.get("T2M", {}).get("ANN"),
                "humidity_pct": p.get("RH2M", {}).get("ANN"),
                "wind_speed_ms": p.get("WS2M", {}).get("ANN"),
                "precipitation_mm_day": p.get("PRECTOTCORR", {}).get("ANN"),
                "cloud_cover_pct": p.get("CLOUD_AMT", {}).get("ANN"),
                "data_years": f"{start_year}-{end_year}",
            }
            return json.dumps(result, indent=2)
        except requests.exceptions.RequestException as e:
            return json.dumps({"error": str(e), "latitude": latitude, "longitude": longitude})
