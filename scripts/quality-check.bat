@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo     ПОЛНАЯ ПРОВЕРКА КАЧЕСТВА ПРОЕКТА
echo ========================================

echo [1/4] Линтер...
call scripts\check.bat

cd /d "%~dp0\.."
echo [2/4] Smoke-тесты...
call scripts\test.bat

cd /d "%~dp0\.."
echo [3/4] API тесты...
call scripts\api-test.bat

cd /d "%~dp0\.."
echo [4/4] Логи...
call scripts\logs-check.bat

echo.
echo ========================================
echo     ПРОВЕРКА КАЧЕСТВА УСПЕШНО ЗАВЕРШЕНА
echo ========================================
pause