@echo off
echo.
echo   QEEG - Quantum EEG Epilepsy Detection System
echo   ==============================================
echo.

:: Find Python (try py launcher first, then direct)
set PYTHON=
where py >nul 2>&1 && set PYTHON=py -3
if "%PYTHON%"=="" (
    where python >nul 2>&1 && set PYTHON=python
)
if "%PYTHON%"=="" (
    where python3 >nul 2>&1 && set PYTHON=python3
)
if "%PYTHON%"=="" (
    echo   ERROR: Python 3.9+ not found.
    echo   Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo   Found Python: %PYTHON%

:: Create venv
if not exist "venv" (
    echo   Creating virtual environment...
    %PYTHON% -m venv venv
)

:: Activate
call venv\Scripts\activate.bat 2>nul
if errorlevel 1 (
    echo   Warning: venv activation issue, continuing anyway...
)

:: Upgrade pip
echo   Upgrading pip...
python -m pip install --upgrade pip -q

:: Install deps
echo   Installing dependencies...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo   Retrying with binary-only packages...
    pip install --only-binary=:all: -r requirements.txt
)

:: Make dirs
if not exist "uploads" mkdir uploads
if not exist "reports" mkdir reports

echo.
echo   Ready! Starting server...
echo.
echo   Open browser: http://localhost:5001
echo.
echo   Press Ctrl+C to stop
echo   ==============================================
echo.

python app.py
pause
