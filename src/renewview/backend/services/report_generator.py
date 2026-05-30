"""PDF generator for the €29 residential solar potential report.

Single entry point: ``generate_report(assessment, customer, out_path, lang)``.
Renders a 1-page A4 PDF using DejaVuSans (full Unicode coverage including
Greek). All customer-facing strings are pulled from
``renewview.frontend.assets.i18n.TRANSLATIONS``.
"""

from __future__ import annotations

import io
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
    Image,
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
_FONT_SERIF = "DejaVuSerif"
_FONT_SERIF_BOLD = "DejaVuSerif-Bold"
_fonts_registered = False

_DASH = "—"
_SUPPORTED_LANGS = ("EN", "PT", "ES", "EL")

# ── Brand palette (mirrors src/renewview/frontend/assets/styles.py) ──
_BRAND_ACCENT = colors.HexColor("#b95f3b")        # terracotta — section heads, underline rules
_BRAND_ACCENT_DARK = colors.HexColor("#a94f31")   # header band fill
_BRAND_BURNT = colors.HexColor("#8f5d34")         # money-figure emphasis
_BRAND_CREAM = colors.HexColor("#fff9ef")         # reversed-out text on band
_BRAND_CREAM_SOFT = colors.HexColor("#f7f1e7")    # alt row shade (lighter)
_BRAND_CREAM_DEEP = colors.HexColor("#f2eadc")    # alt row shade (deeper)
_BRAND_CARD = colors.HexColor("#fffaf2")          # base row / panel cream
_BRAND_HEADING = colors.HexColor("#2e261f")       # h1 / h2 text
_BRAND_BODY = colors.HexColor("#453a31")          # paragraph body
_BRAND_MUTED = colors.HexColor("#8c8174")         # captions, disclaimers
_BRAND_LABEL = colors.HexColor("#766555")         # uppercase widget-style labels
_BRAND_HAIRLINE = colors.HexColor("#d8cfc2")      # ≈ rgba(93,73,55,0.12) on cream
_BRAND_LOSS_TINT = colors.HexColor("#f5d8d4")     # under-zero region fill on chart


def _register_fonts() -> None:
    global _fonts_registered
    if _fonts_registered:
        return

    search_dirs: list[str] = ["/usr/share/fonts/truetype/dejavu"]
    try:
        import matplotlib
        import os

        search_dirs.append(
            os.path.join(
                os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf"
            )
        )
    except ImportError:
        pass

    def _find(stem: str) -> Optional[Path]:
        for d in search_dirs:
            p = Path(d) / f"{stem}.ttf"
            if p.exists():
                return p
        return None

    sans = _find("DejaVuSans")
    sans_bold = _find("DejaVuSans-Bold")
    if not (sans and sans_bold):
        raise RuntimeError(
            "DejaVuSans TTF not found. Install `fonts-dejavu-core` (Debian/Ubuntu) "
            "or ensure matplotlib is installed (it bundles the font)."
        )
    pdfmetrics.registerFont(TTFont(_FONT_REG, str(sans)))
    pdfmetrics.registerFont(TTFont(_FONT_BOLD, str(sans_bold)))

    # Serif: brand wordmark + section heads. Fall back to Sans-Bold if the
    # serif TTFs aren't present (rare — both Debian dejavu and matplotlib bundle them).
    serif = _find("DejaVuSerif")
    serif_bold = _find("DejaVuSerif-Bold")
    if serif and serif_bold:
        pdfmetrics.registerFont(TTFont(_FONT_SERIF, str(serif)))
        pdfmetrics.registerFont(TTFont(_FONT_SERIF_BOLD, str(serif_bold)))
    else:
        pdfmetrics.registerFont(TTFont(_FONT_SERIF, str(sans)))
        pdfmetrics.registerFont(TTFont(_FONT_SERIF_BOLD, str(sans_bold)))

    _fonts_registered = True


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


def _brand_header_band(t: dict, content_width_mm: float) -> Table:
    """Full-width terracotta header band: cream serif wordmark + localized tagline.

    Replaces the old thin brand line and the redundant H1 title. The tagline
    uses ``t["pdf_report_title"]`` so all four languages render correctly.
    """
    wordmark_style = ParagraphStyle(
        "brand_wordmark",
        fontName=_FONT_SERIF_BOLD,
        fontSize=22,
        textColor=_BRAND_CREAM,
        leading=26,
    )
    tagline_style = ParagraphStyle(
        "brand_tagline",
        fontName=_FONT_BOLD,
        fontSize=9,
        textColor=_BRAND_CREAM,
        leading=12,
        alignment=2,  # right
    )
    # Greek titles are longer — give them more right-column room.
    left_w = content_width_mm * 0.45
    right_w = content_width_mm - left_w
    band = Table(
        [[
            Paragraph("RenewView", wordmark_style),
            Paragraph(t["pdf_report_title"], tagline_style),
        ]],
        colWidths=[left_w * mm, right_w * mm],
    )
    band.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), _BRAND_ACCENT_DARK),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (0, 0), 10),
                ("RIGHTPADDING", (-1, 0), (-1, 0), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return band


def _fmt_money_short(value: float, lang: str) -> str:
    """Compact money label for chart axis ticks (e.g. ``€10k`` / ``10 k €``).

    Negative values use the typographic minus ``−`` so the tick reads as a
    single visual unit. Used only inside the chart — body tables keep the
    full ``_fmt_money`` formatting.
    """
    if value == 0:
        return "€0" if lang == "EN" else "0 €"
    sign = "−" if value < 0 else ""
    v = abs(float(value))
    if v >= 1000:
        k = v / 1000.0
        body = f"{k:.0f}k" if abs(k - round(k)) < 0.05 else f"{k:.1f}k"
    else:
        body = f"{int(round(v))}"
    if lang == "EN":
        return f"{sign}€{body}"
    return f"{sign}{body} €".replace(".", ",")


def _render_savings_chart_png(
    assessment: dict, t: dict, lang: str
) -> Optional[bytes]:
    """Render the cumulative 25-year net-savings curve as a PNG.

    Returns ``None`` when there isn't enough data to draw a meaningful curve
    (e.g. zero-kWp / failed-gate cases) — the report then renders without it.
    Reads ``kwp``, ``revenue_eur``, ``payback_years``, ``net_savings_25yr_eur``
    from the assessment dict; computes year-0 install cost from the same
    config constant the methodology line already cites, so no new business
    logic is introduced.
    """
    try:
        kwp = float(assessment.get("kwp") or 0)
        revenue = float(assessment.get("revenue_eur") or 0)
    except (TypeError, ValueError):
        return None
    if kwp <= 0 or revenue <= 0:
        return None

    try:
        net_25 = float(assessment.get("net_savings_25yr_eur") or 0)
    except (TypeError, ValueError):
        net_25 = 0.0

    install_cost = kwp * RESIDENTIAL_INSTALL_COST_PER_KWP
    years = list(range(0, 26))
    cum = [-install_cost + k * revenue for k in years]

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter

    fig, ax = plt.subplots(figsize=(6.5, 2.9), dpi=200)
    fig.patch.set_facecolor("#fffaf2")
    ax.set_facecolor("#fffaf2")

    # Under-zero "loss" region — subtle warm tint so payback feels real.
    ax.fill_between(
        years, cum, 0,
        where=[c < 0 for c in cum],
        color="#f5d8d4", alpha=0.55, linewidth=0,
    )

    # Cumulative-savings line.
    ax.plot(years, cum, color="#b95f3b", linewidth=2.2, zorder=3)

    # Endpoints.
    ax.scatter([0], [-install_cost], color="#a94f31", s=24, zorder=4)
    ax.scatter([25], [net_25], color="#a94f31", s=24, zorder=4)

    # Payback crossing marker + annotation (locale-formatted, reuses existing keys).
    try:
        payback = float(assessment.get("payback_years"))
    except (TypeError, ValueError):
        payback = None
    if payback is not None and 0 < payback < 25:
        ax.scatter(
            [payback], [0],
            color="#8f5d34", s=46, zorder=5,
            edgecolor="#fffaf2", linewidths=1.4,
        )
        label = f"{_fmt_years(payback, lang)} {t['pdf_unit_years']}"
        ax.annotate(
            label,
            xy=(payback, 0),
            xytext=(payback + 1.2, max(install_cost * 0.30, net_25 * 0.10)),
            fontsize=8,
            color="#8f5d34",
            fontweight="bold",
            arrowprops=dict(arrowstyle="-", color="#8f5d34", lw=0.6),
        )

    # Zero rule.
    ax.axhline(0, color="#d8cfc2", linewidth=0.8, linestyle="--", zorder=1)

    # Spines / ticks — keep only left + bottom, brand-tinted.
    for spine_name in ("top", "right"):
        ax.spines[spine_name].set_visible(False)
    for spine_name in ("left", "bottom"):
        ax.spines[spine_name].set_color("#d8cfc2")
    ax.tick_params(axis="both", colors="#8c8174", labelsize=8, length=3)

    ax.set_xlim(-0.5, 25.5)
    ax.set_xticks([0, 5, 10, 15, 20, 25])
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda v, _pos: _fmt_money_short(v, lang))
    )
    ax.set_xlabel(t["pdf_unit_years"], color="#8c8174", fontsize=8)

    buf = io.BytesIO()
    fig.savefig(
        buf, format="png",
        facecolor=fig.get_facecolor(),
        bbox_inches="tight",
        pad_inches=0.18,
    )
    plt.close(fig)
    return buf.getvalue()


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

    # ── styles ── (brand palette pulled from frontend/assets/styles.py)
    s_meta = ParagraphStyle(
        "meta",
        fontName=_FONT_REG,
        fontSize=10,
        textColor=_BRAND_BODY,
        leading=13,
        spaceAfter=1,
    )
    s_h2 = ParagraphStyle(
        "h2",
        fontName=_FONT_SERIF_BOLD,
        fontSize=14,
        textColor=_BRAND_ACCENT,
        leading=17,
        spaceBefore=14,
        spaceAfter=2,
    )
    s_body = ParagraphStyle(
        "body",
        fontName=_FONT_REG,
        fontSize=10,
        textColor=_BRAND_BODY,
        leading=14,
        spaceAfter=4,
    )
    s_kv_label = ParagraphStyle(
        "kvl",
        fontName=_FONT_REG,
        fontSize=10.5,
        textColor=_BRAND_BODY,
        leading=14,
    )
    s_kv_value = ParagraphStyle(
        "kvv",
        fontName=_FONT_BOLD,
        fontSize=10.5,
        textColor=_BRAND_HEADING,
        leading=14,
        alignment=2,  # right
    )
    s_kv_value_money = ParagraphStyle(
        "kvv_money",
        fontName=_FONT_BOLD,
        fontSize=10.5,
        textColor=_BRAND_BURNT,
        leading=14,
        alignment=2,
    )
    s_disc = ParagraphStyle(
        "disc",
        fontName=_FONT_REG,
        fontSize=8,
        textColor=_BRAND_MUTED,
        leading=11,
        spaceBefore=8,
    )

    story = []

    # ── brand header band (terracotta + cream serif wordmark + tagline) ──
    # A4 width 210mm − leftMargin 22 − rightMargin 22 = 166mm usable.
    story.append(_brand_header_band(t, content_width_mm=166))
    story.append(Spacer(1, 10))

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
            thickness=0.8,
            color=_BRAND_ACCENT,
            spaceAfter=4,
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
    sum_table = Table(summary_rows, colWidths=[110 * mm, 56 * mm])
    sum_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [_BRAND_CARD, _BRAND_CREAM_DEEP]),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("LINEBELOW", (0, 0), (-1, -2), 0.25, _BRAND_HAIRLINE),
            ]
        )
    )
    story.append(sum_table)

    # ── Money ──
    story.append(Paragraph(t["pdf_section_money"], s_h2))
    story.append(
        HRFlowable(
            width="100%",
            thickness=0.8,
            color=_BRAND_ACCENT,
            spaceAfter=4,
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
            Paragraph(_fmt_money(assessment.get("revenue_eur"), lang), s_kv_value_money),
        ],
        [
            Paragraph(t["pdf_label_payback"], s_kv_label),
            Paragraph(
                f"{_fmt_years(assessment.get('payback_years'), lang)} {t['pdf_unit_years']}",
                s_kv_value_money,
            ),
        ],
        [
            Paragraph(t["pdf_label_25yr_net"], s_kv_label),
            Paragraph(
                _fmt_money(assessment.get("net_savings_25yr_eur"), lang),
                s_kv_value_money,
            ),
        ],
    ]
    money_table = Table(money_rows, colWidths=[110 * mm, 56 * mm])
    money_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [_BRAND_CARD, _BRAND_CREAM_DEEP]),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                # Brand-tinted rule above the 25-year headline row.
                ("LINEABOVE", (0, 3), (-1, 3), 0.6, _BRAND_ACCENT),
            ]
        )
    )
    story.append(money_table)

    # ── Cumulative savings chart (skipped when assessment lacks numeric data) ──
    chart_png = _render_savings_chart_png(assessment, t, lang)
    if chart_png is not None:
        story.append(Spacer(1, 6))
        chart_img = Image(io.BytesIO(chart_png), width=166 * mm, height=74 * mm)
        story.append(chart_img)

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
            color=_BRAND_HAIRLINE,
            spaceBefore=12,
            spaceAfter=2,
        )
    )
    story.append(Paragraph(t["pdf_body_disclaimer"], s_disc))

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=22 * mm,
        rightMargin=22 * mm,
        topMargin=14 * mm,
        bottomMargin=16 * mm,
        title=f"RenewView Report — {name}",
        author="RenewView",
    )
    doc.build(story)
    return out_path
