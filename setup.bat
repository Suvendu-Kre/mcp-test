@echo off
echo Creating virtual environment...
python -m venv .venv
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Setup complete! To run the agent:
echo   .venv\Scripts\activate.bat
echo   python main.py