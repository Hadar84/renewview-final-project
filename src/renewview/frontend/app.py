"""RenewView — Streamlit Frontend.

Landowner-facing multi-language interface for solar viability assessment.
This file is the entry point: `streamlit run src/renewview/frontend/app.py`
"""

import streamlit as st

from renewview.backend.services.prediction_service import PredictionService
from renewview.frontend.assets.i18n import t
from renewview.frontend.assets.styles import THEME_CSS, welcome_hero_html
from renewview.frontend.components.results_display import render_results
from renewview.frontend.components.site_inputs import render_site_inputs

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="RenewView — Solar Viability",
    page_icon="☀️",
    layout="wide",
)

# ── Inject Theme CSS ────────────────────────────────────────
st.markdown(THEME_CSS, unsafe_allow_html=True)

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

# ── Step State ───────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = 1

# ── Step 1 — Welcome Hero ───────────────────────────────────
if st.session_state.step == 1:
    st.markdown(
        welcome_hero_html(
            title="☀️ RenewView",
            subtitle=t("subtitle", lang),
            intro=t("intro", lang),
        ),
        unsafe_allow_html=True,
    )
    if st.button(t("start_assessment", lang), type="primary", use_container_width=True):
        st.session_state.step = 2
        st.rerun()

    # ── Footer ──────────────────────────────────────────────
    st.divider()
    st.caption(t("disclaimer", lang))

# ── Step 2 — Input Form + About ─────────────────────────────
elif st.session_state.step == 2:
    if st.button("← " + t("back_to_home", lang)):
        st.session_state.step = 1
        st.rerun()

    tab_assess, tab_about = st.tabs([t("tab_assessment", lang), t("tab_about", lang)])

    with tab_assess:
        inputs = render_site_inputs(lang)

        st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)

        if st.button(t("run_assessment", lang), type="primary", use_container_width=True):
            service = PredictionService()

            if not service.load_model():
                st.warning(t("model_not_ready", lang))

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

            st.session_state["_result"] = result
            st.session_state.step = 3
            st.rerun()

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

    st.divider()
    st.caption(t("disclaimer", lang))

# ── Step 3 — Results ─────────────────────────────────────────
elif st.session_state.step == 3:
    if st.button("← " + t("back_to_inputs", lang)):
        st.session_state.step = 2
        st.rerun()

    # Step indicator pill
    st.markdown(
        '<div style="text-align:center; margin-bottom:1rem;">'
        '<span style="background:rgba(0,224,90,0.1); color:#00e05a; '
        'padding:0.3rem 1rem; border-radius:20px; font-size:0.72rem; '
        'font-weight:700; letter-spacing:0.1em; text-transform:uppercase; '
        'border:1px solid rgba(0,224,90,0.25);">'
        'STEP 3 OF 3 — Feasibility Report</span></div>',
        unsafe_allow_html=True,
    )

    result = st.session_state.get("_result")
    if result:
        render_results(result, lang)
    else:
        st.warning("No results found. Please run an assessment first.")
        if st.button(t("start_assessment", lang), type="primary"):
            st.session_state.step = 2
            st.rerun()

    st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)
    if st.button(t("new_assessment", lang), type="primary", use_container_width=True):
        st.session_state.step = 1
        st.session_state.pop("_result", None)
        st.rerun()

    st.divider()
    st.caption(t("disclaimer", lang))
