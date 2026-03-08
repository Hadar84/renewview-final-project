"""Results Display Component — shows viability verdict, score, kWh, € revenue."""

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

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

    # ── Gate pass details ──────────────────────────────────
    gates = [
        t("gate_detail_g1", lang),
        t("gate_detail_g2", lang),
        t("gate_detail_g3", lang),
        t("gate_detail_g4", lang),
    ]
    components.html(gate_pass_html(gates), height=220)

    # Flags
    if result.get("flags"):
        for flag in result["flags"]:
            if flag == "small_commercial":
                st.info("📌 Small commercial parcel (<5 ha) — limited scale")

    # ── Installer CTA (Medium / High only) ──────────────────
    if viability in ("High", "Medium"):
        st.markdown(
            '<a href="https://www.solarpowereurope.org/" target="_blank" '
            'style="text-decoration:none; display:block;">'
            '<div style="'
            'background:linear-gradient(135deg, #00c04a 0%, #00e05a 100%);'
            'color:#0a1a0f;'
            'text-align:center;'
            'padding:1.2rem;'
            'border-radius:12px;'
            'font-size:1.05rem;'
            'font-weight:700;'
            'margin-top:1.2rem;'
            'cursor:pointer;'
            'box-shadow:0 0 20px rgba(0,224,90,0.2);'
            'transition:box-shadow 0.2s ease;'
            '">'
            '🔗 Get a Quote — Connect with Regional Installer'
            '</div></a>',
            unsafe_allow_html=True,
        )
