"""Results Display Component — shows viability verdict, score, kWh, € revenue."""

import streamlit as st
import streamlit.components.v1 as components

from renewview.frontend.assets.i18n import t
from renewview.frontend.assets.styles import (
    gate_pass_html,
    metric_card_html,
    not_viable_card_html,
    svg_gauge_html,
)


_IFRAME_RESET = '<style>body{margin:0;background:transparent;}</style>'


def _dark_html(html: str, height: int) -> None:
    """Render HTML via components.html with transparent iframe background."""
    components.html(_IFRAME_RESET + html, height=height)


def render_results(result: dict, lang: str = "EN") -> None:
    """Render assessment results with dark solar-tech styling."""

    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)

    viability = result["viability_class"]

    # ── Not Viable (eliminated by gate) ─────────────────────
    if viability == "Not Viable":
        card = not_viable_card_html(
            gate=result.get("eliminated_by", ""),
            reason=result.get("reason", ""),
            redirect=result.get("redirect_to"),
        )
        _dark_html(card, height=240 if result.get("redirect_to") else 160)
        return

    # ── SVG Gauge — centered at top ─────────────────────────
    _dark_html(svg_gauge_html(result["score"], viability), height=200)

    # ── Primary metrics — kWh + Revenue ─────────────────────
    m1, m2 = st.columns(2)
    with m1:
        _dark_html(
            metric_card_html(
                t("annual_kwh", lang),
                f'{result["annual_kwh"]:,.0f}',
                icon="⚡",
            ),
            height=120,
        )
    with m2:
        _dark_html(
            metric_card_html(
                t("annual_revenue", lang),
                f'€{result["revenue_eur"]:,.0f}',
                icon="💶",
            ),
            height=120,
        )

    # ── Secondary metrics — GHI + Prediction Source ─────────
    st.markdown('<div style="margin-top: 0.8rem;"></div>', unsafe_allow_html=True)
    if result.get("ghi_used"):
        g1, g2 = st.columns(2)
        with g1:
            _dark_html(
                metric_card_html(
                    "GHI USED",
                    f'{result["ghi_used"]:.2f} kWh/m²/day',
                    icon="☀️",
                ),
                height=120,
            )
        with g2:
            model_label = "ML MODEL" if result.get("used_model") else "HEURISTIC"
            model_icon = "🤖" if result.get("used_model") else "📐"
            _dark_html(
                metric_card_html(
                    "PREDICTION SOURCE",
                    model_label,
                    icon=model_icon,
                ),
                height=120,
            )

    # ── Gate pass details ──────────────────────────────────
    gates = [
        t("gate_detail_g1", lang),
        t("gate_detail_g2", lang),
        t("gate_detail_g3", lang),
        t("gate_detail_g4", lang),
    ]
    _dark_html(gate_pass_html(gates), height=220)

    # Flags
    if result.get("flags"):
        for flag in result["flags"]:
            if flag == "small_commercial":
                st.info("📌 Small commercial parcel (<5 ha) — limited scale")

    # ── Installer CTA (Medium / High only) ──────────────────
    if viability in ("High", "Medium"):
        _dark_html(
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
            'cursor:pointer;'
            'box-shadow:0 0 20px rgba(0,224,90,0.2);'
            'transition:box-shadow 0.2s ease;'
            '">'
            '\U0001f517 Get a Quote \u2014 Connect with Regional Installer'
            '</div></a>',
            height=70,
        )
