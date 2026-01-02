@echo off
REM Batch skript pro spuštění Streamlit aplikace
REM Použití: Dvojklik na tento soubor

echo ========================================
echo Spoustim Darvis PDF aplikaci...
echo ========================================
echo.

REM Zkontrolovat, zda je Python nainstalovaný
REM Zkusit ruzne zpusoby, jak najit Python
set PYTHON_CMD=
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :python_found
)
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto :python_found
)
python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    goto :python_found
)

REM Python neni nalezen
echo ========================================
echo CHYBA: Python neni nalezen!
echo ========================================
echo.
echo Mozne reseni:
echo 1. Zavrete a znovu otevřete tento terminál
echo 2. Restartujte pocitac
echo 3. Zkontrolujte, ze je Python v PATH
echo.
echo Pokud jste prave nainstalovali Python:
echo - Zavrete a znovu otevřete terminál
echo - Nebo restartujte pocitac
echo.
pause
exit /b 1

:python_found
echo Python nalezen: %PYTHON_CMD%
echo.

REM Zkontrolovat, zda je app.py v aktuálním adresáři
if not exist "app.py" (
    echo CHYBA: Soubor app.py nenalezen!
    echo.
    echo Ujistete se, ze jste v spravnem adresari.
    echo.
    pause
    exit /b 1
)

echo Kontroluji zavislosti...
%PYTHON_CMD% -m pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Streamlit neni nainstalovan. Instaluji...
    %PYTHON_CMD% -m pip install streamlit pandas pdfplumber openpyxl
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

REM Spustit aplikaci
%PYTHON_CMD% -m streamlit run app.py

pause

