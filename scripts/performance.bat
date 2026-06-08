@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

:: ВАЖНО: Укажите URL вашего сервера
set API_URL=https://expansionlinguist.onrender.com
:: Для локальной разработки раскомментируйте следующую строку:
:: set API_URL=http://localhost:8000

echo ========================================
echo     CHECKING PERFORMANCE
echo     Target: %API_URL%
echo ========================================
echo.

echo [1] Checking server availability...
curl -s -o nul %API_URL%/
if %errorlevel% neq 0 (
    echo [ERROR] Server is not responding!
    echo.
    echo Possible reasons:
    echo - Free tier sleeping (wake up takes 30-60 sec)
    echo - Server is restarting
    echo - Wrong URL
    echo.
    echo Trying to wake up server...
    start %API_URL%/
    echo Waiting 10 seconds...
    timeout /t 10 > nul
)

echo.
echo [2] Response time check:
echo.

echo [GET %API_URL%/]
curl -s -w "Time: %%{time_total} sec | HTTP: %%{http_code}\n" -o nul %API_URL%/

echo.
echo [GET %API_URL%/words/search?word=hello]
curl -s -w "Time: %%{time_total} sec | HTTP: %%{http_code}\n" -o nul "%API_URL%/words/search?word=hello"

echo.
echo [3] Lighthouse in browser:
echo.
echo Open Chrome and go to: %API_URL%/docs
echo Then press F12 -^> Lighthouse tab -^> Generate report
echo.
echo Opening browser...
start chrome %API_URL%/docs

echo.
echo ========================================
echo     NOTES FOR REMOTE SERVER
echo ========================================
echo.
echo - First request may be slow (waking from sleep)
echo - Response time includes network latency
echo - HTTPS adds encryption overhead
echo - 503 error = server starting up
echo.
echo If you see 503, wait 1 minute and run again
echo.
pause