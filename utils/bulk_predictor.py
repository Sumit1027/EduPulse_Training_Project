import pandas as pd
import numpy as np
from utils.predictor import model, scaler, encoders

REQUIRED_COLUMNS = [
    "Hours_Studied", "Attendance", "Parental_Involvement", "Access_to_Resources",
    "Extracurricular_Activities", "Sleep_Hours", "Previous_Scores", "Motivation_Level",
    "Internet_Access", "Tutoring_Sessions", "Family_Income", "Teacher_Quality",
    "School_Type", "Peer_Influence", "Physical_Activity", "Learning_Disabilities",
    "Parental_Education_Level", "Distance_from_Home", "Gender"
]

def process_bulk_predictions(df_input):
    """
    Processes an uploaded pandas DataFrame containing student records.
    Returns:
      (df_result, summary_dict, error_message)
    """
    try:
        df = df_input.copy()
        
        # Check missing columns
        missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing_cols:
            return None, None, f"Missing required columns in CSV: {', '.join(missing_cols)}"
            
        # Clean & encode
        df_encoded = df[REQUIRED_COLUMNS].copy()
        
        for col, encoder in encoders.items():
            if col in df_encoded.columns:
                # Convert string values to string and strip whitespace
                df_encoded[col] = df_encoded[col].astype(str).str.strip()
                # Use map to handle unseen categories safely
                mapping = dict(zip(encoder.classes_, encoder.transform(encoder.classes_)))
                
                # Check for unmapped values and fallback to default (first class index)
                df_encoded[col] = df_encoded[col].map(mapping)
                if df_encoded[col].isnull().any():
                    default_val = encoder.transform([encoder.classes_[0]])[0]
                    df_encoded[col] = df_encoded[col].fillna(default_val).astype(int)
                else:
                    df_encoded[col] = df_encoded[col].astype(int)

        # Scale features
        scaled_features = scaler.transform(df_encoded)
        
        # Predict scores
        predictions = model.predict(scaled_features)
        predictions = np.clip(np.round(predictions, 2), 0, 100)
        
        df_result = df.copy()
        df_result["Predicted_Exam_Score"] = predictions
        
        # Categorize
        def categorize(score):
            r_score = round(float(score))
            if r_score >= 80:
                return "Excellent (80-100)"
            elif r_score >= 60:
                return "Good (60-79)"
            elif r_score >= 40:
                return "Average (40-59)"
            else:
                return "At Risk (<40)"

        def get_recommendation(score):
            r_score = round(float(score))
            if r_score >= 80:
                return "Maintain high study consistency & mentor peers."
            elif r_score >= 60:
                return "Good performance; focus on weak topic revision."
            elif r_score >= 40:
                return "Increase weekly study hours & attend tutoring sessions."
            else:
                return "Urgent academic intervention & teacher counseling required."

        df_result["Performance_Category"] = df_result["Predicted_Exam_Score"].apply(categorize)
        df_result["Recommendation"] = df_result["Predicted_Exam_Score"].apply(get_recommendation)
        
        # Summary statistics
        total_students = len(df_result)
        avg_predicted = round(float(df_result["Predicted_Exam_Score"].mean()), 2)
        highest_predicted = round(float(df_result["Predicted_Exam_Score"].max()), 2)
        lowest_predicted = round(float(df_result["Predicted_Exam_Score"].min()), 2)
        
        at_risk_count = int((df_result["Predicted_Exam_Score"].apply(lambda s: round(float(s))) < 40).sum())
        excellent_count = int((df_result["Predicted_Exam_Score"] >= 80).sum())
        
        summary = {
            "total_students": total_students,
            "avg_predicted": avg_predicted,
            "highest_predicted": highest_predicted,
            "lowest_predicted": lowest_predicted,
            "at_risk_count": at_risk_count,
            "at_risk_percentage": round((at_risk_count / total_students) * 100, 1),
            "excellent_count": excellent_count,
            "category_counts": df_result["Performance_Category"].value_counts().to_dict()
        }
        
        return df_result, summary, None

    except Exception as e:
        return None, None, f"Error processing bulk prediction file: {str(e)}"
