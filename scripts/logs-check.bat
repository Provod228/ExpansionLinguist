@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo     Проверка логов
echo ========================================

docker compose logs --tail=100 > reports\logs_tail.txt 2>nul
type reports\logs_tail.txt
pause