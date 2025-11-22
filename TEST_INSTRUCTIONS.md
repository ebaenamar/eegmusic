# Testing Instructions - Neurable EEG Music Generator

## 📦 Repository
```
https://github.com/ebaenamar/eegmusic
Branch: mrvertigo
```

## 🚀 Quick Test

### 1. Clone and Setup
```bash
git clone https://github.com/ebaenamar/eegmusic.git
cd eegmusic
git checkout mrvertigo

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Convert Your Data (if JSONL)
```bash
python jsonl_to_csv_converter.py /path/to/eeg_stream.jsonl
# Output: /path/to/eeg_stream.csv
```

### 3. Run the Generator
```bash
# Default stable settings
python stable_music_generator.py /path/to/eeg_stream.csv

# Or with custom settings
python stable_music_generator.py \
  --smoothing 15 \
  --tempo-stability 0.85 \
  --duration 6 \
  /path/to/eeg_stream.csv
```

## 📁 Files Included

### Core System
- `stable_neurable_adapter.py` - Enhanced EEG adapter with smoothing
- `stable_music_generator.py` - Main generator with CLI options
- `neurable_adapter.py` - Original adapter (less stable)
- `neurable_music_generator.py` - Original generator
- `advanced_music_generator.py` - Multi-instrument synthesis
- `neuro_music_mapper.py` - Neurological mapping

### Utilities
- `jsonl_to_csv_converter.py` - Convert JSONL to CSV format

### Documentation
- `QUICKSTART_NEURABLE.md` - Quick start guide with examples
- `NEURABLE_FORMAT.md` - Technical format documentation
- `TECHNICAL_DOCUMENTATION.md` - Full system architecture
- `README.md` - Project overview

## 🎵 What to Expect

### Audio Output
- **Instruments**: Chords, bass, melody, drums, pads
- **Duration**: 6 seconds per phrase (configurable)
- **Tempo**: 60-140 BPM (adapts to arousal)
- **Scales**: Major, Minor, Pentatonic (adapts to valence)

### Console Output
```
🎵 Scale=pentatonic | Tempo=  95 BPM | Arousal=0.45 | Valence=0.38 | Quality=0.00
🎼 Generated: melancholic progression, 4 chords, tempo=95 BPM
```

## ⚙️ Configuration Presets

### Meditation/Relaxation (Very Stable)
```bash
python stable_music_generator.py \
  --smoothing 20 \
  --tempo-stability 0.9 \
  --duration 8 \
  data.csv
```

### Balanced (Default - Recommended)
```bash
python stable_music_generator.py data.csv
```

### Responsive/Dynamic
```bash
python stable_music_generator.py \
  --smoothing 10 \
  --tempo-stability 0.6 \
  --duration 4 \
  data.csv
```

## 🔍 Key Improvements Over Original

1. **Temporal Smoothing**: 15-sample window (vs 5)
2. **Tempo Stability**: Weighted averaging prevents jumps
3. **Scale Stability**: Changes only after 8 consistent samples
4. **Parameter Interpolation**: 70% previous + 30% new
5. **Reduced Variation**: Melody complexity and rhythm variation reduced
6. **Enhanced Logging**: Status every 5 samples

## 🧪 Test Data

### Included Test Files
- Original 8-channel format: `/Users/e.baena/CascadeProjects/test_eeg_data.csv`
- Neurable format: `/Users/e.baena/CascadeProjects/mindfulmakers/neurable-eeg-stream/*.csv`

### Your Data
- Desktop JSONL: `/Users/e.baena/Desktop/eeg_stream.jsonl`
- Desktop CSV: `/Users/e.baena/Desktop/eeg_stream.csv` (after conversion)

## 📊 Expected Behavior

### Good Signal Quality (p_bad < 0.3)
- Smooth musical transitions
- Consistent tempo and scale
- Rich harmonic content
- All instruments active

### Poor Signal Quality (p_bad > 0.5)
- ⚠️ Warnings in console
- Reduced musical complexity
- System still works but less accurate
- May sound more random

## 🐛 Troubleshooting

### No Audio
```bash
# Check audio devices
python -c "import sounddevice as sd; print(sd.query_devices())"

# Test audio
python -c "import sounddevice as sd; import numpy as np; sd.play(np.sin(2*np.pi*440*np.linspace(0,1,44100)), 44100); sd.wait()"
```

### Music Too Unstable
- Increase `--smoothing` (try 20)
- Increase `--tempo-stability` (try 0.9)
- Increase `--duration` (try 8)

### Music Too Static
- Decrease `--smoothing` (try 10)
- Decrease `--tempo-stability` (try 0.6)
- Decrease `--duration` (try 4)

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

## 📈 Performance

- **Latency**: ~100ms per sample
- **CPU Usage**: Moderate (audio synthesis)
- **Memory**: ~200MB
- **Real-time**: Yes (processes faster than playback)

## 🎯 Success Criteria

✅ Audio plays continuously  
✅ Smooth transitions between phrases  
✅ Tempo changes gradually  
✅ Scale changes infrequently  
✅ Musical coherence maintained  
✅ Console shows regular updates  

## 📝 Notes

- Press `Ctrl+C` to stop playback
- First few samples may sound less stable (building history)
- Signal quality warnings are normal if p_bad > 0.5
- Hemisphere balance affects left/right musical features
- Each CSV row generates one musical phrase

## 🔗 Links

- **Repository**: https://github.com/ebaenamar/eegmusic
- **Branch**: mrvertigo
- **Quick Start**: See `QUICKSTART_NEURABLE.md`
- **Format Docs**: See `NEURABLE_FORMAT.md`

---

**Ready to test!** 🎵🧠
