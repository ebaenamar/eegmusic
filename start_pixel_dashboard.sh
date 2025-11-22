#!/bin/bash

echo "=================================="
echo "🎮 Starting Pixel Dashboard"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Start backend server in background
echo "🚀 Starting backend server..."
python pixel_backend_server.py &
BACKEND_PID=$!

# Wait for server to start
sleep 2

# Open dashboard in browser
echo "🌐 Opening dashboard in browser..."
open pixel_dashboard.html

echo ""
echo "✅ Dashboard started!"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Dashboard: file://$(pwd)/pixel_dashboard.html"
echo ""
echo "To stop:"
echo "  kill $BACKEND_PID"
echo "  or press Ctrl+C"
echo ""

# Wait for user to stop
wait $BACKEND_PID
