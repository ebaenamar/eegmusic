# Neurable EEG Format - Technical Documentation

## Overview

The Neurable 12-channel EEG device provides **preprocessed** data with pre-calculated band powers and cognitive metrics for left and right hemispheres.

## CSV Format

### Columns (27 total)

#### Left Hemisphere (13 columns)
```
Left__total_power      - Total signal power
Left__delta            - Delta band power (0.5-4 Hz) [normalized 0-1]
Left__theta            - Theta band power (4-8 Hz) [normalized 0-1]
Left__alpha            - Alpha band power (8-13 Hz) [normalized 0-1]
Left__beta             - Beta band power (13-30 Hz) [normalized 0-1]
Left__beta_low         - Low beta (13-20 Hz) [normalized 0-1]
Left__beta_high        - High beta (20-30 Hz) [normalized 0-1]
Left__gamma            - Gamma band power (30-50 Hz) [normalized 0-1]
Left__a_ta             - Alpha / (Theta + Alpha) ratio
Left__b_tb             - Beta / (Theta + Beta) ratio
Left__b_ab             - Beta / (Alpha + Beta) ratio
Left__mab_tmab         - (Alpha + Beta) / (Theta + Alpha + Beta) ratio
Left__p_bad            - Signal quality (0-1, higher = worse quality)
```

#### Right Hemisphere (13 columns)
Same structure as Left, with `Right__` prefix

#### Timestamp (1 column)
```
time                   - Unix timestamp (milliseconds)
```

### Example Row

```csv
Left__total_power,Left__delta,Left__theta,Left__alpha,Left__beta,...
619653980698.6157,0.01778,0.33025,0.21856,0.36582,...
```

## Neurological Interpretation

### Band Powers (Normalized 0-1)

| Band | Range | Interpretation |
|------|-------|----------------|
| Delta | 0.5-4 Hz | Deep sleep, unconscious processes |
| Theta | 4-8 Hz | Meditation, creativity, drowsiness |
| Alpha | 8-13 Hz | Relaxed awareness, calm focus |
| Beta | 13-30 Hz | Active thinking, concentration |
| Beta Low | 13-20 Hz | Focused attention |
| Beta High | 20-30 Hz | High cognitive load, anxiety |
| Gamma | 30-50 Hz | Peak performance, integration |

**Note:** Powers are already normalized to sum to ~1.0 per hemisphere

### Cognitive Ratios

#### 1. Alpha/Theta+Alpha (a_ta)
```
Focus Indicator = Alpha / (Theta + Alpha)
```
- **High (>0.5)**: Focused, alert, engaged
- **Low (<0.3)**: Drowsy, unfocused, daydreaming
- **Neurological basis**: Alpha dominance over theta indicates wakeful relaxation vs drowsiness

#### 2. Beta/Theta+Beta (b_tb)
```
Alertness = Beta / (Theta + Beta)
```
- **High (>0.5)**: Alert, active thinking
- **Low (<0.3)**: Relaxed, low arousal
- **Neurological basis**: Beta activity indicates cognitive engagement

#### 3. Beta/Alpha+Beta (b_ab)
```
Cognitive Load = Beta / (Alpha + Beta)
```
- **High (>0.6)**: High mental effort, stress
- **Low (<0.4)**: Low effort, relaxed
- **Neurological basis**: Beta/alpha ratio correlates with mental workload

#### 4. (Alpha+Beta)/(Theta+Alpha+Beta) (mab_tmab)
```
Engagement = (Alpha + Beta) / (Theta + Alpha + Beta)
```
- **High (>0.6)**: Engaged, attentive
- **Low (<0.4)**: Disengaged, drowsy
- **Neurological basis**: Combined alpha+beta indicates active engagement

### Signal Quality (p_bad)

```
Signal Quality = 1.0 - p_bad
```
- **p_bad < 0.2**: Excellent signal
- **p_bad 0.2-0.5**: Good signal
- **p_bad > 0.5**: Poor signal (artifacts, movement, poor contact)

## Hemisphere Specialization

### Left Hemisphere
**Specializations:**
- Sequential processing
- Language and verbal tasks
- Analytical thinking
- Logical reasoning
- Timing and rhythm

**Musical Mapping:**
- **Tempo**: Left beta activity → faster tempo
- **Rhythm**: Left theta → rhythm variation
- **Complexity**: Left beta → note density
- **Timing**: Left hemisphere timing precision

### Right Hemisphere
**Specializations:**
- Spatial processing
- Melody and pitch perception
- Holistic thinking
- Emotional processing
- Tonal quality

**Musical Mapping:**
- **Melody**: Right alpha → melodic complexity
- **Harmony**: Right alpha+gamma → harmonic richness
- **Timbre**: Right gamma → tone quality/brightness
- **Pitch**: Right hemisphere pitch perception

## Neurologically-Grounded Mapping

### 1. Arousal (Activation Level)

```python
# From alertness ratio (b_tb)
arousal = beta_theta_ratio
```

**Interpretation:**
- `arousal < 0.3`: Low energy (calm, drowsy)
- `0.3 < arousal < 0.7`: Moderate energy
- `arousal > 0.7`: High energy (alert, active)

### 2. Valence (Emotional Tone)

```python
# From focus ratio (a_ta)
valence = focus_ratio / 2  # Normalize to 0-1
```

**Interpretation:**
- `valence > 0.6`: Positive (focused, engaged)
- `0.4 < valence < 0.6`: Neutral
- `valence < 0.4`: Negative (unfocused, stressed)

**Neurological basis:** High alpha/theta ratio indicates positive, focused state

### 3. Cognitive Load

```python
# From beta/alpha ratio (b_ab)
cognitive_load = beta_alpha_ratio
```

**Interpretation:**
- `load < 0.3`: Low mental effort
- `0.3 < load < 0.6`: Moderate effort
- `load > 0.6`: High mental effort

### 4. Engagement

```python
# From mab_tmab ratio
engagement = (alpha + beta) / (theta + alpha + beta)
```

**Interpretation:**
- `engagement > 0.6`: Highly engaged
- `0.4 < engagement < 0.6`: Moderately engaged
- `engagement < 0.4`: Disengaged

## Musical Parameter Mapping

### Tempo
```python
# Left hemisphere beta (sequential processing)
base_tempo = 60 + arousal * 120  # 60-180 BPM
tempo_modulation = 1.0 + (left_beta - 0.2) * 0.5
final_tempo = base_tempo * tempo_modulation
```

### Scale Selection
```python
if valence > 0.6:
    scale = 'major'      # Positive, focused
elif valence < 0.4:
    scale = 'minor'      # Negative, unfocused
else:
    scale = 'pentatonic' # Neutral
```

### Melody Complexity
```python
# Right hemisphere alpha (creative processing)
melody_complexity = right_alpha
```

### Harmony Richness
```python
# Right hemisphere alpha + gamma
harmony = (right_alpha + right_gamma) / 2
```

### Rhythm Variation
```python
# Left hemisphere theta (timing variation)
rhythm_variation = left_theta
```

### Energy/Volume
```python
# Overall engagement
energy = engagement_ratio
```

### Instrumentation

#### Drums (Rhythm)
```python
if arousal > 0.3:
    drums_enabled = True
    complexity = cognitive_load
```

#### Bass (Foundation)
```python
bass_presence = (left_delta + right_delta) / 2
if arousal > 0.5:
    bass_pattern = 'pulsing'
else:
    bass_pattern = 'steady'
```

#### Chords (Harmony)
```python
chord_richness = (right_alpha + right_gamma) / 2
if valence > 0.5:
    chord_type = 'major'
else:
    chord_type = 'minor'
```

#### Melody (Lead)
```python
num_notes = 2 + arousal * 6 + cognitive_load * 2
melodic_range = right_alpha  # Higher alpha = wider range
```

#### Pads (Ambient)
```python
if arousal < 0.6:
    pad_enabled = True
    pad_volume = 1.0 - arousal
```

## Signal Quality Handling

### Quality Assessment
```python
signal_quality = 1.0 - p_bad

if signal_quality < 0.5:
    # Low quality - reduce weight or skip
    logger.warning("Low signal quality")
```

### Hemisphere Weighting
```python
# Weight by signal quality
left_weight = left_quality / (left_quality + right_quality)
right_weight = right_quality / (left_quality + right_quality)

# Weighted average
combined_value = (left_value * left_weight + 
                 right_value * right_weight)
```

## Example Data Flow

### Input (CSV Row)
```python
{
    'Left__delta': 0.018,
    'Left__theta': 0.330,
    'Left__alpha': 0.219,
    'Left__beta': 0.366,
    'Left__gamma': 0.068,
    'Left__a_ta': 0.406,     # Focus
    'Left__b_tb': 0.526,     # Alertness
    'Left__b_ab': 0.614,     # Cognitive load
    'Left__mab_tmab': 0.523, # Engagement
    'Left__p_bad': 0.999,    # Poor signal!
    
    'Right__delta': 0.025,
    'Right__theta': 0.385,
    'Right__alpha': 0.270,
    'Right__beta': 0.254,
    'Right__gamma': 0.066,
    'Right__a_ta': 0.415,
    'Right__b_tb': 0.411,
    'Right__b_ab': 0.484,
    'Right__mab_tmab': 0.477,
    'Right__p_bad': 0.999
}
```

### Cognitive State
```python
{
    'focus': 0.41,           # Moderate focus
    'alertness': 0.47,       # Moderate alertness
    'cognitive_load': 0.55,  # Moderate-high load
    'engagement': 0.50,      # Moderate engagement
    'signal_quality': 0.00   # POOR! (p_bad = 0.999)
}
```

### Musical Parameters
```python
{
    'arousal': 0.47,         # Moderate energy
    'valence': 0.21,         # Low (unfocused)
    'tempo': 110,            # BPM
    'energy': 0.50,
    'complexity': 0.55,
    'melody_complexity': 0.27,
    'harmony': 0.17,
    'rhythm_variation': 0.36,
    'hemisphere_balance': 0.00
}
```

### Musical Output
```
Scale: Minor (valence < 0.4)
Tempo: 110 BPM (moderate arousal)
Progression: Melancholic (vi-IV-I-V)
Instruments: Chords + Bass (pulsing) + Melody (4-5 notes) + Drums
Style: "moderate balanced contemplative minor, melodic soft tones"
```

## Best Practices

### 1. Signal Quality Filtering
```python
if signal_quality < 0.5:
    # Skip or reduce weight
    continue
```

### 2. Temporal Smoothing
```python
# Use 5-sample moving average
smoothing_window = 5
```

### 3. Hemisphere Balance
```python
# Monitor balance
balance = abs(left_quality - right_quality)
if balance > 0.3:
    logger.warning("Hemisphere imbalance")
```

### 4. Outlier Detection
```python
# Check for unrealistic values
if any(band_power < 0 or band_power > 1):
    logger.error("Invalid band power")
    continue
```

## Advantages of Preprocessed Data

1. **No FFT required**: Band powers pre-calculated
2. **Cognitive metrics included**: Ratios provide direct insight
3. **Hemisphere separation**: Left/right specialization preserved
4. **Signal quality**: Built-in quality metric (p_bad)
5. **Normalized**: Powers already normalized to 0-1
6. **Real-time ready**: Optimized for streaming

## Limitations

1. **No raw signal**: Cannot apply custom filters
2. **Fixed bands**: Cannot adjust frequency ranges
3. **Quality dependency**: Poor signal affects all metrics
4. **Hemisphere averaging**: May lose spatial detail
5. **Proprietary format**: Specific to Neurable device

---

**Version:** 1.0.0  
**Device:** Neurable 12-channel EEG  
**Last Updated:** November 2025
