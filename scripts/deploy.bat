@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo    Развертывание проекта (вариант E)
echo ========================================
echo.

echo [1/3] Отправка изменений бэкенда на GitHub...
git add .
git commit -m "Update backend"
git push origin main

echo.
echo [2/3] Ожидание автоматического деплоя на Render...
echo Render пересоберет и перезапустит бэкенд
echo.

echo [3/3] Сборка новой версии расширения...
call scripts\build_release.bat

echo.
echo ========================================
echo    Развертывание завершено
echo ========================================
echo.
echo Бэкенд: https://expansionlinguist.onrender.com
echo Swagger: https://expansionlinguist.onrender.com/docs
echo Release расширения: release\project_release.zip
echo.
pause