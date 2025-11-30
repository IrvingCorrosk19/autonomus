@echo off
REM Script para ejecutar todas las pruebas (Windows)

echo ==========================================
echo Ejecutando pruebas del Autonomous CRM
echo ==========================================
echo.

REM Verificar que el servidor esté corriendo
echo Verificando que el servidor esté corriendo...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Servidor está corriendo
) else (
    echo [ERROR] Servidor no está corriendo. Inicia con:
    echo    uvicorn app.main:app --reload
    exit /b 1
)

echo.
echo Ejecutando pruebas...
python scripts/test_complete.py

