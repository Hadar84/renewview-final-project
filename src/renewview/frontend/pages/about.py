"""About page — project info, architecture, ethics.

Integrated into the main app via tabs. Can also run standalone.
"""

import streamlit as st

from renewview.frontend.assets.i18n import t


def render_about(lang: str = "EN") -> None:
    """Render the About page content."""
    st.title(t("about", lang))
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


if __name__ == "__main__":
    render_about()
