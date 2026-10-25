import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from utils.predictor import predict_exam_score, explain_prediction, encoders
from utils.pdf_generator import generate_student_pdf_report
from utils.data_loader import setup_theme, get_plotly_layout_params

st.set_page_config(
    page_title="Predict Score - EduPulse",
    page_icon="🎯",
    layout="wide"
)

# Apply Theme
setup_theme()
plotly_layout = get_plotly_layout_params()

st.title("🎯 Single Student Academic Diagnosis")
st.markdown("Enter student parameters across academic, personal, and environmental dimensions to calculate predicted exam performance and generate a formal PDF report.")

st.divider()

# Student Identity Header Inputs
st.subheader("👤 Student Identification")
col_id1, col_id2 = st.columns(2)
with col_id1:
    student_name = st.text_input("Student Full Name", value="Alex Morgan", help="Enter student's full name for the report")
with col_id2:
    student_id = st.text_input("Student Roll / ID Number", value="EDU-2026-8942", help="Unique identifier for record keeping")

st.divider()

# Input Forms organized into Tabs
st.subheader("📝 Student Feature Inputs (19 Parameters)")
tab_academic, tab_personal, tab_environment = st.tabs([
    "📚 Academic & Study Habits",
    "🧘 Personal & Lifestyle Factors",
    "🏡 Environment & Socioeconomic"
])

with tab_academic:
    col1, col2, col3 = st.columns(3)
    with col1:
        hours = st.slider("Hours Studied per Week", 1, 20, 8, help="Weekly self-study hours")
        attendance = st.slider("Class Attendance (%)", 40, 100, 85, help="Percentage of school days attended")
        previous_scores = st.slider("Previous Exam Score", 30, 100, 75, help="Past term examination score")
    with col2:
        tutoring_sessions = st.slider("Tutoring Sessions / Month", 0, 10, 2)
        teacher_quality = st.selectbox("Teacher Quality", ["Low", "Medium", "High"], index=1)
        access = st.selectbox("Access to Educational Resources", ["Low", "Medium", "High"], index=1)
    with col3:
        learning_disabilities = st.selectbox("Learning Disabilities", ["No", "Yes"], index=0)
        school_type = st.selectbox("School Type", ["Public", "Private"], index=0)

with tab_personal:
    col1, col2, col3 = st.columns(3)
    with col1:
        sleep_hours = st.slider("Sleep Hours per Night", 4, 12, 7)
        physical_activity = st.slider("Physical Activity (Hours/Week)", 0, 14, 4)
    with col2:
        motivation = st.selectbox("Motivation Level", ["Low", "Medium", "High"], index=1)
        extracurricular = st.selectbox("Extracurricular Activities", ["No", "Yes"], index=1)
    with col3:
        gender = st.selectbox("Gender", ["Male", "Female"], index=0)
        peer_influence = st.selectbox("Peer Influence", ["Negative", "Neutral", "Positive"], index=2)

with tab_environment:
    col1, col2, col3 = st.columns(3)
    with col1:
        parental = st.selectbox("Parental Involvement", ["Low", "Medium", "High"], index=1)
        parent_education = st.selectbox("Parental Education Level", ["High School", "College", "Postgraduate"], index=1)
    with col2:
        family_income = st.selectbox("Family Income Level", ["Low", "Medium", "High"], index=1)
        internet = st.selectbox("Internet Access at Home", ["No", "Yes"], index=1)
    with col3:
        distance = st.selectbox("Distance from Home to School", ["Near", "Moderate", "Far"], index=0)

st.divider()

col_btn1, col_btn2 = st.columns([1, 4])

with col_btn1:
    predict_clicked = st.button("🚀 Calculate Prediction", use_container_width=True, type="primary")

if predict_clicked:
    raw_dict = {
        "Hours_Studied": hours,
        "Attendance": attendance,
        "Parental_Involvement": parental,
        "Access_to_Resources": access,
        "Extracurricular_Activities": extracurricular,
        "Sleep_Hours": sleep_hours,
        "Previous_Scores": previous_scores,
        "Motivation_Level": motivation,
        "Internet_Access": internet,
        "Tutoring_Sessions": tutoring_sessions,
        "Family_Income": family_income,
        "Teacher_Quality": teacher_quality,
        "School_Type": school_type,
        "Peer_Influence": peer_influence,
        "Physical_Activity": physical_activity,
        "Learning_Disabilities": learning_disabilities,
        "Parental_Education_Level": parent_education,
        "Distance_from_Home": distance,
        "Gender": gender
    }
    
    encoded_dict = raw_dict.copy()
    for col, enc in encoders.items():
        encoded_dict[col] = enc.transform([raw_dict[col]])[0]
        
    df_student = pd.DataFrame([encoded_dict])
    
    predicted_score = predict_exam_score(df_student)
    df_explain = explain_prediction(df_student)
    
    r_score = round(float(predicted_score))
    if r_score >= 80:
        perf_status = "Excellent Academic Standing ⭐"
        badge_class = "badge-excellent"
        recommendation = "The student demonstrates exemplary academic habits! Encourage them to maintain their current study routine and consider peer mentoring."
    elif r_score >= 60:
        perf_status = "Good Academic Standing 👍"
        badge_class = "badge-good"
        recommendation = "Solid academic foundation. To move into top performance tier, focus on boosting study consistency and attending additional tutoring sessions."
    elif r_score >= 40:
        perf_status = "Average - Needs Academic Boost 📘"
        badge_class = "badge-average"
        recommendation = "Moderate risk of underperformance. Increase weekly self-study hours, improve class attendance above 85%, and review weak subject areas."
    else:
        perf_status = "High Academic Risk ⚠️"
        badge_class = "badge-risk"
        recommendation = "Urgent attention required! Arrange teacher counseling, establish structured daily study hours, and eliminate learning barriers."

    st.session_state["last_prediction"] = {
        "student_name": student_name,
        "student_id": student_id,
        "score": predicted_score,
        "status": perf_status,
        "badge": badge_class,
        "recommendation": recommendation,
        "raw_info": raw_dict,
        "df_explain": df_explain
    }

# Display Diagnostic Results
if "last_prediction" in st.session_state:
    res = st.session_state["last_prediction"]
    
    st.subheader("📊 Diagnostic Results & Analysis")
    
    res_col1, res_col2 = st.columns([1, 1.4])
    
    with res_col1:
        st.markdown(f"""
        <div class="glass-container" style="text-align: center;">
            <h4 style="color: #64748B; margin-bottom: 0;">Predicted Exam Score for <b>{res['student_name']}</b></h4>
            <h1 style="font-size: 58px; font-weight: 800; color: #312E81; margin: 12px 0;">{res['score']:.2f} <span style="font-size: 24px; color: #64748B;">/ 100</span></h1>
            <span class="badge {res['badge']}">{res['status']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Gauge Chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = res['score'],
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#4F46E5"},
                'steps': [
                    {'range': [0, 40], 'color': "#FEE2E2"},
                    {'range': [40, 60], 'color': "#FEF3C7"},
                    {'range': [60, 80], 'color': "#E0E7FF"},
                    {'range': [80, 100], 'color': "#DCFCE7"}
                ],
            }
        ))
        fig_gauge.update_layout(
            height=220,
            margin=dict(l=20, r=20, t=10, b=10),
            template=plotly_layout["template"],
            font=plotly_layout["font"],
            paper_bgcolor=plotly_layout["paper_bgcolor"],
            plot_bgcolor=plotly_layout["plot_bgcolor"]
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Printable PDF Download
        pdf_bytes = generate_student_pdf_report(
            student_info=res["raw_info"],
            predicted_score=res["score"],
            performance=res["status"],
            recommendation=res["recommendation"],
            student_name=res["student_name"],
            student_id=res["student_id"]
        )
        
        clean_filename = res['student_name'].replace(" ", "_")
        st.download_button(
            label="📄 Download Official PDF Diagnostic Report",
            data=pdf_bytes,
            file_name=f"EduPulse_Report_{clean_filename}_{res['score']:.0f}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )

    with res_col2:
        st.markdown(f"""
        <div class="glass-container">
            <h4 style="margin-top:0;">💡 Personal Action Plan</h4>
            <p style="font-size: 15px; line-height: 1.6;">{res['recommendation']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("##### 🔍 Top Drivers Influencing This Prediction")
        top_drivers = res["df_explain"].head(7)
        
        fig = px.bar(
            top_drivers,
            x="Contribution",
            y="Feature",
            orientation="h",
            color="Impact",
            color_discrete_map={"Positive": "#4F46E5", "Negative": "#EF4444"},
            title="Feature Contributions (Positive vs Negative)",
            template=plotly_layout["template"]
        )
        fig.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=30, b=10),
            font=plotly_layout["font"],
            paper_bgcolor=plotly_layout["paper_bgcolor"],
            plot_bgcolor=plotly_layout["plot_bgcolor"]
        )
        st.plotly_chart(fig, use_container_width=True)