#!/bin/bash

if [ ! -d "venv" ]; then
    echo "🛠️ Creating virtual environment..."
    python3 -m venv venv

    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📦 Checking dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"

echo "🚀 Starting Qlyuker Bot..."

python3 src/main.py