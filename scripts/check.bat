@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo     Проверка кода + автоисправление
echo ========================================

cd project
ruff check . --fix
pause