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
        
        # Chord function weights (for generative progressions)
        # Based on music theory: tonic, subdominant, dominant relationships
        self.chord_functions = {
            'tonic': [0, 2, 5],        # I, iii, vi (stable, restful)
            'subdominant': [1, 3],     # ii, IV (preparation, tension building)
            'dominant': [4, 6],        # V, vii° (tension, wants resolution)
        }
        
        # Transition probabilities (music theory based)
        self.transitions = {
            'tonic': {'tonic': 0.2, 'subdominant': 0.4, 'dominant': 0.4},
            'subdominant': {'tonic': 0.3, 'subdominant': 0.2, 'dominant': 0.5},
            'dominant': {'tonic': 0.7, 'subdominant': 0.1, 'dominant': 0.2}
        }
    
    def generate_chord_progression(self, num_chords: int, arousal: float, 
                                   valence: float, complexity: float) -> List[int]:
        """
        Generate unique chord progression based on EEG state
        Uses Markov chain with music theory rules
        """
        progression = []
        
        # Always start with tonic (I chord)
        current_function = 'tonic'
        progression.append(0)  # I chord
        
        for i in range(num_chords - 1):
            # Get transition probabilities
            trans_probs = self.transitions[current_function].copy()
            
            # Modify probabilities based on EEG state
            # High arousal = more dominant (tension)
            if arousal > 0.6:
                trans_probs['dominant'] *= 1.5
                trans_probs['tonic'] *= 0.7
            # Low arousal = more tonic (stability)
            elif arousal < 0.4:
                trans_probs['tonic'] *= 1.5
                trans_probs['dominant'] *= 0.7
            
            # High valence = more subdominant-dominant (uplifting)
            if valence > 0.6:
                trans_probs['subdominant'] *= 1.3
            # Low valence = more tonic-subdominant (melancholic)
            elif valence < 0.4:
                trans_probs['tonic'] *= 1.2
                trans_probs['subdominant'] *= 1.2
            
            # High complexity = more variety
            if complexity > 0.6:
                # Flatten probabilities for more randomness
                for key in trans_probs:
                    trans_probs[key] = trans_probs[key] * 0.7 + 0.3
            
            # Normalize probabilities
            total = sum(trans_probs.values())
            trans_probs = {k: v/total for k, v in trans_probs.items()}
            
            # Choose next function
            functions = list(trans_probs.keys())
            probs = list(trans_probs.values())
            next_function = np.random.choice(functions, p=probs)
            
            # Choose specific chord from function
            available_chords = self.chord_functions[next_function]
            next_chord = np.random.choice(available_chords)
            
            progression.append(next_chord)
            current_function = next_function
        
        # Last chord should resolve to tonic (music theory)
        if progression[-1] != 0 and np.random.random() < 0.7:
            progression.append(0)
        
        return progression
        
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
                      complexity: float = 0.5, beta: float = 0.3) -> np.ndarray:
        """
        Generate drum pattern
        Pattern varies with beta (motor activity)
        """
        num_samples = int(duration * self.sample_rate)
        drums = np.zeros(num_samples)
        
        # Calculate beat timing
        beats_per_second = tempo / 60
        beat_duration = 1.0 / beats_per_second
        num_beats = int(duration * beats_per_second)
        
        # Beta determines rhythm pattern (motor cortex activity)
        # High beta = more complex, syncopated rhythms
        kick_pattern = 2 if beta < 0.25 else (3 if beta < 0.35 else 4)
        
        for beat in range(num_beats):
            beat_time = beat * beat_duration
            beat_sample = int(beat_time * self.sample_rate)
            
            # Kick drum - pattern varies with beta
            if beat % kick_pattern == 0:
                kick_duration = 0.1
                kick_samples = int(kick_duration * self.sample_rate)
                t = np.linspace(0, kick_duration, kick_samples)
                kick = np.sin(2 * np.pi * 60 * t) * np.exp(-t * 20)
                end_idx = beat_sample + kick_samples
                if end_idx <= len(drums):
                    drums[beat_sample:end_idx] += kick * 0.6
            
            # Extra kick on off-beats if high beta
            elif beta > 0.4 and np.random.random() < (beta - 0.4):
                kick_duration = 0.1
                kick_samples = int(kick_duration * self.sample_rate)
                t = np.linspace(0, kick_duration, kick_samples)
                kick = np.sin(2 * np.pi * 60 * t) * np.exp(-t * 20)
                end_idx = beat_sample + kick_samples
                if end_idx <= len(drums):
                    drums[beat_sample:end_idx] += kick * 0.3
            
            # Hi-hat - density varies with complexity and beta
            if complexity > 0.3 or beta > 0.3:
                hihat_duration = 0.05
                hihat_samples = int(hihat_duration * self.sample_rate)
                hihat = np.random.randn(hihat_samples) * np.exp(-np.linspace(0, 1, hihat_samples) * 10)
                end_idx = beat_sample + hihat_samples
                if end_idx <= len(drums):
                    drums[beat_sample:end_idx] += hihat * (0.15 + beta * 0.2)
            
            # Snare - pattern varies with beta
            snare_beat = 2 if beta < 0.3 else (3 if np.random.random() < 0.5 else 2)
            if beat % 4 == snare_beat:
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
                       valence: float = 0.5, beta: float = 0.3, 
                       alpha: float = 0.2, chord_tones: List[int] = None) -> np.ndarray:
        """
        Generate melodic line with rhythm variation
        Beta = motor activity (note speed)
        Alpha = relaxation (note length/legato)
        """
        num_samples = int(duration * self.sample_rate)
        melody = np.zeros(num_samples)
        
        # Beta determines note density (motor cortex)
        # High beta = faster notes, more activity
        if beta > 0.35:
            note_speed = 'fast'  # 16th notes
            base_notes = int(duration * 8)  # 8 notes per second
        elif beta > 0.20:
            note_speed = 'medium'  # 8th notes
            base_notes = int(duration * 4)  # 4 notes per second
        else:
            note_speed = 'slow'  # quarter notes  
            base_notes = int(duration * 2)  # 2 notes per second
        
        # Complexity adds more notes
        num_notes = int(base_notes * (0.5 + complexity))
        
        # Reduce notes if low activity (more silence)
        if beta < 0.15:
            num_notes = int(num_notes * 0.6)  # 40% fewer notes for very relaxed states
        
        # Alpha determines articulation
        # High alpha = legato (smooth, connected)
        # Low alpha = staccato (short, detached)
        if alpha > 0.3:
            articulation = 'legato'
            note_length_factor = 0.95  # Notes almost touch
            attack = 0.08
            release = 0.15
        elif alpha > 0.15:
            articulation = 'normal'
            note_length_factor = 0.8
            attack = 0.05
            release = 0.2
        else:
            articulation = 'staccato'
            note_length_factor = 0.5  # Short, detached notes
            attack = 0.02
            release = 0.1
        
        logger.info(f"🎹 Melody: {note_speed} notes, {articulation} (beta={beta:.2f}, alpha={alpha:.2f})")
        
        # Generate melodic contour
        current_degree = len(scale) // 2
        time_position = 0
        
        # If chord tones provided, prefer them (70% of the time)
        use_chord_tones = chord_tones is not None
        
        for i in range(num_notes):
            # Decide if using chord tone or passing tone
            if use_chord_tones and (i % 2 == 0 or np.random.random() < 0.7):
                # Use chord tone (strong beat or 70% probability)
                current_degree = np.random.choice(chord_tones)
            else:
                # Use passing tone or melodic movement
                if i > 0:
                    if valence > 0.6:
                        # Happy = more upward movement
                        movement = np.random.choice([-1, 0, 1, 2], p=[0.1, 0.2, 0.4, 0.3])
                    elif valence < 0.4:
                        # Sad = more downward movement
                        movement = np.random.choice([-2, -1, 0, 1], p=[0.3, 0.4, 0.2, 0.1])
                    else:
                        # Neutral = balanced
                        movement = np.random.choice([-2, -1, 0, 1, 2], 
                                                  p=[0.1, 0.3, 0.2, 0.3, 0.1])
                    current_degree = (current_degree + movement) % len(scale)
            
            # Calculate frequency
            octave = 2 if valence > 0.5 else 1
            semitones = scale[current_degree] + (octave * 12)
            frequency = root_freq * (2 ** (semitones / 12))
            
            # Note duration with variation
            base_duration = duration / num_notes
            # Add rhythmic variation based on position
            if i % 4 == 0:  # Downbeat
                actual_duration = base_duration * 1.2
            elif i % 2 == 1:  # Off-beat
                actual_duration = base_duration * 0.8
            else:
                actual_duration = base_duration
            
            # Apply articulation
            actual_duration *= note_length_factor
            
            # Generate note
            note_samples = int(actual_duration * self.sample_rate)
            tone = self.generate_tone(frequency, actual_duration, waveform='sine', harmonics=3)
            envelope = self.generate_adsr_envelope(note_samples, 
                                                   attack=attack, decay=0.1, 
                                                   sustain=0.6, release=release)
            
            # Add to melody
            start_idx = int(time_position * self.sample_rate)
            end_idx = start_idx + note_samples
            if end_idx <= len(melody):
                melody[start_idx:end_idx] = tone * envelope * 0.3
            
            # Advance time
            time_position += base_duration
        
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
        Uses EEG state as seed for unique variations
        """
        num_samples = int(duration * self.sample_rate)
        arrangement = np.zeros(num_samples)
        
        # Extract parameters
        arousal = music_params.get('arousal', 0.5)
        valence = music_params.get('valence', 0.5)
        complexity = music_params.get('complexity', 0.5)
        tempo = music_params.get('tempo', 90)
        
        # Create unique seed from EEG state (mental fingerprint)
        delta = music_params.get('delta', 0.1)
        theta = music_params.get('theta', 0.3)
        alpha = music_params.get('alpha', 0.2)
        beta = music_params.get('beta', 0.3)
        gamma = music_params.get('gamma', 0.1)
        
        # Generate seed from band powers (0-1000000)
        eeg_seed = int((delta * 1000 + theta * 10000 + alpha * 100000 + 
                       beta * 1000000 + gamma * 10000000) % 1000000)
        np.random.seed(eeg_seed)
        
        # Select scale based on valence OR override
        scale_name = music_params.get('scale', None)
        if scale_name and scale_name in self.scales:
            scale = self.scales[scale_name]
        else:
            # Auto-select based on valence
            if valence > 0.6:
                scale = self.scales['major']
            elif valence < 0.4:
                scale = self.scales['minor']
            else:
                scale = self.scales['pentatonic']
        
        # Base frequency varies with theta (0.5-4 Hz affects root note)
        root_variation = 1.0 + (theta - 0.3) * 0.2  # ±20% variation
        root_freq = 220 * np.clip(root_variation, 0.9, 1.1)  # A3 with variation
        
        # Generate UNIQUE chord progression based on EEG state
        # Number of chords varies with complexity
        num_chords = 3 if complexity < 0.3 else (4 if complexity < 0.7 else 5)
        progression = self.generate_chord_progression(num_chords, arousal, valence, complexity)
        
        chord_duration = duration / len(progression)
        
        logger.info(f"🎼 Generated progression: {progression} (arousal={arousal:.2f}, valence={valence:.2f})")
        
        # Generate each layer
        for i, scale_degree in enumerate(progression):
            chord_start = int(i * chord_duration * self.sample_rate)
            chord_end = int((i + 1) * chord_duration * self.sample_rate)
            
            # Convert to int and clamp to valid scale degrees
            scale_degree = int(scale_degree)
            if scale_degree >= len(scale):
                scale_degree = scale_degree % len(scale)
            
            # Calculate root frequency for this chord using scale intervals
            chord_root = root_freq * (2 ** (scale[scale_degree] / 12))
            
            # Build chord using scale intervals (music theory correct)
            # Triad: root (0), third (2 scale steps), fifth (4 scale steps)
            chord_scale_degrees = [
                scale_degree,                           # Root
                (scale_degree + 2) % len(scale),       # Third
                (scale_degree + 4) % len(scale)        # Fifth
            ]
            
            # Add 7th if gamma is high (complex harmony)
            if gamma > 0.05 and np.random.random() < gamma * 10:
                chord_scale_degrees.append((scale_degree + 6) % len(scale))  # Seventh
            
            # Convert scale degrees to chromatic intervals from root
            chord_intervals = [scale[deg] - scale[scale_degree] for deg in chord_scale_degrees]
            # Ensure all intervals are positive (within octave)
            chord_intervals = [interval if interval >= 0 else interval + 12 for interval in chord_intervals]
            
            # Generate chord
            chord = self.generate_chord(chord_root, chord_intervals, 
                                       chord_duration, amplitude=0.25)
            # Ensure sizes match
            segment_length = min(len(chord), chord_end - chord_start)
            arrangement[chord_start:chord_start + segment_length] += chord[:segment_length]
            
            # Generate bass line - pattern varies with delta/theta ratio
            delta_theta_ratio = delta / (theta + 0.01)
            if delta_theta_ratio > 0.5:  # More delta = steadier bass
                bass_pattern = 'steady'
            else:  # More theta = pulsing bass
                bass_pattern = 'pulsing'
            
            bass = self.generate_bass_line(chord_root, chord_duration, 
                                          pattern=bass_pattern)
            segment_length = min(len(bass), chord_end - chord_start)
            arrangement[chord_start:chord_start + segment_length] += bass[:segment_length]
            
            # Generate pad (ambient layer)
            if arousal < 0.6:  # More pad in calmer music
                pad = self.generate_pad(chord_root, chord_intervals, chord_duration)
                segment_length = min(len(pad), chord_end - chord_start)
                arrangement[chord_start:chord_start + segment_length] += pad[:segment_length]
        
        # Generate melody that follows chord progression
        melody = np.zeros(num_samples)
        for i, scale_degree in enumerate(progression):
            chord_start = int(i * chord_duration * self.sample_rate)
            chord_end = int((i + 1) * chord_duration * self.sample_rate)
            
            # Convert to int and clamp to valid scale degrees
            scale_degree = int(scale_degree)
            if scale_degree >= len(scale):
                scale_degree = scale_degree % len(scale)
            
            # Calculate root for this chord
            chord_root = root_freq * (2 ** (scale[scale_degree] / 12))
            
            # Get chord tones for this chord (scale degrees)
            # Build triad: root, third, fifth (in scale steps)
            chord_tones = [
                scale_degree,                      # Root (1st)
                (scale_degree + 2) % len(scale),  # Third (3rd scale degree)
                (scale_degree + 4) % len(scale)   # Fifth (5th scale degree)
            ]
            
            # Generate melody segment that fits this chord
            melody_segment = self.generate_melody(chord_root, scale, chord_duration, 
                                                 complexity, valence, beta, alpha, chord_tones)
            
            # Add to full melody
            segment_length = min(len(melody_segment), chord_end - chord_start)
            melody[chord_start:chord_start + segment_length] += melody_segment[:segment_length]
        
        arrangement += melody
        
        # Generate drums - pass beta for rhythm variation
        if arousal > 0.3:  # Add drums for more energetic music
            drums = self.generate_drums(duration, tempo, complexity, beta)
            arrangement += drums
        
        # Normalize final mix
        max_val = np.max(np.abs(arrangement))
        if max_val > 0:
            arrangement = arrangement / max_val * 0.8
        
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
