"""Results Display Component — shows viability verdict, score, kWh, € revenue."""

import pandas as pd
import streamlit as st

from renewview.frontend.assets.i18n import t


EMOJI_MAP = {"High": "✅", "Medium": "⚠️", "Low": "🔻", "Not Viable": "❌"}


def render_results(result: dict, lang: str = "EN") -> None:
    """Render assessment results."""

    st.header(t("results", lang))

    viability = result["viability_class"]
    emoji = EMOJI_MAP.get(viability, "❓")

    # ── Not Viable (eliminated by gate) ─────────────────────
    if viability == "Not Viable":
        st.error(f"{emoji} {t('not_viable_msg', lang)}")

        if result.get("eliminated_by"):
            st.markdown(f"**{t('eliminated_by', lang)}:** {result['eliminated_by']}")
        if result.get("reason"):
            st.markdown(f"**{t('reason', lang)}:** {result['reason']}")
        if result.get("redirect_to"):
            st.info(f"**{t('redirect', lang)}:** {result['redirect_to']}")
        return

    # ── Viable results ──────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(t("viability", lang), f"{emoji} {viability}")
    col2.metric(t("score", lang), f"{result['score']:.0f}%")
    col3.metric(t("annual_kwh", lang), f"{result['annual_kwh']:,.0f}")
    col4.metric(t("annual_revenue", lang), f"€{result['revenue_eur']:,.0f}")

    # ── Map ─────────────────────────────────────────────────
    if result.get("ghi_used"):
        lat = st.session_state.get("_last_lat")
        lon = st.session_state.get("_last_lon")
        if lat is not None and lon is not None:
            st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}), zoom=6)

    # ── Gate pass details ───────────────────────────────────
    with st.expander(f"✅ {t('gates_passed', lang)}", expanded=False):
        st.markdown(f"- {t('gate_detail_g1', lang)}")
        st.markdown(f"- {t('gate_detail_g2', lang)}")
        st.markdown(f"- {t('gate_detail_g3', lang)}")
        st.markdown(f"- {t('gate_detail_g4', lang)}")

    # Flags
    if result.get("flags"):
        for flag in result["flags"]:
            if flag == "small_commercial":
                st.info("📌 Small commercial parcel (<5 ha) — limited scale")

    # Model indicator
    if result.get("used_model"):
        st.caption("🤖 Prediction from trained ML model")
    else:
        st.caption("📐 Heuristic estimate — run pipeline for ML predictions")

    # Connect with installer (Medium / High only)
    if viability in ("High", "Medium"):
        st.divider()
        st.success(t("connect_installer", lang))
        st.link_button(
            "Find Installers → SolarPower Europe",
            "https://www.solarpowereurope.org/",
        )
