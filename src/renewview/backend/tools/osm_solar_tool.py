"""OSM Solar Farm Tool — fetches confirmed solar installations from OpenStreetMap.

Uses Overpass API with bounding-box queries. Free, no key required.
Includes retry logic with delays to avoid Overpass rate-limiting.
"""

import json
import time
from typing import Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from renewview.config.settings import OSM_COUNTRY_BBOXES

_MAX_RETRIES = 3
_RETRY_DELAY_SECONDS = 10


class OSMSolarFarmInput(BaseModel):
    """Input schema for OSM Solar Farm tool."""

    country_code: str = Field(
        ..., description="ISO 3166-1 alpha-2: 'PT', 'ES', 'GR', 'IT'"
    )
    limit: int = Field(default=100, description="Max solar farms to return")


class OSMSolarFarmTool(BaseTool):
    """Fetch confirmed solar farm locations from OpenStreetMap."""

    name: str = "osm_solar_farms"
    description: str = (
        "Fetches confirmed solar farm/power plant locations from OpenStreetMap "
        "for PT, ES, GR, or IT. Returns lat, lon, name, capacity. "
        "Has built-in retry logic — safe to call once per country."
    )
    args_schema: Type[BaseModel] = OSMSolarFarmInput

    def _run(self, country_code: str, limit: int = 100) -> str:
        bbox = OSM_COUNTRY_BBOXES.get(country_code.upper())
        if not bbox:
            return json.dumps({"error": f"Unknown country: {country_code}. Use PT/ES/GR/IT."})

        south, west, north, east = bbox
        bbox_str = f"{south},{west},{north},{east}"

        query = f"""
        [out:json][timeout:90];
        (
          node["power"="generator"]["generator:source"="solar"]({bbox_str});
          way["power"="generator"]["generator:source"="solar"]({bbox_str});
          node["power"="plant"]["plant:source"="solar"]({bbox_str});
          way["power"="plant"]["plant:source"="solar"]({bbox_str});
          relation["power"="plant"]["plant:source"="solar"]({bbox_str});
        );
        out center {limit};
        """

        last_error = None
        for attempt in range(_MAX_RETRIES):
            if attempt > 0:
                print(f"  [OSM] Retry {attempt}/{_MAX_RETRIES - 1} for {country_code.upper()}, "
                      f"waiting {_RETRY_DELAY_SECONDS}s...")
                time.sleep(_RETRY_DELAY_SECONDS)

            try:
                resp = requests.post(
                    "https://overpass-api.de/api/interpreter",
                    data={"data": query}, timeout=120,
                )
                resp.raise_for_status()
                data = resp.json()
                farms = []
                for el in data.get("elements", []):
                    lat = el.get("lat") or el.get("center", {}).get("lat")
                    lon = el.get("lon") or el.get("center", {}).get("lon")
                    if lat and lon:
                        tags = el.get("tags", {})
                        farms.append({
                            "latitude": lat, "longitude": lon,
                            "name": tags.get("name", "unnamed"),
                            "capacity_mw": tags.get(
                                "plant:output:electricity",
                                tags.get("generator:output:electricity", "unknown"),
                            ),
                            "osm_id": el.get("id"),
                        })
                return json.dumps({
                    "country": country_code.upper(),
                    "total_found": len(farms),
                    "farms": farms[:limit],
                }, indent=2)
            except requests.exceptions.RequestException as e:
                last_error = e

        return json.dumps({
            "error": f"Failed after {_MAX_RETRIES} attempts: {last_error}",
            "country": country_code,
        })
