# 🚀 Quick Start Guide

## First Time Setup (5 minutes)

1. **Run setup script**:
   ```bash
   cd /Users/e.baena/CascadeProjects/eeg-music-generator
   ./setup.sh
   ```
   
   This will:
   - Create a virtual environment
   - Install all dependencies (numpy, sounddevice, websockets, pandas, scipy)
   - Prepare the app for use

## Running the App

### Option 1: Quick Run (Recommended)
```bash
./run.sh
```

### Option 2: Manual Run
```bash
source venv/bin/activate
python start_app.py
```

### Option 3: Server Only (for development)
```bash
source venv/bin/activate
python music_server.py
```
Then open `web_dashboard.html` in your browser.

## Using the Dashboard

1. **Dashboard opens automatically** in your browser
2. **Select EEG data file** from dropdown
3. **Choose musical scale**:
   - Pentatonic (peaceful)
   - Major (happy)
   - Minor (melancholic)
   - Blues (soulful)
4. **Adjust base frequency** (110-440 Hz)
5. **Click "Start Music"** 🎵
6. **Watch the magic happen!**
   - See brainwaves in real-time
   - Monitor music parameters
   - Visualize EEG signals

## What You'll See

### Brainwave Bands
- **Delta** (0.5-4 Hz) → Controls bass
- **Theta** (4-8 Hz) → Controls tempo/rhythm
- **Alpha** (8-13 Hz) → Controls melody complexity
- **Beta** (13-30 Hz) → Controls energy/volume
- **Gamma** (30-50 Hz) → Controls brightness

### Music Parameters
- **Energy**: How loud/intense the music is
- **Melody**: How complex the melodies are
- **Tempo**: Speed in BPM (60-180)
- **Bass**: Low frequency presence
- **Brightness**: High frequency content

## Troubleshooting

### No sound?
```bash
# Test audio
source venv/bin/activate
python -c "import sounddevice as sd; print(sd.query_devices())"
```

### WebSocket error?
- Make sure port 8765 is not in use
- Restart the server

### Dashboard not opening?
- Manually open: `/Users/e.baena/CascadeProjects/eeg-music-generator/web_dashboard.html`

## Tips for Best Results

1. **Start with Pentatonic scale** - it's the most pleasant
2. **Use base frequency 220 Hz** (A3) - good middle ground
3. **Let it run for 30+ seconds** - patterns emerge over time
4. **Try different EEG files** - each creates unique music
5. **Experiment with scales** - different moods for different data

## Stopping the App

Press `Ctrl+C` in the terminal

## Next Steps

- Read the full [README.md](README.md) for advanced features
- Modify `brainwave_music_generator.py` to customize mappings
- Add your own EEG CSV files
- Experiment with different musical scales

---

**Enjoy creating music with your mind! 🧠🎵**
