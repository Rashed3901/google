@echo off
:menu
cls
color 2
echo =========================
echo        MAIN MENU
echo =========================
echo 1. Open Number Generator
echo 2. Open Main LMS
echo 3. Exit
echo =========================
set /p choice=Enter your choice (1-3): 

if "%choice%"=="1" goto numbergen
if "%choice%"=="2" goto mainlms
if "%choice%"=="3" goto exit
echo Invalid choice, try again.
pause
goto menu

:numbergen
cls
color 2
py gen.py
pause
goto menu

:mainlms
cls
color 2
py py.py
pause
goto menu

:exit
cls
color 2
pause
exit