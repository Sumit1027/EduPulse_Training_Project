@echo off
title Launching EduPulse Streamlit Platform...
echo ===================================================
echo   EDUPULSE ACADEMIC ANALYTICS & PREDICTION SYSTEM
echo ===================================================
echo.
echo Checking required Python dependencies...
python -m pip install -r requirements.txt
echo.
echo Launching Streamlit web server...
python -m streamlit run App.py
pause
