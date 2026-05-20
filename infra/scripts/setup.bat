@echo off
REM UstaadX Setup Script for Windows
REM This script sets up the complete development environment

echo =========================================
echo UstaadX Development Environment Setup
echo =========================================
echo.

REM Check prerequisites
echo Checking prerequisites...
echo.

where docker >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Docker installed
) else (
    echo [ERROR] Docker not found
    goto :error
)

where docker-compose >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Docker Compose installed
) else (
    echo [ERROR] Docker Compose not found
    goto :error
)

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Python installed
) else (
    echo [ERROR] Python not found
    goto :error
)

where flutter >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Flutter installed
) else (
    echo [WARNING] Flutter not found (optional for backend-only development)
)

where git >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Git installed
) else (
    echo [ERROR] Git not found
    goto :error
)

echo.

REM Setup backend
echo =========================================
echo Setting up Backend
echo =========================================
echo.

cd apps\backend_api

if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo [OK] .env file created
) else (
    echo [WARNING] .env file already exists, skipping
)

if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [WARNING] Virtual environment already exists, skipping
)

echo Installing Python dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
echo [OK] Python dependencies installed

cd ..\..

REM Setup mobile app
where flutter >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo =========================================
    echo Setting up Mobile App
    echo =========================================
    echo.

    cd apps\mobile_app

    if not exist .env (
        echo Creating .env file...
        copy .env.example .env
        echo [OK] .env file created
    ) else (
        echo [WARNING] .env file already exists, skipping
    )

    echo Installing Flutter dependencies...
    flutter pub get >nul 2>&1
    echo [OK] Flutter dependencies installed

    cd ..\..
)

REM Setup Docker
echo.
echo =========================================
echo Setting up Docker Services
echo =========================================
echo.

echo Starting Docker services...
docker-compose up -d

echo Waiting for services to be ready...
timeout /t 5 /nobreak >nul

docker-compose ps | findstr "Up" >nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Docker services started
) else (
    echo [ERROR] Failed to start Docker services
    goto :error
)

REM Run migrations
echo.
echo =========================================
echo Running Database Migrations
echo =========================================
echo.

cd apps\backend_api
call venv\Scripts\activate.bat

echo Initializing Alembic...
alembic revision --autogenerate -m "Initial migration" >nul 2>&1

echo Running migrations...
alembic upgrade head
echo [OK] Database migrations complete

cd ..\..

REM Final instructions
echo.
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo Next steps:
echo.
echo 1. Start the backend:
echo    cd apps\backend_api
echo    venv\Scripts\activate.bat
echo    uvicorn app.main:app --reload
echo.
echo 2. Start Celery worker (in another terminal):
echo    cd apps\backend_api
echo    venv\Scripts\activate.bat
echo    celery -A app.core.celery_app worker --loglevel=info
echo.

where flutter >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo 3. Run the mobile app (in another terminal):
    echo    cd apps\mobile_app
    echo    flutter run
    echo.
)

echo 4. Access the API documentation:
echo    http://localhost:8000/docs
echo.
echo 5. Check health endpoint:
echo    curl http://localhost:8000/health
echo.
echo For more information, see docs\setup_guide.md
echo.

goto :end

:error
echo.
echo [ERROR] Setup failed. Please fix the errors and try again.
exit /b 1

:end
