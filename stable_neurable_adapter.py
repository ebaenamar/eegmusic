#!/usr/bin/env python3
"""
Stable Neurable EEG Adapter - Enhanced stability and musical coherence
Features:
- Larger smoothing window (configurable)
- Smooth transitions between states
- Tempo and scale stability
- Harmonic consistency
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from collections import deque

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StableNeurableAdapter:
    """
    Enhanced adapter with improved musical stability and coherence.
    """
    
    def __init__(self, 
                 smoothing_window: int = 15,
                 tempo_stability: float = 0.8,
                 scale_stability_samples: int = 8):
        """
        Args:
            smoothing_window: Number of samples for temporal smoothing (default: 15)
            tempo_stability: Weight for previous tempo (0-1, higher = more stable)
            scale_stability_samples: Minimum samples before scale change
        """
        self.smoothing_window = smoothing_window
        self.tempo_stability = tempo_stability
        self.scale_stability_samples = scale_stability_samples
        
        # History buffers for smoothing
        self.history = {
            'left_bands': deque(maxlen=smoothing_window),
            'right_bands': deque(maxlen=smoothing_window),
            'cognitive_ratios': deque(maxlen=smoothing_window),
            'tempo': deque(maxlen=smoothing_window),
            'arousal': deque(maxlen=smoothing_window),
            'valence': deque(maxlen=smoothing_window)
        }
        
        # State tracking
        self.current_scale = 'pentatonic'
        self.scale_counter = 0
        self.previous_tempo = 90
        self.previous_params = None
        
        # Signal quality threshold
        self.quality_threshold = 0.3
        
        logger.info(f"✨ Stable Adapter initialized:")
        logger.info(f"   Smoothing window: {smoothing_window} samples")
        logger.info(f"   Tempo stability: {tempo_stability}")
        logger.info(f"   Scale stability: {scale_stability_samples} samples")
    
    def read_neurable_csv(self, csv_path: str) -> pd.DataFrame:
        """Read Neurable CSV file"""
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"✅ Loaded {len(df)} samples from {csv_path}")
            return df
        except Exception as e:
            logger.error(f"❌ Error reading CSV: {e}")
            return None
    
    def extract_hemisphere_data(self, row: pd.Series, hemisphere: str) -> Dict[str, float]:
        """Extract band powers and metrics for one hemisphere"""
        prefix = f"{hemisphere}__"
        
        return {
            'delta': row.get(f'{prefix}delta', 0),
            'theta': row.get(f'{prefix}theta', 0),
            'alpha': row.get(f'{prefix}alpha', 0),
            'beta': row.get(f'{prefix}beta', 0),
            'gamma': row.get(f'{prefix}gamma', 0),
            'focus': row.get(f'{prefix}a_ta', 0),
            'alertness': row.get(f'{prefix}b_tb', 0),
            'cognitive_load': row.get(f'{prefix}b_ab', 0),
            'engagement': row.get(f'{prefix}mab_tmab', 0),
            'signal_quality': 1.0 - row.get(f'{prefix}p_bad', 0)
        }
    
    def smooth_values(self, history_key: str, new_value: Dict[str, float]) -> Dict[str, float]:
        """Apply temporal smoothing using exponential moving average"""
        self.history[history_key].append(new_value)
        
        if len(self.history[history_key]) < 2:
            return new_value
        
        # Exponential moving average
        smoothed = {}
        alpha = 2.0 / (len(self.history[history_key]) + 1)
        
        for key in new_value.keys():
            values = [h[key] for h in self.history[history_key]]
            # EMA: S_t = α * Y_t + (1-α) * S_{t-1}
            smoothed[key] = values[0]
            for val in values[1:]:
                smoothed[key] = alpha * val + (1 - alpha) * smoothed[key]
        
        return smoothed
    
    def calculate_arousal_valence(self, left_data: Dict, right_data: Dict) -> tuple:
        """
        Calculate arousal and valence with quality weighting.
        Returns: (arousal, valence, quality)
        """
        left_quality = left_data['signal_quality']
        right_quality = right_data['signal_quality']
        total_quality = left_quality + right_quality
        
        if total_quality > 0:
            left_weight = left_quality / total_quality
            right_weight = right_quality / total_quality
        else:
            left_weight = right_weight = 0.5
        
        # Arousal from alertness (beta/theta ratio)
        arousal = (left_data['alertness'] * left_weight + 
                  right_data['alertness'] * right_weight)
        
        # Valence from focus (alpha/theta ratio)
        valence = (left_data['focus'] * left_weight + 
                  right_data['focus'] * right_weight)
        
        # Normalize valence to 0-1
        valence = np.clip(valence, 0, 1)
        
        quality = (left_quality + right_quality) / 2
        
        return arousal, valence, quality
    
    def select_stable_scale(self, valence: float) -> str:
        """
        Select musical scale with stability (avoid frequent changes).
        """
        # Determine target scale from valence
        if valence > 0.55:
            target_scale = 'major'
        elif valence < 0.35:
            target_scale = 'minor'
        else:
            target_scale = 'pentatonic'
        
        # Only change if target differs and counter reached
        if target_scale != self.current_scale:
            self.scale_counter += 1
            if self.scale_counter >= self.scale_stability_samples:
                logger.info(f"🎼 Scale change: {self.current_scale} → {target_scale}")
                self.current_scale = target_scale
                self.scale_counter = 0
        else:
            self.scale_counter = 0
        
        return self.current_scale
    
    def calculate_stable_tempo(self, arousal: float, left_beta: float) -> float:
        """
        Calculate tempo with stability (smooth transitions).
        """
        # Base tempo from arousal
        base_tempo = 70 + arousal * 80  # 70-150 BPM range
        
        # Modulation from left hemisphere beta
        beta_modulation = 1.0 + (left_beta - 0.2) * 0.3  # ±30% max
        target_tempo = base_tempo * np.clip(beta_modulation, 0.8, 1.2)
        
        # Smooth transition from previous tempo
        stable_tempo = (self.tempo_stability * self.previous_tempo + 
                       (1 - self.tempo_stability) * target_tempo)
        
        # Clamp to reasonable range
        stable_tempo = np.clip(stable_tempo, 60, 140)
        
        self.previous_tempo = stable_tempo
        
        return stable_tempo
    
    def map_to_music_parameters(self, left_data: Dict, right_data: Dict) -> Dict[str, float]:
        """
        Map hemisphere data to stable musical parameters.
        """
        # Smooth hemisphere data
        left_smooth = self.smooth_values('left_bands', left_data)
        right_smooth = self.smooth_values('right_bands', right_data)
        
        # Calculate arousal and valence
        arousal, valence, quality = self.calculate_arousal_valence(left_smooth, right_smooth)
        
        # Smooth arousal and valence
        self.history['arousal'].append(arousal)
        self.history['valence'].append(valence)
        
        arousal_smooth = np.mean(list(self.history['arousal']))
        valence_smooth = np.mean(list(self.history['valence']))
        
        # Check signal quality
        if quality < self.quality_threshold:
            logger.warning(f"⚠️ Low signal quality: {quality:.2f}")
        
        # Select stable scale
        scale = self.select_stable_scale(valence_smooth)
        
        # Calculate stable tempo
        tempo = self.calculate_stable_tempo(arousal_smooth, left_smooth['beta'])
        
        # Combine band powers (weighted by quality)
        combined_bands = {}
        for band in ['delta', 'theta', 'alpha', 'beta', 'gamma']:
            left_val = left_smooth[band] * left_smooth['signal_quality']
            right_val = right_smooth[band] * right_smooth['signal_quality']
            combined_bands[band] = (left_val + right_val) / 2
        
        # Musical parameters
        params = {
            # Core dimensions
            'arousal': arousal_smooth,
            'valence': valence_smooth,
            'energy': (left_smooth['engagement'] + right_smooth['engagement']) / 2,
            'cognitive_load': (left_smooth['cognitive_load'] + right_smooth['cognitive_load']) / 2,
            
            # Tempo and rhythm
            'tempo': tempo,
            'rhythm_variation': left_smooth['theta'] * 0.5,  # Reduced variation
            
            # Melody and harmony (right hemisphere)
            'melody_complexity': right_smooth['alpha'] * 0.7,  # Reduced complexity
            'harmony': (right_smooth['alpha'] + right_smooth['gamma']) / 2,
            'brightness': right_smooth['gamma'],
            
            # Scale and structure
            'scale': scale,
            'complexity': np.clip(combined_bands['beta'] + combined_bands['gamma'], 0.3, 0.8),
            
            # Quality metrics
            'signal_quality': quality,
            'hemisphere_balance': abs(left_smooth['signal_quality'] - right_smooth['signal_quality']),
            
            # Band powers
            **combined_bands
        }
        
        # Interpolate with previous parameters for ultra-smooth transitions
        if self.previous_params is not None:
            interpolation_weight = 0.7  # 70% previous, 30% new
            for key in ['tempo', 'energy', 'complexity', 'melody_complexity', 'harmony']:
                if key in params and key in self.previous_params:
                    params[key] = (interpolation_weight * self.previous_params[key] + 
                                  (1 - interpolation_weight) * params[key])
        
        self.previous_params = params.copy()
        
        return params
    
    def process_neurable_row(self, row: pd.Series) -> Dict[str, float]:
        """Process a single row from Neurable CSV"""
        left_data = self.extract_hemisphere_data(row, 'Left')
        right_data = self.extract_hemisphere_data(row, 'Right')
        
        music_params = self.map_to_music_parameters(left_data, right_data)
        
        # Log state (less verbose)
        if len(self.history['arousal']) % 5 == 0:  # Log every 5 samples
            logger.info(
                f"🎵 Scale={music_params['scale']:>10} | "
                f"Tempo={music_params['tempo']:>5.0f} BPM | "
                f"Arousal={music_params['arousal']:.2f} | "
                f"Valence={music_params['valence']:.2f} | "
                f"Quality={music_params['signal_quality']:.2f}"
            )
        
        return music_params
    
    def stream_from_csv(self, csv_path: str, callback_fn, delay: float = 4.0):
        """Stream data from Neurable CSV file"""
        import time
        
        df = self.read_neurable_csv(csv_path)
        if df is None:
            return
        
        logger.info(f"🎵 Starting stable Neurable EEG music stream...")
        logger.info(f"📊 {len(df)} samples, {delay}s delay")
        
        for idx, row in df.iterrows():
            try:
                music_params = self.process_neurable_row(row)
                callback_fn(music_params)
                time.sleep(delay)
                
            except KeyboardInterrupt:
                logger.info("⏹️ Stream stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Error processing row {idx}: {e}")
                continue
        
        logger.info("✅ Stream complete")

def test_stable_adapter():
    """Test the stable adapter"""
    adapter = StableNeurableAdapter(
        smoothing_window=15,
        tempo_stability=0.8,
        scale_stability_samples=8
    )
    
    csv_path = "/Users/e.baena/Desktop/eeg_stream.csv"
    
    df = adapter.read_neurable_csv(csv_path)
    if df is not None and len(df) > 0:
        print("\n🧪 Testing first 10 rows:")
        print("=" * 80)
        
        for idx in range(min(10, len(df))):
            row = df.iloc[idx]
            params = adapter.process_neurable_row(row)
            
            if idx % 3 == 0:  # Print every 3rd
                print(f"\nSample {idx}:")
                print(f"  Scale: {params['scale']}, Tempo: {params['tempo']:.0f} BPM")
                print(f"  Arousal: {params['arousal']:.2f}, Valence: {params['valence']:.2f}")
                print(f"  Energy: {params['energy']:.2f}, Complexity: {params['complexity']:.2f}")

if __name__ == "__main__":
    test_stable_adapter()
