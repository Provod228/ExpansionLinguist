@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo    Проверка состояния проекта
echo ========================================
echo.

echo --- Проверка бэкенда ---
curl -s -o nul -w "HTTP Status: %%{http_code}\n" https://expansionlinguist.onrender.com
echo.

echo --- Проверка Swagger ---
curl -s -o nul -w "HTTP Status: %%{http_code}\n" https://expansionlinguist.onrender.com/docs
echo.

echo --- Открытие бэкенда в браузере ---
start https://expansionlinguist.onrender.com/docs

echo.
echo --- Проверка расширения ---
if exist "release\project_release.zip" (
    echo Release-архив найден: release\project_release.zip
    echo Размер: 
    dir "release\project_release.zip" | find "project_release.zip"
) else (
    echo Внимание: release\project_release.zip не найден
    echo Запустите scripts\build_release.bat для сборки
)

echo.
echo --- Логи бэкенда ---
start https://dashboard.render.com

echo.
pause