@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo     Просмотр логов Docker
echo ========================================

docker compose logs -f
pause