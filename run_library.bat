@echo off
REM Run the library stats Python program
python library_stats.py books.csv

REM Wait for user to press a key
pause

REM Open the output summary text file
start notepad library_summary.txt
