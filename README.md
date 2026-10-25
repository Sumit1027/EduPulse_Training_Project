# 🎓 EduPulse: Intelligent Insights for Student Academic Well-being

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.0%2B-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![University Submission](https://img.shields.io/badge/45--Day%20Training-University%20Project-purple.svg)]()

---

## 📌 Executive Summary

**EduPulse** is an end-to-end Machine Learning web application designed to analyze, predict, and diagnose student academic performance. Built using **Python, Scikit-Learn, Streamlit, and Plotly**, EduPulse allows educational institutions, teachers, and counselors to:
- Predict student final exam scores based on 19 demographic, academic, and behavioral features.
- Identify at-risk students ($<40\%$ score threshold) early for timely intervention.
- Conduct interactive **"What-If" scenario simulations** to see how score predictions change with study habit improvements.
- Execute **bulk CSV predictions** for class datasets (up to thousands of students).
- Generate and download **official PDF diagnostic reports** for parents and academic counselors.

---

## 🚀 Key Features

- 🏠 **Executive Dashboard**: High-level metrics, dataset stats, and ML pipeline roadmap.
- 🎯 **Single Student Academic Diagnosis**: Interactive form with risk badges, feature impact bar charts, and **instant downloadable PDF diagnostic reports**.
- ⚡ **What-If Score Improvement Simulator**: Interactive sliders to simulate how adding $+2$ study hours or boosting attendance affects predicted performance.
- 📂 **Bulk Student CSV Prediction**: Batch upload class datasets, categorize risk levels, view interactive distribution charts, and export annotated CSVs.
- 📊 **Exploratory Data Analytics (EDA)**: Interactive correlation heatmaps, feature vs. exam score scatter plots (with OLS trendlines), and boxplots.
- ℹ️ **Model Evaluation & Specs**: Comparative performance benchmarks across Linear Regression, Random Forest, Decision Tree, and Ridge models.

---

## 📁 Repository Structure

```
EduPulse/
│
├── .streamlit/
│   └── config.toml                # Custom Streamlit theme configuration
│
├── Dataset/
│   ├── StudentPerformanceFactors.csv          # Raw student dataset
│   └── StudentPerformanceFactors_Cleaned.csv  # Preprocessed dataset (6,607 records)
│
├── Model/
│   ├── final_linear_regression_model.pkl      # Trained Scikit-Learn Model
│   ├── scaler.pkl                             # Trained StandardScaler object
│   ├── encoders.pkl                           # LabelEncoders dictionary
│   └── label_encoder.pkl                      # Target Encoder
│
├── Notebook/
│   ├── EDA.ipynb                              # Exploratory Data Analysis
│   ├── Feature_Engineering.ipynb              # Feature Selection & Transformation
│   ├── Model_Building.ipynb                   # Initial Model Training
│   ├── Model_Evaluation.ipynb                 # Comparative Performance Metrics
│   ├── Model_Improvement.ipynb                # Feature Tuning & Scaling
│   ├── Hyperparameter_Tuning.ipynb            # GridSearch Hyperparameter Optimization
│   ├── Model_Saving_Loading.ipynb             # Model Serialization (Joblib)
│   └── Predict_New_Student.ipynb              # Inference Script Test
│
├── pages/
│   ├── 2_Predict.py                           # Single Student Predictor + PDF Export
│   ├── 3_WhatIf_Simulator.py                  # Interactive Habit Simulator
│   ├── 4_Bulk_Prediction.py                   # CSV Batch Processing & Analytics
│   ├── 5_Analytics.py                         # Correlation Matrix & EDA Dashboard
│   └── 6_About.py                             # Model Specs & Benchmarks
│
├── utils/
│   ├── data_loader.py                         # Dataset Ingestion Utility
│   ├── predictor.py                           # Model Inference & Feature Attribution
│   ├── bulk_predictor.py                      # Batch CSV Prediction Engine
│   └── pdf_generator.py                       # ReportLab PDF Report Generator
│
├── Report/
│   └── EduPulse_45_Days_Training_Report.md    # Formal 45-Day University Training Project Report
│
├── assets/
│   ├── logo.png                               # Project Logo
│   └── style.css                              # Custom CSS Design Tokens & Glassmorphism Theme
│
├── App.py                                     # Primary Streamlit Entry Point (Home Dashboard)
├── requirements.txt                           # Python Dependencies List
└── README.md                                  # Project Documentation
```

> **Note:** `App.py` at the project root *is* the Home dashboard (live dataset metrics, insight
> charts, and the ML pipeline overview) — run it with `streamlit run App.py`. Streamlit
> automatically lists the numbered files under `pages/` alongside it in the sidebar navigation.

---

## 📊 Machine Learning Model Benchmarks

Multiple regression algorithms were evaluated during model development on the 6,607 student record dataset:

| Algorithm | R² Score (%) | MAE | RMSE | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Linear Regression (Selected)** | **68.88%** | **1.02** | **2.10** | 🏆 **Deployed Model** |
| Ridge Regression | 68.86% | 1.02 | 2.10 | Baseline Comparison |
| Random Forest Regressor | 67.13% | 1.15 | 2.22 | Secondary Benchmark |
| Decision Tree Regressor | 58.40% | 1.48 | 2.76 | Baseline Model |

> **Key Model Finding**: Linear Regression achieved the best overall generalization score ($R^2 = 68.88\%$) with minimum mean absolute error ($\text{MAE} = 1.02\text{ marks}$), indicating strong linear dependency between study habits, attendance, past scores, and final exam performance.

---

## 📋 Dataset Schema & Feature Description

The model uses 19 input features covering academic, personal, and socioeconomic factors:

| Feature Name | Type | Description / Range |
| :--- | :--- | :--- |
| `Hours_Studied` | Numeric | Self-study hours per week (1 - 20 hrs) |
| `Attendance` | Numeric | Class attendance percentage (40% - 100%) |
| `Parental_Involvement` | Categorical | Low, Medium, High |
| `Access_to_Resources` | Categorical | Low, Medium, High |
| `Extracurricular_Activities` | Categorical | No, Yes |
| `Sleep_Hours` | Numeric | Nightly sleep duration (4 - 12 hrs) |
| `Previous_Scores` | Numeric | Previous term examination score (30 - 100) |
| `Motivation_Level` | Categorical | Low, Medium, High |
| `Internet_Access` | Categorical | No, Yes |
| `Tutoring_Sessions` | Numeric | Tutoring sessions attended per month (0 - 10) |
| `Family_Income` | Categorical | Low, Medium, High |
| `Teacher_Quality` | Categorical | Low, Medium, High |
| `School_Type` | Categorical | Public, Private |
| `Peer_Influence` | Categorical | Negative, Neutral, Positive |
| `Physical_Activity` | Numeric | Weekly physical activity hours (0 - 14 hrs) |
| `Learning_Disabilities` | Categorical | No, Yes |
| `Parental_Education_Level` | Categorical | High School, College, Postgraduate |
| `Distance_from_Home` | Categorical | Near, Moderate, Far |
| `Gender` | Categorical | Male, Female |

---

## ⚙️ Installation & Setup Guide

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone Repository
```bash
git clone https://github.com/YOUR-USERNAME/EduPulse_Training_Project.git
cd EduPulse_Training_Project
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux / MacOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
streamlit run App.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📑 45-Day University Training Project Report
A complete, academic-grade project report has been prepared for university submission under:
👉 [`Report/EduPulse_45_Days_Training_Report.md`](Report/EduPulse_45_Days_Training_Report.md)

---

## 📜 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

Developed as a Machine Learning Project for **45-Day University Training / Internship Program**.
