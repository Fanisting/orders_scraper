@echo off

REM Check if the OS is Windows
IF "%OS%"=="Windows_NT" (
    REM Run the virtual environment activation script (for Windows)
    call env\Scripts\activate
)

REM Run the Python script (assuming the script is named test.py)
python test_pdd.py
