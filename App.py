import streamlit as st
import plotly.express as px
from pathlib import Path
from utils.data_loader import get_dashboard_stats, load_dataset, setup_theme, get_plotly_layout_params

# Page Configuration
st.set_page_config(
    page_title="App - EduPulse Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Theme (Base CSS + Sidebar Switcher + Dark/Light injection)
setup_theme()

# Sidebar Branding
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-card">
        <div style="font-size: 38px;">🎓</div>
        <h2>EduPulse</h2>
        <p>Academic Analytics & Performance Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📌 Navigation Guide")
    st.markdown("""
    - 🏠 **App**: Executive Overview & Statistics
    - 🎯 **Predict**: Single Student Diagnosis & PDF Report
    - ⚡ **Performance Simulator**: Interactive Habit Lab
    - 📂 **Bulk Prediction**: Batch CSV Processing
    - 📊 **Analytics**: Exploratory Data Visualizations
    - ℹ️ **About**: Model Benchmarks & Architecture
    """)
    st.divider()

# Header Banner
st.markdown("""
<div class="univ-banner">
    <span>🎓 <b>EDUPULSE ACADEMIC PLATFORM</b> | Machine Learning & Data Analytics System</span>
    <span><b>Version:</b> 1.0 Production</span>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-card">
    <span class="hero-eyebrow">✨ MACHINE LEARNING · EDUCATIONAL DATA SCIENCE</span>
    <h1>🎓 EduPulse Platform</h1>
    <p>Welcome to <b>EduPulse</b> — an end-to-end Machine Learning ecosystem engineered to accurately predict student academic performance, diagnose behavioral & lifestyle risk factors, and empower educators with actionable, data-backed interventions.</p>
</div>
""", unsafe_allow_html=True)

# Live Metric Summary Row
stats = get_dashboard_stats()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="icon">📚</div>
        <div class="title">Dataset Records</div>
        <div class="value">{stats["total_students"]:,}</div>
        <div class="subtitle">Cleaned Student Profiles</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="icon">🧬</div>
        <div class="title">Evaluated Factors</div>
        <div class="value">{stats["total_features"]}</div>
        <div class="subtitle">Academic & Environmental</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="icon">🎯</div>
        <div class="title">Model Accuracy</div>
        <div class="value">68.88%</div>
        <div class="subtitle">R² Score Benchmark</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="icon">⚡</div>
        <div class="title">Mean Error (MAE)</div>
        <div class="value">1.02</div>
        <div class="subtitle">Precision Mark Margin</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

# Interactive Insights Dashboard
df = load_dataset()
plotly_layout = get_plotly_layout_params()

st.subheader("📈 Dataset & Performance Distribution Overview")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    fig1 = px.histogram(
        df,
        x="Exam_Score",
        nbins=30,
        title="Distribution of Exam Scores Across 6,607 Students",
        color_discrete_sequence=["#4F46E5"],
        template=plotly_layout["template"]
    )
    fig1.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=340,
        font=plotly_layout["font"],
        paper_bgcolor=plotly_layout["paper_bgcolor"],
        plot_bgcolor=plotly_layout["plot_bgcolor"]
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    fig2 = px.scatter(
        df.sample(min(1200, len(df)), random_state=42),
        x="Attendance",
        y="Exam_Score",
        color="Parental_Involvement",
        size="Hours_Studied",
        title="Attendance vs Exam Score (Sized by Study Hours)",
        color_discrete_map={"Low": "#EF4444", "Medium": "#F59E0B", "High": "#10B981"},
        template=plotly_layout["template"]
    )
    fig2.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=340,
        font=plotly_layout["font"],
        paper_bgcolor=plotly_layout["paper_bgcolor"],
        plot_bgcolor=plotly_layout["plot_bgcolor"]
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ML Pipeline Roadmap Section
st.subheader("⚙️ Machine Learning Pipeline Architecture")

st.markdown("""
<div class="step-card">
    <div class="step-number">1</div>
    <div class="step-body">
        <h4>Data Ingestion & Preprocessing</h4>
        <p>Cleaned 6,600+ student observations, handled null values via median/mode imputation, and structured 19 academic & environmental parameters.</p>
    </div>
</div>
<div class="step-card">
    <div class="step-number">2</div>
    <div class="step-body">
        <h4>Exploratory Data Analysis (EDA)</h4>
        <p>Computed correlation matrices and identified key drivers: Study hours (r = 0.62) and attendance (r = 0.58) strongly dictate exam results.</p>
    </div>
</div>
<div class="step-card">
    <div class="step-number">3</div>
    <div class="step-body">
        <h4>Feature Engineering & Normalization</h4>
        <p>Encoded 13 categorical factors using LabelEncoder and normalized numeric ranges via StandardScaler for zero mean and unit variance.</p>
    </div>
</div>
<div class="step-card">
    <div class="step-number">4</div>
    <div class="step-body">
        <h4>Model Training & Hyperparameter Tuning</h4>
        <p>Trained Multiple Linear Regression, Ridge, Decision Tree, and Random Forest models. Linear Regression achieved the top score (R² = 68.88%).</p>
    </div>
</div>
<div class="step-card">
    <div class="step-number">5</div>
    <div class="step-body">
        <h4>Web Platform & Automated Diagnostics</h4>
        <p>Integrated trained model artifacts into Streamlit with single-student PDF diagnostic generation, Performance Simulator, and batch CSV prediction.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")
st.success("👉 Select a module from the **Sidebar Navigation** on the left to begin exploring predictions and analytics.")


import sys
from streamlit.web import cli as stcli
sys.argv = ["streamlit", "run", __file__]
