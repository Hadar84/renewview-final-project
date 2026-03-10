"""Site Inputs Component — adaptive forms per site type (proposal Section 4).

Ground parcels: terrain, grid distance, wetland status, parcel size (ha).
Rooftop/Parking: usable m², skip terrain.
Includes optional live NASA POWER data fetch, address geocoding, and polygon drawing.
"""

import json
import math

import folium
import requests
import streamlit as st
from folium.plugins import Draw
from shapely.geometry import shape
from shapely.ops import transform
from streamlit_folium import st_folium

from renewview.config.settings import (
    ELEVATION_GRID_STEP_DEG,
    MAP_DEFAULT_ZOOM,
    MAP_TILE_PROVIDER,
    NASA_POWER_PARAMS,
    NOMINATIM_TIMEOUT,
    NOMINATIM_URL,
    NOMINATIM_USER_AGENT,
    OPEN_ELEVATION_TIMEOUT,
    OPEN_ELEVATION_URL,
    OVERPASS_TIMEOUT,
    OVERPASS_URL,
    SUBSTATION_SEARCH_RADII_KM,
    TERRAIN_COUNTRY_FALLBACK,
    TERRAIN_VARIANCE_FLAT,
    TERRAIN_VARIANCE_HILLY,
)
from renewview.frontend.assets.i18n import t
from renewview.frontend.assets.styles import nasa_card_header_html, section_header_html


def _fetch_nasa_power(latitude: float, longitude: float) -> dict | None:
    """Fetch climate data from NASA POWER API. Returns dict or None on error."""
    url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
    params = {
        "parameters": NASA_POWER_PARAMS,
        "community": "RE",
        "longitude": longitude,
        "latitude": latitude,
        "format": "JSON",
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        p = data.get("properties", {}).get("parameter", {})
        return {
            "ghi": p.get("ALLSKY_SFC_SW_DWN", {}).get("ANN"),
            "dni": p.get("ALLSKY_SFC_SW_DNI", {}).get("ANN"),
            "temperature": p.get("T2M", {}).get("ANN"),
            "humidity": p.get("RH2M", {}).get("ANN"),
            "wind_speed": p.get("WS2M", {}).get("ANN"),
            "precipitation": p.get("PRECTOTCORR", {}).get("ANN"),
            "cloud_cover": p.get("CLOUD_AMT", {}).get("ANN"),
        }
    except (requests.exceptions.RequestException, KeyError, json.JSONDecodeError):
        return None


def _geocode_address(address: str) -> dict | None:
    """Geocode an address via Nominatim. Returns {"lat", "lon", "display_name"} or None."""
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
        "viewbox": "-10,44,30,34",
        "bounded": 0,
    }
    headers = {"User-Agent": NOMINATIM_USER_AGENT}
    try:
        resp = requests.get(
            NOMINATIM_URL, params=params, headers=headers, timeout=NOMINATIM_TIMEOUT,
        )
        resp.raise_for_status()
        results = resp.json()
        if results:
            return {
                "lat": float(results[0]["lat"]),
                "lon": float(results[0]["lon"]),
                "display_name": results[0].get("display_name", ""),
            }
    except (requests.exceptions.RequestException, KeyError, ValueError, json.JSONDecodeError):
        pass
    return None


def _polygon_area_m2(coords: list[list[float]]) -> float:
    """Calculate area of a lat/lon polygon in m² using local meter projection.

    Args:
        coords: List of [longitude, latitude] pairs (GeoJSON order).

    Returns:
        Area in square meters.
    """
    geojson_geom = {"type": "Polygon", "coordinates": [coords]}
    polygon = shape(geojson_geom)
    centroid = polygon.centroid
    lat_rad = math.radians(centroid.y)

    m_per_deg_lat = 111_320.0
    m_per_deg_lon = 111_320.0 * math.cos(lat_rad)

    def _to_meters(lon: float, lat: float) -> tuple[float, float]:
        return (lon * m_per_deg_lon, lat * m_per_deg_lat)

    projected = transform(_to_meters, polygon)
    return abs(projected.area)


def _polygon_centroid(coords: list[list[float]]) -> tuple[float, float]:
    """Return (latitude, longitude) centroid of a polygon.

    Args:
        coords: List of [longitude, latitude] pairs (GeoJSON order).

    Returns:
        (latitude, longitude) tuple.
    """
    geojson_geom = {"type": "Polygon", "coordinates": [coords]}
    polygon = shape(geojson_geom)
    c = polygon.centroid
    return (c.y, c.x)


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Haversine distance in km between two lat/lon points."""
    r = 6371.0
    la1, lo1, la2, lo2 = map(math.radians, (lat1, lon1, lat2, lon2))
    dlat, dlon = la2 - la1, lo2 - lo1
    a = math.sin(dlat / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(dlon / 2) ** 2
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _detect_grid_distance(lat: float, lon: float) -> float | None:
    """Query Overpass for nearest substation, trying progressively larger radii."""
    for radius_km in SUBSTATION_SEARCH_RADII_KM:
        radius_m = int(radius_km * 1000)
        query = (
            f"[out:json][timeout:{OVERPASS_TIMEOUT}];"
            f'node["power"="substation"](around:{radius_m},{lat},{lon});'
            f"out body;"
        )
        try:
            resp = requests.post(
                OVERPASS_URL, data={"data": query}, timeout=OVERPASS_TIMEOUT + 5,
            )
            resp.raise_for_status()
            elements = resp.json().get("elements", [])
            if elements:
                min_dist = min(
                    _haversine_km(lat, lon, e["lat"], e["lon"]) for e in elements
                )
                return round(min_dist, 2)
        except (requests.exceptions.RequestException, KeyError, ValueError, json.JSONDecodeError):
            return None
    return None


def _detect_terrain(lat: float, lon: float, country: str = "") -> str:
    """Detect terrain type from elevation variance at a 3x3 grid.

    Falls back to country-based estimate if the API is unavailable.
    """
    locations = []
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            locations.append({
                "latitude": lat + dy * ELEVATION_GRID_STEP_DEG,
                "longitude": lon + dx * ELEVATION_GRID_STEP_DEG,
            })

    try:
        resp = requests.post(
            OPEN_ELEVATION_URL,
            json={"locations": locations},
            timeout=OPEN_ELEVATION_TIMEOUT,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        elevations = [r["elevation"] for r in results if r.get("elevation") is not None]
        if len(elevations) < 3:
            raise ValueError("Too few elevation points")

        mean_elev = sum(elevations) / len(elevations)
        variance = sum((e - mean_elev) ** 2 for e in elevations) / len(elevations)
        std_dev = math.sqrt(variance)

        if std_dev < TERRAIN_VARIANCE_FLAT:
            return "flat"
        if std_dev < TERRAIN_VARIANCE_HILLY:
            return "hilly"
        return "mountainous"
    except (requests.exceptions.RequestException, KeyError, ValueError, json.JSONDecodeError):
        # Fallback: estimate terrain from country
        return TERRAIN_COUNTRY_FALLBACK.get(country, "hilly")


def render_site_inputs(lang: str = "EN") -> dict:
    """Render adaptive input form based on site type. Returns input dict."""

    # ══════════════════════════════════════════════════════════
    # SECTION A — Location
    # ══════════════════════════════════════════════════════════
    st.markdown(section_header_html(t("location", lang)), unsafe_allow_html=True)

    # ── Address search ──────────────────────────────────────
    search_col, btn_col = st.columns([4, 1])
    with search_col:
        address_query = st.text_input(
            t("search_address", lang),
            placeholder=t("search_address_placeholder", lang),
            label_visibility="collapsed",
        )
    with btn_col:
        search_clicked = st.button(
            t("search_button", lang), use_container_width=True,
        )

    if search_clicked and address_query.strip():
        with st.spinner(t("searching_address", lang)):
            geo = _geocode_address(address_query.strip())
        if geo:
            st.session_state["_geo_lat"] = geo["lat"]
            st.session_state["_geo_lon"] = geo["lon"]
            st.session_state["_geo_display"] = geo["display_name"]
            st.rerun()
        else:
            st.warning(t("address_not_found", lang))

    if st.session_state.get("_geo_display"):
        st.success(
            f'{t("address_found", lang)} '
            f'({st.session_state["_geo_display"][:80]})'
        )

    # ── Country (always visible) ─────────────────────────────
    country = st.selectbox(
        t("country", lang),
        ["Portugal", "Spain", "Greece", "Italy"],
    )

    # ── Lat / Lon (collapsed expander) ────────────────────
    with st.expander(t("advanced_coords", lang), expanded=False):
        coord1, coord2 = st.columns(2)
        with coord1:
            latitude = st.number_input(
                t("latitude", lang), min_value=34.0, max_value=44.0,
                value=float(st.session_state.get("_geo_lat", 38.7)),
                step=0.1,
            )
        with coord2:
            longitude = st.number_input(
                t("longitude", lang), min_value=-10.0, max_value=30.0,
                value=float(st.session_state.get("_geo_lon", -9.1)),
                step=0.1,
            )

    # ── Folium map with Draw plugin ─────────────────────────
    st.caption(t("draw_parcel", lang))

    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=MAP_DEFAULT_ZOOM,
        tiles=MAP_TILE_PROVIDER,
    )

    folium.Marker(
        [latitude, longitude],
        icon=folium.Icon(color="green", icon="sun-o", prefix="fa"),
        popup="Selected location",
    ).add_to(m)

    Draw(
        export=False,
        draw_options={
            "polyline": False,
            "rectangle": False,
            "circle": False,
            "circlemarker": False,
            "marker": False,
            "polygon": {
                "shapeOptions": {
                    "color": "#00e05a",
                    "fillColor": "#00e05a",
                    "fillOpacity": 0.15,
                    "weight": 2,
                },
                "allowIntersection": False,
            },
        },
        edit_options={"edit": True, "remove": True},
    ).add_to(m)

    # Re-add previously drawn polygon so it persists across reruns
    if st.session_state.get("_drawn_geojson"):
        folium.GeoJson(
            st.session_state["_drawn_geojson"],
            style_function=lambda _: {
                "color": "#00e05a",
                "fillColor": "#00e05a",
                "fillOpacity": 0.15,
                "weight": 2,
            },
        ).add_to(m)

    map_data = st_folium(m, height=300, width=None, returned_objects=["last_active_drawing"])

    # ── Process drawn polygon ───────────────────────────────
    drawing = map_data.get("last_active_drawing") if map_data else None
    if drawing and drawing.get("geometry", {}).get("type") == "Polygon":
        coords = drawing["geometry"]["coordinates"][0]
        area = _polygon_area_m2(coords)
        centroid_lat, centroid_lon = _polygon_centroid(coords)

        st.session_state["_drawn_area_m2"] = area
        st.session_state["_drawn_lat"] = centroid_lat
        st.session_state["_drawn_lon"] = centroid_lon
        st.session_state["_drawn_geojson"] = drawing
        st.session_state["_geo_lat"] = centroid_lat
        st.session_state["_geo_lon"] = centroid_lon

    if st.session_state.get("_drawn_area_m2"):
        area_m2 = st.session_state["_drawn_area_m2"]
        area_ha = area_m2 / 10_000
        st.success(
            f'{t("polygon_area_detected", lang)}: '
            f"{area_m2:,.0f} m\u00b2 ({area_ha:,.2f} ha)"
        )

    st.caption("\u2190 " + t("map_instructions", lang))

    # ── Auto-detect site properties ───────────────────────────
    if st.button(t("auto_detect_btn", lang), use_container_width=True):
        with st.spinner(t("detecting_properties", lang)):
            grid_dist = _detect_grid_distance(latitude, longitude)
            terrain_type = _detect_terrain(latitude, longitude, country)

        parts: list[str] = []
        used_fallback = False

        if grid_dist is not None:
            st.session_state["_auto_grid_km"] = grid_dist
            parts.append(f"Grid distance: {grid_dist:.1f} km")
        else:
            st.warning(t("detection_grid_fail", lang))

        if terrain_type:
            st.session_state["_auto_terrain"] = terrain_type
            # Check if we used the country fallback (API failure)
            if terrain_type == TERRAIN_COUNTRY_FALLBACK.get(country):
                used_fallback = True
            parts.append(f"Terrain: {terrain_type}")

        if used_fallback:
            st.warning(t("detection_terrain_fail", lang))
        if parts:
            st.success(f'{t("detection_success", lang)}: {" | ".join(parts)}')
            st.rerun()

    # ══════════════════════════════════════════════════════════
    # SECTION B — Site Details
    # ══════════════════════════════════════════════════════════
    st.markdown(section_header_html(t("details", lang)), unsafe_allow_html=True)

    site_type_labels = {
        t("ground_parcel", lang): "ground_parcel",
        t("commercial_rooftop", lang): "commercial_rooftop",
        t("parking_structure", lang): "parking_structure",
    }
    site_type_keys = list(site_type_labels.keys())
    preq_site = st.session_state.get("_preq_site_type", "")
    site_type_default_idx = 0
    if preq_site:
        for i, v in enumerate(site_type_labels.values()):
            if v == preq_site:
                site_type_default_idx = i
                break
    site_label = st.selectbox(
        t("site_type", lang), site_type_keys, index=site_type_default_idx,
    )
    site_type = site_type_labels[site_label]

    # ── Adaptive fields per site type ─────────────────────
    parcel_size_ha = 0.0
    usable_m2 = 0.0
    terrain = "flat"
    land_status = "agricultural"
    grid_distance_km = 5.0

    # Default from drawn polygon (converted to ha for ground, m² for rooftop)
    drawn_area = st.session_state.get("_drawn_area_m2")

    if site_type == "ground_parcel":
        d1, d2 = st.columns(2)
        with d1:
            parcel_size_ha = st.number_input(
                t("parcel_size", lang), min_value=0.1, max_value=500.0,
                value=round(drawn_area / 10_000, 1) if drawn_area else 5.0,
                step=0.5,
            )
            terrain_options = ["flat", "gentle_slope", "steep_slope", "hilly", "mountainous"]
            auto_terrain = st.session_state.get("_auto_terrain")
            terrain_idx = terrain_options.index(auto_terrain) if auto_terrain in terrain_options else 0
            terrain = st.selectbox(
                t("terrain", lang),
                terrain_options,
                index=terrain_idx,
            )
        with d2:
            land_status = st.selectbox(
                t("land_status", lang),
                ["agricultural", "industrial", "unused", "unknown",
                 "wetland", "protected", "flood_zone"],
            )
            auto_grid = st.session_state.get("_auto_grid_km")
            grid_distance_km = st.slider(
                t("grid_distance", lang), 0.0, 50.0,
                min(auto_grid, 50.0) if auto_grid is not None else 5.0,
                0.5,
            )
    else:
        # Rooftop / Parking — ask for usable m², skip terrain
        d1, d2 = st.columns(2)
        with d1:
            usable_m2 = st.number_input(
                t("usable_area", lang), min_value=10.0, max_value=50000.0,
                value=round(drawn_area, 0) if drawn_area else 500.0,
                step=50.0,
            )
        with d2:
            auto_grid_r = st.session_state.get("_auto_grid_km")
            grid_distance_km = st.slider(
                t("grid_distance", lang), 0.0, 20.0,
                min(auto_grid_r, 20.0) if auto_grid_r is not None else 2.0,
                0.5,
            )
        land_status = "commercial"

    # ── Climate Data ──────────────────────────────────────
    st.markdown('<div style="margin-top: 0.5rem;"></div>', unsafe_allow_html=True)
    st.markdown(nasa_card_header_html(t("climate_data", lang)), unsafe_allow_html=True)

    if st.button(t("fetch_solar_data", lang), use_container_width=True):
        with st.spinner(t("fetching_data", lang)):
            nasa_data = _fetch_nasa_power(latitude, longitude)
        if nasa_data and nasa_data.get("ghi") is not None:
            st.session_state["nasa_data"] = nasa_data
            st.success(t("solar_data_loaded", lang))
        else:
            st.warning(t("solar_data_error", lang))

    nasa = st.session_state.get("nasa_data", {})
    st.caption(t("climate_manual_note", lang))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        ghi = st.number_input(
            t("ghi_label", lang), min_value=0.0, max_value=8.0,
            value=float(nasa.get("ghi", 0.0)), step=0.1,
            format="%.2f",
        )
    with c2:
        dni = st.number_input(
            t("dni_label", lang), min_value=0.0, max_value=8.0,
            value=float(nasa.get("dni", 0.0)), step=0.1,
            format="%.2f",
        )
    with c3:
        temperature = st.number_input(
            t("temperature_label", lang), min_value=-10.0, max_value=50.0,
            value=float(nasa.get("temperature", 18.0)), step=0.5,
            format="%.1f",
        )
    with c4:
        humidity = st.number_input(
            t("humidity_label", lang), min_value=0.0, max_value=100.0,
            value=float(nasa.get("humidity", 65.0)), step=1.0,
            format="%.1f",
        )

    c5, c6, c7, _ = st.columns(4)
    with c5:
        wind_speed = st.number_input(
            t("wind_speed_label", lang), min_value=0.0, max_value=30.0,
            value=float(nasa.get("wind_speed", 3.0)), step=0.1,
            format="%.2f",
        )
    with c6:
        precipitation = st.number_input(
            t("precipitation_label", lang), min_value=0.0, max_value=30.0,
            value=float(nasa.get("precipitation", 2.0)), step=0.1,
            format="%.2f",
        )
    with c7:
        cloud_cover = st.number_input(
            t("cloud_cover_label", lang), min_value=0.0, max_value=100.0,
            value=float(nasa.get("cloud_cover", 40.0)), step=1.0,
            format="%.1f",
        )

    return {
        "country": country,
        "latitude": latitude,
        "longitude": longitude,
        "site_type": site_type,
        "parcel_size_ha": parcel_size_ha,
        "usable_m2": usable_m2,
        "terrain": terrain,
        "land_status": land_status,
        "grid_distance_km": grid_distance_km,
        "ghi": ghi if ghi > 0 else None,
        "dni": dni if dni > 0 else None,
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "precipitation": precipitation,
        "cloud_cover": cloud_cover,
    }
