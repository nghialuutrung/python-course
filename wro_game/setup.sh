#!/bin/bash
# Setup script for WRO Game Practice

echo "[ROBOT] WRO Game Practice - Setup"
echo "================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found. Please install Python 3.8+"
    exit 1
fi

echo "[OK] Python3 found"

# Create virtual environment
echo "[SETUP] Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "[SETUP] Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "[SETUP] Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "[INSTALL] Installing dependencies..."
pip install -r requirements.txt

echo "[OK] Setup complete!"
echo ""
echo "To run the game:"
echo "1. source venv/bin/activate"
echo "2. python main.py"
echo ""
echo "Or run: ./start_game.sh"
