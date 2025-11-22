#!/usr/bin/env python3
"""
Neurable EEG Adapter - Neurologically-grounded mapping for 12-channel preprocessed data
Handles Left/Right hemisphere data with pre-calculated band powers
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
import logging
from neuro_music_mapper import NeuroMusicMapper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NeurableEEGAdapter:
    """
    Adapter for Neurable 12-channel EEG device with preprocessed data.
    
    Input format (per hemisphere):
    - total_power: Total signal power
    - delta, theta, alpha, beta, beta_low, beta_high, gamma: Band powers (normalized)
    - a_ta: Alpha/Theta+Alpha ratio
    - b_tb: Beta/Theta+Beta ratio
    - b_ab: Beta/Alpha+Beta ratio
    - mab_tmab: (Alpha+Beta)/(Theta+Alpha+Beta) ratio
    - p_bad: Signal quality (0-1, higher = worse)
    
    Neurological mapping:
    - Left hemisphere: Language, logic, analytical processing
    - Right hemisphere: Spatial, creative, holistic processing
    """
    
    def __init__(self, smoothing_window: int = 5):
        self.neuro_mapper = NeuroMusicMapper(smoothing_window=smoothing_window)
        
        # Hemisphere-specific weights for musical parameters
        self.hemisphere_weights = {
            'left': {
                'tempo': 0.6,        # Left = sequential processing → tempo
                'complexity': 0.7,   # Left = analytical → complexity
                'rhythm': 0.6,       # Left = timing → rhythm
                'melody': 0.4        # Right-dominant
            },
            'right': {
                'tempo': 0.4,
                'complexity': 0.3,
                'rhythm': 0.4,
                'melody': 0.6,       # Right = melody/pitch → melody
                'harmony': 0.7,      # Right = spatial → harmony
                'timbre': 0.7        # Right = tone quality
            }
        }
        
        # Signal quality thresholds
        self.quality_threshold = 0.5  # p_bad < 0.5 = good signal
        
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
        """
        Extract band powers and metrics for one hemisphere.
        
        Args:
            row: DataFrame row
            hemisphere: 'Left' or 'Right'
        
        Returns:
            Dictionary with band powers and metrics
        """
        prefix = f"{hemisphere}__"
        
        return {
            'total_power': row.get(f'{prefix}total_power', 0),
            'delta': row.get(f'{prefix}delta', 0),
            'theta': row.get(f'{prefix}theta', 0),
            'alpha': row.get(f'{prefix}alpha', 0),
            'beta': row.get(f'{prefix}beta', 0),
            'beta_low': row.get(f'{prefix}beta_low', 0),
            'beta_high': row.get(f'{prefix}beta_high', 0),
            'gamma': row.get(f'{prefix}gamma', 0),
            
            # Cognitive ratios
            'alpha_theta_ratio': row.get(f'{prefix}a_ta', 0),      # Focus/relaxation
            'beta_theta_ratio': row.get(f'{prefix}b_tb', 0),       # Alertness
            'beta_alpha_ratio': row.get(f'{prefix}b_ab', 0),       # Cognitive load
            'engagement': row.get(f'{prefix}mab_tmab', 0),         # Overall engagement
            
            # Signal quality
            'signal_quality': 1.0 - row.get(f'{prefix}p_bad', 0)   # Invert p_bad
        }
    
    def assess_cognitive_state_from_ratios(self, left_data: Dict, right_data: Dict) -> Dict[str, float]:
        """
        Assess cognitive state using pre-calculated ratios.
        
        Neurological basis:
        - Alpha/Theta ratio: Focus vs drowsiness
        - Beta/Theta ratio: Alertness vs relaxation
        - Beta/Alpha ratio: Cognitive load
        - Engagement: Overall mental engagement
        """
        # Average across hemispheres (weighted by signal quality)
        left_quality = left_data['signal_quality']
        right_quality = right_data['signal_quality']
        total_quality = left_quality + right_quality
        
        if total_quality > 0:
            left_weight = left_quality / total_quality
            right_weight = right_quality / total_quality
        else:
            left_weight = right_weight = 0.5
        
        # Weighted average of ratios
        alpha_theta = (left_data['alpha_theta_ratio'] * left_weight + 
                      right_data['alpha_theta_ratio'] * right_weight)
        
        beta_theta = (left_data['beta_theta_ratio'] * left_weight + 
                     right_data['beta_theta_ratio'] * right_weight)
        
        beta_alpha = (left_data['beta_alpha_ratio'] * left_weight + 
                     right_data['beta_alpha_ratio'] * right_weight)
        
        engagement = (left_data['engagement'] * left_weight + 
                     right_data['engagement'] * right_weight)
        
        return {
            'focus': alpha_theta,           # High = focused, low = drowsy
            'alertness': beta_theta,        # High = alert, low = relaxed
            'cognitive_load': beta_alpha,   # High = high load, low = low load
            'engagement': engagement,       # Overall engagement level
            'signal_quality': (left_quality + right_quality) / 2
        }
    
    def map_hemispheres_to_music(self, left_data: Dict, right_data: Dict) -> Dict[str, float]:
        """
        Map left and right hemisphere data to musical parameters.
        
        Neurologically-grounded approach:
        - Left hemisphere: Tempo, rhythm, sequential processing
        - Right hemisphere: Melody, harmony, spatial/tonal processing
        - Integration: Balanced musical output
        """
        # Get cognitive state from ratios
        cognitive_state = self.assess_cognitive_state_from_ratios(left_data, right_data)
        
        # Check signal quality
        if cognitive_state['signal_quality'] < self.quality_threshold:
            logger.warning(f"⚠️ Low signal quality: {cognitive_state['signal_quality']:.2f}")
        
        # Combine band powers (weighted by hemisphere specialization)
        combined_bands = {}
        
        for band in ['delta', 'theta', 'alpha', 'beta', 'gamma']:
            # Weight by signal quality
            left_val = left_data[band] * left_data['signal_quality']
            right_val = right_data[band] * right_data['signal_quality']
            
            # Average
            combined_bands[band] = (left_val + right_val) / 2
        
        # Use neuro mapper for base parameters
        base_params = self.neuro_mapper.get_musical_parameters(combined_bands)
        
        # Enhance with hemisphere-specific modulation
        enhanced_params = base_params.copy()
        
        # Left hemisphere → Tempo and Rhythm
        left_beta = left_data['beta']
        left_theta = left_data['theta']
        
        # Tempo: Left hemisphere beta activity
        tempo_modulation = 1.0 + (left_beta - 0.2) * 0.5  # ±50% modulation
        enhanced_params['tempo'] = base_params['tempo'] * np.clip(tempo_modulation, 0.7, 1.3)
        
        # Rhythm variation: Left hemisphere theta
        enhanced_params['rhythm_variation'] = left_theta
        
        # Right hemisphere → Melody and Harmony
        right_alpha = right_data['alpha']
        right_gamma = right_data['gamma']
        
        # Melody complexity: Right hemisphere alpha (relaxed creativity)
        enhanced_params['melody_complexity'] = right_alpha
        
        # Harmony richness: Right hemisphere alpha + gamma
        enhanced_params['harmony'] = (right_alpha + right_gamma) / 2
        
        # Brightness: Right hemisphere gamma (high-frequency perception)
        enhanced_params['brightness'] = right_gamma * 2
        
        # Cognitive load from ratios
        enhanced_params['cognitive_load'] = cognitive_state['cognitive_load']
        
        # Engagement → Energy
        enhanced_params['energy'] = cognitive_state['engagement']
        
        # Arousal from alertness
        enhanced_params['arousal'] = cognitive_state['alertness']
        
        # Valence from focus (high focus = positive)
        enhanced_params['valence'] = np.clip(cognitive_state['focus'] / 2, 0, 1)
        
        # Add hemisphere balance metric
        enhanced_params['hemisphere_balance'] = abs(
            left_data['signal_quality'] - right_data['signal_quality']
        )
        
        # Add cognitive state metrics
        enhanced_params.update(cognitive_state)
        
        return enhanced_params
    
    def process_neurable_row(self, row: pd.Series) -> Dict[str, float]:
        """
        Process a single row from Neurable CSV.
        
        Args:
            row: DataFrame row with Left__ and Right__ columns
        
        Returns:
            Musical parameters dictionary
        """
        # Extract hemisphere data
        left_data = self.extract_hemisphere_data(row, 'Left')
        right_data = self.extract_hemisphere_data(row, 'Right')
        
        # Map to music
        music_params = self.map_hemispheres_to_music(left_data, right_data)
        
        # Log state
        logger.info(
            f"🧠 L/R Balance: {music_params['hemisphere_balance']:.2f} | "
            f"Focus: {music_params['focus']:.2f} | "
            f"Engagement: {music_params['engagement']:.2f} | "
            f"Quality: {music_params['signal_quality']:.2f}"
        )
        
        return music_params
    
    def stream_from_csv(self, csv_path: str, callback_fn, delay: float = 1.0):
        """
        Stream data from Neurable CSV file.
        
        Args:
            csv_path: Path to CSV file
            callback_fn: Function to call with music parameters
            delay: Delay between samples (seconds)
        """
        import time
        
        df = self.read_neurable_csv(csv_path)
        if df is None:
            return
        
        logger.info(f"🎵 Starting Neurable EEG music stream...")
        logger.info(f"📊 {len(df)} samples, {delay}s delay")
        
        for idx, row in df.iterrows():
            try:
                # Process row
                music_params = self.process_neurable_row(row)
                
                # Call callback
                callback_fn(music_params)
                
                # Wait
                time.sleep(delay)
                
            except KeyboardInterrupt:
                logger.info("⏹️ Stream stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Error processing row {idx}: {e}")
                continue
        
        logger.info("✅ Stream complete")

def test_neurable_adapter():
    """Test the Neurable adapter"""
    adapter = NeurableEEGAdapter()
    
    # Test with sample data
    csv_path = "/Users/e.baena/CascadeProjects/mindfulmakers/neurable-eeg-stream/eeg_data_20251122_143416.csv"
    
    df = adapter.read_neurable_csv(csv_path)
    if df is not None and len(df) > 0:
        print("\n🧪 Testing first row:")
        print("=" * 60)
        
        row = df.iloc[0]
        
        # Extract hemisphere data
        left = adapter.extract_hemisphere_data(row, 'Left')
        right = adapter.extract_hemisphere_data(row, 'Right')
        
        print(f"\n📊 Left Hemisphere:")
        print(f"  Delta: {left['delta']:.3f}, Theta: {left['theta']:.3f}, Alpha: {left['alpha']:.3f}")
        print(f"  Beta: {left['beta']:.3f}, Gamma: {left['gamma']:.3f}")
        print(f"  Focus (α/θ+α): {left['alpha_theta_ratio']:.3f}")
        print(f"  Signal Quality: {left['signal_quality']:.3f}")
        
        print(f"\n📊 Right Hemisphere:")
        print(f"  Delta: {right['delta']:.3f}, Theta: {right['theta']:.3f}, Alpha: {right['alpha']:.3f}")
        print(f"  Beta: {right['beta']:.3f}, Gamma: {right['gamma']:.3f}")
        print(f"  Focus (α/θ+α): {right['alpha_theta_ratio']:.3f}")
        print(f"  Signal Quality: {right['signal_quality']:.3f}")
        
        # Process to music
        music_params = adapter.process_neurable_row(row)
        
        print(f"\n🎵 Musical Parameters:")
        print(f"  Arousal: {music_params['arousal']:.2f}")
        print(f"  Valence: {music_params['valence']:.2f}")
        print(f"  Tempo: {music_params['tempo']:.0f} BPM")
        print(f"  Energy: {music_params['energy']:.2f}")
        print(f"  Complexity: {music_params['complexity']:.2f}")
        print(f"  Hemisphere Balance: {music_params['hemisphere_balance']:.2f}")

if __name__ == "__main__":
    test_neurable_adapter()
