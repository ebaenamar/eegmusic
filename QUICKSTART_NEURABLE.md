# Neurable EEG Music Generator - Quick Start

## 🚀 Quick Start

### 1. Convert JSONL to CSV (if needed)
```bash
python jsonl_to_csv_converter.py /path/to/eeg_stream.jsonl
```

### 2. Run Stable Music Generator
```bash
# Default settings (recommended)
python stable_music_generator.py /path/to/eeg_data.csv

# High stability (smoother, slower changes)
python stable_music_generator.py --smoothing 20 --tempo-stability 0.9 data.csv

# More responsive (faster changes)
python stable_music_generator.py --smoothing 10 --tempo-stability 0.6 data.csv

# Longer musical phrases
python stable_music_generator.py --duration 8 data.csv
```

## 📊 Configuration Options

### Smoothing Window (`--smoothing`, `-s`)
- **Range**: 5-30 samples
- **Default**: 15
- **Effect**: Higher = smoother, more stable transitions
- **Recommended**:
  - `10`: Responsive, follows EEG changes quickly
  - `15`: Balanced (default)
  - `20`: Very stable, slow transitions

### Tempo Stability (`--tempo-stability`, `-t`)
- **Range**: 0.5-0.95
- **Default**: 0.8
- **Effect**: Higher = tempo changes more slowly
- **Recommended**:
  - `0.6`: Dynamic tempo changes
  - `0.8`: Balanced (default)
  - `0.9`: Very stable tempo

### Arrangement Duration (`--duration`, `-d`)
- **Range**: 3-10 seconds
- **Default**: 6
- **Effect**: Length of each musical phrase
- **Recommended**:
  - `4s`: Quick changes, more variety
  - `6s`: Balanced (default)
  - `8s`: Longer, more developed phrases

## 🎵 Example Commands

### For meditation/relaxation (very stable)
```bash
python stable_music_generator.py \
  --smoothing 20 \
  --tempo-stability 0.9 \
  --duration 8 \
  meditation_data.csv
```

### For active monitoring (responsive)
```bash
python stable_music_generator.py \
  --smoothing 10 \
  --tempo-stability 0.6 \
  --duration 4 \
  active_data.csv
```

### Default balanced mode
```bash
python stable_music_generator.py data.csv
```

## 🧠 What Gets Mapped

### Left Hemisphere → Tempo & Rhythm
- Beta activity → Tempo modulation
- Theta activity → Rhythm variation
- Sequential processing → Timing precision

### Right Hemisphere → Melody & Harmony
- Alpha activity → Melodic complexity
- Gamma activity → Harmonic richness
- Spatial processing → Tone quality

### Cognitive Ratios → Musical Features
- **Focus (α/θ+α)** → Valence (major/minor scale)
- **Alertness (β/θ+β)** → Arousal (tempo, energy)
- **Cognitive Load (β/α+β)** → Complexity
- **Engagement** → Overall energy level

## 🎼 Musical Output

### Scales (auto-selected by valence)
- **Major**: Valence > 0.55 (focused, positive)
- **Pentatonic**: 0.35 < Valence < 0.55 (neutral)
- **Minor**: Valence < 0.35 (unfocused, contemplative)

### Instruments
- **Chords**: Harmonic foundation
- **Bass**: Rhythmic foundation (pulsing/steady)
- **Melody**: 2-8 notes based on arousal
- **Drums**: Active when arousal > 0.3
- **Pads**: Ambient layer when arousal < 0.6

## 🔧 Troubleshooting

### Music changes too quickly
```bash
# Increase smoothing and tempo stability
python stable_music_generator.py --smoothing 20 --tempo-stability 0.9 data.csv
```

### Music too static/boring
```bash
# Decrease smoothing and tempo stability
python stable_music_generator.py --smoothing 8 --tempo-stability 0.6 data.csv
```

### Low signal quality warnings
- Check EEG electrode contact
- Data may have `p_bad` values > 0.5
- System will still work but with reduced accuracy

## 📁 File Formats

### Input: Neurable CSV
```csv
Left__total_power,Left__delta,Left__theta,Left__alpha,Left__beta,...
619653980698.6,0.0178,0.3302,0.2186,0.3658,...
```

### Input: Neurable JSONL
```json
{"Left__total_power": 900940197038.7, "Left__delta": 0.0364, ...}
{"Left__total_power": 299824794698.4, "Left__delta": 0.0481, ...}
```

## 🎯 Tips for Best Results

1. **Start with defaults**: Try default settings first
2. **Adjust gradually**: Change one parameter at a time
3. **Match your goal**:
   - Meditation → High stability
   - Active work → Medium stability
   - Gaming/sports → Low stability (responsive)
4. **Monitor quality**: Watch for signal quality warnings
5. **Experiment**: Different people may prefer different settings

## 📊 Understanding the Output

### Console Output
```
🎵 Scale=pentatonic | Tempo=  95 BPM | Arousal=0.45 | Valence=0.38 | Quality=0.00
```

- **Scale**: Current musical scale
- **Tempo**: Beats per minute (60-140 range)
- **Arousal**: Energy level (0-1)
- **Valence**: Emotional tone (0-1)
- **Quality**: Signal quality (0-1, higher is better)

### Log Messages
- `🎼 Generated`: New musical phrase created
- `⚠️ Low signal quality`: EEG signal quality < 0.3
- `🎼 Scale change`: Musical scale changed

## 🔄 Comparison: Original vs Stable

| Feature | Original | Stable |
|---------|----------|--------|
| Smoothing | 5 samples | 15 samples (configurable) |
| Tempo changes | Immediate | Gradual (weighted avg) |
| Scale changes | Immediate | After 8 samples |
| Transitions | Direct | Interpolated |
| Complexity | Full | Reduced (70%) |
| Rhythm variation | Full | Reduced (50%) |

## 📝 Notes

- Press `Ctrl+C` to stop playback
- Audio plays continuously with smooth transitions
- Each arrangement duration should match the delay parameter
- System automatically handles signal quality weighting
- Hemisphere data is balanced by signal quality

---

**For more details, see:**
- `NEURABLE_FORMAT.md` - Technical format documentation
- `TECHNICAL_DOCUMENTATION.md` - Full system architecture
- `README.md` - General project overview
