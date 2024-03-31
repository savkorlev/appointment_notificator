@echo off
:loop
python main_pyauto.py
timeout /t 180
goto loop