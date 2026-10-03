@echo off
echo Prüfe alte Umgebung...
if exist .venv (
    echo Alter .venv-Ordner gefunden. Lösche alte Umgebung...
    rmdir /s /q .venv
)

echo Erstelle frische virtuelle Umgebung...
python -m venv .venv
if %errorlevel% neq 0 (
    echo.
    echo FEHLER: Python wurde nicht gefunden oder ist nicht im PATH enthalten!
    echo Bitte stelle sicher, dass Python auf diesem PC installiert ist.
    pause
    exit /b
)

echo Installiere Pakete offline aus dem wheels-Ordner...
.venv\Scripts\python.exe -m pip install --no-index --find-links=./wheels -r requirements.txt

echo.
echo Fertig! Du kannst die App jetzt mit start.bat starten.
pause