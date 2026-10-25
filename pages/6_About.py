import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from utils.data_loader import setup_theme, get_plotly_layout_params

st.set_page_config(
    page_title="About & System Specs - EduPulse",
    page_icon="ℹ️",
    layout="wide"
)

# Apply Theme
setup_theme()
plotly_layout = get_plotly_layout_params()

st.title("ℹ️ About EduPulse & Machine Learning Specifications")
st.markdown("Comprehensive technical documentation, model cross-validation benchmarks, and project architecture specifications.")

st.divider()

col_desc, col_metrics = st.columns([1.2, 1])

with col_desc:
    st.subheader("🎓 Project Architecture & Overview")
    st.markdown("""
    **EduPulse** is an end-to-end Machine Learning solution developed for predicting student examination performance and identifying early behavioral risk indicators.
    
    The platform bridges data engineering, machine learning modeling, and web application deployment to assist educators and academic counselors in proactive student support.
    """)
    
    st.markdown(r"""
    ### 🎯 Key System Deliverables
    1. **Supervised Regression Modeling**: Predict continuous examination scores based on 19 student factors.
    2. **Risk Tier Stratification**: Classify students into 4 performance tiers (*Excellent, Good, Average, At-Risk*).
    3. **Performance Simulator**: Allow real-time scenario testing ($\Delta$ score gain) for habit adjustments.
    4. **Batch CSV Processing**: Ingest student datasets for automated batch risk diagnosis.
    5. **ReportLab PDF Engine**: Export printable, formal academic diagnostic reports.
    """)

with col_metrics:
    st.subheader("🤖 Machine Learning Algorithm Benchmarks")
    
    m_data = {
        "Model Architecture": ["Linear Regression (Selected)", "Ridge Regression", "Random Forest Regressor", "Decision Tree Regressor"],
        "R² Score (%)": [68.88, 68.86, 67.13, 58.40],
        "MAE (Marks)": [1.02, 1.02, 1.15, 1.48],
        "RMSE (Marks)": [2.10, 2.10, 2.22, 2.76],
        "Status": ["🏆 Deployed", "Benchmark", "Benchmark", "Baseline"]
    }
    df_metrics = pd.DataFrame(m_data)
    st.dataframe(df_metrics, use_container_width=True)
    
    fig_comp = px.bar(
        df_metrics,
        x="Model Architecture",
        y="R² Score (%)",
        color="Model Architecture",
        text="R² Score (%)",
        title="Model Accuracy Comparison (R² Score)",
        color_discrete_sequence=["#4F46E5", "#6366F1", "#818CF8", "#CBD5E1"],
        template=plotly_layout["template"]
    )
    fig_comp.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig_comp.update_layout(
        height=280,
        margin=dict(l=10, r=10, t=35, b=10),
        font=plotly_layout["font"],
        paper_bgcolor=plotly_layout["paper_bgcolor"],
        plot_bgcolor=plotly_layout["plot_bgcolor"]
    )
    st.plotly_chart(fig_comp, use_container_width=True)

st.divider()

st.subheader("🛠️ Technology Stack & Engineering Libraries")

t_col1, t_col2, t_col3, t_col4 = st.columns(4)

with t_col1:
    st.markdown("""
    **Core & Data Science**
    - Python 3.10+
    - Pandas (Dataframes)
    - NumPy (Vector math)
    """)

with t_col2:
    st.markdown("""
    **Machine Learning**
    - Scikit-Learn
    - StandardScaler
    - LabelEncoder
    - Joblib Artifacts
    """)

with t_col3:
    st.markdown("""
    **Frontend & Web UI**
    - Streamlit Framework
    - Custom Glassmorphism CSS
    - Plotly & Feature Factory
    """)

with t_col4:
    st.markdown("""
    **Reporting & Tools**
    - ReportLab PDF Engine
    - Batch CSV Processor
    - Git & VS Code
    """)

st.divider()

st.markdown("""
<div class="callout-box info">
    <h4 style="margin: 0 0 6px 0; color: #312E81;">🎓 EduPulse - Intelligent Student Performance Platform</h4>
    <p style="margin: 0; color: #4338CA; font-size: 14px;">
        <b>Domain:</b> Machine Learning, Data Analytics & Educational Systems<br/>
        <b>Platform Architecture:</b> End-to-End Supervised ML Pipeline & Web Application
    </p>
</div>
""", unsafe_allow_html=True)
