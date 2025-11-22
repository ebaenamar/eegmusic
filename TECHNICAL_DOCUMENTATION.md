# 🧠🎵 Brainwave Music Generator - Technical Documentation

## Overview

A neurologically-grounded system that generates real-time music from EEG brainwave patterns. The system uses scientifically-based mappings from neural activity to musical parameters, ensuring consistency and musical coherence.

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    EEG Input Layer                          │
│  CSV File → Stream Handler → (8 channels × 250 samples)    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Signal Processing Layer                    │
│  FFT Analysis → Band Power Extraction → Normalization      │
│  Output: {delta, theta, alpha, beta, gamma}                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Neurological Mapping Layer                     │
│  Band Powers → Arousal/Valence/Cognitive Load              │
│  Temporal Smoothing (5-sample window)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                Music Generation Layer                       │
│  Chords + Bass + Melody + Drums + Pads                     │
│  Output: 4-second musical arrangement                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
                  🔊 Audio Output
```

## Input Specifications

### EEG Signal Format

```python
# Input shape
eeg_data: np.ndarray
shape: (channels, samples)
example: (8, 250)

# Specifications
channels: 8 (CH1-CH8)
sampling_rate: 250 Hz
window_duration: 1 second
data_range: typically -100 to +100 μV (normalized)

# CSV Format
CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8
-0.142,0.343,0.419,0.561,-0.128,-0.139,-0.243,0.273
-0.110,-0.162,0.352,0.622,-0.363,-0.369,0.016,0.160
...
```

### Frequency Bands

| Band  | Frequency Range | Associated State           |
|-------|----------------|----------------------------|
| Delta | 0.5-4 Hz       | Deep sleep, unconscious    |
| Theta | 4-8 Hz         | Meditation, creativity     |
| Alpha | 8-13 Hz        | Relaxed awareness          |
| Beta  | 13-30 Hz       | Active thinking, focus     |
| Gamma | 30-50 Hz       | Peak cognitive performance |

## Signal Processing Pipeline

### 1. FFT Analysis

```python
def analyze_eeg_bands(eeg_data: np.ndarray) -> Dict[str, float]:
    """
    Extract power in each frequency band using FFT.
    
    Input: (8, 250) - 8 channels, 250 samples
    Output: {'delta': 0.2, 'theta': 0.25, ...}
    """
    
    for band_name, (low_freq, high_freq) in bands.items():
        # Apply FFT to all channels
        fft_vals = np.fft.fft(eeg_data, axis=1)
        freqs = np.fft.fftfreq(250, 1.0/250)
        
        # Extract power in frequency band
        band_mask = (freqs >= low_freq) & (freqs <= high_freq)
        band_power = np.mean(np.abs(fft_vals[:, band_mask])**2)
        
    # Normalize to sum = 1.0
    return normalized_powers
```

**Frequency Resolution:**
- Window: 250 samples at 250 Hz
- Resolution: 1 Hz per bin
- Nyquist frequency: 125 Hz

### 2. Band Power Normalization

```python
# Normalize powers to sum to 1.0
total_power = sum(band_powers.values())
normalized = {k: v/total for k, v in band_powers.items()}

# Example output:
{
    'delta': 0.15,  # 15% of total power
    'theta': 0.20,  # 20%
    'alpha': 0.35,  # 35% (dominant)
    'beta': 0.20,   # 20%
    'gamma': 0.10   # 10%
}
```

## Neurological Mapping

### Psychological Dimensions

The system maps brainwave patterns to three core psychological dimensions based on neuroscience research:

#### 1. Arousal (Activation Level)

```python
arousal = (
    0.1 * delta +    # Very low activation
    0.2 * theta +    # Low activation
    0.3 * alpha +    # Medium activation
    0.5 * beta +     # High activation
    0.7 * gamma      # Very high activation
)
# Range: [0, 1]
```

**Interpretation:**
- `arousal < 0.3`: Low energy, drowsy, calm
- `0.3 < arousal < 0.7`: Moderate energy, balanced
- `arousal > 0.7`: High energy, alert, active

#### 2. Valence (Emotional Tone)

```python
valence = alpha - 0.3*theta - 0.2*abs(beta - theta)
valence = (valence + 0.5) / 1.0  # Normalize to [0, 1]
```

**Interpretation:**
- `valence > 0.6`: Positive emotion (happy, relaxed)
- `0.4 < valence < 0.6`: Neutral emotion
- `valence < 0.4`: Negative emotion (stressed, anxious)

**Neurological Basis:**
- High alpha: Associated with positive affect and relaxation
- High theta: Associated with drowsiness or anxiety
- Beta/theta imbalance: Indicator of stress

#### 3. Cognitive Load (Mental Effort)

```python
cognitive_load = (beta + 0.5*gamma) / (alpha + 0.1)
# Range: [0, 1+]
```

**Interpretation:**
- `load < 0.3`: Low mental effort, relaxed
- `0.3 < load < 0.6`: Moderate effort
- `load > 0.6`: High mental effort, concentration

### Cognitive State Detection

```python
states = {
    'deep_rest': {
        'delta': > 0.4, 'beta': < 0.2
    },
    'meditation': {
        'theta': > 0.35, 'alpha': > 0.35
    },
    'relaxed_focus': {
        'alpha': > 0.45, 'beta': > 0.25
    },
    'active_focus': {
        'beta': > 0.4, 'gamma': > 0.2
    },
    'high_performance': {
        'beta': > 0.35, 'gamma': > 0.3
    }
}
```

### Temporal Smoothing

To prevent abrupt musical changes:

```python
smoothing_window = 5  # samples

# Each parameter is averaged over last 5 readings
arousal_smoothed = mean([arousal_t-4, ..., arousal_t])
valence_smoothed = mean([valence_t-4, ..., valence_t])
cognitive_load_smoothed = mean([load_t-4, ..., load_t])
```

**Effect:** Smooth transitions between musical states, preventing jarring changes.

## Musical Mapping

### Tempo Mapping

```python
# Arousal controls tempo
if arousal > 0.7:
    tempo_range = (120, 180)  # Fast
elif arousal > 0.4:
    tempo_range = (90, 120)   # Moderate
else:
    tempo_range = (60, 90)    # Slow

tempo = 60 + arousal * 120  # Linear mapping
```

### Scale Selection

```python
# Valence controls musical scale
if valence > 0.6:
    scale = 'major'           # Happy, uplifting
    intervals = [0,2,4,5,7,9,11]
elif valence < 0.4:
    scale = 'minor'           # Sad, melancholic
    intervals = [0,2,3,5,7,8,10]
else:
    scale = 'pentatonic'      # Neutral, peaceful
    intervals = [0,2,4,7,9]
```

### Chord Progressions

```python
progressions = {
    'uplifting': [I, V, vi, IV],      # valence > 0.6
    'peaceful': [I, IV, V, I],        # 0.4 < valence < 0.6
    'melancholic': [vi, IV, I, V],    # valence < 0.4
    'emotional': [I, vi, IV, V]
}
```

### Instrumentation

#### Chords (Harmony)
```python
# 4-chord progression, 1 second each
# Triad type based on valence
if valence > 0.5:
    chord_intervals = [0, 4, 7]  # Major triad
else:
    chord_intervals = [0, 3, 7]  # Minor triad

# ADSR envelope
attack = 0.1
decay = 0.2
sustain = 0.6
release = 0.3
```

#### Bass Line
```python
# One octave below root
bass_freq = root_freq / 2

if arousal > 0.5:
    pattern = 'pulsing'  # 4 pulses per measure
else:
    pattern = 'steady'   # Sustained note

amplitude = 0.5
```

#### Melody
```python
# Number of notes
num_notes = int(2 + arousal*6 + complexity*2)  # 2-10 notes
num_notes = clamp(num_notes, 2, 10)

# Melodic movement (stepwise, not jumps)
for i in range(num_notes):
    if i > 0:
        movement = int((rhythm_variation - 0.5) * 3)  # -1, 0, +1
        scale_degree = (scale_degree + movement) % len(scale)
    
    # Octave based on arousal
    octave = 1 if arousal < 0.3 else (2 if arousal < 0.7 else 3)
```

#### Drums/Percussion
```python
if arousal > 0.3:
    # Kick drum (60 Hz sine burst)
    kick_on_beats = [1, 3]  # Beats 1 and 3
    
    # Hi-hat (filtered noise)
    hihat_on_beats = all_beats if complexity > 0.3
    
    # Snare (200 Hz + noise)
    snare_on_beats = [2, 4] if complexity > 0.5
```

#### Ambient Pad
```python
if arousal < 0.6:
    # Sustained chords with slow attack/release
    attack = 0.3
    release = 0.4
    amplitude = 0.15  # Quiet background layer
```

## Audio Generation

### Synthesis Parameters

```python
sample_rate = 44100 Hz
arrangement_duration = 4 seconds
total_samples = 176400

# Waveform generation
waveform = 'sine'  # with harmonics
harmonics = 3      # fundamental + 2 overtones
```

### ADSR Envelope

```python
def generate_adsr_envelope(num_samples, attack, decay, sustain, release):
    """
    Attack: 0 → 1
    Decay: 1 → sustain_level
    Sustain: sustain_level (held)
    Release: sustain_level → 0
    """
    envelope = np.ones(num_samples)
    
    attack_samples = int(attack * num_samples)
    decay_samples = int(decay * num_samples)
    release_samples = int(release * num_samples)
    
    # Apply envelope stages
    # ...
    
    return envelope
```

### Mixing

```python
# Final arrangement mix
arrangement = (
    chords * 0.25 +      # 25% volume
    bass * 0.5 +         # 50% volume
    melody * 0.3 +       # 30% volume
    drums * 0.4 +        # 40% volume
    pad * 0.15           # 15% volume
)

# Normalize to prevent clipping
max_val = np.max(np.abs(arrangement))
arrangement = arrangement / max_val * 0.8  # Leave headroom
```

## Performance Characteristics

### Latency

```
EEG Reading: ~1 second (250 samples)
FFT Analysis: ~10 ms
Neurological Mapping: ~5 ms
Music Generation: ~500 ms
Total Latency: ~1.5 seconds
```

### Update Rate

```
New music generated every: ~4 seconds
(generation time + playback time)

Smooth transitions via:
- Temporal smoothing (5-sample window)
- Consistent chord progressions
- Stepwise melodic motion
```

### Computational Complexity

```
FFT: O(n log n) where n = 250 samples
Band Extraction: O(n * b) where b = 5 bands
Music Generation: O(m) where m = arrangement samples
Total: O(n log n) dominated by FFT
```

## Example Mapping

### Input EEG State

```python
band_powers = {
    'delta': 0.10,   # Low (awake)
    'theta': 0.15,   # Low-medium
    'alpha': 0.50,   # High (relaxed)
    'beta': 0.20,    # Medium (some focus)
    'gamma': 0.05    # Low
}
```

### Psychological Dimensions

```python
arousal = 0.26          # Low-medium (calm)
valence = 0.67          # Positive (happy/relaxed)
cognitive_load = 0.38   # Low (little mental effort)
state = 'relaxed_focus'
```

### Musical Parameters

```python
tempo = 90 BPM
scale = 'major'
progression = 'uplifting' [I, V, vi, IV]
num_notes = 4-5
instruments = ['chords', 'bass_steady', 'melody', 'pad']
drums = False  # arousal < 0.3
```

### Musical Description

```
"slow calm uplifting lo-fi chill, melodic soft tones"
```

## API Reference

### Main Classes

#### `BrainwaveMusicGenerator`
```python
generator = BrainwaveMusicGenerator(sample_rate=44100)

# Start generation from EEG stream
generator.start_music_generation(eeg_stream_manager)

# Stop generation
generator.stop_music_generation(eeg_stream_manager)
```

#### `NeuroMusicMapper`
```python
mapper = NeuroMusicMapper(smoothing_window=5)

# Get musical parameters from band powers
params = mapper.get_musical_parameters(band_powers)
# Returns: {arousal, valence, cognitive_load, tempo, ...}

# Get music description
description = mapper.map_to_music_description(band_powers)
# Returns: "slow calm uplifting ambient, melodic soft tones"
```

#### `AdvancedMusicGenerator`
```python
generator = AdvancedMusicGenerator(sample_rate=44100)

# Generate full arrangement
audio = generator.generate_full_arrangement(
    music_params,
    duration=4.0
)
# Returns: np.ndarray of shape (176400,)
```

## Configuration

### Adjustable Parameters

```python
# Smoothing
smoothing_window = 5  # samples (default)

# Music generation
arrangement_duration = 4.0  # seconds
sample_rate = 44100  # Hz

# EEG processing
window_size = 250  # samples
sampling_rate = 250  # Hz

# Audio queue
max_queue_size = 10  # arrangements
```

## Future Enhancements

### Potential Improvements

1. **Channel-specific mapping**
   - Frontal channels → Attention/focus
   - Posterior channels → Visual processing
   - Central channels → Motor activity

2. **Advanced signal processing**
   - Notch filter at 60Hz (power line noise)
   - Bandpass filter 0.5-50Hz
   - Artifact rejection (eye blinks, muscle)

3. **Enhanced musical features**
   - MIDI output
   - Multiple instrument timbres
   - Audio effects (reverb, delay)
   - Recording/export functionality

4. **Machine learning**
   - Learn user preferences
   - Personalized mappings
   - Style transfer

## References

### Neuroscience Basis

- Arousal/Valence model: Russell (1980)
- EEG band associations: Niedermeyer & da Silva (2005)
- Cognitive load: Gevins & Smith (2003)

### Musical Theory

- Chord progressions: Common practice harmony
- Scale selection: Emotional associations (Hevner, 1936)
- Instrumentation: Orchestration principles

## License

MIT License - See LICENSE file for details

---

**Version:** 1.0.0  
**Last Updated:** November 2025  
**Authors:** EEG Music Generator Team
