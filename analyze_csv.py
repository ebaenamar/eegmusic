#!/usr/bin/env python3
"""Analyze CSV for variability"""

import pandas as pd
import numpy as np

csv_path = "/Users/e.baena/Desktop/eeg_stream.csv"

# Read CSV
df = pd.read_csv(csv_path)

print("=" * 70)
print("📊 EEG CSV Analysis")
print("=" * 70)
print(f"\nTotal samples: {len(df)}")
print(f"Columns: {len(df.columns)}")

# Analyze key columns
key_cols = {
    'Left__alpha': 'Left Alpha',
    'Right__alpha': 'Right Alpha',
    'Left__beta': 'Left Beta',
    'Right__beta': 'Right Beta',
    'Left__a_ta': 'Left Focus',
    'Right__a_ta': 'Right Focus',
    'Left__b_tb': 'Left Alertness',
    'Right__b_tb': 'Right Alertness'
}

print("\n" + "=" * 70)
print("📈 Statistical Analysis")
print("=" * 70)

for col, name in key_cols.items():
    if col in df.columns:
        values = df[col]
        print(f"\n{name}:")
        print(f"  Mean: {values.mean():.4f}")
        print(f"  Std:  {values.std():.4f}")
        print(f"  Min:  {values.min():.4f}")
        print(f"  Max:  {values.max():.4f}")
        print(f"  Range: {values.max() - values.min():.4f}")
        print(f"  CV (Coefficient of Variation): {(values.std() / values.mean() * 100):.2f}%")

# Calculate variability score
print("\n" + "=" * 70)
print("🎯 Variability Score")
print("=" * 70)

variability_scores = []
for col in key_cols.keys():
    if col in df.columns:
        cv = df[col].std() / df[col].mean() * 100
        variability_scores.append(cv)

avg_variability = np.mean(variability_scores)
print(f"\nAverage Variability: {avg_variability:.2f}%")

if avg_variability < 10:
    print("❌ VERY LOW variability - Music will be very repetitive")
elif avg_variability < 20:
    print("⚠️  LOW variability - Music will be somewhat repetitive")
elif avg_variability < 40:
    print("✅ MODERATE variability - Music will have some variation")
else:
    print("✅ HIGH variability - Music will be very varied")

# Analyze consecutive differences
print("\n" + "=" * 70)
print("📉 Consecutive Sample Changes")
print("=" * 70)

for col, name in list(key_cols.items())[:4]:  # Just first 4
    if col in df.columns:
        diffs = df[col].diff().abs()
        print(f"\n{name}:")
        print(f"  Avg change: {diffs.mean():.4f}")
        print(f"  Max change: {diffs.max():.4f}")

# Recommendations
print("\n" + "=" * 70)
print("💡 Recommendations")
print("=" * 70)

if avg_variability < 20:
    print("""
This CSV has LOW variability. To make music less repetitive:

1. REDUCE smoothing window:
   - Current: 15 samples
   - Try: 5-8 samples
   - This will make it more responsive to small changes

2. REDUCE tempo stability:
   - Current: 0.85
   - Try: 0.5-0.6
   - This will allow faster tempo changes

3. REDUCE duration:
   - Current: 6 seconds
   - Try: 3-4 seconds
   - Shorter phrases = more variety

4. USE different CSV:
   - This CSV appears to be from a stable mental state
   - Try recording during different activities
   - More mental state changes = more musical variety

5. FORCE scale changes:
   - Use manual scale selection
   - Switch between Major/Minor/Pentatonic manually
""")
else:
    print("""
This CSV has good variability. Music should be varied.
If it still sounds repetitive, try:

1. Reduce smoothing window (5-10)
2. Reduce tempo stability (0.5-0.7)
3. Shorter phrase duration (3-4s)
""")

print("\n" + "=" * 70)
