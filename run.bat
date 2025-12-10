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

echo 📋 Checking environment configuration...
if not exist ".env" (
    echo 📄 Copying .env-example to .env...
    copy .env-example .env > nul
    echo ✅ .env file created from .env-example
) else (
        echo ✅ .env file already exists
)

echo 📦 Checking dependencies...
pip install -r requirements.txt
echo ✅ Dependencies installed

echo 🚀 Starting Qlyuker Bot...

python src/main.py