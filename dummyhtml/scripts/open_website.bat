@echo off
echo ========================================
echo   Opening Bakery Website in Browser
echo ========================================
echo.
echo Server: http://127.0.0.1:8000/
echo.
echo IMPORTANT: Using HTTP (not HTTPS)
echo ========================================
echo.

REM Open homepage
start http://127.0.0.1:8000/

timeout /t 2 /nobreak >nul

REM Open menu page
start http://127.0.0.1:8000/menu/

echo.
echo ========================================
echo Browser windows opened!
echo ========================================
echo.
echo If you still see SSL errors:
echo 1. Check the address bar shows "http://" not "https://"
echo 2. Try typing the URL manually
echo 3. Clear your browser cache (Ctrl+Shift+Delete)
echo 4. Try a different browser (Chrome, Firefox, Edge)
echo.
echo Homepage: http://127.0.0.1:8000/
echo Menu:     http://127.0.0.1:8000/menu/
echo.
pause
