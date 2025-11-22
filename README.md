# 🧠🎵 Brainwave Music Generator

Transform EEG brainwave patterns into beautiful, real-time generated music using neurologically-grounded mappings.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Neurable Compatible](https://img.shields.io/badge/Neurable-12ch-green.svg)](https://neurable.com/)

## Features

- **Real-time Music Generation**: Converts EEG signals into musical compositions
- **Brainwave Mapping**: 
  - Delta waves → Bass frequencies
  - Theta waves → Rhythm and tempo
  - Alpha waves → Melody complexity (relaxation)
  - Beta waves → Energy and volume (focus)
  - Gamma waves → High frequencies and brightness
- **Interactive Web Dashboard**: Beautiful real-time visualization
- **Multiple Musical Scales**: Pentatonic, Major, Minor, Blues
- **Configurable Parameters**: Base frequency, scale selection, playback speed

## How It Works

1. **EEG Analysis**: Analyzes brainwave data using FFT to extract power in different frequency bands
2. **Musical Mapping**: Maps brainwave patterns to musical parameters:
   - Higher alpha = more complex melodies
   - Higher beta = more energetic music
   - Higher theta = faster tempo
   - Higher delta = stronger bass
   - Higher gamma = brighter tones
3. **Sound Generation**: Creates musical notes with harmonics and ADSR envelopes
4. **Real-time Playback**: Streams generated audio continuously

## Installation

1. **Install dependencies**:
   ```bash
   cd /Users/e.baena/CascadeProjects/eeg-music-generator
   pip install -r requirements.txt
   ```

2. **Verify audio device**:
   ```bash
   python -c "import sounddevice as sd; print(sd.query_devices())"
   ```

## Usage

### Quick Start

```bash
python start_app.py
```

This will:
- Check dependencies
- Start the WebSocket server
- Open the dashboard in your browser
- Begin streaming when you click "Start Music"

### Manual Start

1. **Start the server**:
   ```bash
   python music_server.py
   ```

2. **Open dashboard**:
   - Open `web_dashboard.html` in your browser
   - Or navigate to: `file:///Users/e.baena/CascadeProjects/eeg-music-generator/web_dashboard.html`

3. **Generate music**:
   - Select an EEG data file
   - Choose a musical scale
   - Adjust base frequency
   - Click "Start Music"

### Standalone Mode (No Dashboard)

```bash
python brainwave_music_generator.py
```

## Dashboard Features

- **Real-time Brainwave Visualization**: See power levels in all 5 frequency bands
- **Music Parameters Display**: Monitor energy, melody, tempo, bass, and brightness
- **EEG Signal Plot**: View raw EEG data in real-time
- **Power Timeline**: Track brainwave changes over time
- **Controls**: Start/stop, scale selection, frequency adjustment

## Musical Scales

- **Pentatonic**: Peaceful, meditative (default)
- **Major**: Happy, uplifting
- **Minor**: Melancholic, introspective
- **Blues**: Soulful, expressive

## EEG Data Format

The system works with CSV files containing EEG channel data:
- 8 channels: CH1-CH8
- Sampling rate: 250Hz (configurable)
- Format: CSV with channel headers

### Example Files

- `/Users/e.baena/CascadeProjects/test_eeg_data.csv` - Test data (8 channels, 1000 samples)
- Custom CSV files with EEG recordings

## Architecture

```
┌─────────────────┐
│  EEG CSV File   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  EEG Stream     │
│  Handler        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FFT Analysis   │
│  (Band Powers)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Music Mapper   │
│  (Parameters)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Sound Gen      │
│  (Audio)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│  Audio Output   │     │  Web Dashboard  │
│  (Speakers)     │◄────┤  (WebSocket)    │
└─────────────────┘     └─────────────────┘
```

## Customization

### Change Musical Scale

Edit in dashboard or modify `brainwave_music_generator.py`:
```python
self.scales = {
    'custom': [0, 2, 4, 7, 9, 11],  # Your custom scale
}
```

### Adjust Mapping

Modify `map_brainwaves_to_music()` in `brainwave_music_generator.py`:
```python
music_params['tempo'] = 60 + band_powers.get('theta', 0.5) * 180
```

### Add Effects

Extend `generate_note()` to add reverb, delay, or other effects.

## Troubleshooting

### No Audio Output
```bash
# Check audio devices
python -c "import sounddevice as sd; print(sd.query_devices())"

# Test audio
python -c "import sounddevice as sd; import numpy as np; sd.play(np.sin(2*np.pi*440*np.linspace(0,1,44100)), 44100); sd.wait()"
```

### WebSocket Connection Failed
- Ensure port 8765 is not in use
- Check firewall settings
- Try restarting the server

### Poor Audio Quality
- Adjust `sample_rate` (default: 44100)
- Modify ADSR envelope parameters
- Change amplitude levels

## Future Enhancements

- [ ] MIDI output support
- [ ] Multiple instrument synthesis
- [ ] Audio effects (reverb, delay, chorus)
- [ ] Recording and export to WAV/MP3
- [ ] Real-time EEG device support (OpenBCI, Muse)
- [ ] Machine learning for better mapping
- [ ] Collaborative sessions (multiple users)

## Credits

Built on top of:
- `eeg_stream_handler.py` - EEG streaming infrastructure
- `sounddevice` - Audio playback
- `websockets` - Real-time communication
- Chart.js - Dashboard visualization

## License

MIT License - Feel free to use and modify!

---

**Enjoy creating music with your mind! 🧠🎵**
