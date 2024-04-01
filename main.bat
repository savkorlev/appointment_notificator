@echo off
:loop
python main_pyauto.py
timeout /t 60
goto loop