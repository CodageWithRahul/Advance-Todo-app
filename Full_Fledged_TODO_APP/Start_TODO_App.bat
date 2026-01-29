@echo off
REM ==== GO TO PROJECT ROOT ====
cd /d "C:\Rahul\Full_Fledged Django TODO Web App\Full_Fledged_TODO_APP"

REM ==== ACTIVATE VENV ====
call "C:\Rahul\Full_Fledged Django TODO Web App\venv\Scripts\activate.bat"

REM ==== START SERVER IN NEW WINDOW ====
start cmd /k python manage.py runserver

REM ==== WAIT A BIT ====
timeout /t 3 > nul

REM ==== OPEN BROWSER ====
start http://127.0.0.1:8000/
