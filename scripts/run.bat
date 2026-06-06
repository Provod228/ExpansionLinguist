@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo     Запуск backend
echo ========================================

cd project
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause