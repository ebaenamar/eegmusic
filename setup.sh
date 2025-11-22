#!/bin/bash
# Setup script for Brainwave Music Generator

echo "🧠🎵 Brainwave Music Generator - Setup"
echo "======================================"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run the app:"
echo "   source venv/bin/activate"
echo "   python start_app.py"
echo ""
echo "Or use the quick start script:"
echo "   ./run.sh"
