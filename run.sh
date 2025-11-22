#!/bin/bash
# Quick run script for Brainwave Music Generator

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "📦 Run setup first: ./setup.sh"
    exit 1
fi

# Activate venv and run
source venv/bin/activate
python start_app.py
