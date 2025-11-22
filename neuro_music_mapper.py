#!/usr/bin/env python3
"""
Neurologically-grounded EEG to Music Mapping
Maps brainwave patterns to musical parameters with scientific basis
"""

import numpy as np
from typing import Dict, List, Tuple
from collections import deque
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NeuroMusicMapper:
    """
    Maps EEG brainwave patterns to music with neurological consistency.
    
    Based on established neuroscience research:
    - Delta (0.5-4 Hz): Deep sleep, unconscious processes → Bass, foundation
    - Theta (4-8 Hz): Meditation, creativity, flow → Rhythm, tempo modulation
    - Alpha (8-13 Hz): Relaxed awareness, calm focus → Harmony, melody smoothness
    - Beta (13-30 Hz): Active thinking, concentration → Complexity, note density
    - Gamma (30-50 Hz): Peak cognitive performance → Brightness, high frequencies
    """
    
    def __init__(self, smoothing_window: int = 5):
        self.smoothing_window = smoothing_window
        
        # Buffers for temporal smoothing (prevent sudden jumps)
        self.band_history = {
            'delta': deque(maxlen=smoothing_window),
            'theta': deque(maxlen=smoothing_window),
            'alpha': deque(maxlen=smoothing_window),
            'beta': deque(maxlen=smoothing_window),
            'gamma': deque(maxlen=smoothing_window)
        }
        
        self.music_param_history = {
            'arousal': deque(maxlen=smoothing_window),
            'valence': deque(maxlen=smoothing_window),
            'cognitive_load': deque(maxlen=smoothing_window)
        }
        
        # Neurological state thresholds (based on research)
        self.state_thresholds = {
            'deep_rest': {'alpha': 0.4, 'theta': 0.3},
            'meditation': {'theta': 0.35, 'alpha': 0.35},
            'relaxed_focus': {'alpha': 0.45, 'beta': 0.25},
            'active_focus': {'beta': 0.4, 'gamma': 0.2},
            'high_performance': {'beta': 0.35, 'gamma': 0.3}
        }
    
    def smooth_values(self, current: Dict[str, float], history: Dict[str, deque]) -> Dict[str, float]:
        """Apply temporal smoothing to prevent abrupt changes"""
        smoothed = {}
        
        for key, value in current.items():
            if key in history:
                history[key].append(value)
                smoothed[key] = np.mean(list(history[key]))
            else:
                smoothed[key] = value
        
        return smoothed
    
    def normalize_band_powers(self, raw_powers: Dict[str, float]) -> Dict[str, float]:
        """
        Normalize band powers to sum to 1.0
        Ensures consistency across different EEG amplitudes
        """
        total = sum(raw_powers.values())
        if total > 0:
            return {k: v/total for k, v in raw_powers.items()}
        return raw_powers
    
    def calculate_arousal_valence(self, band_powers: Dict[str, float]) -> Tuple[float, float]:
        """
        Calculate arousal and valence from EEG bands.
        
        Arousal (activation level):
        - High: Beta + Gamma dominant (active, alert)
        - Low: Delta + Theta dominant (calm, drowsy)
        
        Valence (emotional tone):
        - Positive: Alpha dominant, low theta (relaxed, positive)
        - Negative: High theta/alpha ratio, high beta (stress, anxiety)
        
        Returns: (arousal, valence) both in [0, 1]
        """
        # Arousal: weighted sum of high-frequency bands
        arousal = (
            0.1 * band_powers.get('delta', 0) +
            0.2 * band_powers.get('theta', 0) +
            0.3 * band_powers.get('alpha', 0) +
            0.5 * band_powers.get('beta', 0) +
            0.7 * band_powers.get('gamma', 0)
        )
        
        # Valence: alpha promotes positive, theta/beta imbalance indicates negative
        alpha = band_powers.get('alpha', 0)
        theta = band_powers.get('theta', 0)
        beta = band_powers.get('beta', 0)
        
        # High alpha = positive, high theta or beta/theta imbalance = negative
        valence = alpha - 0.3 * theta - 0.2 * abs(beta - theta)
        valence = (valence + 0.5) / 1.0  # Normalize to [0, 1]
        
        return np.clip(arousal, 0, 1), np.clip(valence, 0, 1)
    
    def calculate_cognitive_load(self, band_powers: Dict[str, float]) -> float:
        """
        Estimate cognitive load (mental effort).
        
        High cognitive load: High beta, moderate gamma, low alpha
        Low cognitive load: High alpha, low beta
        
        Returns: cognitive_load in [0, 1]
        """
        beta = band_powers.get('beta', 0)
        gamma = band_powers.get('gamma', 0)
        alpha = band_powers.get('alpha', 0)
        
        # Cognitive load increases with beta, decreases with alpha
        load = (beta + 0.5 * gamma) / (alpha + 0.1)
        
        return np.clip(load, 0, 1)
    
    def detect_cognitive_state(self, band_powers: Dict[str, float]) -> str:
        """
        Detect current cognitive state based on band power patterns.
        
        States:
        - deep_rest: High delta, low beta/gamma
        - meditation: High theta, moderate alpha
        - relaxed_focus: High alpha, moderate beta
        - active_focus: High beta, moderate gamma
        - high_performance: High beta and gamma
        """
        # Score each state
        scores = {}
        
        for state, thresholds in self.state_thresholds.items():
            score = sum(
                band_powers.get(band, 0) 
                for band, threshold in thresholds.items()
                if band_powers.get(band, 0) >= threshold
            )
            scores[state] = score
        
        # Return state with highest score
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        return 'neutral'
    
    def map_to_music_description(self, band_powers: Dict[str, float]) -> str:
        """
        Map EEG state to musical description for MusicGen.
        Ensures neurologically consistent and musically coherent output.
        """
        # Normalize and smooth
        normalized = self.normalize_band_powers(band_powers)
        smoothed = self.smooth_values(normalized, self.band_history)
        
        # Calculate psychological dimensions
        arousal, valence = self.calculate_arousal_valence(smoothed)
        cognitive_load = self.calculate_cognitive_load(smoothed)
        state = self.detect_cognitive_state(smoothed)
        
        # Smooth psychological dimensions
        psych_dims = {
            'arousal': arousal,
            'valence': valence,
            'cognitive_load': cognitive_load
        }
        smoothed_psych = self.smooth_values(psych_dims, self.music_param_history)
        
        # Map to musical parameters
        music_desc = self._build_music_description(
            smoothed_psych['arousal'],
            smoothed_psych['valence'],
            smoothed_psych['cognitive_load'],
            state,
            smoothed
        )
        
        logger.info(f"🧠 State: {state} | Arousal: {arousal:.2f} | Valence: {valence:.2f} | Load: {cognitive_load:.2f}")
        
        return music_desc
    
    def _build_music_description(self, arousal: float, valence: float, 
                                 cognitive_load: float, state: str,
                                 band_powers: Dict[str, float]) -> str:
        """
        Build coherent music description based on neurological state.
        """
        # Tempo (based on arousal and theta)
        if arousal > 0.7:
            tempo = "fast"
        elif arousal > 0.4:
            tempo = "moderate"
        else:
            tempo = "slow"
        
        # Energy/Intensity (based on arousal)
        if arousal > 0.6:
            intensity = "energetic"
        elif arousal > 0.3:
            intensity = "balanced"
        else:
            intensity = "calm"
        
        # Mood (based on valence)
        if valence > 0.6:
            mood = "uplifting"
        elif valence > 0.4:
            mood = "peaceful"
        else:
            mood = "contemplative"
        
        # Musical style (based on cognitive state)
        style_map = {
            'deep_rest': "ambient drone",
            'meditation': "meditative ambient",
            'relaxed_focus': "lo-fi chill",
            'active_focus': "minimal techno",
            'high_performance': "progressive electronic"
        }
        style = style_map.get(state, "ambient")
        
        # Complexity (based on cognitive load and beta)
        beta = band_powers.get('beta', 0)
        if cognitive_load > 0.6 or beta > 0.4:
            complexity = "complex layered"
        elif cognitive_load > 0.3:
            complexity = "melodic"
        else:
            complexity = "simple"
        
        # Texture (based on gamma for brightness)
        gamma = band_powers.get('gamma', 0)
        if gamma > 0.3:
            texture = "bright"
        elif gamma > 0.15:
            texture = "warm"
        else:
            texture = "soft"
        
        # Build coherent description
        description = f"{tempo} {intensity} {mood} {style}, {complexity} {texture} tones"
        
        return description
    
    def get_musical_parameters(self, band_powers: Dict[str, float]) -> Dict[str, float]:
        """
        Get detailed musical parameters for custom synthesis.
        Returns consistent, smoothed parameters.
        """
        normalized = self.normalize_band_powers(band_powers)
        smoothed = self.smooth_values(normalized, self.band_history)
        
        arousal, valence = self.calculate_arousal_valence(smoothed)
        cognitive_load = self.calculate_cognitive_load(smoothed)
        
        # Smooth psychological dimensions
        psych_dims = {
            'arousal': arousal,
            'valence': valence,
            'cognitive_load': cognitive_load
        }
        smoothed_psych = self.smooth_values(psych_dims, self.music_param_history)
        
        return {
            # Core dimensions
            'arousal': smoothed_psych['arousal'],
            'valence': smoothed_psych['valence'],
            'cognitive_load': smoothed_psych['cognitive_load'],
            
            # Musical parameters
            'tempo': 60 + smoothed_psych['arousal'] * 120,  # 60-180 BPM
            'energy': smoothed_psych['arousal'],
            'brightness': smoothed['gamma'] * 2,  # Gamma → high frequencies
            'complexity': cognitive_load,
            'harmony': smoothed['alpha'],  # Alpha → harmonic content
            'rhythm_variation': smoothed['theta'],  # Theta → rhythm changes
            'bass_presence': smoothed['delta'],  # Delta → bass
            
            # Band powers (smoothed)
            'delta': smoothed['delta'],
            'theta': smoothed['theta'],
            'alpha': smoothed['alpha'],
            'beta': smoothed['beta'],
            'gamma': smoothed['gamma']
        }

def test_mapper():
    """Test the neurological mapper"""
    mapper = NeuroMusicMapper()
    
    # Test different brain states
    test_states = {
        'Deep Rest': {
            'delta': 0.5, 'theta': 0.2, 'alpha': 0.15, 'beta': 0.1, 'gamma': 0.05
        },
        'Meditation': {
            'delta': 0.15, 'theta': 0.4, 'alpha': 0.3, 'beta': 0.1, 'gamma': 0.05
        },
        'Relaxed Focus': {
            'delta': 0.1, 'theta': 0.15, 'alpha': 0.5, 'beta': 0.2, 'gamma': 0.05
        },
        'Active Focus': {
            'delta': 0.05, 'theta': 0.1, 'alpha': 0.2, 'beta': 0.5, 'gamma': 0.15
        },
        'High Performance': {
            'delta': 0.05, 'theta': 0.1, 'alpha': 0.15, 'beta': 0.4, 'gamma': 0.3
        }
    }
    
    print("🧠 Neurological Music Mapper Test")
    print("=" * 60)
    
    for state_name, bands in test_states.items():
        print(f"\n{state_name}:")
        print(f"  Bands: {bands}")
        
        description = mapper.map_to_music_description(bands)
        print(f"  🎵 Music: {description}")
        
        params = mapper.get_musical_parameters(bands)
        print(f"  📊 Arousal: {params['arousal']:.2f} | Valence: {params['valence']:.2f}")
        print(f"  🎼 Tempo: {params['tempo']:.0f} BPM | Energy: {params['energy']:.2f}")

if __name__ == "__main__":
    test_mapper()
