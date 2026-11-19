@echo off
title Ertugrul YZ - Gunluk Borsa Al-Sat
cd /d "%~dp0"
echo ========================================================
echo        ERTUGRUL YZ - GUNLUK BORSA AL-SAT VE KARAR MOTORU
echo ========================================================
echo.
echo Sunucu baslatiliyor: http://localhost:5055
start http://localhost:5055
python core\server.py
