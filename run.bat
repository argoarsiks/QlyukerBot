@echo off
chcp 65001 > nul

if not exist "venv" (
    echo 🛠️ Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

echo 📦 Checking dependencies...
pip install -r requirements.txt
echo ✅ Dependencies installed

echo 🚀 Starting Qlyuker Bot...

python src/main.py