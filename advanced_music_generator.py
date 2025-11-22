#!/usr/bin/env python3
"""
Advanced Music Generator with Multiple Instruments
Generates rich, musical compositions with harmony, rhythm, and multiple layers
"""

import numpy as np
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedMusicGenerator:
    """
    Generates complete musical arrangements with:
    - Chord progressions
    - Bass lines
    - Melody
    - Drums/Percussion
    - Ambient pads
    """
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        
        # Musical scales
        self.scales = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
            'pentatonic': [0, 2, 4, 7, 9],
            'blues': [0, 3, 5, 6, 7, 10]
        }
        
        # Chord progressions (in scale degrees)
        self.progressions = {
            'peaceful': [0, 3, 4, 0],      # I - IV - V - I
            'emotional': [0, 5, 3, 4],     # I - vi - IV - V
            'uplifting': [0, 4, 5, 3],     # I - V - vi - IV
            'melancholic': [5, 3, 0, 4]    # vi - IV - I - V
        }
        
    def generate_adsr_envelope(self, num_samples: int, 
                               attack: float = 0.05, 
                               decay: float = 0.1,
                               sustain: float = 0.7, 
                               release: float = 0.2) -> np.ndarray:
        """Generate ADSR envelope"""
        envelope = np.ones(num_samples)
        
        attack_samples = int(attack * num_samples)
        decay_samples = int(decay * num_samples)
        release_samples = int(release * num_samples)
        
        # Attack
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Decay
        if decay_samples > 0:
            envelope[attack_samples:attack_samples+decay_samples] = \
                np.linspace(1, sustain, decay_samples)
        
        # Sustain (already set to 1, will be multiplied by sustain level)
        sustain_start = attack_samples + decay_samples
        sustain_end = num_samples - release_samples
        if sustain_end > sustain_start:
            envelope[sustain_start:sustain_end] = sustain
        
        # Release
        if release_samples > 0:
            envelope[-release_samples:] = np.linspace(sustain, 0, release_samples)
        
        return envelope
    
    def generate_tone(self, frequency: float, duration: float, 
                     waveform: str = 'sine', harmonics: int = 3) -> np.ndarray:
        """Generate a tone with harmonics"""
        num_samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, num_samples)
        
        if waveform == 'sine':
            tone = np.sin(2 * np.pi * frequency * t)
            # Add harmonics for richness
            for h in range(2, harmonics + 1):
                tone += (1/h) * np.sin(2 * np.pi * frequency * h * t)
        
        elif waveform == 'square':
            tone = np.sign(np.sin(2 * np.pi * frequency * t))
        
        elif waveform == 'saw':
            tone = 2 * (t * frequency - np.floor(t * frequency + 0.5))
        
        elif waveform == 'triangle':
            tone = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
        
        else:  # Default to sine
            tone = np.sin(2 * np.pi * frequency * t)
        
        # Normalize
        tone = tone / np.max(np.abs(tone))
        
        return tone
    
    def generate_chord(self, root_freq: float, chord_intervals: List[int], 
                      duration: float, amplitude: float = 0.3) -> np.ndarray:
        """Generate a chord with multiple notes"""
        num_samples = int(duration * self.sample_rate)
        chord = np.zeros(num_samples)
        
        for interval in chord_intervals:
            freq = root_freq * (2 ** (interval / 12))
            tone = self.generate_tone(freq, duration, waveform='sine', harmonics=2)
            envelope = self.generate_adsr_envelope(num_samples, 
                                                   attack=0.1, decay=0.2, 
                                                   sustain=0.6, release=0.3)
            chord += tone * envelope
        
        # Normalize and apply amplitude
        chord = chord / len(chord_intervals) * amplitude
        
        return chord
    
    def generate_bass_line(self, root_freq: float, duration: float, 
                          pattern: str = 'steady') -> np.ndarray:
        """Generate bass line"""
        num_samples = int(duration * self.sample_rate)
        bass = np.zeros(num_samples)
        
        # Bass is one octave below root
        bass_freq = root_freq / 2
        
        if pattern == 'steady':
            # Steady bass note
            tone = self.generate_tone(bass_freq, duration, waveform='sine', harmonics=2)
            envelope = self.generate_adsr_envelope(num_samples, 
                                                   attack=0.01, decay=0.1, 
                                                   sustain=0.8, release=0.2)
            bass = tone * envelope * 0.5
        
        elif pattern == 'pulsing':
            # Pulsing bass (4 pulses per measure)
            pulse_duration = duration / 4
            for i in range(4):
                pulse_samples = int(pulse_duration * self.sample_rate)
                tone = self.generate_tone(bass_freq, pulse_duration, waveform='sine')
                envelope = self.generate_adsr_envelope(pulse_samples, 
                                                       attack=0.01, decay=0.05, 
                                                       sustain=0.3, release=0.1)
                start_idx = int(i * pulse_duration * self.sample_rate)
                end_idx = start_idx + pulse_samples
                if end_idx <= len(bass):
                    bass[start_idx:end_idx] = tone * envelope * 0.5
        
        return bass
    
    def generate_drums(self, duration: float, tempo: float, 
                      complexity: float = 0.5) -> np.ndarray:
        """Generate drum pattern"""
        num_samples = int(duration * self.sample_rate)
        drums = np.zeros(num_samples)
        
        # Calculate beat timing
        beats_per_second = tempo / 60
        beat_duration = 1.0 / beats_per_second
        num_beats = int(duration * beats_per_second)
        
        for beat in range(num_beats):
            beat_time = beat * beat_duration
            beat_sample = int(beat_time * self.sample_rate)
            
            # Kick drum (low frequency click)
            if beat % 2 == 0:  # On beats 1 and 3
                kick_duration = 0.1
                kick_samples = int(kick_duration * self.sample_rate)
                t = np.linspace(0, kick_duration, kick_samples)
                kick = np.sin(2 * np.pi * 60 * t) * np.exp(-t * 20)
                end_idx = beat_sample + kick_samples
                if end_idx <= len(drums):
                    drums[beat_sample:end_idx] += kick * 0.6
            
            # Hi-hat (high frequency noise)
            if complexity > 0.3:
                hihat_duration = 0.05
                hihat_samples = int(hihat_duration * self.sample_rate)
                hihat = np.random.randn(hihat_samples) * np.exp(-np.linspace(0, 1, hihat_samples) * 10)
                end_idx = beat_sample + hihat_samples
                if end_idx <= len(drums):
                    drums[beat_sample:end_idx] += hihat * 0.2
            
            # Snare (on beats 2 and 4)
            if beat % 4 == 2 and complexity > 0.5:
                snare_duration = 0.08
                snare_samples = int(snare_duration * self.sample_rate)
                t = np.linspace(0, snare_duration, snare_samples)
                snare = (np.sin(2 * np.pi * 200 * t) + 
                        0.5 * np.random.randn(snare_samples)) * np.exp(-t * 15)
                end_idx = beat_sample + snare_samples
                if end_idx <= len(drums):
                    drums[beat_sample:end_idx] += snare * 0.4
        
        return drums
    
    def generate_melody(self, root_freq: float, scale: List[int], 
                       duration: float, complexity: float = 0.5,
                       valence: float = 0.5) -> np.ndarray:
        """Generate melodic line"""
        num_samples = int(duration * self.sample_rate)
        melody = np.zeros(num_samples)
        
        # Number of notes based on complexity
        num_notes = int(2 + complexity * 6)  # 2-8 notes
        note_duration = duration / num_notes
        
        # Generate melodic contour
        current_degree = len(scale) // 2  # Start in middle of scale
        
        for i in range(num_notes):
            # Melodic movement (stepwise motion, not jumps)
            if i > 0:
                # Move up or down by 1-2 steps
                movement = np.random.choice([-2, -1, 0, 1, 2], 
                                          p=[0.1, 0.3, 0.2, 0.3, 0.1])
                current_degree = (current_degree + movement) % len(scale)
            
            # Calculate frequency
            octave = 2 if valence > 0.5 else 1  # Higher octave for positive valence
            semitones = scale[current_degree] + (octave * 12)
            frequency = root_freq * (2 ** (semitones / 12))
            
            # Generate note
            note_samples = int(note_duration * self.sample_rate)
            tone = self.generate_tone(frequency, note_duration, waveform='sine', harmonics=3)
            envelope = self.generate_adsr_envelope(note_samples, 
                                                   attack=0.05, decay=0.1, 
                                                   sustain=0.6, release=0.2)
            
            # Add to melody
            start_idx = int(i * note_duration * self.sample_rate)
            end_idx = start_idx + note_samples
            if end_idx <= len(melody):
                melody[start_idx:end_idx] = tone * envelope * 0.3
        
        return melody
    
    def generate_pad(self, root_freq: float, chord_intervals: List[int], 
                    duration: float) -> np.ndarray:
        """Generate ambient pad (sustained chords)"""
        num_samples = int(duration * self.sample_rate)
        pad = np.zeros(num_samples)
        
        # Generate soft, sustained chord
        for interval in chord_intervals:
            freq = root_freq * (2 ** (interval / 12))
            tone = self.generate_tone(freq, duration, waveform='sine', harmonics=1)
            # Very slow attack and release for pad
            envelope = self.generate_adsr_envelope(num_samples, 
                                                   attack=0.3, decay=0.1, 
                                                   sustain=0.8, release=0.4)
            pad += tone * envelope
        
        # Normalize and make quiet
        pad = pad / len(chord_intervals) * 0.15
        
        return pad
    
    def generate_full_arrangement(self, music_params: Dict[str, float], 
                                 duration: float = 4.0) -> np.ndarray:
        """
        Generate complete musical arrangement with all instruments
        """
        num_samples = int(duration * self.sample_rate)
        arrangement = np.zeros(num_samples)
        
        # Extract parameters
        arousal = music_params.get('arousal', 0.5)
        valence = music_params.get('valence', 0.5)
        complexity = music_params.get('complexity', 0.5)
        tempo = music_params.get('tempo', 90)
        
        # Select scale based on valence
        if valence > 0.6:
            scale = self.scales['major']
            progression_type = 'uplifting'
        elif valence < 0.4:
            scale = self.scales['minor']
            progression_type = 'melancholic'
        else:
            scale = self.scales['pentatonic']
            progression_type = 'peaceful'
        
        # Base frequency (root note)
        root_freq = 220  # A3
        
        # Get chord progression
        progression = self.progressions[progression_type]
        chord_duration = duration / len(progression)
        
        # Generate each layer
        for i, scale_degree in enumerate(progression):
            chord_start = int(i * chord_duration * self.sample_rate)
            chord_end = int((i + 1) * chord_duration * self.sample_rate)
            
            # Calculate root frequency for this chord
            chord_root = root_freq * (2 ** (scale[scale_degree] / 12))
            
            # Chord intervals (triad)
            if valence > 0.5:
                chord_intervals = [0, 4, 7]  # Major triad
            else:
                chord_intervals = [0, 3, 7]  # Minor triad
            
            # Generate chord
            chord = self.generate_chord(chord_root, chord_intervals, 
                                       chord_duration, amplitude=0.25)
            arrangement[chord_start:chord_end] += chord[:chord_end-chord_start]
            
            # Generate bass line
            bass_pattern = 'pulsing' if arousal > 0.5 else 'steady'
            bass = self.generate_bass_line(chord_root, chord_duration, 
                                          pattern=bass_pattern)
            arrangement[chord_start:chord_end] += bass[:chord_end-chord_start]
            
            # Generate pad (ambient layer)
            if arousal < 0.6:  # More pad in calmer music
                pad = self.generate_pad(chord_root, chord_intervals, chord_duration)
                arrangement[chord_start:chord_end] += pad[:chord_end-chord_start]
        
        # Generate melody over entire duration
        melody = self.generate_melody(root_freq, scale, duration, 
                                     complexity, valence)
        arrangement += melody
        
        # Generate drums
        if arousal > 0.3:  # Add drums for more energetic music
            drums = self.generate_drums(duration, tempo, complexity)
            arrangement += drums
        
        # Normalize final mix
        max_val = np.max(np.abs(arrangement))
        if max_val > 0:
            arrangement = arrangement / max_val * 0.8
        
        logger.info(f"🎼 Generated: {progression_type} progression, "
                   f"{len(progression)} chords, tempo={tempo:.0f} BPM")
        
        return arrangement

def test_generator():
    """Test the advanced music generator"""
    generator = AdvancedMusicGenerator()
    
    test_params = {
        'arousal': 0.6,
        'valence': 0.7,
        'complexity': 0.5,
        'tempo': 100
    }
    
    print("🎵 Generating test arrangement...")
    audio = generator.generate_full_arrangement(test_params, duration=4.0)
    print(f"✅ Generated {len(audio)} samples ({len(audio)/44100:.1f} seconds)")
    
    # Try to play if sounddevice available
    try:
        import sounddevice as sd
        print("🔊 Playing...")
        sd.play(audio, 44100)
        sd.wait()
        print("✅ Done!")
    except ImportError:
        print("⚠️ sounddevice not available for playback")

if __name__ == "__main__":
    test_generator()
