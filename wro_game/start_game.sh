#!/bin/bash
# Script to run WRO Game Practice

echo "[ROBOT] Starting WRO Game Practice..."

# Check virtual environment
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not created"
    echo "Please run: ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run game
python main.py
