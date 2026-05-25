"""Mediterranean solar assessment theme — custom CSS for Streamlit."""

THEME_CSS = """
<style>
/* RenewView — Mediterranean property-assessment theme */

/* ── Global Background ──────────────────────────────────── */
.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(215, 181, 128, 0.20), transparent 30%),
        linear-gradient(180deg, #f7f1e7 0%, #f2eadc 100%) !important;
}

/* Main content area */
.stApp > header {
    background-color: rgba(247, 241, 231, 0.92) !important;
    border-bottom: 1px solid rgba(93, 73, 55, 0.08) !important;
}

section[data-testid="stMain"] {
    background-color: transparent !important;
}

.block-container {
    max-width: 1040px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ── Sidebar ────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background-color: #fff9ef !important;
    border-right: 1px solid rgba(93, 73, 55, 0.12) !important;
}

section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li {
    color: #6f665d !important;
    font-size: 0.9rem;
    line-height: 1.55;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #3a3027 !important;
    font-family: Georgia, "Times New Roman", serif !important;
}

section[data-testid="stSidebar"] .stSelectbox label {
    color: #7d6c58 !important;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
}

/* Sidebar dividers */
section[data-testid="stSidebar"] hr {
    border-color: rgba(93, 73, 55, 0.12) !important;
}

/* ── Typography ─────────────────────────────────────────── */
h1, h2, h3 {
    color: #2e261f !important;
    font-family: Georgia, "Times New Roman", serif !important;
}

h1 {
    font-weight: 700 !important;
    letter-spacing: 0 !important;
}

p, li, span, label, .stMarkdown {
    color: #453a31 !important;
    line-height: 1.55;
}

/* Category labels — uppercase small */
.stSelectbox label,
.stNumberInput label,
.stSlider label,
.stRadio label,
.stTextInput label {
    color: #766555 !important;
    text-transform: uppercase !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em !important;
    font-weight: 600 !important;
}

/* Captions */
.stCaption, small, .stCaption p {
    color: #8c8174 !important;
}

/* ── Dividers ───────────────────────────────────────────── */
hr {
    border-color: rgba(93, 73, 55, 0.12) !important;
    margin: 1.5rem 0 !important;
}

/* ── Cards — warm panels with refined borders ───────────── */
div[data-testid="stExpander"] {
    background-color: #fffaf2 !important;
    border: 1px solid rgba(93, 73, 55, 0.13) !important;
    border-radius: 12px !important;
    overflow: hidden;
    box-shadow: 0 10px 28px rgba(71, 54, 37, 0.06) !important;
}

div[data-testid="stExpander"] summary {
    color: #8f5d34 !important;
    font-weight: 600;
}

div[data-testid="stExpander"] .stMarkdown p {
    color: #6f665d !important;
}

/* ── Tabs ───────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background-color: #eadfcd !important;
    border-radius: 999px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(93, 73, 55, 0.10);
}

.stTabs [data-baseweb="tab"] {
    color: #766555 !important;
    background-color: transparent !important;
    border-radius: 999px !important;
    font-weight: 650;
    padding: 8px 20px;
}

.stTabs [aria-selected="true"] {
    color: #6f3d24 !important;
    background-color: #fff9ef !important;
    border-bottom: none !important;
    box-shadow: 0 8px 18px rgba(71, 54, 37, 0.08) !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: #b95f3b !important;
}

.stTabs [data-baseweb="tab-border"] {
    display: none;
}

/* ── Buttons ────────────────────────────────────────────── */
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #a94f31 0%, #c66f49 100%) !important;
    color: #fff9ef !important;
    border: 1px solid rgba(111, 61, 36, 0.22) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.72rem 1.5rem !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 14px 30px rgba(185, 95, 59, 0.20) !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    background: linear-gradient(135deg, #98482e 0%, #b95f3b 100%) !important;
    box-shadow: 0 18px 34px rgba(185, 95, 59, 0.28) !important;
    transform: translateY(-1px) !important;
}

/* Secondary buttons (like NASA fetch) */
.stButton > button[kind="secondary"],
.stButton > button[data-testid="stBaseButton-secondary"] {
    background-color: rgba(255, 249, 239, 0.78) !important;
    color: #7a4d2e !important;
    border: 1px solid rgba(122, 77, 46, 0.22) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.stButton > button[kind="secondary"]:hover,
.stButton > button[data-testid="stBaseButton-secondary"]:hover {
    background-color: #fff9ef !important;
    border-color: #b95f3b !important;
    color: #6f3d24 !important;
}

/* Link buttons */
.stLinkButton > a {
    background: linear-gradient(135deg, #a94f31 0%, #c66f49 100%) !important;
    color: #fff9ef !important;
    border: 1px solid rgba(111, 61, 36, 0.22) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    box-shadow: 0 14px 30px rgba(185, 95, 59, 0.20) !important;
}

/* ── Input Widgets ──────────────────────────────────────── */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background-color: #fffaf2 !important;
    color: #2e261f !important;
    border: 1px solid rgba(93, 73, 55, 0.18) !important;
    border-radius: 10px !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.58) !important;
}

.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus {
    border-color: #b95f3b !important;
    box-shadow: 0 0 0 3px rgba(185, 95, 59, 0.14) !important;
}

/* Selectbox dropdown */
[data-baseweb="popover"] {
    background-color: #fffaf2 !important;
    border: 1px solid rgba(93, 73, 55, 0.16) !important;
    box-shadow: 0 18px 38px rgba(71, 54, 37, 0.14) !important;
}

[data-baseweb="popover"] li {
    color: #453a31 !important;
}

[data-baseweb="popover"] li:hover {
    background-color: rgba(185, 95, 59, 0.10) !important;
}

/* Slider */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: #b95f3b !important;
}

.stSlider [data-testid="stThumbValue"] {
    color: #8f5d34 !important;
}

/* ── Metric cards (Streamlit native) ────────────────────── */
div[data-testid="stMetric"] {
    background-color: #fffaf2 !important;
    border: 1px solid rgba(93, 73, 55, 0.13) !important;
    border-radius: 12px !important;
    padding: 1.2rem 1rem !important;
    text-align: center;
    box-shadow: 0 12px 28px rgba(71, 54, 37, 0.07) !important;
}

div[data-testid="stMetric"] label {
    color: #766555 !important;
    text-transform: uppercase !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #8f5d34 !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}

/* ── Alert boxes ────────────────────────────────────────── */
.stAlert [data-testid="stAlertContentError"] {
    background-color: rgba(255, 60, 60, 0.08) !important;
    border: 1px solid rgba(255, 60, 60, 0.3) !important;
    border-radius: 12px !important;
    color: #ff6666 !important;
}

div[data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) {
    background-color: rgba(111, 130, 92, 0.10) !important;
    border: 1px solid rgba(111, 130, 92, 0.28) !important;
    border-radius: 12px !important;
}

div[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) {
    background-color: rgba(86, 139, 142, 0.10) !important;
    border: 1px solid rgba(86, 139, 142, 0.25) !important;
    border-radius: 12px !important;
}

div[data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) {
    background-color: rgba(203, 146, 63, 0.12) !important;
    border: 1px solid rgba(203, 146, 63, 0.28) !important;
    border-radius: 12px !important;
}

/* ── Map ────────────────────────────────────────────────── */
iframe {
    border-radius: 12px !important;
    border: 1px solid rgba(93, 73, 55, 0.14) !important;
    box-shadow: 0 12px 28px rgba(71, 54, 37, 0.08) !important;
}

/* ── Spinner ────────────────────────────────────────────── */
.stSpinner > div {
    border-top-color: #b95f3b !important;
}

/* ── Scrollbar ──────────────────────────────────────────── */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: #f7f1e7;
}

::-webkit-scrollbar-thumb {
    background: rgba(122, 77, 46, 0.28);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(122, 77, 46, 0.45);
}

/* ── Hide default sidebar navigation ──────────────────── */
[data-testid='stSidebarNav'] {
    display: none;
}

/* ── Button text contrast ──────────────────────────────── */
button[kind='primary'] p,
.stButton button[data-testid='stBaseButton-primary'] p {
    color: #fff9ef !important;
    font-weight: 700 !important;
}
</style>
"""


def section_header_html(title: str) -> str:
    """Styled section header with terracotta left accent bar."""
    return f"""
    <div style="
        border-left: 4px solid #b95f3b;
        padding: 0.4rem 0 0.4rem 1rem;
        margin: 1.35rem 0 0.9rem;
    ">
        <span style="
            color: #2e261f;
            font-family: Georgia, 'Times New Roman', serif;
            font-size: 1.22rem;
            font-weight: 700;
            letter-spacing: 0;
        ">{title}</span>
    </div>
    """


def welcome_hero_html(title: str, subtitle: str, intro: str) -> str:
    """HTML block for the welcome hero section with solar panel background."""
    bg_url = "https://images.unsplash.com/photo-1509391366360-2e959784a276?w=1200&q=80"
    return f"""
    <div style="
        position:relative;
        background:url('{bg_url}') center/cover no-repeat;
        border-radius:20px;
        overflow:hidden;
        margin:-0.5rem 0 0;
        padding:0;
        border:1px solid rgba(93,73,55,0.14);
        box-shadow:0 22px 60px rgba(71,54,37,0.16);
    ">
        <div style="
            background:linear-gradient(
                90deg,
                rgba(46,38,31,0.66) 0%,
                rgba(92,73,55,0.45) 54%,
                rgba(247,241,231,0.28) 100%
            );
            padding:4.4rem 2rem 3.4rem;
            text-align:left;
        ">
            <div style="
                display:inline-block;
                max-width:680px;
                background:rgba(255,249,239,0.92);
                border:1px solid rgba(255,249,239,0.72);
                border-radius:18px;
                padding:1.35rem 1.45rem 1.25rem;
                box-shadow:0 18px 44px rgba(46,38,31,0.24);
                backdrop-filter:blur(3px);
            ">
                <h1 style="
                    font-family:Georgia, 'Times New Roman', serif;
                    font-size:clamp(2.55rem, 7vw, 4.4rem);
                    font-weight:700;
                    color:#2e261f !important;
                    margin:0 0 0.45rem;
                    line-height:0.98;
                    letter-spacing:0;
                ">{title}</h1>
                <p style="
                    color:#4a3d32 !important;
                    font-size:1.18rem;
                    margin:0 0 0.55rem;
                    max-width:620px;
                    line-height:1.45;
                    font-weight:600;
                ">{subtitle}</p>
                <p style="
                    color:#6f665d !important;
                    font-size:0.96rem;
                    line-height:1.6;
                    max-width:600px;
                    margin:0;
                ">{intro}</p>
            </div>
        </div>
    </div>
    """


def svg_gauge_html(score: float, viability: str) -> str:
    """SVG circular gauge — warm report ring with arc proportional to score.

    Args:
        score: 0–100 feasibility score.
        viability: One of High / Medium / Low / Not Viable.

    Returns:
        HTML/SVG string for embedding in Streamlit.
    """
    # Arc colors per viability class
    arc_colors = {
        "High": "#6f825c",
        "Medium": "#c07a3d",
        "Low": "#c66f49",
        "Not Viable": "#b94d42",
    }
    arc_color = arc_colors.get(viability, "#8c8174")

    badge_bg = {
        "High": "#eef3e6",
        "Medium": "#fbecd4",
        "Low": "#f8dfd3",
        "Not Viable": "#f5d8d4",
    }
    badge_text = {
        "High": "#53643f",
        "Medium": "#8a5526",
        "Low": "#924c31",
        "Not Viable": "#8f302c",
    }
    badge_label = {
        "High": "HIGH VIABILITY",
        "Medium": "MEDIUM VIABILITY",
        "Low": "LOW VIABILITY",
        "Not Viable": "NOT VIABLE",
    }.get(viability, viability.upper())

    # SVG math: circle of radius 54, centered at 60×60
    r = 54
    circumference = 2 * 3.14159265 * r  # ≈ 339.29
    offset = circumference * (1 - score / 100)

    return f"""
    <div style="
        text-align:center;
        padding:1.5rem 0 1.2rem;
        background:#fffaf2;
        border:1px solid rgba(93,73,55,0.13);
        border-radius:16px;
        box-shadow:0 14px 34px rgba(71,54,37,0.08);
    ">
        <svg width="160" height="160" viewBox="0 0 120 120"
             style="display:block; margin:0 auto;">
            <circle cx="60" cy="60" r="{r}"
                    fill="none" stroke="#eadfcd" stroke-width="10" />
            <circle cx="60" cy="60" r="{r}"
                    fill="none" stroke="{arc_color}" stroke-width="10"
                    stroke-linecap="round"
                    stroke-dasharray="{circumference:.2f}"
                    stroke-dashoffset="{offset:.2f}"
                    transform="rotate(-90 60 60)"
                    style="transition: stroke-dashoffset 0.8s ease;" />
            <text x="60" y="56" text-anchor="middle" dominant-baseline="central"
                  fill="{arc_color}" font-size="26" font-weight="800"
                  font-family="Georgia, serif">{score:.0f}%</text>
            <text x="60" y="78" text-anchor="middle"
                  fill="#8c8174" font-size="8" font-weight="700"
                  font-family="sans-serif" letter-spacing="0.15em">SCORE</text>
        </svg>
        <div style="
            display:inline-block;
            background:{badge_bg.get(viability, '#8a9a8a')};
            color:{badge_text.get(viability, '#151515')};
            padding:0.38rem 1.25rem;
            border-radius:20px;
            font-size:0.72rem;
            font-weight:800;
            letter-spacing:0.08em;
            margin-top:0.6rem;
            text-transform:uppercase;
            border:1px solid rgba(93,73,55,0.08);
        ">{badge_label}</div>
    </div>
    """


def score_card_html(score: float, viability: str, lang: str = "EN") -> str:
    """Generate HTML for the large centered score display with viability badge."""
    badge_colors = {
        "High": ("#eef3e6", "#53643f"),
        "Medium": ("#fbecd4", "#8a5526"),
        "Low": ("#f8dfd3", "#924c31"),
        "Not Viable": ("#f5d8d4", "#8f302c"),
    }
    bg, text_bg = badge_colors.get(viability, ("#eadfcd", "#453a31"))

    badge_label = {
        "High": "HIGH VIABILITY",
        "Medium": "MEDIUM VIABILITY",
        "Low": "LOW VIABILITY",
        "Not Viable": "NOT VIABLE",
    }.get(viability, viability.upper())

    return f"""
    <div style="
        background: #fffaf2;
        border: 1px solid rgba(93,73,55,0.13);
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 14px 34px rgba(71,54,37,0.08);
    ">
        <div style="
            color: #766555;
            text-transform: uppercase;
            font-size: 0.7rem;
            letter-spacing: 0.12em;
            margin-bottom: 0.5rem;
            font-weight: 600;
        ">FEASIBILITY SCORE</div>
        <div style="
            color: #8f5d34;
            font-family: Georgia, 'Times New Roman', serif;
            font-size: 3.5rem;
            font-weight: 700;
            line-height: 1.1;
        ">{score:.0f}%</div>
        <div style="
            display: inline-block;
            background: {bg};
            color: {text_bg};
            padding: 0.35rem 1.2rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            margin-top: 0.8rem;
            text-transform: uppercase;
            border: 1px solid rgba(93,73,55,0.08);
        ">{badge_label}</div>
    </div>
    """


def metric_card_html(label: str, value: str, icon: str = "") -> str:
    """Generate HTML for a single metric card."""
    return f"""
    <div style="
        background: #fffaf2;
        border: 1px solid rgba(93,73,55,0.13);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 14px 34px rgba(71,54,37,0.08);
    ">
        <div style="
            color: #766555;
            text-transform: uppercase;
            font-size: 0.68rem;
            letter-spacing: 0.08em;
            font-weight: 600;
            margin-bottom: 0.5rem;
        ">{icon} {label}</div>
        <div style="
            color: #8f5d34;
            font-family: Georgia, 'Times New Roman', serif;
            font-size: 1.9rem;
            font-weight: 700;
            line-height: 1.2;
        ">{value}</div>
    </div>
    """


def not_viable_card_html(gate: str, reason: str) -> str:
    """Generate HTML for the Not Viable elimination card (no recommendation box)."""
    return (
        '<div style="background:#fff5f1;border:1px solid rgba(185,77,66,0.24);'
        'border-radius:16px;padding:1.5rem;margin-bottom:1rem;'
        'box-shadow:0 14px 34px rgba(71,54,37,0.08);">'
        '<div style="color:#8f302c;font-size:1.3rem;font-weight:700;'
        'font-family:Georgia,serif;'
        f'margin-bottom:0.5rem;">SITE NOT VIABLE</div>'
        '<div style="color:#9b6f64;font-size:0.72rem;text-transform:uppercase;'
        'letter-spacing:0.08em;font-weight:600;margin-bottom:0.3rem;">'
        f"ELIMINATED BY GATE {gate}</div>"
        '<div style="color:#5e4a42;font-size:0.9rem;line-height:1.5;">'
        f"{reason}</div>"
        "</div>"
    )


def nasa_card_header_html(title: str = "Climate Data — NASA POWER") -> str:
    """HTML header for the NASA climate data card."""
    return f"""
    <div style="
        background: #fffaf2;
        border: 1px solid rgba(93,73,55,0.13);
        border-radius: 16px 16px 0 0;
        padding: 1rem 1.5rem 0.5rem;
        margin-top: 0.5rem;
        box-shadow: 0 10px 24px rgba(71,54,37,0.06);
    ">
        <div style="
            color: #2e261f;
            font-family: Georgia, 'Times New Roman', serif;
            font-size: 1.1rem;
            font-weight: 700;
        ">☀️ {title}</div>
        <div style="
            color: #8c8174;
            font-size: 0.75rem;
            margin-top: 0.2rem;
        ">Annual averages from satellite observations</div>
    </div>
    """


def gate_pass_html(gates: list[str]) -> str:
    """Generate HTML for gate pass checklist."""
    icons = ["\U0001f3db\ufe0f", "\u26a1", "\u2600\ufe0f", "\U0001f4d0"]
    items = ""
    for i, g in enumerate(gates):
        icon = icons[i] if i < len(icons) else "\u2713"
        items += f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.4rem 0;
            color: #5d5148;
            font-size: 1rem;
        ">
            <span style="font-size: 1.1rem;">{icon}</span>
            <span style="color: #6f825c; font-size: 1rem;">&#10003;</span>
            {g}
        </div>
        """
    return f"""
    <div style="
        background: #fffaf2;
        border: 1px solid rgba(93,73,55,0.13);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        margin: 0.8rem 0;
        box-shadow: 0 14px 34px rgba(71,54,37,0.08);
    ">
        <div style="
            color: #766555;
            text-transform: uppercase;
            font-size: 0.68rem;
            letter-spacing: 0.08em;
            font-weight: 600;
            margin-bottom: 0.6rem;
        ">PRE-SCREENING GATES PASSED</div>
        {items}
    </div>
    """
