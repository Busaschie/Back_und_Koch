@echo off
echo ===================================================
echo Starte Applikations-Infrastruktur...
echo ===================================================

:: Wechselt automatisch in das Verzeichnis dieser BAT-Datei
cd /d "%~dp0"

:: -----------------------------------------------------
:: 0. Apache & MySQL (XAMPP Portable) im Hintergrund starten
:: -----------------------------------------------------
echo [XAMPP] Starte MySQL Datenbank...
start "MySQL" /D "%~dp0xampp" /b mysql_start.bat

echo [XAMPP] Starte Apache Webserver...
start "Apache" /D "%~dp0xampp" /b apache_start.bat

:: Kurz warten, bis Datenbank/Apache hochgefahren sind
timeout /t 2 /nobreak >nul

:: -----------------------------------------------------
:: 1. Python VENV & Umgebung
:: -----------------------------------------------------
set VENV_PYTHON="%~dp0.venv\Scripts\python.exe"
set PYTHONPATH=%CD%

:: -----------------------------------------------------
:: 2. FastAPI Backend starten
:: -----------------------------------------------------
echo [BACKEND] Starte FastAPI Backend...
start "FastAPI_Backend" /D "%~dp0rest_api" /b %VENV_PYTHON% -m uvicorn main:app --host 127.0.0.1 --port 8000

:: Kurz warten, bis das Backend bereit ist
timeout /t 3 /nobreak >nul

:: -----------------------------------------------------
:: 3. Streamlit Frontend starten
:: -----------------------------------------------------
echo [FRONTEND] Starte Streamlit Frontend...
start "Streamlit_Frontend" cmd /k %VENV_PYTHON% -m streamlit run app.py --server.port 8501

echo ===================================================
echo Alle Dienste wurden gestartet!
echo Schliessen Sie dieses Hauptfenster nicht.
echo ===================================================
pause
