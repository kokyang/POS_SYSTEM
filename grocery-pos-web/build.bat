@echo off
REM ============================================================
REM  NAM CHONG POS — Windows .exe builder
REM  Run this file on a Windows PC with Python installed.
REM  Output: dist\NamChongPOS\NamChongPOS.exe
REM ============================================================

echo Installing dependencies...
pip install flask pywebview pyinstaller

echo.
echo Building Windows application...
pyinstaller ^
    --name "NamChongPOS" ^
    --windowed ^
    --noconfirm ^
    --add-data "templates;templates" ^
    --hidden-import "webview.platforms.winforms" ^
    --hidden-import "clr" ^
    --hidden-import "flask" ^
    --hidden-import "jinja2" ^
    --hidden-import "werkzeug" ^
    main.py

echo.
echo ============================================================
echo  Done! Your app is at:  dist\NamChongPOS\NamChongPOS.exe
echo  Share the entire dist\NamChongPOS\ folder with your user.
echo ============================================================
pause
