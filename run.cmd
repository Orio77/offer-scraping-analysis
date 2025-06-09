@echo off
REM Job Offer Scraping and Analysis Project Runner
REM This script runs the main application from the project root directory

echo Starting Job Offer Scraping and Analysis...
echo.

REM Change to the project root directory (where this script is located)
cd /d "%~dp0"

REM Run the main application using the conda environment
C:\Users\macie\anaconda3\envs\skrypt\python.exe -m src.main.main

echo.
echo Project execution completed.
pause
