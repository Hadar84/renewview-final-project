"""PDF generator for the €29 residential solar potential report.

Single entry point: ``generate_report(assessment, customer, out_path, lang)``.
Renders a 1-page A4 PDF using DejaVuSans (full Unicode coverage including
Greek). All customer-facing strings are pulled from
``renewview.frontend.assets.i18n.TRANSLATIONS``.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from renewview.config.settings import (
    RESIDENTIAL_INSTALL_COST_PER_KWP,
    RESIDENTIAL_KWH_RATE_EUR,
    ROOF_KWP_PER_M2,
)
from renewview.frontend.assets.i18n import TRANSLATIONS

_FONT_REG = "DejaVuSans"
_FONT_BOLD = "DejaVuSans-Bold"
_fonts_registered = False

_DASH = "—"
_SUPPORTED_LANGS = ("EN", "PT", "ES", "EL")


def _register_fonts() -> None:
    global _fonts_registered
    if _fonts_registered:
        return
    candidates: list[tuple[str, str]] = [
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ),
    ]
    try:
        import matplotlib
        import os

        ttf = os.path.join(
            os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf"
        )
        candidates.append(
            (
                os.path.join(ttf, "DejaVuSans.ttf"),
                os.path.join(ttf, "DejaVuSans-Bold.ttf"),
            )
        )
    except ImportError:
        pass

    for reg, bold in candidates:
        if Path(reg).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont(_FONT_REG, reg))
            pdfmetrics.registerFont(TTFont(_FONT_BOLD, bold))
            _fonts_registered = True
            return

    raise RuntimeError(
        "DejaVuSans TTF not found. Install `fonts-dejavu-core` (Debian/Ubuntu) "
        "or ensure matplotlib is installed (it bundles the font)."
    )


def _normalize_lang(lang: Optional[str]) -> str:
    if not lang:
        return "EN"
    u = lang.upper()
    return u if u in _SUPPORTED_LANGS else "EN"


def _fmt_int(n, lang: str) -> str:
    try:
        v = int(round(float(n)))
    except (TypeError, ValueError):
        return _DASH
    s = f"{v:,}"
    return s if lang == "EN" else s.replace(",", ".")


def _fmt_decimal(n, lang: str, places: int = 1) -> str:
    try:
        v = float(n)
    except (TypeError, ValueError):
        return _DASH
    if v != v:  # NaN
        return _DASH
    if v == int(v):
        return _fmt_int(v, lang)
    s = f"{v:.{places}f}"
    return s if lang == "EN" else s.replace(".", ",")


def _fmt_money(n, lang: str) -> str:
    try:
        v = int(round(float(n)))
    except (TypeError, ValueError):
        return _DASH
    s = f"{v:,}"
    if lang == "EN":
        return f"€{s}"
    return f"{s.replace(',', '.')} €"


def _fmt_money_2dec(n, lang: str) -> str:
    try:
        v = float(n)
    except (TypeError, ValueError):
        return _DASH
    if lang == "EN":
        return f"€{v:,.2f}"
    s = f"{v:,.2f}"
    # comma <-> period swap for European decimal/thousand notation
    s = s.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"{s} €"


def _fmt_years(n, lang: str) -> str:
    try:
        v = float(n)
    except (TypeError, ValueError):
        return _DASH
    if v != v or v <= 0 or v == float("inf"):
        return _DASH
    if v >= 99:
        return "99+"
    s = f"{v:.1f}"
    return s if lang == "EN" else s.replace(".", ",")


def _viability_label(t: dict, klass: Optional[str]) -> str:
    mapping = {
        "High": "pdf_viability_high",
        "Medium": "pdf_viability_medium",
        "Low": "pdf_viability_low",
        "Not Viable": "pdf_viability_not_viable",
    }
    key = mapping.get(klass or "")
    if key and key in t:
        return t[key]
    return klass or _DASH


def _shading_label(t: dict, shading: Optional[str]) -> str:
    if not shading:
        return _DASH
    key = f"pdf_shading_{shading.lower()}"
    return t.get(key, shading)


def _orientation_label(orientation: Optional[str]) -> str:
    if not orientation:
        return _DASH
    return str(orientation).upper()


def generate_report(
    assessment: dict,
    customer: dict,
    out_path: Path | str,
    lang: str = "EN",
) -> Path:
    """Render a single-page PDF report from a residential-roof assessment.

    Args:
        assessment: Dict from ``PredictionService._assess_residential_roof``.
            Expected keys: viability_class, score, annual_kwh, revenue_eur,
            kwp, payback_years, net_savings_25yr_eur, orientation, shading.
            Missing or non-numeric values render as "—".
        customer: ``{"name": str, "email": str, "location": str}``. Missing
            string values render as "—".
        out_path: Where to write the PDF. Parent directory is created if missing.
        lang: One of "EN" / "PT" / "ES" / "EL" (case-insensitive). Unknown
            values fall back to "EN".

    Returns:
        Absolute path of the written PDF.
    """
    _register_fonts()
    lang = _normalize_lang(lang)
    t = TRANSLATIONS[lang]
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # ── styles ──
    s_brand = ParagraphStyle(
        "brand",
        fontName=_FONT_BOLD,
        fontSize=9,
        textColor=colors.HexColor("#555555"),
        spaceAfter=2,
    )
    s_title = ParagraphStyle(
        "title",
        fontName=_FONT_BOLD,
        fontSize=22,
        textColor=colors.black,
        leading=26,
        spaceAfter=6,
    )
    s_meta = ParagraphStyle(
        "meta",
        fontName=_FONT_REG,
        fontSize=10,
        textColor=colors.HexColor("#333333"),
        leading=13,
        spaceAfter=1,
    )
    s_h2 = ParagraphStyle(
        "h2",
        fontName=_FONT_BOLD,
        fontSize=13,
        textColor=colors.black,
        leading=16,
        spaceBefore=12,
        spaceAfter=2,
    )
    s_body = ParagraphStyle(
        "body",
        fontName=_FONT_REG,
        fontSize=10,
        textColor=colors.black,
        leading=14,
        spaceAfter=4,
    )
    s_kv_label = ParagraphStyle(
        "kvl",
        fontName=_FONT_REG,
        fontSize=10.5,
        textColor=colors.HexColor("#333333"),
        leading=14,
    )
    s_kv_value = ParagraphStyle(
        "kvv",
        fontName=_FONT_BOLD,
        fontSize=10.5,
        textColor=colors.black,
        leading=14,
        alignment=2,  # right
    )
    s_disc = ParagraphStyle(
        "disc",
        fontName=_FONT_REG,
        fontSize=8,
        textColor=colors.HexColor("#555555"),
        leading=11,
        spaceBefore=8,
    )

    story = []

    # ── brand band ──
    story.append(Paragraph("RenewView", s_brand))
    story.append(
        HRFlowable(
            width="100%",
            thickness=0.6,
            color=colors.HexColor("#999999"),
            spaceBefore=2,
            spaceAfter=10,
        )
    )
    story.append(Paragraph(t["pdf_report_title"], s_title))

    # ── meta block ──
    today = date.today().isoformat()
    name = (customer.get("name") or _DASH).strip() or _DASH
    location = (customer.get("location") or _DASH).strip() or _DASH
    story.append(Paragraph(f"{t['pdf_label_date']}: {today}", s_meta))
    story.append(Paragraph(f"{t['pdf_label_customer']}: {name}", s_meta))
    story.append(Paragraph(f"{t['pdf_label_location']}: {location}", s_meta))
    story.append(Spacer(1, 4))

    # ── Summary ──
    story.append(Paragraph(t["pdf_section_summary"], s_h2))
    story.append(
        HRFlowable(
            width="100%",
            thickness=0.4,
            color=colors.HexColor("#cccccc"),
            spaceAfter=2,
        )
    )

    kwp_raw = assessment.get("kwp") or 0
    try:
        panels_approx = int(round(float(kwp_raw) / 0.4))
    except (TypeError, ValueError):
        panels_approx = 0

    score_raw = assessment.get("score")
    score_str = (
        f"{_fmt_decimal(score_raw, lang)} / 100" if score_raw is not None else _DASH
    )

    summary_rows = [
        [
            Paragraph(t["pdf_label_viability"], s_kv_label),
            Paragraph(_viability_label(t, assessment.get("viability_class")), s_kv_value),
        ],
        [
            Paragraph(t["pdf_label_score"], s_kv_label),
            Paragraph(score_str, s_kv_value),
        ],
        [
            Paragraph(t["pdf_label_system_size"], s_kv_label),
            Paragraph(
                f"{_fmt_decimal(kwp_raw, lang)} {t['pdf_unit_kwp']}", s_kv_value
            ),
        ],
        [
            Paragraph(t["pdf_label_panels_approx"], s_kv_label),
            Paragraph(f"≈ {_fmt_int(panels_approx, lang)}", s_kv_value),
        ],
        [
            Paragraph(t["pdf_label_orientation"], s_kv_label),
            Paragraph(_orientation_label(assessment.get("orientation")), s_kv_value),
        ],
        [
            Paragraph(t["pdf_label_shading"], s_kv_label),
            Paragraph(_shading_label(t, assessment.get("shading")), s_kv_value),
        ],
    ]
    sum_table = Table(summary_rows, colWidths=[110 * mm, 60 * mm])
    sum_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.append(sum_table)

    # ── Money ──
    story.append(Paragraph(t["pdf_section_money"], s_h2))
    story.append(
        HRFlowable(
            width="100%",
            thickness=0.4,
            color=colors.HexColor("#cccccc"),
            spaceAfter=2,
        )
    )

    money_rows = [
        [
            Paragraph(t["pdf_label_annual_production"], s_kv_label),
            Paragraph(
                f"{_fmt_int(assessment.get('annual_kwh'), lang)} {t['pdf_unit_kwh_year']}",
                s_kv_value,
            ),
        ],
        [
            Paragraph(t["pdf_label_annual_savings"], s_kv_label),
            Paragraph(_fmt_money(assessment.get("revenue_eur"), lang), s_kv_value),
        ],
        [
            Paragraph(t["pdf_label_payback"], s_kv_label),
            Paragraph(
                f"{_fmt_years(assessment.get('payback_years'), lang)} {t['pdf_unit_years']}",
                s_kv_value,
            ),
        ],
        [
            Paragraph(t["pdf_label_25yr_net"], s_kv_label),
            Paragraph(
                _fmt_money(assessment.get("net_savings_25yr_eur"), lang), s_kv_value
            ),
        ],
    ]
    money_table = Table(money_rows, colWidths=[110 * mm, 60 * mm])
    money_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                # Stronger rule above the 25-year row to highlight the headline figure.
                ("LINEABOVE", (0, 3), (-1, 3), 0.6, colors.HexColor("#888888")),
            ]
        )
    )
    story.append(money_table)

    # ── Methodology ──
    methodology = t["pdf_body_methodology"].format(
        w_per_m2=int(round(ROOF_KWP_PER_M2 * 1000)),
        rate=f"{_fmt_money_2dec(RESIDENTIAL_KWH_RATE_EUR, lang)}/kWh",
        cost=f"{_fmt_money(RESIDENTIAL_INSTALL_COST_PER_KWP, lang)}/kWp",
    )
    story.append(Paragraph(t["pdf_section_methodology"], s_h2))
    story.append(Paragraph(methodology, s_body))

    # ── Next step (lead-capture line) ──
    story.append(Paragraph(t["pdf_section_next_step"], s_h2))
    story.append(Paragraph(t["pdf_body_next_step"], s_body))

    # ── Disclaimer footer ──
    story.append(
        HRFlowable(
            width="100%",
            thickness=0.4,
            color=colors.HexColor("#cccccc"),
            spaceBefore=12,
            spaceAfter=2,
        )
    )
    story.append(Paragraph(t["pdf_body_disclaimer"], s_disc))

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=16 * mm,
        title=f"RenewView Report — {name}",
        author="RenewView",
    )
    doc.build(story)
    return out_path
