"""Site Inputs Component — adaptive forms per site type (proposal Section 4).

Ground parcels: terrain, grid distance, wetland status, parcel size (ha).
Rooftop/Parking: usable m², skip terrain.
"""

import streamlit as st

from renewview.frontend.assets.i18n import t


def render_site_inputs(lang: str = "EN") -> dict:
    """Render adaptive input form based on site type. Returns input dict."""

    col1, col2 = st.columns(2)

    with col1:
        st.header(t("location", lang))

        country = st.selectbox(
            t("country", lang),
            ["Portugal", "Spain", "Greece", "Italy"],
        )

        latitude = st.number_input(
            t("latitude", lang), min_value=34.0, max_value=44.0,
            value=38.7, step=0.1,
        )
        longitude = st.number_input(
            t("longitude", lang), min_value=-10.0, max_value=30.0,
            value=-9.1, step=0.1,
        )

    with col2:
        st.header(t("details", lang))

        site_type_labels = {
            t("ground_parcel", lang): "ground_parcel",
            t("commercial_rooftop", lang): "commercial_rooftop",
            t("parking_structure", lang): "parking_structure",
        }
        site_label = st.selectbox(t("site_type", lang), list(site_type_labels.keys()))
        site_type = site_type_labels[site_label]

        # ── Adaptive fields per site type ───────────────────
        parcel_size_ha = 0.0
        usable_m2 = 0.0
        terrain = "flat"
        land_status = "agricultural"
        grid_distance_km = 5.0

        if site_type == "ground_parcel":
            parcel_size_ha = st.number_input(
                t("parcel_size", lang), min_value=0.1, max_value=500.0,
                value=5.0, step=0.5,
            )
            terrain = st.selectbox(
                t("terrain", lang),
                ["flat", "gentle_slope", "steep_slope", "hilly"],
            )
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
            usable_m2 = st.number_input(
                t("usable_area", lang), min_value=10.0, max_value=50000.0,
                value=500.0, step=50.0,
            )
            grid_distance_km = st.slider(
                t("grid_distance", lang), 0.0, 20.0, 2.0, 0.5,
            )
            land_status = "commercial"  # no land exclusion for rooftops

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
    }
