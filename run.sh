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

echo "📋 Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "📄 Copying .env-example to .env..."
    cp .env-example .env

    fi
    echo "✅ .env file created from .env-example"
else
    echo "✅ .env file already exists"

echo "📦 Checking dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"

echo "🚀 Starting Qlyuker Bot..."

python3 src/main.py