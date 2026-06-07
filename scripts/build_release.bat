@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo    Сборка release-архива расширения
echo ========================================
echo.

if not exist "extension\dist" (
    echo Ошибка: папка extension\dist не найдена
    echo.
    echo Запустите сборку расширения:
    echo cd extension
    echo npm install
    echo npm run build
    echo.
    pause
    exit /b 1
)

if not exist "release" mkdir release

if exist "release\project_release.zip" del "release\project_release.zip"

echo Копирование файлов расширения...
cd extension\dist
powershell -Command "Compress-Archive -Path * -DestinationPath ..\..\release\project_release.zip -Force"
cd ..\..

echo.
echo ========================================
echo    Готово!
echo ========================================
echo.
echo Архив создан: release\project_release.zip
echo.
echo Для установки расширения:
echo 1. Распаковать архив
echo 2. chrome://extensions/ → Режим разработчика
echo 3. Загрузить распакованное расширение
echo 4. В настройках указать API URL: https://expansionlinguist.onrender.com
echo.
pause