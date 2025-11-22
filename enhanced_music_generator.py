#!/usr/bin/env python3
"""
Enhanced Music Generator with Individual EEG Fingerprinting
Uses unique EEG characteristics to create distinct musical patterns
"""

import numpy as np
from typing import Dict, List
from advanced_music_generator import AdvancedMusicGenerator

class EnhancedMusicGenerator(AdvancedMusicGenerator):
    """
    Enhanced generator that creates unique musical patterns based on
    individual EEG characteristics (EEG fingerprinting)
    """
    
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.eeg_fingerprint = None
        
    def calculate_eeg_fingerprint(self, music_params: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate unique EEG fingerprint from band power ratios
        This creates a unique musical "signature" for each individual
        """
        # Band power ratios (unique to each person)
        delta = music_params.get('delta', 0.1)
        theta = music_params.get('theta', 0.3)
        alpha = music_params.get('alpha', 0.2)
        beta = music_params.get('beta', 0.3)
        gamma = music_params.get('gamma', 0.1)
        
        total = delta + theta + alpha + beta + gamma
        if total > 0:
            delta /= total
            theta /= total
            alpha /= total
            beta /= total
            gamma /= total
        
        # Create fingerprint
        fingerprint = {
            # Rhythmic signature (from delta/theta)
            'rhythm_density': delta + theta,  # 0-1, lower freq = denser rhythm
            'rhythm_complexity': theta / (delta + 0.01),  # Theta/Delta ratio
            
            # Melodic signature (from alpha/beta)
            'melodic_range': alpha + beta,  # Higher = wider range
            'melodic_direction': beta / (alpha + 0.01),  # Up vs down tendency
            
            # Harmonic signature (from beta/gamma)
            'harmonic_richness': beta + gamma,  # More harmonics
            'harmonic_tension': gamma / (beta + 0.01),  # Dissonance level
            
            # Temporal signature
            'note_duration_bias': alpha,  # Higher alpha = longer notes
            'syncopation': theta * beta,  # Off-beat tendency
            
            # Timbral signature
            'brightness': gamma,  # High freq content
            'warmth': delta + theta,  # Low freq content
        }
        
        return fingerprint
    
    def generate_drums_with_fingerprint(self, tempo: float, duration: float,
                                       arousal: float, fingerprint: Dict) -> np.ndarray:
        """Generate drums using EEG fingerprint for unique patterns"""
        num_samples = int(duration * self.sample_rate)
        drums = np.zeros(num_samples)
        
        if arousal < 0.3:
            return drums
        
        # Beat parameters from fingerprint
        beat_duration = 60.0 / tempo
        samples_per_beat = int(beat_duration * self.sample_rate)
        
        # Rhythm density from fingerprint (more delta/theta = more hits)
        rhythm_density = fingerprint['rhythm_density']
        hit_probability = 0.3 + rhythm_density * 0.5  # 0.3-0.8
        
        # Syncopation from fingerprint
        syncopation = fingerprint['syncopation']
        
        # Generate kick and snare
        kick = self.generate_tone(60, 0.1, waveform='sine')
        snare = np.random.randn(int(0.1 * self.sample_rate)) * 0.5
        
        num_beats = int(duration / beat_duration)
        
        for beat in range(num_beats):
            beat_sample = beat * samples_per_beat
            
            # Kick pattern (influenced by rhythm complexity)
            if beat % 4 == 0:  # Downbeat
                end_idx = min(beat_sample + len(kick), len(drums))
                drums[beat_sample:end_idx] += kick[:end_idx - beat_sample] * 0.6
            elif np.random.random() < rhythm_density * 0.5:  # Extra kicks
                end_idx = min(beat_sample + len(kick), len(drums))
                drums[beat_sample:end_idx] += kick[:end_idx - beat_sample] * 0.4
            
            # Snare pattern (influenced by syncopation)
            if beat % 4 == 2:  # Backbeat
                end_idx = min(beat_sample + len(snare), len(drums))
                drums[beat_sample:end_idx] += snare[:end_idx - beat_sample] * 0.5
            elif np.random.random() < syncopation:  # Syncopated hits
                offset = int(samples_per_beat * 0.5)  # Off-beat
                synco_sample = beat_sample + offset
                end_idx = min(synco_sample + len(snare), len(drums))
                drums[synco_sample:end_idx] += snare[:end_idx - synco_sample] * 0.3
        
        return drums
    
    def generate_melody_with_fingerprint(self, root_freq: float, scale: List[int],
                                        duration: float, complexity: float,
                                        valence: float, fingerprint: Dict) -> np.ndarray:
        """Generate melody using EEG fingerprint for unique patterns"""
        num_samples = int(duration * self.sample_rate)
        melody = np.zeros(num_samples)
        
        # Number of notes influenced by complexity and melodic range
        melodic_range = fingerprint['melodic_range']
        num_notes = int(2 + complexity * 4 + melodic_range * 4)  # 2-10 notes
        num_notes = min(num_notes, 12)  # Cap at 12
        
        note_duration = duration / num_notes
        
        # Melodic direction bias from fingerprint
        melodic_direction = fingerprint['melodic_direction']
        up_bias = melodic_direction  # Higher = more upward movement
        
        # Note duration bias from fingerprint
        duration_bias = fingerprint['note_duration_bias']
        
        current_degree = len(scale) // 2
        
        for i in range(num_notes):
            if i > 0:
                # Movement influenced by melodic direction fingerprint
                if np.random.random() < up_bias:
                    movement = np.random.choice([0, 1, 2], p=[0.2, 0.5, 0.3])
                else:
                    movement = np.random.choice([-2, -1, 0], p=[0.3, 0.5, 0.2])
                
                current_degree = (current_degree + movement) % len(scale)
            
            # Octave selection influenced by melodic range
            if melodic_range > 0.6:
                octave = np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2])
            else:
                octave = np.random.choice([1, 2], p=[0.6, 0.4])
            
            semitones = scale[current_degree] + (octave * 12)
            frequency = root_freq * (2 ** (semitones / 12))
            
            # Note duration influenced by duration bias
            actual_duration = note_duration * (0.7 + duration_bias * 0.6)
            note_samples = int(actual_duration * self.sample_rate)
            
            # Harmonics influenced by harmonic richness
            harmonic_richness = fingerprint['harmonic_richness']
            num_harmonics = int(1 + harmonic_richness * 4)  # 1-5 harmonics
            
            tone = self.generate_tone(frequency, actual_duration, 
                                     waveform='sine', harmonics=num_harmonics)
            
            # Envelope influenced by note duration bias
            attack = 0.05 * (1 - duration_bias * 0.5)  # Shorter attack for short notes
            release = 0.2 * (1 + duration_bias)  # Longer release for long notes
            
            envelope = self.generate_adsr_envelope(note_samples,
                                                   attack=attack, decay=0.1,
                                                   sustain=0.6, release=release)
            
            start_idx = int(i * note_duration * self.sample_rate)
            end_idx = start_idx + note_samples
            if end_idx <= len(melody):
                melody[start_idx:end_idx] = tone * envelope * 0.3
        
        return melody
    
    def generate_bass_with_fingerprint(self, root_freq: float, tempo: float,
                                      duration: float, fingerprint: Dict) -> np.ndarray:
        """Generate bass line using EEG fingerprint"""
        num_samples = int(duration * self.sample_rate)
        bass = np.zeros(num_samples)
        
        beat_duration = 60.0 / tempo
        samples_per_beat = int(beat_duration * self.sample_rate)
        num_beats = int(duration / beat_duration)
        
        # Bass pattern influenced by warmth and rhythm density
        warmth = fingerprint['warmth']
        rhythm_density = fingerprint['rhythm_density']
        
        # More warmth = more sustained bass
        # More rhythm density = more pulsing bass
        if warmth > 0.5:
            # Sustained bass
            bass_type = 'sustained'
            note_duration = beat_duration * 2
        else:
            # Pulsing bass
            bass_type = 'pulsing'
            note_duration = beat_duration * 0.5
        
        for beat in range(0, num_beats, 2 if bass_type == 'sustained' else 1):
            beat_sample = beat * samples_per_beat
            
            # Root note
            tone = self.generate_tone(root_freq / 2, note_duration, 
                                     waveform='sine', harmonics=2)
            envelope = self.generate_adsr_envelope(len(tone),
                                                   attack=0.01, decay=0.1,
                                                   sustain=0.7, release=0.2)
            
            end_idx = min(beat_sample + len(tone), len(bass))
            bass[beat_sample:end_idx] += (tone * envelope)[:end_idx - beat_sample] * 0.4
        
        return bass
    
    def generate_full_arrangement(self, music_params: Dict[str, float],
                                 duration: float = 4.0) -> np.ndarray:
        """
        Generate complete arrangement using EEG fingerprinting
        """
        # Calculate EEG fingerprint
        fingerprint = self.calculate_eeg_fingerprint(music_params)
        
        # Store for analysis
        self.eeg_fingerprint = fingerprint
        
        num_samples = int(duration * self.sample_rate)
        arrangement = np.zeros(num_samples)
        
        # Extract parameters
        arousal = music_params.get('arousal', 0.5)
        valence = music_params.get('valence', 0.5)
        complexity = music_params.get('complexity', 0.5)
        tempo = music_params.get('tempo', 90)
        scale_name = music_params.get('scale', 'pentatonic')
        
        # Get scale and root
        scale = self.scales.get(scale_name, self.scales['pentatonic'])
        root_freq = 220.0  # A3
        
        # Generate chords
        chord_intervals = self.generate_chord_progression(scale, valence, complexity)
        chords = self.generate_chords(root_freq, chord_intervals, duration, tempo)
        arrangement += chords
        
        # Generate bass with fingerprint
        bass = self.generate_bass_with_fingerprint(root_freq, tempo, duration, fingerprint)
        arrangement += bass
        
        # Generate melody with fingerprint
        if arousal > 0.2:
            melody = self.generate_melody_with_fingerprint(
                root_freq, scale, duration, complexity, valence, fingerprint
            )
            arrangement += melody
        
        # Generate drums with fingerprint
        if arousal > 0.3:
            drums = self.generate_drums_with_fingerprint(tempo, duration, arousal, fingerprint)
            arrangement += drums
        
        # Generate pad (ambient)
        if arousal < 0.6:
            pad = self.generate_pad(root_freq, chord_intervals[0], duration)
            arrangement += pad
        
        # Normalize
        max_val = np.max(np.abs(arrangement))
        if max_val > 0:
            arrangement = arrangement / max_val * 0.8
        
        return arrangement
