"""Dark solar-tech theme — custom CSS for Streamlit."""

THEME_CSS = """
<style>
/* ═══════════════════════════════════════════════════════════
   RenewView — Dark Solar-Tech Theme
   Background: near-black green  |  Accent: neon green #00e05a
   ═══════════════════════════════════════════════════════════ */

/* ── Global Background ──────────────────────────────────── */
.stApp {
    background-color: #0a1a0f !important;
}

/* Main content area */
.stApp > header {
    background-color: #0a1a0f !important;
}

section[data-testid="stMain"] {
    background-color: #0a1a0f !important;
}

/* ── Sidebar ────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background-color: #111b14 !important;
    border-right: 1px solid rgba(0, 224, 90, 0.15) !important;
}

section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li {
    color: #8a9a8a !important;
    font-size: 0.9rem;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #d0e0d0 !important;
}

section[data-testid="stSidebar"] .stSelectbox label {
    color: #8a9a8a !important;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
}

/* Sidebar dividers */
section[data-testid="stSidebar"] hr {
    border-color: rgba(0, 224, 90, 0.12) !important;
}

/* ── Typography ─────────────────────────────────────────── */
h1, h2, h3 {
    color: #ffffff !important;
}

h1 {
    font-weight: 700 !important;
}

p, li, span, label, .stMarkdown {
    color: #c0d0c0 !important;
}

/* Category labels — uppercase small */
.stSelectbox label,
.stNumberInput label,
.stSlider label {
    color: #8a9a8a !important;
    text-transform: uppercase !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em !important;
    font-weight: 600 !important;
}

/* Captions */
.stCaption, small, .stCaption p {
    color: #5a6a5a !important;
}

/* ── Dividers ───────────────────────────────────────────── */
hr {
    border-color: rgba(0, 224, 90, 0.10) !important;
    margin: 1.5rem 0 !important;
}

/* ── Cards — dark panels with green border ──────────────── */
div[data-testid="stExpander"] {
    background-color: #152015 !important;
    border: 1px solid rgba(0, 224, 90, 0.2) !important;
    border-radius: 12px !important;
    overflow: hidden;
}

div[data-testid="stExpander"] summary {
    color: #00e05a !important;
    font-weight: 600;
}

div[data-testid="stExpander"] .stMarkdown p {
    color: #8a9a8a !important;
}

/* ── Tabs ───────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background-color: #111b14 !important;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    color: #8a9a8a !important;
    background-color: transparent !important;
    border-radius: 8px !important;
    font-weight: 500;
    padding: 8px 20px;
}

.stTabs [aria-selected="true"] {
    color: #00e05a !important;
    background-color: rgba(0, 224, 90, 0.08) !important;
    border-bottom: none !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: #00e05a !important;
}

.stTabs [data-baseweb="tab-border"] {
    display: none;
}

/* ── Buttons — green gradient ───────────────────────────── */
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #00c04a 0%, #00e05a 50%, #00ff6a 100%) !important;
    color: #0a1a0f !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.65rem 1.5rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 0 20px rgba(0, 224, 90, 0.15) !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    box-shadow: 0 0 30px rgba(0, 224, 90, 0.35) !important;
    transform: translateY(-1px) !important;
}

/* Secondary buttons (like NASA fetch) */
.stButton > button[kind="secondary"],
.stButton > button[data-testid="stBaseButton-secondary"] {
    background-color: rgba(0, 224, 90, 0.08) !important;
    color: #00e05a !important;
    border: 1px solid rgba(0, 224, 90, 0.3) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.stButton > button[kind="secondary"]:hover,
.stButton > button[data-testid="stBaseButton-secondary"]:hover {
    background-color: rgba(0, 224, 90, 0.15) !important;
    border-color: #00e05a !important;
}

/* Link buttons */
.stLinkButton > a {
    background: linear-gradient(135deg, #00c04a 0%, #00e05a 100%) !important;
    color: #0a1a0f !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}

/* ── Input Widgets ──────────────────────────────────────── */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background-color: #152015 !important;
    color: #e0f0e0 !important;
    border: 1px solid rgba(0, 224, 90, 0.2) !important;
    border-radius: 8px !important;
}

.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus {
    border-color: #00e05a !important;
    box-shadow: 0 0 8px rgba(0, 224, 90, 0.2) !important;
}

/* Selectbox dropdown */
[data-baseweb="popover"] {
    background-color: #152015 !important;
    border: 1px solid rgba(0, 224, 90, 0.2) !important;
}

[data-baseweb="popover"] li {
    color: #c0d0c0 !important;
}

[data-baseweb="popover"] li:hover {
    background-color: rgba(0, 224, 90, 0.1) !important;
}

/* Slider */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: #00e05a !important;
}

.stSlider [data-testid="stThumbValue"] {
    color: #00e05a !important;
}

/* ── Metric cards (Streamlit native) ────────────────────── */
div[data-testid="stMetric"] {
    background-color: #152015 !important;
    border: 1px solid rgba(0, 224, 90, 0.2) !important;
    border-radius: 12px !important;
    padding: 1.2rem 1rem !important;
    text-align: center;
}

div[data-testid="stMetric"] label {
    color: #8a9a8a !important;
    text-transform: uppercase !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #00e05a !important;
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
    background-color: rgba(0, 224, 90, 0.06) !important;
    border: 1px solid rgba(0, 224, 90, 0.25) !important;
    border-radius: 12px !important;
}

div[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) {
    background-color: rgba(0, 150, 255, 0.06) !important;
    border: 1px solid rgba(0, 150, 255, 0.25) !important;
    border-radius: 12px !important;
}

div[data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) {
    background-color: rgba(255, 180, 0, 0.06) !important;
    border: 1px solid rgba(255, 180, 0, 0.25) !important;
    border-radius: 12px !important;
}

/* ── Map ────────────────────────────────────────────────── */
iframe {
    border-radius: 12px !important;
    border: 1px solid rgba(0, 224, 90, 0.15) !important;
}

/* ── Spinner ────────────────────────────────────────────── */
.stSpinner > div {
    border-top-color: #00e05a !important;
}

/* ── Scrollbar ──────────────────────────────────────────── */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: #0a1a0f;
}

::-webkit-scrollbar-thumb {
    background: rgba(0, 224, 90, 0.25);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 224, 90, 0.45);
}

/* ── Hide default sidebar navigation ──────────────────── */
[data-testid='stSidebarNav'] {
    display: none;
}
</style>
"""


def section_header_html(title: str) -> str:
    """Styled section header with green left accent bar."""
    return f"""
    <div style="
        border-left: 3px solid #00e05a;
        padding: 0.4rem 0 0.4rem 1rem;
        margin: 1.2rem 0 0.8rem;
    ">
        <span style="
            color: #ffffff;
            font-size: 1.15rem;
            font-weight: 700;
        ">{title}</span>
    </div>
    """


def welcome_hero_html(title: str, subtitle: str, intro: str) -> str:
    """HTML block for the welcome hero section at the top of the app."""
    return f"""
    <div style="text-align:center; padding:2.5rem 1rem 1rem;">
        <h1 style="
            font-size:2.8rem;
            font-weight:800;
            color:#00e05a !important;
            margin-bottom:0.3rem;
            text-shadow:0 0 40px rgba(0,224,90,0.25);
        ">{title}</h1>
        <p style="
            color:#8a9a8a !important;
            font-size:1.1rem;
            margin-top:0.2rem;
            margin-bottom:0.3rem;
        ">{subtitle}</p>
        <p style="
            color:#5a6a5a !important;
            font-size:0.88rem;
        ">{intro}</p>
    </div>
    <hr style="border-color:rgba(0,224,90,0.12); margin:0.5rem 0 1.5rem;">
    """


def svg_gauge_html(score: float, viability: str) -> str:
    """SVG circular gauge — dark ring with green arc proportional to score.

    Args:
        score: 0–100 feasibility score.
        viability: One of High / Medium / Low / Not Viable.

    Returns:
        HTML/SVG string for embedding in Streamlit.
    """
    # Arc colors per viability class
    arc_colors = {
        "High": "#00e05a",
        "Medium": "#ffb800",
        "Low": "#ff6644",
        "Not Viable": "#ff3c3c",
    }
    arc_color = arc_colors.get(viability, "#8a9a8a")

    badge_bg = {
        "High": "#00e05a",
        "Medium": "#ffb800",
        "Low": "#ff6644",
        "Not Viable": "#ff3c3c",
    }
    badge_text = {
        "High": "#0a1a0f",
        "Medium": "#1a1500",
        "Low": "#1a0a05",
        "Not Viable": "#1a0505",
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
    <div style="text-align:center; padding:1.5rem 0;">
        <svg width="160" height="160" viewBox="0 0 120 120"
             style="display:block; margin:0 auto;">
            <!-- background ring -->
            <circle cx="60" cy="60" r="{r}"
                    fill="none" stroke="#152015" stroke-width="10" />
            <!-- score arc -->
            <circle cx="60" cy="60" r="{r}"
                    fill="none" stroke="{arc_color}" stroke-width="10"
                    stroke-linecap="round"
                    stroke-dasharray="{circumference:.2f}"
                    stroke-dashoffset="{offset:.2f}"
                    transform="rotate(-90 60 60)"
                    style="transition: stroke-dashoffset 0.8s ease;" />
            <!-- score text -->
            <text x="60" y="56" text-anchor="middle" dominant-baseline="central"
                  fill="{arc_color}" font-size="26" font-weight="800"
                  font-family="sans-serif">{score:.0f}%</text>
            <text x="60" y="78" text-anchor="middle"
                  fill="#8a9a8a" font-size="8" font-weight="700"
                  font-family="sans-serif" letter-spacing="0.15em">SCORE</text>
        </svg>
        <!-- viability pill badge -->
        <div style="
            display:inline-block;
            background:{badge_bg.get(viability, '#8a9a8a')};
            color:{badge_text.get(viability, '#151515')};
            padding:0.35rem 1.4rem;
            border-radius:20px;
            font-size:0.72rem;
            font-weight:800;
            letter-spacing:0.12em;
            margin-top:0.6rem;
            text-transform:uppercase;
        ">{badge_label}</div>
    </div>
    """


def score_card_html(score: float, viability: str, lang: str = "EN") -> str:
    """Generate HTML for the large centered score display with viability badge."""
    badge_colors = {
        "High": ("#00e05a", "#0a1a0f"),
        "Medium": ("#ffb800", "#1a1500"),
        "Low": ("#ff6644", "#1a0a05"),
        "Not Viable": ("#ff3c3c", "#1a0505"),
    }
    bg, text_bg = badge_colors.get(viability, ("#8a9a8a", "#151515"))

    badge_label = {
        "High": "HIGH VIABILITY",
        "Medium": "MEDIUM VIABILITY",
        "Low": "LOW VIABILITY",
        "Not Viable": "NOT VIABLE",
    }.get(viability, viability.upper())

    return f"""
    <div style="
        background: #152015;
        border: 1px solid rgba(0,224,90,0.2);
        border-radius: 12px;
        padding: 2rem 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
    ">
        <div style="
            color: #8a9a8a;
            text-transform: uppercase;
            font-size: 0.7rem;
            letter-spacing: 0.12em;
            margin-bottom: 0.5rem;
            font-weight: 600;
        ">FEASIBILITY SCORE</div>
        <div style="
            color: #00e05a;
            font-size: 3.5rem;
            font-weight: 800;
            line-height: 1.1;
            text-shadow: 0 0 30px rgba(0,224,90,0.3);
        ">{score:.0f}%</div>
        <div style="
            display: inline-block;
            background: {bg};
            color: {text_bg};
            padding: 0.35rem 1.2rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            margin-top: 0.8rem;
            text-transform: uppercase;
        ">{badge_label}</div>
    </div>
    """


def metric_card_html(label: str, value: str, icon: str = "") -> str:
    """Generate HTML for a single metric card."""
    return f"""
    <div style="
        background: #152015;
        border: 1px solid rgba(0,224,90,0.2);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    ">
        <div style="
            color: #8a9a8a;
            text-transform: uppercase;
            font-size: 0.68rem;
            letter-spacing: 0.1em;
            font-weight: 600;
            margin-bottom: 0.5rem;
        ">{icon} {label}</div>
        <div style="
            color: #00e05a;
            font-size: 1.8rem;
            font-weight: 700;
            line-height: 1.2;
        ">{value}</div>
    </div>
    """


def not_viable_card_html(gate: str, reason: str, redirect: str | None = None) -> str:
    """Generate HTML for the Not Viable elimination card."""
    redirect_html = ""
    if redirect:
        redirect_html = f"""
        <div style="
            margin-top: 1rem;
            padding: 0.8rem 1rem;
            background: rgba(0, 150, 255, 0.06);
            border: 1px solid rgba(0, 150, 255, 0.25);
            border-radius: 8px;
            color: #66aaff;
            font-size: 0.85rem;
        ">Recommendation: {redirect}</div>
        """

    return f"""
    <div style="
        background: #1a0a0a;
        border: 1px solid rgba(255, 60, 60, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    ">
        <div style="
            color: #ff5555;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        ">SITE NOT VIABLE</div>
        <div style="
            color: #8a6a6a;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
            margin-bottom: 0.3rem;
        ">ELIMINATED BY GATE {gate}</div>
        <div style="color: #cc8888; font-size: 0.9rem; line-height: 1.5;">
            {reason}
        </div>
        {redirect_html}
    </div>
    """


def nasa_card_header_html(title: str = "Climate Data — NASA POWER") -> str:
    """HTML header for the NASA climate data card."""
    return f"""
    <div style="
        background: #152015;
        border: 1px solid rgba(0,224,90,0.2);
        border-radius: 12px 12px 0 0;
        padding: 1rem 1.5rem 0.5rem;
        margin-top: 0.5rem;
    ">
        <div style="
            color: #ffffff;
            font-size: 1.1rem;
            font-weight: 700;
        ">☀️ {title}</div>
        <div style="
            color: #5a6a5a;
            font-size: 0.75rem;
            margin-top: 0.2rem;
        ">Annual averages from satellite observations</div>
    </div>
    """


def gate_pass_html(gates: list[str]) -> str:
    """Generate HTML for gate pass checklist."""
    items = ""
    for g in gates:
        items += f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.4rem 0;
            color: #8a9a8a;
            font-size: 0.85rem;
        ">
            <span style="color: #00e05a; font-size: 1rem;">&#10003;</span>
            {g}
        </div>
        """
    return f"""
    <div style="
        background: #152015;
        border: 1px solid rgba(0,224,90,0.2);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 0.8rem 0;
    ">
        <div style="
            color: #8a9a8a;
            text-transform: uppercase;
            font-size: 0.68rem;
            letter-spacing: 0.1em;
            font-weight: 600;
            margin-bottom: 0.6rem;
        ">PRE-SCREENING GATES PASSED</div>
        {items}
    </div>
    """
