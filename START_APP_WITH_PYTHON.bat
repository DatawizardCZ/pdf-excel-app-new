@echo off
REM Batch file to run app with the correct Python path
REM Uses Python 3.10.6 from Miniconda pydata-book environment

set PYTHON_PATH=%USERPROFILE%\miniconda3\envs\pydata-book\python.exe

echo ========================================
echo Spoustim Darvis PDF aplikaci...
echo Pouzivam Python: %PYTHON_PATH%
echo ========================================
echo.

REM Check if Python exists
if not exist "%PYTHON_PATH%" (
    echo CHYBA: Python neni nalezen na: %PYTHON_PATH%
    echo.
    echo Zkontrolujte, ze je Python nainstalovan v Miniconda.
    pause
    exit /b 1
)

REM Check if app.py exists
if not exist "app.py" (
    echo CHYBA: Soubor app.py nenalezen!
    echo Ujistete se, ze jste v spravnem adresari.
    pause
    exit /b 1
)

REM Check dependencies
echo Kontroluji zavislosti...
"%PYTHON_PATH%" -m pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Streamlit neni nainstalovan. Instaluji...
    "%PYTHON_PATH%" -m pip install streamlit pandas pdfplumber openpyxl
    if errorlevel 1 (
        echo CHYBA: Nepodarilo se nainstalovat zavislosti!
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo Spoustim aplikaci...
echo ========================================
echo.
echo Aplikace se otevře v prohlizeci.
echo Pro zastaveni stisknete Ctrl+C v tomto okne.
echo.

REM Run the app
"%PYTHON_PATH%" -m streamlit run app.py

pause


