"""RenewView — Streamlit Frontend.

Landowner-facing multi-language interface for solar viability assessment.
This file is the entry point: `streamlit run src/renewview/frontend/app.py`
"""

import streamlit as st

from renewview.backend.services.prediction_service import PredictionService
from renewview.frontend.assets.i18n import t
from renewview.frontend.components.results_display import render_results
from renewview.frontend.components.site_inputs import render_site_inputs

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="RenewView — Solar Viability",
    page_icon="☀️",
    layout="wide",
)

# ── Language Selector ───────────────────────────────────────
lang = st.sidebar.selectbox(
    "🌍 Language",
    ["EN", "PT", "ES", "EL"],
    format_func=lambda x: {"EN": "🇬🇧 English", "PT": "🇵🇹 Português",
                            "ES": "🇪🇸 Español", "EL": "🇬🇷 Ελληνικά"}[x],
)

# ── Sidebar ─────────────────────────────────────────────────
with st.sidebar:
    st.header(t("about", lang))
    st.markdown(t("sidebar_about_text", lang))
    st.divider()
    st.header(t("ethics_title", lang))
    st.markdown(t("sidebar_ethics_text", lang))
    st.divider()
    st.caption(t("sidebar_built_with", lang))
    st.caption(t("sidebar_course", lang))

# ── Header ──────────────────────────────────────────────────
st.title(t("title", lang))
st.subheader(t("subtitle", lang))
st.markdown(t("intro", lang))
st.divider()

# ── Tabs ────────────────────────────────────────────────────
tab_assess, tab_about = st.tabs([t("tab_assessment", lang), t("tab_about", lang)])

with tab_assess:
    # ── Input Form ──────────────────────────────────────────
    inputs = render_site_inputs(lang)

    st.divider()

    # ── Assessment ──────────────────────────────────────────
    if st.button(t("run_assessment", lang), type="primary", use_container_width=True):
        service = PredictionService()

        if not service.load_model():
            st.warning(t("model_not_ready", lang))

        # Store lat/lon for map rendering
        st.session_state["_last_lat"] = inputs["latitude"]
        st.session_state["_last_lon"] = inputs["longitude"]

        with st.spinner("Analyzing site..."):
            result = service.assess_site(
                latitude=inputs["latitude"],
                longitude=inputs["longitude"],
                country=inputs["country"],
                site_type=inputs["site_type"],
                parcel_size_ha=inputs["parcel_size_ha"],
                grid_distance_km=inputs["grid_distance_km"],
                land_status=inputs["land_status"],
                ghi=inputs["ghi"],
                dni=inputs["dni"],
                temperature=inputs["temperature"],
                humidity=inputs["humidity"],
                wind_speed=inputs["wind_speed"],
                precipitation=inputs["precipitation"],
                cloud_cover=inputs["cloud_cover"],
                usable_m2=inputs["usable_m2"] if inputs["usable_m2"] > 0 else None,
            )

        render_results(result, lang)

with tab_about:
    st.markdown(t("about_problem", lang))
    st.markdown(t("about_problem_text", lang))
    st.markdown(t("about_solution", lang))
    st.markdown(t("about_solution_text", lang))
    st.markdown(t("about_architecture", lang))
    st.markdown(t("about_architecture_text", lang))
    st.markdown(t("about_ethics", lang))
    st.markdown(t("about_ethics_text", lang))
    st.markdown(t("about_stack", lang))
    st.markdown(t("about_stack_text", lang))
    st.markdown(t("about_course", lang))
    st.markdown(t("about_course_text", lang))

# ── Footer ──────────────────────────────────────────────────
st.divider()
st.caption(t("disclaimer", lang))
