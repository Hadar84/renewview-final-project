"""About page — project info, architecture, ethics."""

import streamlit as st


def render_about():
    st.title("About RenewView")

    st.markdown("""
    ## Problem
    The EU targets 700 GW solar by 2030, but landowners in Southern Europe have
    no data-driven way to assess land viability before hiring consultants.

    ## Solution
    A CrewAI-powered pre-screening decision gate that predicts solar feasibility,
    classifies risk tiers, estimates energy output, and connects viable sites to
    regional installers.

    ## Architecture
    - **Crew 1 — Land Intelligence:** 4 agents (ingestion, cleaning, EDA, contract)
    - **Validation Gate:** Schema check before ML
    - **Crew 2 — Prediction:** 4 agents (validator, features, training, evaluation)
    - **Elimination Gates:** G1–G4 hard filters before classification
    - **Frontend:** Multi-language Streamlit (EN/PT/ES/EL)

    ## Ethics & Limitations
    - **Regional bias:** More training data available for Spain and Italy
    - **False positives:** Marginal sites may receive optimistic assessments
    - **Land conversion:** Solar development on agricultural land has trade-offs
    - **Preliminary only:** Always consult a qualified professional

    ## Stack
    CrewAI Flow, Python, Pandas, Scikit-Learn, Matplotlib, Seaborn, Streamlit

    ## Course
    AI Development & Collaboration — Hebrew University 2026 — Dr. Zvi Ben Ami
    """)


if __name__ == "__main__":
    render_about()
