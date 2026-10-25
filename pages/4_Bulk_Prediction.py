import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from utils.bulk_predictor import process_bulk_predictions, REQUIRED_COLUMNS
from utils.data_loader import load_dataset, setup_theme, get_plotly_layout_params

st.set_page_config(
    page_title="Bulk CSV Prediction - EduPulse",
    page_icon="📂",
    layout="wide"
)

# Apply Theme
setup_theme()
plotly_layout = get_plotly_layout_params()

st.title("📂 Bulk Student CSV Prediction & Batch Risk Assessment")
st.markdown("Upload a student dataset CSV containing feature attributes to generate batch exam score predictions, filter across multi-dimensional criteria, and download annotated reports.")

st.divider()

col_up, col_info = st.columns([2, 1])

with col_up:
    uploaded_file = st.file_uploader("Upload Student Dataset CSV File (.csv)", type=["csv"])

with col_info:
    st.info("""
    **CSV Template Instructions:**
    - File must include feature headers (`Hours_Studied`, `Attendance`, `Parental_Involvement`, etc.).
    - Use the buttons below to load sample records or download a CSV template.
    """)
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        if st.button("📥 Load 200 Samples", use_container_width=True):
            st.session_state["sample_loaded"] = True
    with col_t2:
        # Generate Sample Template CSV
        sample_template_df = load_dataset().head(10)[REQUIRED_COLUMNS]
        template_csv = sample_template_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download CSV Template",
            data=template_csv,
            file_name="EduPulse_Student_Batch_Template.csv",
            mime="text/csv",
            use_container_width=True
        )

if "sample_loaded" in st.session_state and st.session_state["sample_loaded"] and not uploaded_file:
    df_raw = load_dataset().sample(min(200, len(load_dataset())), random_state=42)[REQUIRED_COLUMNS]
    st.success("Successfully loaded 200 sample student records from dataset.")
elif uploaded_file:
    try:
        df_raw = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        df_raw = None
else:
    df_raw = None

if df_raw is not None:
    st.subheader("📋 Dataset Preview")
    st.dataframe(df_raw.head(5), use_container_width=True)
    
    if st.button("⚡ Execute Batch Prediction Engine", type="primary"):
        with st.spinner("Processing batch predictions with Scikit-Learn model pipeline..."):
            df_result, summary, error = process_bulk_predictions(df_raw)
            
            if error:
                st.error(error)
            else:
                st.session_state["bulk_result"] = {
                    "df": df_result,
                    "summary": summary
                }

if "bulk_result" in st.session_state:
    res = st.session_state["bulk_result"]
    df_res = res["df"]
    
    st.divider()
    
    col_hdr1, col_hdr2 = st.columns([3, 1])
    with col_hdr1:
        st.subheader("🔍 Student Risk & Performance Filters")
        st.markdown("Filter batch student records across performance classification tiers, score ranges, and attendance.")
    with col_hdr2:
        st.write("")
        reset_filters = st.button("🔄 Reset All Filters", use_container_width=True)

    if reset_filters:
        for key in ["f_cat", "f_gen", "f_score", "f_att", "f_search"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    with st.expander("⚙️ Click to Open / Adjust Student Filters", expanded=True):
        f_col1, f_col2 = st.columns(2)

        # 1. Performance Tier Multi-select
        all_cats = list(df_res["Performance_Category"].unique()) if "Performance_Category" in df_res.columns else []
        with f_col1:
            sel_categories = st.multiselect(
                "🎯 Risk / Performance Category",
                options=all_cats,
                default=all_cats,
                key="f_cat",
                help="Filter by student academic performance classification"
            )

        # 2. Gender Multi-select
        all_genders = list(df_res["Gender"].dropna().unique()) if "Gender" in df_res.columns else []
        with f_col2:
            sel_genders = st.multiselect(
                "👤 Gender",
                options=all_genders,
                default=all_genders,
                key="f_gen"
            ) if all_genders else []

        f_col3, f_col4 = st.columns(2)

        # 3. Predicted Score Range Slider
        min_score = float(df_res["Predicted_Exam_Score"].min()) if "Predicted_Exam_Score" in df_res.columns else 0.0
        max_score = float(df_res["Predicted_Exam_Score"].max()) if "Predicted_Exam_Score" in df_res.columns else 100.0
        with f_col3:
            sel_score_range = st.slider(
                "📊 Predicted Score Range",
                min_value=0.0,
                max_value=100.0,
                value=(min_score, max_score),
                step=1.0,
                key="f_score"
            )

        # 4. Attendance Range Slider
        min_att = int(df_res["Attendance"].min()) if "Attendance" in df_res.columns else 40
        max_att = int(df_res["Attendance"].max()) if "Attendance" in df_res.columns else 100
        with f_col4:
            sel_att_range = st.slider(
                "📅 Class Attendance (%)",
                min_value=40,
                max_value=100,
                value=(min_att, max_att),
                step=1,
                key="f_att"
            )

        # 5. Text search box
        search_query = st.text_input("🔎 Search Student Records by Name, ID, or Keywords:", value="", key="f_search")

    # Apply All Filters Dynamically
    df_filtered = df_res.copy()

    if sel_categories:
        df_filtered = df_filtered[df_filtered["Performance_Category"].isin(sel_categories)]
    else:
        df_filtered = df_filtered.iloc[0:0]

    if all_genders and sel_genders:
        df_filtered = df_filtered[df_filtered["Gender"].isin(sel_genders)]

    if "Predicted_Exam_Score" in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered["Predicted_Exam_Score"] >= sel_score_range[0]) &
            (df_filtered["Predicted_Exam_Score"] <= sel_score_range[1])
        ]

    if "Attendance" in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered["Attendance"] >= sel_att_range[0]) &
            (df_filtered["Attendance"] <= sel_att_range[1])
        ]

    if search_query:
        mask = df_filtered.astype(str).apply(lambda row: row.str.contains(search_query, case=False).any(), axis=1)
        df_filtered = df_filtered[mask]

    # Recalculate Live Filtered Summary
    total_filt = len(df_filtered)
    avg_filt = round(float(df_filtered["Predicted_Exam_Score"].mean()), 2) if total_filt > 0 else 0.0
    max_filt = round(float(df_filtered["Predicted_Exam_Score"].max()), 2) if total_filt > 0 else 0.0
    risk_filt_count = int((df_filtered["Predicted_Exam_Score"].apply(lambda s: round(float(s))) < 40).sum()) if total_filt > 0 else 0
    risk_filt_pct = round((risk_filt_count / total_filt) * 100, 1) if total_filt > 0 else 0.0

    st.markdown(f"Showing **{total_filt:,}** out of **{len(df_res):,}** student records matching active filters.")

    # Dynamic KPI Summary Cards
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    with kpi_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="title">Filtered Students</div>
            <div class="value">{total_filt}</div>
            <div class="subtitle">Matched / {len(df_res)} Total</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="title">Filtered Avg Score</div>
            <div class="value">{avg_filt}</div>
            <div class="subtitle">Mean Score for Filtered</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="title">Filtered Top Score</div>
            <div class="value">{max_filt}</div>
            <div class="subtitle">Highest Filtered Mark</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col4:
        st.markdown(f"""
        <div class="metric-card" style="border: 2px solid #FCA5A5;">
            <div class="title">Filtered At-Risk (&lt;40)</div>
            <div class="value" style="color: #DC2626;">{risk_filt_count} ({risk_filt_pct}%)</div>
            <div class="subtitle">Intervention Target</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Dynamic Filtered Visualizations
    if total_filt > 0:
        c_vis1, c_vis2 = st.columns(2)

        with c_vis1:
            cat_counts = df_filtered["Performance_Category"].value_counts().to_dict()
            fig_pie = px.pie(
                names=list(cat_counts.keys()),
                values=list(cat_counts.values()),
                title=f"Filtered Performance Risk Tier Breakdown ({total_filt} Students)",
                color_discrete_sequence=["#4F46E5", "#10B981", "#F59E0B", "#EF4444"],
                hole=0.4,
                template=plotly_layout["template"]
            )
            fig_pie.update_layout(
                font=plotly_layout["font"],
                paper_bgcolor=plotly_layout["paper_bgcolor"],
                plot_bgcolor=plotly_layout["plot_bgcolor"]
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with c_vis2:
            fig_hist = px.histogram(
                df_filtered,
                x="Predicted_Exam_Score",
                nbins=25,
                title="Distribution of Filtered Predicted Scores",
                color_discrete_sequence=["#312E81"],
                template=plotly_layout["template"]
            )
            fig_hist.update_layout(
                font=plotly_layout["font"],
                paper_bgcolor=plotly_layout["paper_bgcolor"],
                plot_bgcolor=plotly_layout["plot_bgcolor"]
            )
            st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.warning("⚠️ No student records match the selected filter criteria. Please broaden your filters above.")

    st.subheader("📑 Filtered & Annotated Predictions Table")
    st.dataframe(df_filtered, use_container_width=True)

    # Dual Export Options
    exp_col1, exp_col2 = st.columns(2)
    
    with exp_col1:
        csv_filtered = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Export Filtered Subset CSV ({total_filt} records)",
            data=csv_filtered,
            file_name="EduPulse_Filtered_Batch_Predictions.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True
        )

    with exp_col2:
        csv_full = df_res.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Export Complete Batch Report CSV ({len(df_res)} records)",
            data=csv_full,
            file_name="EduPulse_Complete_Batch_Predictions.csv",
            mime="text/csv",
            use_container_width=True
        )
