@echo off
REM Simple batch file to start the app
REM Make sure you're in the project directory!

cd /d "%~dp0"

set PYTHON=%USERPROFILE%\miniconda3\envs\pydata-book\python.exe

echo.
echo ========================================
echo Starting Darvis PDF App
echo ========================================
echo.
echo Python: %PYTHON%
echo Directory: %CD%
echo.

if not exist "%PYTHON%" (
    echo ERROR: Python not found!
    echo Expected: %PYTHON%
    echo.
    pause
    exit /b 1
)

if not exist "app.py" (
    echo ERROR: app.py not found!
    echo Make sure you're in the project directory.
    echo.
    pause
    exit /b 1
)

echo Starting Streamlit...
echo The app will open at http://localhost:8501
echo.
echo Press Ctrl+C to stop the app
echo.

"%PYTHON%" -m streamlit run app.py

pause


