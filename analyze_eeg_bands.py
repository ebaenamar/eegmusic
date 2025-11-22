#!/usr/bin/env python3
"""
Analyze EEG band characteristics for synesthetic music mapping
"""

import pandas as pd
import numpy as np
import sys

def analyze_eeg_bands(csv_path, num_samples=100):
    """Analyze EEG bands to find unique characteristics"""
    
    print("=" * 80)
    print("🧠 EEG BAND ANALYSIS FOR SYNESTHETIC MAPPING")
    print("=" * 80)
    print(f"\n📂 CSV: {csv_path}")
    print(f"📊 Analyzing {num_samples} samples\n")
    
    # Read CSV
    df = pd.read_csv(csv_path)
    df = df.head(num_samples)
    
    # Extract band powers
    bands = {
        'Delta': (df['Left__delta'] + df['Right__delta']) / 2,
        'Theta': (df['Left__theta'] + df['Right__theta']) / 2,
        'Alpha': (df['Left__alpha'] + df['Right__alpha']) / 2,
        'Beta': (df['Left__beta'] + df['Right__beta']) / 2,
        'Gamma': (df['Left__gamma'] + df['Right__gamma']) / 2
    }
    
    # Calculate ratios (these are the "fingerprints")
    ratios = {
        'Delta/Theta': bands['Delta'] / (bands['Theta'] + 0.001),
        'Alpha/Beta': bands['Alpha'] / (bands['Beta'] + 0.001),
        'Beta/Gamma': bands['Beta'] / (bands['Gamma'] + 0.001),
        'Theta/Alpha': bands['Theta'] / (bands['Alpha'] + 0.001),
        'Low_Freq': (bands['Delta'] + bands['Theta']) / 2,
        'High_Freq': (bands['Beta'] + bands['Gamma']) / 2
    }
    
    print("=" * 80)
    print("📊 BAND POWER STATISTICS")
    print("=" * 80)
    
    for band_name, values in bands.items():
        mean = values.mean()
        std = values.std()
        cv = (std / mean * 100) if mean > 0 else 0
        print(f"\n{band_name}:")
        print(f"  Mean: {mean:.4f}")
        print(f"  Std:  {std:.4f}")
        print(f"  CV:   {cv:.1f}%")
        print(f"  Range: {values.min():.4f} - {values.max():.4f}")
    
    print("\n" + "=" * 80)
    print("🔬 BAND RATIOS (EEG Fingerprint)")
    print("=" * 80)
    
    for ratio_name, values in ratios.items():
        mean = values.mean()
        std = values.std()
        print(f"\n{ratio_name}:")
        print(f"  Mean: {mean:.3f}")
        print(f"  Std:  {std:.3f}")
        print(f"  Range: {values.min():.3f} - {values.max():.3f}")
    
    print("\n" + "=" * 80)
    print("🎵 SYNESTHETIC MAPPING RECOMMENDATIONS")
    print("=" * 80)
    
    # Dominant band
    band_means = {name: values.mean() for name, values in bands.items()}
    dominant_band = max(band_means, key=band_means.get)
    
    print(f"\n🏆 Dominant Band: {dominant_band} ({band_means[dominant_band]:.4f})")
    
    # Musical characteristics
    delta_theta_ratio = ratios['Delta/Theta'].mean()
    alpha_beta_ratio = ratios['Alpha/Beta'].mean()
    low_high_ratio = ratios['Low_Freq'].mean() / (ratios['High_Freq'].mean() + 0.001)
    
    print("\n🎼 Suggested Musical Characteristics:")
    
    # Tempo
    if bands['Beta'].mean() > 0.3:
        print("  • TEMPO: Fast (110-140 BPM) - High beta activity")
    elif bands['Beta'].mean() > 0.2:
        print("  • TEMPO: Medium (90-110 BPM) - Moderate beta")
    else:
        print("  • TEMPO: Slow (70-90 BPM) - Low beta")
    
    # Rhythm
    if delta_theta_ratio > 0.8:
        print(f"  • RHYTHM: Steady, grounded (Delta/Theta = {delta_theta_ratio:.2f})")
    elif delta_theta_ratio > 0.5:
        print(f"  • RHYTHM: Balanced (Delta/Theta = {delta_theta_ratio:.2f})")
    else:
        print(f"  • RHYTHM: Flowing, syncopated (Delta/Theta = {delta_theta_ratio:.2f})")
    
    # Articulation
    if bands['Alpha'].mean() > 0.25:
        print(f"  • ARTICULATION: Legato, smooth (Alpha = {bands['Alpha'].mean():.3f})")
    elif bands['Alpha'].mean() > 0.15:
        print(f"  • ARTICULATION: Normal (Alpha = {bands['Alpha'].mean():.3f})")
    else:
        print(f"  • ARTICULATION: Staccato, sharp (Alpha = {bands['Alpha'].mean():.3f})")
    
    # Harmonic complexity
    if bands['Gamma'].mean() > 0.05:
        print(f"  • HARMONY: Complex, rich (Gamma = {bands['Gamma'].mean():.3f})")
    elif bands['Gamma'].mean() > 0.02:
        print(f"  • HARMONY: Moderate (Gamma = {bands['Gamma'].mean():.3f})")
    else:
        print(f"  • HARMONY: Simple, pure (Gamma = {bands['Gamma'].mean():.3f})")
    
    # Density
    if low_high_ratio > 1.5:
        print(f"  • DENSITY: Sparse, spacious (Low/High = {low_high_ratio:.2f})")
    elif low_high_ratio > 0.8:
        print(f"  • DENSITY: Balanced (Low/High = {low_high_ratio:.2f})")
    else:
        print(f"  • DENSITY: Dense, busy (Low/High = {low_high_ratio:.2f})")
    
    # Timbre
    if bands['Gamma'].mean() > 0.04:
        print("  • TIMBRE: Bright, sharp")
    elif bands['Delta'].mean() > 0.3:
        print("  • TIMBRE: Dark, warm")
    else:
        print("  • TIMBRE: Neutral, balanced")
    
    print("\n" + "=" * 80)
    print("🎨 SYNESTHETIC COLOR MAPPING")
    print("=" * 80)
    
    # Color based on dominant frequencies
    if dominant_band == 'Delta':
        print("  🟤 BROWN/DEEP RED - Deep, grounded, earthy")
    elif dominant_band == 'Theta':
        print("  🟣 PURPLE/INDIGO - Meditative, creative, flowing")
    elif dominant_band == 'Alpha':
        print("  🟢 GREEN/BLUE - Relaxed, calm, balanced")
    elif dominant_band == 'Beta':
        print("  🟡 YELLOW/ORANGE - Active, alert, focused")
    elif dominant_band == 'Gamma':
        print("  ⚪ WHITE/BRIGHT - Intense, sharp, high-energy")
    
    print("\n" + "=" * 80)
    
    return {
        'bands': band_means,
        'ratios': {k: v.mean() for k, v in ratios.items()},
        'dominant': dominant_band
    }

def compare_two_csvs(csv1, csv2, num_samples=100):
    """Compare two CSVs and show how music should differ"""
    
    print("\n" + "=" * 80)
    print("🎭 SYNESTHETIC COMPARISON")
    print("=" * 80)
    
    stats1 = analyze_eeg_bands(csv1, num_samples)
    print("\n\n")
    stats2 = analyze_eeg_bands(csv2, num_samples)
    
    print("\n" + "=" * 80)
    print("🎵 MUSICAL DIFFERENCES")
    print("=" * 80)
    
    print(f"\nCSV 1 Dominant: {stats1['dominant']}")
    print(f"CSV 2 Dominant: {stats2['dominant']}")
    
    if stats1['dominant'] != stats2['dominant']:
        print("✅ DIFFERENT DOMINANT BANDS - Music should sound VERY different")
    else:
        print("⚠️  SAME DOMINANT BAND - Check ratios for differences")
    
    print("\nKey Ratio Differences:")
    for ratio in ['Delta/Theta', 'Alpha/Beta', 'Beta/Gamma']:
        diff = abs(stats1['ratios'][ratio] - stats2['ratios'][ratio])
        pct = diff / max(stats1['ratios'][ratio], stats2['ratios'][ratio]) * 100
        print(f"  {ratio}: {stats1['ratios'][ratio]:.2f} vs {stats2['ratios'][ratio]:.2f} ({pct:.0f}% diff)")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_eeg_bands.py <csv1> [csv2] [num_samples]")
        sys.exit(1)
    
    csv1 = sys.argv[1]
    num_samples = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    
    if len(sys.argv) > 2:
        csv2 = sys.argv[2]
        compare_two_csvs(csv1, csv2, num_samples)
    else:
        analyze_eeg_bands(csv1, num_samples)
