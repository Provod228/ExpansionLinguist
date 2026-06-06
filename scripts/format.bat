@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo     Форматирование кода
echo ========================================

cd project
ruff format .
pause