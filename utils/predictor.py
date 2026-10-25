from pathlib import Path
import joblib
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "Model" / "final_linear_regression_model.pkl"
SCALER_PATH = BASE_DIR / "Model" / "scaler.pkl"
ENCODER_PATH = BASE_DIR / "Model" / "encoders.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
encoders = joblib.load(ENCODER_PATH)

FEATURE_NAMES = [
    "Hours_Studied", "Attendance", "Parental_Involvement", "Access_to_Resources",
    "Extracurricular_Activities", "Sleep_Hours", "Previous_Scores", "Motivation_Level",
    "Internet_Access", "Tutoring_Sessions", "Family_Income", "Teacher_Quality",
    "School_Type", "Peer_Influence", "Physical_Activity", "Learning_Disabilities",
    "Parental_Education_Level", "Distance_from_Home", "Gender"
]

def predict_exam_score(student_data):
    """
    Predicts the exam score for a single student record (pandas DataFrame).
    Clips output to reasonable range [0, 100].
    """
    student_scaled = scaler.transform(student_data)
    prediction = model.predict(student_scaled)
    score = round(float(prediction[0]), 2)
    return max(0.0, min(100.0, score))


def explain_prediction(student_data):
    """
    Calculates feature contributions for the predicted score using model coefficients.
    Returns a DataFrame with Feature, Value, Coefficient, and Contribution.
    """
    student_scaled = scaler.transform(student_data)[0]
    coefficients = model.coef_
    
    contributions = student_scaled * coefficients
    
    df_explain = pd.DataFrame({
        "Feature": FEATURE_NAMES,
        "Raw_Value": student_data.iloc[0].values,
        "Coefficient": coefficients,
        "Contribution": contributions
    })
    
    df_explain["Impact"] = np.where(df_explain["Contribution"] >= 0, "Positive", "Negative")
    df_explain["Abs_Contribution"] = np.abs(df_explain["Contribution"])
    df_explain = df_explain.sort_values(by="Abs_Contribution", ascending=False)
    
    return df_explain