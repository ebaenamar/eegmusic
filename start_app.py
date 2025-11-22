#!/usr/bin/env python3
"""
Easy launcher for Brainwave Music Generator
Starts the server and opens the dashboard
"""

import subprocess
import webbrowser
import time
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required = ['numpy', 'sounddevice', 'websockets', 'pandas']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n📦 Install with: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main launcher"""
    print("🧠🎵 Brainwave Music Generator")
    print("=" * 50)
    print()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        return
    print("✅ All dependencies installed\n")
    
    # Get current directory
    current_dir = Path(__file__).parent
    dashboard_path = current_dir / "web_dashboard.html"
    
    # Start server in background
    print("🚀 Starting WebSocket server...")
    print("   Server will run on ws://localhost:8765")
    print("   Press Ctrl+C to stop\n")
    
    # Open dashboard in browser
    print("🌐 Opening dashboard in browser...")
    webbrowser.open(f"file://{dashboard_path.absolute()}")
    
    time.sleep(2)
    
    # Start server (this will block)
    print("\n📡 Server running...")
    print("=" * 50)
    
    try:
        from music_server import MusicGeneratorServer
        import asyncio
        
        server = MusicGeneratorServer()
        asyncio.run(server.start_server())
        
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
        print("✅ Server stopped successfully")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTry running manually:")
        print("  1. python music_server.py")
        print("  2. Open web_dashboard.html in browser")

if __name__ == "__main__":
    main()
