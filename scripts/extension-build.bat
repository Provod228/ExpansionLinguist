@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo     Сборка Chrome Extension
echo ========================================

cd extension

echo Установка зависимостей...
call npm install

echo Сборка расширения...
call npm run build

echo ========================================
echo     Сборка завершена!
echo ========================================
echo Расширение собрано в папке extension/dist/
echo Теперь загрузи папку extension в chrome://extensions/
pause