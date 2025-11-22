#!/usr/bin/env python3
"""
Debug script to verify music generation is actually changing
"""

import pandas as pd
import numpy as np
from stable_neurable_adapter import StableNeurableAdapter

def debug_music_generation(csv_path, num_samples=20):
    """Debug music generation to see if parameters actually change"""
    
    print("=" * 80)
    print("🔍 DEBUG: Music Generation Analysis")
    print("=" * 80)
    print(f"\n📂 CSV: {csv_path}")
    print(f"📊 Analyzing {num_samples} samples with DYNAMIC preset")
    print()
    
    # Read CSV
    df = pd.read_csv(csv_path)
    df = df.head(num_samples)
    
    # Initialize adapter with DYNAMIC settings
    adapter = StableNeurableAdapter(
        smoothing_window=5,  # DYNAMIC
        tempo_stability=0.5,  # DYNAMIC
        scale_stability_samples=8
    )
    
    print("Configuration:")
    print(f"  Smoothing Window: 5")
    print(f"  Tempo Stability: 0.5")
    print(f"  Scale Stability: 8 samples")
    print()
    
    # Track parameters
    tempos = []
    scales = []
    arousals = []
    valences = []
    complexities = []
    
    print("=" * 80)
    print("Sample-by-Sample Analysis:")
    print("=" * 80)
    
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
        complexities.append(music_params['complexity'])
        
        # Print every 5th sample
        if idx % 5 == 0:
            print(f"\nSample {idx}:")
            print(f"  Tempo: {music_params['tempo']:.1f} BPM")
            print(f"  Scale: {music_params['scale']}")
            print(f"  Arousal: {music_params['arousal']:.3f}")
            print(f"  Valence: {music_params['valence']:.3f}")
            print(f"  Complexity: {music_params['complexity']:.3f}")
            print(f"  Left Beta: {left_data['beta']:.3f}, Right Beta: {right_data['beta']:.3f}")
    
    print()
    print("=" * 80)
    print("📊 VARIATION ANALYSIS")
    print("=" * 80)
    
    # Analyze variation
    tempo_std = np.std(tempos)
    tempo_range = max(tempos) - min(tempos)
    arousal_std = np.std(arousals)
    valence_std = np.std(valences)
    
    print(f"\nTempo:")
    print(f"  Mean: {np.mean(tempos):.1f} BPM")
    print(f"  Std Dev: {tempo_std:.1f} BPM")
    print(f"  Range: {min(tempos):.1f} - {max(tempos):.1f} BPM ({tempo_range:.1f} BPM)")
    print(f"  Coefficient of Variation: {(tempo_std / np.mean(tempos) * 100):.1f}%")
    
    if tempo_std < 3:
        print(f"  ❌ VERY LOW variation - will sound monotonous")
    elif tempo_std < 8:
        print(f"  ⚠️  LOW variation - minimal tempo changes")
    elif tempo_std < 15:
        print(f"  ✅ MODERATE variation - noticeable changes")
    else:
        print(f"  ✅ HIGH variation - significant changes")
    
    print(f"\nScale Distribution:")
    for scale in set(scales):
        count = scales.count(scale)
        pct = count / len(scales) * 100
        print(f"  {scale}: {count}/{len(scales)} ({pct:.1f}%)")
    
    if len(set(scales)) == 1:
        print(f"  ❌ NO VARIATION - always {scales[0]}")
    elif len(set(scales)) == 2:
        print(f"  ⚠️  LIMITED variation - only 2 scales")
    else:
        print(f"  ✅ GOOD variation - {len(set(scales))} different scales")
    
    print(f"\nArousal:")
    print(f"  Mean: {np.mean(arousals):.3f}")
    print(f"  Std Dev: {arousal_std:.3f}")
    print(f"  Range: {min(arousals):.3f} - {max(arousals):.3f}")
    
    if arousal_std < 0.05:
        print(f"  ❌ VERY LOW variation")
    elif arousal_std < 0.1:
        print(f"  ⚠️  LOW variation")
    else:
        print(f"  ✅ GOOD variation")
    
    print(f"\nValence:")
    print(f"  Mean: {np.mean(valences):.3f}")
    print(f"  Std Dev: {valence_std:.3f}")
    print(f"  Range: {min(valences):.3f} - {max(valences):.3f}")
    
    if valence_std < 0.05:
        print(f"  ❌ VERY LOW variation")
    elif valence_std < 0.1:
        print(f"  ⚠️  LOW variation")
    else:
        print(f"  ✅ GOOD variation")
    
    print()
    print("=" * 80)
    print("🎯 DIAGNOSIS")
    print("=" * 80)
    
    issues = []
    
    if tempo_std < 8:
        issues.append("Tempo barely changes")
    if len(set(scales)) == 1:
        issues.append("Scale never changes")
    if arousal_std < 0.1:
        issues.append("Arousal/energy barely changes")
    if valence_std < 0.1:
        issues.append("Valence/mood barely changes")
    
    if issues:
        print("\n❌ PROBLEMS FOUND:")
        for issue in issues:
            print(f"  • {issue}")
        print("\nThis explains why music sounds the same!")
        print("\nPOSSIBLE CAUSES:")
        print("  1. Smoothing window too large (even 5 may be too much)")
        print("  2. Tempo stability too high")
        print("  3. CSV data has low variation")
        print("  4. Scale stability preventing changes")
    else:
        print("\n✅ Parameters ARE changing significantly")
        print("   If music still sounds the same, the problem is in:")
        print("   1. Music generator not using the parameters correctly")
        print("   2. Audio generation not reflecting parameter changes")
        print("   3. Scale/chord progressions too similar")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    import sys
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "/Users/e.baena/Desktop/eeg_stream.csv"
    num_samples = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    
    debug_music_generation(csv_path, num_samples)
