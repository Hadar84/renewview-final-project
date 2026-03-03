"""Results Display Component — shows viability verdict, score, kWh, € revenue."""

import pandas as pd
import streamlit as st

from renewview.frontend.assets.i18n import t
from renewview.frontend.assets.styles import (
    gate_pass_html,
    metric_card_html,
    not_viable_card_html,
    svg_gauge_html,
)


def render_results(result: dict, lang: str = "EN") -> None:
    """Render assessment results with dark solar-tech styling."""

    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)

    viability = result["viability_class"]

    # ── Not Viable (eliminated by gate) ─────────────────────
    if viability == "Not Viable":
        st.markdown(
            not_viable_card_html(
                gate=result.get("eliminated_by", ""),
                reason=result.get("reason", ""),
                redirect=result.get("redirect_to"),
            ),
            unsafe_allow_html=True,
        )
        return

    # ── SVG Gauge — centered at top ─────────────────────────
    st.markdown(
        svg_gauge_html(result["score"], viability),
        unsafe_allow_html=True,
    )

    # ── Primary metrics — kWh + Revenue ─────────────────────
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(
            metric_card_html(
                t("annual_kwh", lang),
                f'{result["annual_kwh"]:,.0f}',
                icon="⚡",
            ),
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            metric_card_html(
                t("annual_revenue", lang),
                f'€{result["revenue_eur"]:,.0f}',
                icon="💶",
            ),
            unsafe_allow_html=True,
        )

    # ── Secondary metrics — GHI + Prediction Source ─────────
    st.markdown('<div style="margin-top: 0.8rem;"></div>', unsafe_allow_html=True)
    if result.get("ghi_used"):
        g1, g2 = st.columns(2)
        with g1:
            st.markdown(
                metric_card_html(
                    "GHI USED",
                    f'{result["ghi_used"]:.2f} kWh/m²/day',
                    icon="☀️",
                ),
                unsafe_allow_html=True,
            )
        with g2:
            model_label = "ML MODEL" if result.get("used_model") else "HEURISTIC"
            model_icon = "🤖" if result.get("used_model") else "📐"
            st.markdown(
                metric_card_html(
                    "PREDICTION SOURCE",
                    model_label,
                    icon=model_icon,
                ),
                unsafe_allow_html=True,
            )

    # ── Map ─────────────────────────────────────────────────
    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
    lat = st.session_state.get("_last_lat")
    lon = st.session_state.get("_last_lon")
    if lat is not None and lon is not None:
        st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}), zoom=6)

    # ── Gate pass details (expandable) ──────────────────────
    with st.expander(t("gate_detail_g1", lang).split(":")[0].strip() + " — Pre-screening Gates", expanded=False):
        gates = [
            t("gate_detail_g1", lang),
            t("gate_detail_g2", lang),
            t("gate_detail_g3", lang),
            t("gate_detail_g4", lang),
        ]
        st.markdown(gate_pass_html(gates), unsafe_allow_html=True)

    # Flags
    if result.get("flags"):
        for flag in result["flags"]:
            if flag == "small_commercial":
                st.info("📌 Small commercial parcel (<5 ha) — limited scale")

    # ── Installer CTA (Medium / High only) ──────────────────
    if viability in ("High", "Medium"):
        st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
        st.success(t("connect_installer", lang))
        st.link_button(
            "Find Installers → SolarPower Europe",
            "https://www.solarpowereurope.org/",
            use_container_width=True,
        )

    # ── Disclaimer ──────────────────────────────────────────
    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
    st.caption(t("disclaimer", lang))
