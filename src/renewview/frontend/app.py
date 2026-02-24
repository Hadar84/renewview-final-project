"""RenewView — Streamlit Frontend.

Landowner-facing multi-language interface for solar viability assessment.
This file is the entry point: `streamlit run src/renewview/frontend/app.py`
"""

import streamlit as st

from renewview.backend.services.prediction_service import PredictionService
from renewview.frontend.assets.i18n import t
from renewview.frontend.components.site_inputs import render_site_inputs
from renewview.frontend.components.results_display import render_results

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

# ── Header ──────────────────────────────────────────────────
st.title(t("title", lang))
st.subheader(t("subtitle", lang))
st.markdown(t("intro", lang))
st.divider()

# ── Sidebar ─────────────────────────────────────────────────
with st.sidebar:
    st.header(t("about", lang))
    st.markdown(
        """
        **RenewView** uses multi-agent AI to assess solar viability.

        **Pipeline:**
        1. Elimination gates (protected land, grid distance, irradiance)
        2. ML classification (Random Forest / Gradient Boosting)
        3. Energy & revenue estimation

        **Data:** NASA POWER API + OpenStreetMap

        **Regions:** Portugal, Spain, Greece, Italy
        """
    )
    st.divider()
    st.header(t("ethics_title", lang))
    st.markdown(
        """
        - Bias toward data-rich regions (Spain, Italy have more data)
        - False positive risk on marginal sites
        - Agricultural land conversion trade-offs
        - Always consult a professional before investing
        """
    )
    st.divider()
    st.caption("Built with CrewAI, Scikit-Learn & Streamlit")
    st.caption("Final Project — AI Development Course 2026")

# ── Input Form ──────────────────────────────────────────────
inputs = render_site_inputs(lang)

st.divider()

# ── Assessment ──────────────────────────────────────────────
if st.button(t("run_assessment", lang), type="primary", use_container_width=True):
    service = PredictionService()

    if not service.load_model():
        st.warning(t("model_not_ready", lang))

    with st.spinner("Analyzing site..."):
        result = service.assess_site(
            latitude=inputs["latitude"],
            longitude=inputs["longitude"],
            country=inputs["country"],
            site_type=inputs["site_type"],
            parcel_size_ha=inputs["parcel_size_ha"],
            grid_distance_km=inputs["grid_distance_km"],
            land_status=inputs["land_status"],
            usable_m2=inputs["usable_m2"] if inputs["usable_m2"] > 0 else None,
        )

    render_results(result, lang)

# ── Footer ──────────────────────────────────────────────────
st.divider()
st.caption(t("disclaimer", lang))
