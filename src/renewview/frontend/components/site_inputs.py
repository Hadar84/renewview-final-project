"""Site Inputs Component — adaptive forms per site type (proposal Section 4).

Ground parcels: terrain, grid distance, wetland status, parcel size (ha).
Rooftop/Parking: usable m², skip terrain.
Includes optional live NASA POWER data fetch.
"""

import json

import pandas as pd
import requests
import streamlit as st

from renewview.config.settings import NASA_POWER_PARAMS
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


def render_site_inputs(lang: str = "EN") -> dict:
    """Render adaptive input form based on site type. Returns input dict."""

    # ══════════════════════════════════════════════════════════
    # SECTION A — Location
    # ══════════════════════════════════════════════════════════
    st.markdown(section_header_html(t("location", lang)), unsafe_allow_html=True)

    loc1, loc2, loc3 = st.columns(3)
    with loc1:
        country = st.selectbox(
            t("country", lang),
            ["Portugal", "Spain", "Greece", "Italy"],
        )
    with loc2:
        latitude = st.number_input(
            t("latitude", lang), min_value=34.0, max_value=44.0,
            value=38.7, step=0.1,
        )
    with loc3:
        longitude = st.number_input(
            t("longitude", lang), min_value=-10.0, max_value=30.0,
            value=-9.1, step=0.1,
        )

    # Map preview — directly below location inputs
    st.caption(t("map_preview", lang))
    st.map(pd.DataFrame({"lat": [latitude], "lon": [longitude]}), zoom=11, height=220)

    # ══════════════════════════════════════════════════════════
    # SECTION B — Site Details
    # ══════════════════════════════════════════════════════════
    st.markdown(section_header_html(t("details", lang)), unsafe_allow_html=True)

    site_type_labels = {
        t("ground_parcel", lang): "ground_parcel",
        t("commercial_rooftop", lang): "commercial_rooftop",
        t("parking_structure", lang): "parking_structure",
    }
    site_label = st.selectbox(t("site_type", lang), list(site_type_labels.keys()))
    site_type = site_type_labels[site_label]

    # ── Adaptive fields per site type ─────────────────────
    parcel_size_ha = 0.0
    usable_m2 = 0.0
    terrain = "flat"
    land_status = "agricultural"
    grid_distance_km = 5.0

    if site_type == "ground_parcel":
        d1, d2 = st.columns(2)
        with d1:
            parcel_size_ha = st.number_input(
                t("parcel_size", lang), min_value=0.1, max_value=500.0,
                value=5.0, step=0.5,
            )
            terrain = st.selectbox(
                t("terrain", lang),
                ["flat", "gentle_slope", "steep_slope", "hilly"],
            )
        with d2:
            land_status = st.selectbox(
                t("land_status", lang),
                ["agricultural", "industrial", "unused", "wetland",
                 "protected", "flood_zone"],
            )
            grid_distance_km = st.slider(
                t("grid_distance", lang), 0.0, 50.0, 5.0, 0.5,
            )
    else:
        # Rooftop / Parking — ask for usable m², skip terrain
        d1, d2 = st.columns(2)
        with d1:
            usable_m2 = st.number_input(
                t("usable_area", lang), min_value=10.0, max_value=50000.0,
                value=500.0, step=50.0,
            )
        with d2:
            grid_distance_km = st.slider(
                t("grid_distance", lang), 0.0, 20.0, 2.0, 0.5,
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
