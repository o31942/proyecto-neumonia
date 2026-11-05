@echo off
title Deteccion de Neumonia - Streamlit App (UAO)
echo ========================================================
echo  Iniciando aplicacion web de Deteccion de Neumonia...
echo ========================================================
cd /d "C:\Users\odsanchez\.gemini\antigravity\scratch\proyecto-neumonia"
"C:\Users\odsanchez\.local\bin\uv.exe" run streamlit run src\neumonia_detection\app.py
pause
