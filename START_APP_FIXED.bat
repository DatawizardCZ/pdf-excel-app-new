@echo off
REM Fixed batch file - ensures correct directory and Python path

REM Change to script's directory (where app.py is)
cd /d "%~dp0"

set PYTHON=%USERPROFILE%\miniconda3\envs\pydata-book\python.exe

echo.
echo ========================================
echo Starting Darvis PDF App
echo ========================================
echo.
echo Current directory: %CD%
echo Python: %PYTHON%
echo.

REM Verify files exist
if not exist "app.py" (
    echo ERROR: app.py not found in: %CD%
    echo.
    pause
    exit /b 1
)

if not exist "pdf_processor.py" (
    echo ERROR: pdf_processor.py not found in: %CD%
    echo.
    pause
    exit /b 1
)

if not exist "%PYTHON%" (
    echo ERROR: Python not found at: %PYTHON%
    echo.
    pause
    exit /b 1
)

echo All files found! Starting Streamlit...
echo.
echo The app will open at http://localhost:8501
echo Keep this window open while using the app.
echo Press Ctrl+C to stop.
echo.
echo ========================================
echo.

REM Start Streamlit from current directory
REM Disable email prompt and auto-open browser
"%PYTHON%" -m streamlit run app_secure.py --browser.gatherUsageStats=false

pause



