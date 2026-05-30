"""Tests for the €29 residential solar PDF report generator."""

import pytest

from renewview.backend.services.report_generator import (
    _fmt_decimal,
    _fmt_int,
    _fmt_money,
    _fmt_years,
    _normalize_lang,
    generate_report,
)


# ── shared fixtures ──────────────────────────────────────────


def _full_assessment() -> dict:
    return {
        "viability_class": "Medium",
        "score": 74.0,
        "annual_kwh": 18093.78,
        "revenue_eur": 3980.63,
        "kwp": 12.96,
        "payback_years": 3.9,
        "net_savings_25yr_eur": 83964,
        "ghi_used": 4.5,
        "orientation": "S",
        "shading": "light",
    }


def _customer() -> dict:
    return {
        "name": "Maria Silva",
        "email": "maria@example.pt",
        "location": "Lisboa, Portugal",
    }


# ── render: each language produces a non-empty PDF ───────────


def test_pdf_generated_en(tmp_path):
    out = tmp_path / "report_en.pdf"
    result = generate_report(_full_assessment(), _customer(), out, lang="EN")
    assert result == out
    assert out.exists()
    assert out.stat().st_size > 2000
    assert out.read_bytes()[:4] == b"%PDF"


def test_pdf_generated_pt(tmp_path):
    out = tmp_path / "report_pt.pdf"
    generate_report(_full_assessment(), _customer(), out, lang="PT")
    assert out.exists()
    assert out.stat().st_size > 2000


def test_pdf_generated_es(tmp_path):
    out = tmp_path / "report_es.pdf"
    generate_report(_full_assessment(), _customer(), out, lang="ES")
    assert out.exists()
    assert out.stat().st_size > 2000


def test_pdf_generated_el(tmp_path):
    out = tmp_path / "report_el.pdf"
    generate_report(_full_assessment(), _customer(), out, lang="EL")
    assert out.exists()
    # Greek glyphs make the file noticeably larger than Latin-only — still
    # bounded sanity check, not an exact size assertion.
    assert out.stat().st_size > 2000


# ── degenerate input: no crashes ─────────────────────────────


def test_all_zero_numeric_fields_render(tmp_path):
    """If gates fail, customer still gets a (zero-valued) report. Must not crash."""
    assessment = {
        "viability_class": "Not Viable",
        "score": 0.0,
        "annual_kwh": 0,
        "revenue_eur": 0,
        "kwp": 0,
        "payback_years": 0,
        "net_savings_25yr_eur": 0,
        "ghi_used": 0,
        "orientation": "N",
        "shading": "heavy",
    }
    out = tmp_path / "zeros.pdf"
    generate_report(assessment, _customer(), out, lang="EN")
    assert out.exists() and out.stat().st_size > 1000


def test_missing_optional_fields_use_dash(tmp_path):
    """A skinny assessment dict (only viability_class) must still render."""
    out = tmp_path / "skinny.pdf"
    generate_report({"viability_class": "Medium"}, _customer(), out, lang="PT")
    assert out.exists() and out.stat().st_size > 1000


def test_missing_customer_keys_no_crash(tmp_path):
    """Empty customer dict must not crash — fields render as '—'."""
    out = tmp_path / "nocust.pdf"
    generate_report(_full_assessment(), {}, out, lang="EN")
    assert out.exists() and out.stat().st_size > 1000


def test_empty_string_customer_fields(tmp_path):
    """Empty strings (vs missing keys) must also degrade to '—'."""
    out = tmp_path / "emptystr.pdf"
    generate_report(
        _full_assessment(),
        {"name": "", "email": "", "location": ""},
        out,
        lang="EN",
    )
    assert out.exists() and out.stat().st_size > 1000


# ── formatter unit tests ─────────────────────────────────────


def test_payback_edge_cases_render_dash():
    assert _fmt_years(0, "EN") == "—"
    assert _fmt_years(-1, "EN") == "—"
    assert _fmt_years(float("inf"), "EN") == "—"
    assert _fmt_years(float("nan"), "EN") == "—"
    assert _fmt_years(None, "EN") == "—"
    assert _fmt_years("not-a-number", "EN") == "—"


def test_payback_caps_at_99():
    assert _fmt_years(150, "EN") == "99+"


def test_money_anglo_vs_european():
    assert _fmt_money(1234, "EN") == "€1,234"
    assert _fmt_money(1234, "PT") == "1.234 €"
    assert _fmt_money(0, "EN") == "€0"
    assert _fmt_money(None, "EN") == "—"


def test_int_thousand_separator():
    assert _fmt_int(18094, "EN") == "18,094"
    assert _fmt_int(18094, "PT") == "18.094"
    assert _fmt_int(None, "EN") == "—"


def test_decimal_locale():
    assert _fmt_decimal(13.0, "EN") == "13"  # integer-valued floats collapse
    assert _fmt_decimal(12.96, "EN") == "13.0"
    assert _fmt_decimal(12.96, "PT") == "13,0"
    assert _fmt_decimal(None, "EN") == "—"


# ── language normalisation ───────────────────────────────────


def test_unknown_lang_falls_back_to_en():
    assert _normalize_lang("xx") == "EN"
    assert _normalize_lang("") == "EN"
    assert _normalize_lang(None) == "EN"
    assert _normalize_lang("en") == "EN"
    assert _normalize_lang("pt") == "PT"
    assert _normalize_lang("EL") == "EL"


def test_unknown_lang_in_generate_report_still_renders(tmp_path):
    out = tmp_path / "fallback.pdf"
    generate_report(_full_assessment(), _customer(), out, lang="zz")
    assert out.exists() and out.stat().st_size > 2000


# ── content extraction (skipped if pypdf not installed) ──────


def test_greek_glyphs_present_in_extracted_text(tmp_path):
    """Catches silent font-registration regressions — if DejaVu fails and
    reportlab falls back to Helvetica, the Greek title would be unextractable
    (rendered as missing-glyph boxes), and this assertion would catch it.
    """
    pypdf = pytest.importorskip("pypdf")
    out = tmp_path / "el.pdf"
    generate_report(_full_assessment(), _customer(), out, lang="EL")
    text = pypdf.PdfReader(out).pages[0].extract_text() or ""
    assert "Αναφορά" in text
    assert "Ηλιακού" in text


def test_portuguese_title_and_location_in_extracted_text(tmp_path):
    pypdf = pytest.importorskip("pypdf")
    out = tmp_path / "pt.pdf"
    generate_report(_full_assessment(), _customer(), out, lang="PT")
    text = pypdf.PdfReader(out).pages[0].extract_text() or ""
    assert "Relatório do Potencial Solar" in text
    assert "Lisboa, Portugal" in text
    # Confirm Portuguese number formatting reached the page.
    assert "3.981 €" in text
