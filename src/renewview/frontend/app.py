"""RenewView — Streamlit Frontend.

Landowner-facing multi-language interface for solar viability assessment.
This file is the entry point: `streamlit run src/renewview/frontend/app.py`
"""

import streamlit as st
import streamlit.components.v1 as components

from renewview.backend.services.prediction_service import PredictionService
from renewview.frontend.assets.i18n import t
from renewview.frontend.assets.styles import THEME_CSS, section_header_html, welcome_hero_html
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
    st.markdown('<div class="sidebar-kicker">RenewView</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### " + t("about", lang))
        st.markdown(t("sidebar_about_text", lang))
    with st.container(border=True):
        st.markdown("### " + t("ethics_title", lang))
        st.markdown(t("sidebar_ethics_text", lang))

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

    # ── Pre-qualification card ─────────────────────────────
    st.markdown('<div style="margin-top:1.25rem;"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(section_header_html(t("prequalify_heading", lang)), unsafe_allow_html=True)
        st.markdown(
            f'<p class="precheck-note">{t("precheck_note", lang)}</p>',
            unsafe_allow_html=True,
        )

        land_size_options = [
            t("land_size_option_small", lang),
            t("land_size_option_medium", lang),
            t("land_size_option_large", lang),
            t("land_size_option_xlarge", lang),
        ]
        land_size = st.radio(
            t("land_size_question", lang),
            land_size_options,
            index=1,
            key="_preq_land_size_radio",
        )

        if land_size == land_size_options[0]:
            st.info(t("land_size_rooftop_hint", lang))

        name_col, email_col = st.columns(2)
        with name_col:
            lead_name = st.text_input(t("lead_name", lang), key="_preq_name")
        with email_col:
            lead_email = st.text_input(t("lead_email", lang), key="_preq_email")
        st.caption(t("lead_optional_note", lang))

        components.html(
            """
            <script>
            setTimeout(function() {
                const doc = window.parent.document;
                const inputs = doc.querySelectorAll('input[aria-label]');
                inputs.forEach(function(el) {
                    const label = (el.getAttribute('aria-label') || '').toLowerCase();
                    if (label.includes('email') || label.includes('name')) {
                        el.setAttribute('autocomplete', 'new-password');
                    }
                });
            }, 500);
            </script>
            """,
            height=0,
        )

        st.markdown('<div style="margin-top:0.85rem;"></div>', unsafe_allow_html=True)
        if st.button(t("start_assessment", lang), type="primary", use_container_width=True):
            st.session_state["_preq_land_size"] = land_size
            if land_size == land_size_options[0]:
                st.session_state["_preq_site_type"] = "commercial_rooftop"
            else:
                st.session_state.pop("_preq_site_type", None)
            st.session_state.step = 2
            st.rerun()

    st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
    st.caption(t("disclaimer", lang))

# ── Step 2 — Input Form + About ─────────────────────────────
elif st.session_state.step == 2:
    if st.button("← " + t("back_to_home", lang)):
        st.session_state.step = 1
        st.rerun()

    st.markdown(
        '<div style="text-align:center; margin-bottom:1rem;">'
        '<span style="background:#fff9ef; color:#8f5d34; '
        'padding:0.3rem 1rem; border-radius:20px; font-size:0.72rem; '
        'font-weight:700; letter-spacing:0.08em; text-transform:uppercase; '
        'border:1px solid rgba(143,93,52,0.22); '
        'box-shadow:0 8px 20px rgba(71,54,37,0.07);">'
        'STEP 2 OF 3 — Site Details</span></div>',
        unsafe_allow_html=True,
    )

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
                    roof_area_m2=inputs.get("roof_area_m2") or None,
                    orientation=inputs.get("orientation"),
                    shading=inputs.get("shading"),
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
        '<span style="background:#fff9ef; color:#8f5d34; '
        'padding:0.3rem 1rem; border-radius:20px; font-size:0.72rem; '
        'font-weight:700; letter-spacing:0.08em; text-transform:uppercase; '
        'border:1px solid rgba(143,93,52,0.22); '
        'box-shadow:0 8px 20px rgba(71,54,37,0.07);">'
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

    # ── Paid report CTA ─────────────────────────────────────
    if result:
        if result.get("viability_class") != "Not Viable":
            st.markdown(
                '<div style="margin-top:2rem; padding-top:1.25rem; '
                'border-top:1px solid rgba(93,73,55,0.13); text-align:center;">'
                '<p style="color:#453a31; font-size:1rem; line-height:1.5; '
                'margin:0 auto 0.9rem auto; max-width:620px;">'
                + t("cta_headline", lang) +
                '</p></div>',
                unsafe_allow_html=True,
            )
            st.link_button(
                t("cta_button", lang),
                "https://citrusstudio.lemonsqueezy.com/checkout/buy/4f7ec202-a6ac-4dd8-89d9-f98e1330b6a8",
                use_container_width=True,
            )
            st.markdown(
                '<p style="color:#8c8174; font-size:0.82rem; text-align:center; '
                'margin:0.6rem 0 0 0;">'
                + t("cta_trust", lang) +
                '</p>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="margin-top:2rem; padding:1.1rem 1rem; '
                'border-top:1px solid rgba(93,73,55,0.13); text-align:center;">'
                '<p style="color:#8c8174; font-size:0.9rem; line-height:1.5; '
                'margin:0 auto; max-width:620px;">'
                + t("cta_not_viable_note", lang) +
                '</p></div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)
    if st.button(t("new_assessment", lang), type="primary", use_container_width=True):
        st.session_state.step = 1
        for _key in ("_result", "_drawn_area_m2", "_drawn_lat", "_drawn_lon",
                      "_drawn_geojson", "_geo_lat", "_geo_lon", "_geo_display",
                      "_auto_grid_km", "_auto_terrain",
                      "_preq_land_size", "_preq_name", "_preq_email",
                      "_preq_site_type"):
            st.session_state.pop(_key, None)
        st.rerun()

    st.divider()
    st.caption(t("disclaimer", lang))
