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
    """Render assessment results with Mediterranean report styling."""

    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)

    viability = result["viability_class"]
    is_residential = result.get("site_type") == "residential_roof"

    # ── Not Viable (eliminated by gate) ─────────────────────
    if viability == "Not Viable":
        card = not_viable_card_html(
            gate=result.get("eliminated_by", ""),
            reason=result.get("reason", ""),
        )
        _dark_html(card, height=160)
        if result.get("redirect_to"):
            st.info(f"💡 {t('redirect', lang)}: {result['redirect_to']}")
        return

    # ── SVG Gauge — centered at top ─────────────────────────
    _dark_html(svg_gauge_html(result["score"], viability), height=200)

    # ── Primary metrics ─────────────────────────────────────
    if is_residential:
        # Row 1: System Size · Annual Production · Annual Savings
        c1, c2, c3 = st.columns(3)
        with c1:
            _dark_html(
                metric_card_html(
                    t("system_size", lang),
                    f'{result.get("kwp", 0):.2f} kWp',
                    icon="🔋",
                ),
                height=120,
            )
        with c2:
            _dark_html(
                metric_card_html(
                    t("est_annual_production", lang),
                    f'{result["annual_kwh"]:,.0f}',
                    icon="⚡",
                ),
                height=120,
            )
        with c3:
            _dark_html(
                metric_card_html(
                    t("annual_savings", lang),
                    f'€{result["revenue_eur"]:,.0f}',
                    icon="💶",
                ),
                height=120,
            )
        # Row 2: Payback Period · 25-Year Net Savings
        st.markdown('<div style="margin-top: 0.8rem;"></div>', unsafe_allow_html=True)
        c4, c5 = st.columns(2)
        with c4:
            _dark_html(
                metric_card_html(
                    t("payback_period", lang),
                    f'{result.get("payback_years", 0):.1f} {t("years_unit", lang)}',
                    icon="⏱",
                ),
                height=120,
            )
        with c5:
            _dark_html(
                metric_card_html(
                    t("net_savings_25yr", lang),
                    f'€{result.get("net_savings_25yr_eur", 0):,.0f}',
                    icon="📈",
                ),
                height=120,
            )
    else:
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
    if is_residential:
        gates = [
            t("roof_gate_g1", lang),
            t("roof_gate_g2", lang),
            t("roof_gate_g3", lang),
            t("roof_gate_g4", lang),
        ]
    else:
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
            'background:linear-gradient(135deg, #a94f31 0%, #c66f49 100%);'
            'color:#fff9ef;'
            'text-align:center;'
            'padding:1.2rem;'
            'border-radius:12px;'
            'font-size:1.05rem;'
            'font-weight:700;'
            'cursor:pointer;'
            'box-shadow:0 14px 30px rgba(185,95,59,0.20);'
            'transition:box-shadow 0.2s ease;'
            '">'
            '\U0001f517 Get a Quote \u2014 Connect with Regional Installer'
            '</div></a>',
            height=70,
        )

    # \u2500\u2500 Local incentives note (residential, small muted text) \u2500
    if is_residential:
        st.markdown(
            f'<div style="margin-top:1.2rem; color:#8c8174; '
            f'font-size:0.85rem; line-height:1.5; text-align:center; '
            f'opacity:0.85; padding:0 0.5rem;">'
            f'{t("local_incentives_note", lang)}'
            f'</div>',
            unsafe_allow_html=True,
        )
