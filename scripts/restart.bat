@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo    Перезапуск сервиса (бэкенд)
echo ========================================
echo.

echo Способ 1: через панель Render
start https://dashboard.render.com
echo.
echo Способ 2: через git push
echo git commit --allow-empty -m "Restart backend"
echo git push origin main
echo.
echo Расширение переустанавливать не нужно
echo (достаточно обновить в chrome://extensions/)
echo.
pause