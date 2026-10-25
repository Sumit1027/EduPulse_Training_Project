import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from utils.predictor import predict_exam_score, encoders
from utils.data_loader import setup_theme, get_plotly_layout_params

st.set_page_config(
    page_title="Performance Simulator - EduPulse",
    page_icon="⚡",
    layout="wide"
)

# Apply Theme
setup_theme()
plotly_layout = get_plotly_layout_params()

st.title("⚡ Performance Simulator & Habit Lab")
st.markdown(r"Experiment with lifestyle and study habit adjustments to calculate the real-time predicted score gain ($\Delta$).")

st.divider()

# Quick Presets Bar
st.subheader("⚡ Quick Intervention Presets")
preset_col1, preset_col2, preset_col3 = st.columns(3)

if "sim_h_val" not in st.session_state:
    st.session_state["sim_h_val"] = 7
if "sim_a_val" not in st.session_state:
    st.session_state["sim_a_val"] = 85
if "sim_t_val" not in st.session_state:
    st.session_state["sim_t_val"] = 3

with preset_col1:
    if st.button("🚀 +3 Study Hours Sprint", use_container_width=True):
        st.session_state["sim_h_val"] = 9
        st.session_state["sim_a_val"] = 85
        st.session_state["sim_t_val"] = 3

with preset_col2:
    if st.button("📈 +15% Attendance Focus", use_container_width=True):
        st.session_state["sim_h_val"] = 7
        st.session_state["sim_a_val"] = 95
        st.session_state["sim_t_val"] = 3

with preset_col3:
    if st.button("🎓 Intensive Tutoring (+3 Sessions)", use_container_width=True):
        st.session_state["sim_h_val"] = 8
        st.session_state["sim_a_val"] = 90
        st.session_state["sim_t_val"] = 5

st.write("")

col_base, col_sim = st.columns(2)

with col_base:
    st.markdown("""
    <div class="glass-container">
        <h3>📌 Baseline Profile</h3>
        <p style="color: #64748B;">Current student academic baseline parameters.</p>
    </div>
    """, unsafe_allow_html=True)
    
    base_hours = st.slider("Baseline Study Hours/Week", 1, 15, 4, key="b_h")
    base_attendance = st.slider("Baseline Attendance (%)", 50, 100, 70, key="b_a")
    base_tutoring = st.slider("Baseline Tutoring Sessions", 0, 8, 1, key="b_t")
    base_prev = st.slider("Previous Exam Score Baseline", 40, 100, 65, key="b_p")

with col_sim:
    st.markdown("""
    <div class="glass-container" style="border-color: #4F46E5;">
        <h3 style="color: #4F46E5;">🚀 Simulated Scenario</h3>
        <p style="color: #64748B;">Adjust parameters to test score improvements.</p>
    </div>
    """, unsafe_allow_html=True)
    
    sim_hours = st.slider("Simulated Study Hours/Week", 1, 15, st.session_state["sim_h_val"], key="s_h")
    sim_attendance = st.slider("Simulated Attendance (%)", 50, 100, st.session_state["sim_a_val"], key="s_a")
    sim_tutoring = st.slider("Simulated Tutoring Sessions", 0, 8, st.session_state["sim_t_val"], key="s_t")
    sim_prev = base_prev  # Past score remains fixed

# Default feature mapping
default_categorical = {
    "Parental_Involvement": "Medium",
    "Access_to_Resources": "Medium",
    "Extracurricular_Activities": "Yes",
    "Sleep_Hours": 7,
    "Motivation_Level": "Medium",
    "Internet_Access": "Yes",
    "Family_Income": "Medium",
    "Teacher_Quality": "Medium",
    "School_Type": "Public",
    "Peer_Influence": "Positive",
    "Physical_Activity": 4,
    "Learning_Disabilities": "No",
    "Parental_Education_Level": "College",
    "Distance_from_Home": "Near",
    "Gender": "Female"
}

def build_encoded_df(h, a, t, p):
    data = default_categorical.copy()
    data["Hours_Studied"] = h
    data["Attendance"] = a
    data["Tutoring_Sessions"] = t
    data["Previous_Scores"] = p
    
    encoded = {}
    for k, v in data.items():
        if k in encoders:
            encoded[k] = encoders[k].transform([v])[0]
        else:
            encoded[k] = v
            
    ordered_cols = [
        "Hours_Studied", "Attendance", "Parental_Involvement", "Access_to_Resources",
        "Extracurricular_Activities", "Sleep_Hours", "Previous_Scores", "Motivation_Level",
        "Internet_Access", "Tutoring_Sessions", "Family_Income", "Teacher_Quality",
        "School_Type", "Peer_Influence", "Physical_Activity", "Learning_Disabilities",
        "Parental_Education_Level", "Distance_from_Home", "Gender"
    ]
    
    return pd.DataFrame([{col: encoded[col] for col in ordered_cols}])

df_base = build_encoded_df(base_hours, base_attendance, base_tutoring, base_prev)
df_sim = build_encoded_df(sim_hours, sim_attendance, sim_tutoring, sim_prev)

base_score = predict_exam_score(df_base)
sim_score = predict_exam_score(df_sim)
delta = round(sim_score - base_score, 2)

st.divider()

st.subheader("🎯 Comparative Simulation Results")

res_col1, res_col2, res_col3 = st.columns(3)

with res_col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="title">Baseline Predicted Score</div>
        <div class="value">{base_score:.2f}</div>
        <div class="subtitle">Current Habit Level</div>
    </div>
    """, unsafe_allow_html=True)

with res_col2:
    st.markdown(f"""
    <div class="metric-card" style="border: 2px solid #4F46E5;">
        <div class="title">Simulated Score</div>
        <div class="value" style="color: #4F46E5;">{sim_score:.2f}</div>
        <div class="subtitle">With Improved Habits</div>
    </div>
    """, unsafe_allow_html=True)

with res_col3:
    delta_color = "#15803D" if delta >= 0 else "#B91C1C"
    delta_sign = "+" if delta >= 0 else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="title">Potential Score Gain</div>
        <div class="value" style="color: {delta_color};">{delta_sign}{delta:.2f}</div>
        <div class="subtitle">Estimated Point Improvement</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Target score indicator gauge
fig = go.Figure()

fig.add_trace(go.Indicator(
    mode = "number+gauge+delta",
    value = sim_score,
    delta = {'reference': base_score, 'increasing': {'color': "green"}},
    title = {'text': "Simulated Target Score Gauge"},
    gauge = {
        'axis': {'range': [None, 100]},
        'bar': {'color': "#4F46E5"},
        'steps': [
            {'range': [0, 40], 'color': "#FEE2E2"},
            {'range': [40, 60], 'color': "#FEF3C7"},
            {'range': [60, 80], 'color': "#E0E7FF"},
            {'range': [80, 100], 'color': "#DCFCE7"}
        ],
    },
    domain = {'x': [0, 1], 'y': [0, 1]}
))

fig.update_layout(
    height=320,
    margin=dict(l=20, r=20, t=40, b=20),
    template=plotly_layout["template"],
    font=plotly_layout["font"],
    paper_bgcolor=plotly_layout["paper_bgcolor"],
    plot_bgcolor=plotly_layout["plot_bgcolor"]
)
st.plotly_chart(fig, use_container_width=True)
