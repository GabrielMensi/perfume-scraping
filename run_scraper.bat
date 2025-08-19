@echo off
REM Este script instala las dependencias y ejecuta el scraper de perfumes

REM Verifica si Python está instalado
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python no está instalado. Por favor, instale Python desde https://www.python.org/downloads/
    pause
    exit /b
)

REM Instala las dependencias
pip install -r requirements.txt

REM Ejecuta el script principal
python scrap_perfumes.py

pause
