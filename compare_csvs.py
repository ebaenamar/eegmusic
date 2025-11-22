#!/usr/bin/env python3
"""
Compare two CSV files and predict musical differences
"""

import pandas as pd
import numpy as np
import sys
from stable_neurable_adapter import StableNeurableAdapter

def analyze_csv_musical_characteristics(csv_path, num_samples=50):
    """Analyze a CSV and extract musical characteristics"""
    
    # Read CSV
    df = pd.read_csv(csv_path)
    df = df.head(num_samples)  # First N samples
    
    # Initialize adapter
    adapter = StableNeurableAdapter(smoothing_window=5, tempo_stability=0.5)
    
    # Process samples
    tempos = []
    scales = []
    arousals = []
    valences = []
    energies = []
    complexities = []
    
    for idx, row in df.iterrows():
        # Extract hemisphere data
        left_data = {
            'delta': row.get('Left__delta', 0),
            'theta': row.get('Left__theta', 0),
            'alpha': row.get('Left__alpha', 0),
            'beta': row.get('Left__beta', 0),
            'gamma': row.get('Left__gamma', 0),
            'focus': row.get('Left__a_ta', 0),
            'alertness': row.get('Left__b_tb', 0),
            'cognitive_load': row.get('Left__b_ab', 0),
            'engagement': row.get('Left__mab_tmab', 0),
            'signal_quality': 1.0 - row.get('Left__p_bad', 0)
        }
        
        right_data = {
            'delta': row.get('Right__delta', 0),
            'theta': row.get('Right__theta', 0),
            'alpha': row.get('Right__alpha', 0),
            'beta': row.get('Right__beta', 0),
            'gamma': row.get('Right__gamma', 0),
            'focus': row.get('Right__a_ta', 0),
            'alertness': row.get('Right__b_tb', 0),
            'cognitive_load': row.get('Right__b_ab', 0),
            'engagement': row.get('Right__mab_tmab', 0),
            'signal_quality': 1.0 - row.get('Right__p_bad', 0)
        }
        
        # Get music parameters
        music_params = adapter.map_to_music_parameters(left_data, right_data)
        
        tempos.append(music_params['tempo'])
        scales.append(music_params['scale'])
        arousals.append(music_params['arousal'])
        valences.append(music_params['valence'])
        energies.append(music_params['energy'])
        complexities.append(music_params['complexity'])
    
    # Calculate statistics
    return {
        'tempo': {
            'mean': np.mean(tempos),
            'std': np.std(tempos),
            'min': np.min(tempos),
            'max': np.max(tempos),
            'range': np.max(tempos) - np.min(tempos)
        },
        'scale_distribution': {
            scale: scales.count(scale) / len(scales) * 100 
            for scale in set(scales)
        },
        'arousal': {
            'mean': np.mean(arousals),
            'std': np.std(arousals)
        },
        'valence': {
            'mean': np.mean(valences),
            'std': np.std(valences)
        },
        'energy': {
            'mean': np.mean(energies),
            'std': np.std(energies)
        },
        'complexity': {
            'mean': np.mean(complexities),
            'std': np.std(complexities)
        },
        'raw_data': {
            'tempos': tempos,
            'scales': scales,
            'arousals': arousals,
            'valences': valences
        }
    }

def compare_csvs(csv1_path, csv2_path, num_samples=50):
    """Compare two CSVs and show musical differences"""
    
    print("=" * 80)
    print("🎵 CSV MUSICAL COMPARISON")
    print("=" * 80)
    print()
    
    print(f"📂 CSV 1: {csv1_path}")
    print(f"📂 CSV 2: {csv2_path}")
    print(f"📊 Analyzing first {num_samples} samples...")
    print()
    
    # Analyze both CSVs
    stats1 = analyze_csv_musical_characteristics(csv1_path, num_samples)
    stats2 = analyze_csv_musical_characteristics(csv2_path, num_samples)
    
    # Compare Tempo
    print("=" * 80)
    print("🥁 TEMPO COMPARISON")
    print("=" * 80)
    print(f"CSV 1: {stats1['tempo']['mean']:.1f} BPM (±{stats1['tempo']['std']:.1f})")
    print(f"       Range: {stats1['tempo']['min']:.1f} - {stats1['tempo']['max']:.1f} BPM")
    print(f"       Variation: {stats1['tempo']['range']:.1f} BPM")
    print()
    print(f"CSV 2: {stats2['tempo']['mean']:.1f} BPM (±{stats2['tempo']['std']:.1f})")
    print(f"       Range: {stats2['tempo']['min']:.1f} - {stats2['tempo']['max']:.1f} BPM")
    print(f"       Variation: {stats2['tempo']['range']:.1f} BPM")
    print()
    
    tempo_diff = abs(stats1['tempo']['mean'] - stats2['tempo']['mean'])
    if tempo_diff > 10:
        print(f"✅ SIGNIFICANT DIFFERENCE: {tempo_diff:.1f} BPM")
    elif tempo_diff > 5:
        print(f"⚠️  MODERATE DIFFERENCE: {tempo_diff:.1f} BPM")
    else:
        print(f"❌ MINIMAL DIFFERENCE: {tempo_diff:.1f} BPM")
    print()
    
    # Compare Scales
    print("=" * 80)
    print("🎼 SCALE DISTRIBUTION")
    print("=" * 80)
    print("CSV 1:")
    for scale, pct in stats1['scale_distribution'].items():
        print(f"  {scale:>12}: {pct:>5.1f}%")
    print()
    print("CSV 2:")
    for scale, pct in stats2['scale_distribution'].items():
        print(f"  {scale:>12}: {pct:>5.1f}%")
    print()
    
    # Compare dominant scales
    dominant1 = max(stats1['scale_distribution'].items(), key=lambda x: x[1])
    dominant2 = max(stats2['scale_distribution'].items(), key=lambda x: x[1])
    
    if dominant1[0] != dominant2[0]:
        print(f"✅ DIFFERENT DOMINANT SCALES: {dominant1[0]} vs {dominant2[0]}")
    else:
        print(f"⚠️  SAME DOMINANT SCALE: {dominant1[0]}")
    print()
    
    # Compare Arousal
    print("=" * 80)
    print("⚡ AROUSAL (Energy Level)")
    print("=" * 80)
    print(f"CSV 1: {stats1['arousal']['mean']:.3f} (±{stats1['arousal']['std']:.3f})")
    print(f"CSV 2: {stats2['arousal']['mean']:.3f} (±{stats2['arousal']['std']:.3f})")
    arousal_diff = abs(stats1['arousal']['mean'] - stats2['arousal']['mean'])
    print(f"Difference: {arousal_diff:.3f}")
    if arousal_diff > 0.1:
        print("✅ SIGNIFICANT DIFFERENCE")
    else:
        print("❌ MINIMAL DIFFERENCE")
    print()
    
    # Compare Valence
    print("=" * 80)
    print("😊 VALENCE (Emotional Tone)")
    print("=" * 80)
    print(f"CSV 1: {stats1['valence']['mean']:.3f} (±{stats1['valence']['std']:.3f})")
    print(f"CSV 2: {stats2['valence']['mean']:.3f} (±{stats2['valence']['std']:.3f})")
    valence_diff = abs(stats1['valence']['mean'] - stats2['valence']['mean'])
    print(f"Difference: {valence_diff:.3f}")
    if valence_diff > 0.1:
        print("✅ SIGNIFICANT DIFFERENCE")
    else:
        print("❌ MINIMAL DIFFERENCE")
    print()
    
    # Compare Energy
    print("=" * 80)
    print("🔋 ENERGY (Volume/Intensity)")
    print("=" * 80)
    print(f"CSV 1: {stats1['energy']['mean']:.3f} (±{stats1['energy']['std']:.3f})")
    print(f"CSV 2: {stats2['energy']['mean']:.3f} (±{stats2['energy']['std']:.3f})")
    energy_diff = abs(stats1['energy']['mean'] - stats2['energy']['mean'])
    print(f"Difference: {energy_diff:.3f}")
    if energy_diff > 0.1:
        print("✅ SIGNIFICANT DIFFERENCE")
    else:
        print("❌ MINIMAL DIFFERENCE")
    print()
    
    # Compare Complexity
    print("=" * 80)
    print("🎹 COMPLEXITY (Musical Richness)")
    print("=" * 80)
    print(f"CSV 1: {stats1['complexity']['mean']:.3f} (±{stats1['complexity']['std']:.3f})")
    print(f"CSV 2: {stats2['complexity']['mean']:.3f} (±{stats2['complexity']['std']:.3f})")
    complexity_diff = abs(stats1['complexity']['mean'] - stats2['complexity']['mean'])
    print(f"Difference: {complexity_diff:.3f}")
    if complexity_diff > 0.1:
        print("✅ SIGNIFICANT DIFFERENCE")
    else:
        print("❌ MINIMAL DIFFERENCE")
    print()
    
    # Overall Assessment
    print("=" * 80)
    print("📊 OVERALL ASSESSMENT")
    print("=" * 80)
    
    significant_diffs = 0
    if tempo_diff > 10: significant_diffs += 1
    if arousal_diff > 0.1: significant_diffs += 1
    if valence_diff > 0.1: significant_diffs += 1
    if energy_diff > 0.1: significant_diffs += 1
    if complexity_diff > 0.1: significant_diffs += 1
    if dominant1[0] != dominant2[0]: significant_diffs += 1
    
    print(f"Significant differences found: {significant_diffs}/6")
    print()
    
    if significant_diffs >= 4:
        print("✅ CSVS PRODUCE VERY DIFFERENT MUSIC")
        print("   The two CSVs should sound distinctly different.")
    elif significant_diffs >= 2:
        print("⚠️  CSVS PRODUCE MODERATELY DIFFERENT MUSIC")
        print("   Some differences should be audible.")
    else:
        print("❌ CSVS PRODUCE SIMILAR MUSIC")
        print("   The two CSVs will sound very similar.")
        print("   Consider using DYNAMIC preset for more variation.")
    print()
    
    # Recommendations
    print("=" * 80)
    print("💡 RECOMMENDATIONS")
    print("=" * 80)
    
    if significant_diffs < 3:
        print("To increase musical variation:")
        print("1. Use DYNAMIC preset (smoothing=5, tempo_stability=0.5)")
        print("2. Reduce phrase duration to 3-4 seconds")
        print("3. Force different base scales manually")
        print("4. Record CSVs during different mental activities")
    else:
        print("Good variation detected! To enhance further:")
        print("1. Use RESPONSIVE or DYNAMIC preset")
        print("2. Let base scale be AUTO for natural changes")
    
    print()
    print("=" * 80)

def main():
    if len(sys.argv) < 3:
        print("Usage: python compare_csvs.py <csv1> <csv2> [num_samples]")
        print("\nExample:")
        print("  python compare_csvs.py person1.csv person2.csv 50")
        sys.exit(1)
    
    csv1 = sys.argv[1]
    csv2 = sys.argv[2]
    num_samples = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    
    compare_csvs(csv1, csv2, num_samples)

if __name__ == "__main__":
    main()
