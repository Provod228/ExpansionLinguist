@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo     Проверка API (Integration Tests)
echo ========================================

cd project

echo Запуск тестов регистрации и авторизации...
python -m pytest tests/integration/test_users_api.py -q --tb=no

echo Запуск тестов административной панели...
python -m pytest tests/integration/test_admin_api.py -q --tb=no

echo Запуск тестов работы со словами...
python -m pytest tests/integration/test_words_api.py -q --tb=no

echo.
echo ========================================
echo     Проверка API завершена
echo ========================================
pause