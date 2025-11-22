#!/usr/bin/env python3
"""
Test setup for Brainwave Music Generator
Verifies all dependencies and components
"""

import sys
from pathlib import Path

def test_imports():
    """Test if all required packages are available"""
    print("🔍 Testing imports...")
    
    tests = {
        'numpy': 'NumPy',
        'sounddevice': 'SoundDevice (audio)',
        'websockets': 'WebSockets',
        'pandas': 'Pandas'
    }
    
    passed = []
    failed = []
    
    for module, name in tests.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
            passed.append(name)
        except ImportError:
            print(f"  ❌ {name} - NOT INSTALLED")
            failed.append(module)
    
    return len(failed) == 0, failed

def test_eeg_handler():
    """Test EEG stream handler"""
    print("\n🔍 Testing EEG stream handler...")
    
    try:
        sys.path.append('/Users/e.baena/CascadeProjects')
        from eeg_stream_handler import EEGStreamManager
        print("  ✅ EEG stream handler imported")
        
        manager = EEGStreamManager()
        print("  ✅ EEG manager created")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_audio():
    """Test audio output"""
    print("\n🔍 Testing audio output...")
    
    try:
        import sounddevice as sd
        import numpy as np
        
        # List audio devices
        devices = sd.query_devices()
        print(f"  ℹ️  Found {len(devices)} audio device(s)")
        
        # Get default device
        default = sd.default.device
        print(f"  ℹ️  Default device: {default}")
        
        # Test tone generation
        print("  🔊 Playing test tone (1 second)...")
        duration = 1.0
        frequency = 440  # A4
        sample_rate = 44100
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        tone = 0.3 * np.sin(2 * np.pi * frequency * t)
        
        sd.play(tone, sample_rate)
        sd.wait()
        
        print("  ✅ Audio output working")
        return True
        
    except Exception as e:
        print(f"  ❌ Audio error: {e}")
        return False

def test_csv_files():
    """Test if EEG CSV files exist"""
    print("\n🔍 Testing EEG data files...")
    
    files = [
        "/Users/e.baena/CascadeProjects/test_eeg_data.csv",
        "/Users/e.baena/Desktop/SUNDAI_STUFF/EEG Counter/Feautres/eeg_metrics.csv"
    ]
    
    found = []
    missing = []
    
    for file_path in files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {path.name} ({size:,} bytes)")
            found.append(file_path)
        else:
            print(f"  ⚠️  {path.name} - NOT FOUND")
            missing.append(file_path)
    
    return len(found) > 0, found

def test_components():
    """Test music generator components"""
    print("\n🔍 Testing music generator components...")
    
    try:
        from brainwave_music_generator import BrainwaveMusicGenerator
        print("  ✅ Music generator imported")
        
        generator = BrainwaveMusicGenerator()
        print("  ✅ Generator created")
        
        # Test band analysis
        import numpy as np
        test_data = np.random.randn(8, 250)
        bands = generator.analyze_eeg_bands(test_data)
        print(f"  ✅ Band analysis working: {list(bands.keys())}")
        
        # Test music mapping
        music_params = generator.map_brainwaves_to_music(bands)
        print(f"  ✅ Music mapping working: {list(music_params.keys())}")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧠🎵 Brainwave Music Generator - Setup Test")
    print("=" * 60)
    print()
    
    results = []
    
    # Test imports
    success, failed = test_imports()
    results.append(('Dependencies', success))
    
    if failed:
        print(f"\n❌ Missing packages: {', '.join(failed)}")
        print("📦 Install with: pip install -r requirements.txt")
    
    # Test EEG handler
    results.append(('EEG Handler', test_eeg_handler()))
    
    # Test CSV files
    success, found = test_csv_files()
    results.append(('EEG Data Files', success))
    
    # Test components
    results.append(('Music Components', test_components()))
    
    # Test audio (optional)
    print("\n🔍 Testing audio (optional - may play sound)...")
    response = input("  Play test tone? (y/n): ").lower()
    if response == 'y':
        results.append(('Audio Output', test_audio()))
    else:
        print("  ⏭️  Skipped audio test")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:10} {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("\n🚀 Ready to run:")
        print("   python start_app.py")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("\n📝 Please fix the issues above before running the app")
    print("=" * 60)

if __name__ == "__main__":
    main()
