import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from pathlib import Path
from utils.data_loader import load_dataset, setup_theme, get_plotly_layout_params

st.set_page_config(
    page_title="Analytics - EduPulse",
    page_icon="📊",
    layout="wide"
)

# Apply Theme
setup_theme()
plotly_layout = get_plotly_layout_params()

st.title("📊 Exploratory Data Analytics Studio")
st.markdown("Interactively inspect feature correlations, distribution shapes, and socioeconomic score drivers across 6,607 student observations.")

st.divider()

df = load_dataset()

# Filter sidebar / header controls
st.subheader("🔍 Demographic & Socioeconomic Data Filters")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    gender_filter = st.multiselect("Gender", options=df["Gender"].unique(), default=df["Gender"].unique())
with col_f2:
    income_filter = st.multiselect("Family Income", options=df["Family_Income"].unique(), default=df["Family_Income"].unique())
with col_f3:
    school_filter = st.multiselect("School Type", options=df["School_Type"].unique(), default=df["School_Type"].unique())

filtered_df = df[
    (df["Gender"].isin(gender_filter)) & 
    (df["Family_Income"].isin(income_filter)) &
    (df["School_Type"].isin(school_filter))
]

st.caption(f"Showing **{len(filtered_df):,}** out of **{len(df):,}** student records.")

st.divider()

st.subheader("🔥 Feature Correlation Heatmap")
numeric_df = filtered_df.select_dtypes(include="number")
corr = numeric_df.corr()

fig_corr = ff.create_annotated_heatmap(
    z=corr.values,
    x=list(corr.columns),
    y=list(corr.index),
    annotation_text=corr.round(2).values,
    colorscale="Viridis",
    showscale=True
)
fig_corr.update_layout(
    height=550,
    margin=dict(l=20, r=20, t=30, b=20),
    template=plotly_layout["template"],
    font=plotly_layout["font"],
    paper_bgcolor=plotly_layout["paper_bgcolor"],
    plot_bgcolor=plotly_layout["plot_bgcolor"]
)
st.plotly_chart(fig_corr, use_container_width=True)

st.divider()

st.subheader("📌 Key Behavioral & Academic Score Drivers")

col_a1, col_a2 = st.columns(2)

with col_a1:
    cat_factor = st.selectbox("Categorical Attribute for Boxplot Analysis", [
        "Parental_Involvement", "Access_to_Resources", "Motivation_Level",
        "Teacher_Quality", "School_Type", "Parental_Education_Level", "Peer_Influence"
    ])
    
    fig_box = px.box(
        filtered_df,
        x=cat_factor,
        y="Exam_Score",
        color=cat_factor,
        title=f"Exam Score Distribution by {cat_factor.replace('_', ' ')}",
        color_discrete_sequence=px.colors.qualitative.Set2,
        template=plotly_layout["template"]
    )
    fig_box.update_layout(
        font=plotly_layout["font"],
        paper_bgcolor=plotly_layout["paper_bgcolor"],
        plot_bgcolor=plotly_layout["plot_bgcolor"]
    )
    st.plotly_chart(fig_box, use_container_width=True)

with col_a2:
    num_factor = st.selectbox("Numeric Factor for Trendline Scatter Plot", [
        "Hours_Studied", "Attendance", "Sleep_Hours", "Previous_Scores", "Tutoring_Sessions"
    ])
    
    fig_scatter = px.scatter(
        filtered_df.sample(min(1500, len(filtered_df)), random_state=42),
        x=num_factor,
        y="Exam_Score",
        color="Parental_Involvement",
        trendline="ols",
        title=f"{num_factor.replace('_', ' ')} vs Exam Score (OLS Trendline)",
        color_discrete_map={"Low": "#EF4444", "Medium": "#F59E0B", "High": "#10B981"},
        template=plotly_layout["template"]
    )
    fig_scatter.update_layout(
        font=plotly_layout["font"],
        paper_bgcolor=plotly_layout["paper_bgcolor"],
        plot_bgcolor=plotly_layout["plot_bgcolor"]
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
