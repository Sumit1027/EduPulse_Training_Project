from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "Dataset" / "StudentPerformanceFactors_Cleaned.csv"
CSS_PATH = BASE_DIR / "assets" / "style.css"

def load_dataset():
    return pd.read_csv(DATA_PATH)


def get_dashboard_stats():
    df = load_dataset()

    return {
        "total_students": len(df),
        "total_features": len(df.columns) - 1,
        "average_score": round(df["Exam_Score"].mean(), 2),
        "highest_score": df["Exam_Score"].max(),
    }


def get_theme():
    """Returns the active theme: 'Light' or 'Dark'."""
    if "theme_mode" not in st.session_state:
        st.session_state["theme_mode"] = "Light"
    return st.session_state["theme_mode"]


def render_theme_toggle_sidebar():
    """Renders the Light / Dark theme switcher in the sidebar."""
    if "theme_mode" not in st.session_state:
        st.session_state["theme_mode"] = "Light"

    current_theme = st.session_state["theme_mode"]

    st.sidebar.markdown("### 🎨 Theme & Color Mode")
    
    # Segmented/Radio theme selector
    theme_selection = st.sidebar.radio(
        label="Select App Color Mode",
        options=["☀️ Light (White)", "🌙 Dark (Black)"],
        index=0 if current_theme == "Light" else 1,
        key="app_theme_radio",
        label_visibility="collapsed"
    )

    new_theme = "Light" if "Light" in theme_selection else "Dark"
    if new_theme != current_theme:
        st.session_state["theme_mode"] = new_theme
        st.rerun()

    st.sidebar.caption(f"Active Theme: **{new_theme} Mode**")
    st.sidebar.divider()


def get_dark_mode_css():
    """Returns CSS overrides for Dark (Black) mode."""
    return """
    <style>
    :root {
        --text-main: #F8FAFC !important;
        --text-muted: #94A3B8 !important;
        --surface-bg: #0B0F19 !important;
        --surface-card: #1E293B !important;
        --border-color: #334155 !important;
        --border-highlight: #6366F1 !important;
        --brand-dark: #A5B4FC !important;
        --card-gradient: linear-gradient(135deg, rgba(30,41,59,0.95) 0%, rgba(15,23,42,0.95) 100%) !important;
    }

    .stApp {
        background: 
            radial-gradient(circle at 10% 0%, rgba(99, 102, 241, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 90% 10%, rgba(129, 140, 248, 0.12) 0%, transparent 45%),
            radial-gradient(circle at 50% 90%, rgba(79, 70, 229, 0.08) 0%, transparent 50%),
            #090D16 !important;
        color: #F8FAFC !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, label, div, .stMarkdown {
        color: #F8FAFC;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D111D 0%, #080B12 100%) !important;
        border-right: 1px solid #1E293B !important;
    }

    section[data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }

    .metric-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        border: 1px solid #334155 !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4) !important;
    }

    .metric-card .title {
        color: #94A3B8 !important;
    }

    .metric-card .value {
        background: linear-gradient(135deg, #C7D2FE, #818CF8) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }

    .metric-card .subtitle {
        color: #94A3B8 !important;
    }

    .glass-container {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid #334155 !important;
        color: #F8FAFC !important;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.5) !important;
    }

    .glass-container h1, .glass-container h2, .glass-container h3, .glass-container h4, .glass-container p {
        color: #F8FAFC !important;
    }

    .step-card {
        background: #141B2D !important;
        border: 1px solid #334155 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }

    .step-body h4 {
        color: #F8FAFC !important;
    }

    .step-body p {
        color: #94A3B8 !important;
    }

    .univ-banner {
        background: #020617 !important;
        border: 1px solid #1E293B !important;
        color: #E2E8F0 !important;
    }

    .callout-box {
        background: rgba(6, 78, 59, 0.3) !important;
        border-left: 4px solid #10B981 !important;
        color: #D1FAE5 !important;
    }

    .callout-box.info {
        background: rgba(30, 27, 75, 0.6) !important;
        border-left: 4px solid #818CF8 !important;
        color: #E0E7FF !important;
    }

    .callout-box.info h4 {
        color: #C7D2FE !important;
    }

    .callout-box.warning {
        background: rgba(69, 26, 3, 0.4) !important;
        border-left: 4px solid #F59E0B !important;
        color: #FEF3C7 !important;
    }

    [data-baseweb="input"], [data-baseweb="select"], .stTextInput > div > div, .stNumberInput > div > div {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border-color: #334155 !important;
    }

    [data-baseweb="select"] * {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
    }

    [data-baseweb="popover"], [data-baseweb="menu"] {
        background-color: #1E293B !important;
    }

    [data-baseweb="menu"] * {
        color: #F8FAFC !important;
    }

    div[data-testid="stFileUploader"] {
        background: #141B2D !important;
        border: 1px dashed #475569 !important;
    }

    div[data-testid="stFileUploader"] * {
        color: #E2E8F0 !important;
    }

    button[data-baseweb="tab"] {
        color: #94A3B8 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #818CF8 !important;
        border-bottom-color: #818CF8 !important;
    }

    hr {
        border-color: #334155 !important;
    }

    [data-testid="stDataFrame"] {
        background-color: #0F172A !important;
        border: 1px solid #334155 !important;
    }

    .stCaption {
        color: #94A3B8 !important;
    }
    </style>
    """


def setup_theme():
    """
    Main entrypoint for every page.
    Renders sidebar toggle, loads base styles, and injects dark mode if chosen.
    """
    if CSS_PATH.exists():
        with open(CSS_PATH) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    render_theme_toggle_sidebar()

    if get_theme() == "Dark":
        st.markdown(get_dark_mode_css(), unsafe_allow_html=True)


def get_plotly_layout_params():
    """Returns Plotly layout dictionary matching the current Light/Dark theme."""
    is_dark = get_theme() == "Dark"
    
    return {
        "template": "plotly_dark" if is_dark else "plotly_white",
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": "Plus Jakarta Sans",
            "color": "#F8FAFC" if is_dark else "#0F172A"
        }
    }