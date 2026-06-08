@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo     Запуск всех тестов (Smoke + Unit + Integration)
echo ========================================

cd project

echo --- Smoke тесты (критические сценарии) ---
python -m pytest tests/test_smoke.py -q --tb=no

echo --- Unit и Integration тесты ---
python -m pytest tests/ -q --tb=no -m "not smoke"

echo.
echo ========================================
echo     Все тесты завершены
echo ========================================
pause