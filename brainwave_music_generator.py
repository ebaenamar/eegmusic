#!/usr/bin/env python3
"""
Brainwave Music Generator - Real-time music generation from EEG signals
Converts brain activity patterns into musical compositions
"""

import numpy as np
import threading
import time
import queue
from typing import Dict, List, Optional
import logging

# Audio generation
try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️ sounddevice not available. Install with: pip install sounddevice")

# Import the EEG stream handler
import sys
sys.path.append('/Users/e.baena/CascadeProjects')

# Make serial import optional in eeg_stream_handler
import importlib.util
if importlib.util.find_spec('serial') is None:
    # Mock serial module if not available
    sys.modules['serial'] = type('serial', (), {'Serial': None})()

from eeg_stream_handler import EEGStreamManager, FileEEGStream
from neuro_music_mapper import NeuroMusicMapper
from advanced_music_generator import AdvancedMusicGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrainwaveMusicGenerator:
    """Generate music from EEG brainwave patterns"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.is_playing = False
        self.audio_queue = queue.Queue(maxsize=10)
        
        # Neurologically-grounded mapper
        self.neuro_mapper = NeuroMusicMapper(smoothing_window=5)
        
        # Advanced music generator (with multiple instruments)
        self.music_generator = AdvancedMusicGenerator(sample_rate=sample_rate)
        
        # Musical scales and parameters
        self.scales = {
            'pentatonic': [0, 2, 4, 7, 9],  # Major pentatonic
            'minor': [0, 2, 3, 5, 7, 8, 10],
            'major': [0, 2, 4, 5, 7, 9, 11],
            'blues': [0, 3, 5, 6, 7, 10]
        }
        
        self.base_frequency = 220  # A3
        self.current_scale = 'pentatonic'
        
        # EEG frequency bands (Hz)
        self.bands = {
            'delta': (0.5, 4),
            'theta': (4, 8),
            'alpha': (8, 13),
            'beta': (13, 30),
            'gamma': (30, 50)
        }
        
    def analyze_eeg_bands(self, eeg_data: np.ndarray) -> Dict[str, float]:
        """Analyze EEG data to extract frequency band powers"""
        # eeg_data shape: (channels, samples)
        band_powers = {}
        
        for band_name, (low_freq, high_freq) in self.bands.items():
            # Simple power calculation using FFT
            fft_vals = np.fft.fft(eeg_data, axis=1)
            freqs = np.fft.fftfreq(eeg_data.shape[1], 1.0/250)  # Assuming 250Hz sampling
            
            # Get power in frequency band
            band_mask = (freqs >= low_freq) & (freqs <= high_freq)
            band_power = np.mean(np.abs(fft_vals[:, band_mask])**2)
            band_powers[band_name] = band_power
            
        # Normalize powers
        total_power = sum(band_powers.values())
        if total_power > 0:
            band_powers = {k: v/total_power for k, v in band_powers.items()}
            
        return band_powers
    
    def map_brainwaves_to_music(self, band_powers: Dict[str, float]) -> Dict[str, float]:
        """
        Map brainwave patterns to musical parameters using neurologically-grounded mapper.
        Ensures consistency and prevents sudden jumps.
        """
        # Use the neurological mapper for consistent, smoothed parameters
        music_params = self.neuro_mapper.get_musical_parameters(band_powers)
        
        # Add legacy compatibility fields
        music_params['bass_level'] = music_params['bass_presence']
        music_params['melody_complexity'] = music_params['harmony']
        
        return music_params
    
    def generate_note(self, frequency: float, duration: float, 
                     amplitude: float = 0.3) -> np.ndarray:
        """Generate a single note with ADSR envelope"""
        num_samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, num_samples)
        
        # Generate tone with harmonics
        tone = np.sin(2 * np.pi * frequency * t)
        tone += 0.5 * np.sin(2 * np.pi * frequency * 2 * t)  # 2nd harmonic
        tone += 0.25 * np.sin(2 * np.pi * frequency * 3 * t)  # 3rd harmonic
        
        # ADSR envelope
        attack = int(0.1 * num_samples)
        decay = int(0.2 * num_samples)
        sustain_level = 0.7
        release = int(0.3 * num_samples)
        
        envelope = np.ones(num_samples)
        envelope[:attack] = np.linspace(0, 1, attack)
        envelope[attack:attack+decay] = np.linspace(1, sustain_level, decay)
        envelope[-release:] = np.linspace(sustain_level, 0, release)
        
        return tone * envelope * amplitude
    
    def generate_chord(self, root_freq: float, chord_type: str, 
                      duration: float, amplitude: float = 0.2) -> np.ndarray:
        """Generate a chord"""
        intervals = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            'seventh': [0, 4, 7, 10]
        }
        
        chord = np.zeros(int(duration * self.sample_rate))
        for interval in intervals.get(chord_type, [0, 4, 7]):
            freq = root_freq * (2 ** (interval / 12))
            chord += self.generate_note(freq, duration, amplitude)
            
        return chord / len(intervals[chord_type])
    
    def create_musical_phrase(self, music_params: Dict[str, float], 
                            duration: float = 2.0) -> np.ndarray:
        """
        Create a musical phrase based on neurologically-grounded parameters.
        Uses arousal/valence to ensure musical consistency.
        """
        phrase = np.zeros(int(duration * self.sample_rate))
        
        # Get neurological dimensions
        arousal = music_params.get('arousal', 0.5)
        valence = music_params.get('valence', 0.5)
        complexity = music_params.get('complexity', 0.5)
        
        # Select scale based on valence (emotional tone)
        if valence > 0.6:
            scale = self.scales['major']  # Positive emotion
        elif valence < 0.4:
            scale = self.scales['minor']  # Negative emotion
        else:
            scale = self.scales['pentatonic']  # Neutral/peaceful
        
        # Number of notes based on complexity and arousal
        # Low arousal = fewer, longer notes
        # High arousal = more, shorter notes
        num_notes = int(2 + arousal * 6 + complexity * 2)  # 2-10 notes
        num_notes = max(2, min(num_notes, 10))  # Clamp to reasonable range
        note_duration = duration / num_notes
        
        # Generate melody with consistent progression
        for i in range(num_notes):
            # Select note from scale - use rhythm_variation for melodic movement
            rhythm_var = music_params.get('rhythm_variation', 0.5)
            
            # Create melodic contour (not random jumps)
            if i == 0:
                scale_degree = int(len(scale) / 2)  # Start in middle
            else:
                # Move up or down based on rhythm variation
                movement = int((rhythm_var - 0.5) * 3)  # -1, 0, or +1
                scale_degree = (scale_degree + movement) % len(scale)
            
            # Calculate frequency with consistent octave
            base_octave = 1 if arousal < 0.3 else (2 if arousal < 0.7 else 3)
            brightness = music_params.get('brightness', 0.3)
            octave_adjust = 1 if brightness > 0.5 else 0
            
            semitones = scale[scale_degree] + ((base_octave + octave_adjust) * 12)
            frequency = self.base_frequency * (2 ** (semitones / 12))
            
            # Generate note with amplitude based on arousal
            amplitude = 0.2 + 0.3 * arousal  # 0.2-0.5 range
            note = self.generate_note(frequency, note_duration, amplitude)
            
            # Add to phrase
            start_idx = int(i * note_duration * self.sample_rate)
            end_idx = start_idx + len(note)
            if end_idx <= len(phrase):
                phrase[start_idx:end_idx] += note
        
        # Add bass note based on delta (foundation)
        bass_presence = music_params.get('bass_presence', 0.2)
        if bass_presence > 0.25:
            bass_freq = self.base_frequency / 2
            bass = self.generate_note(bass_freq, duration, 
                                     0.4 * music_params['bass_level'])
            phrase += bass[:len(phrase)]
        
        # Normalize
        max_val = np.max(np.abs(phrase))
        if max_val > 0:
            phrase = phrase / max_val * 0.7
            
        return phrase
    
    def eeg_to_music_callback(self, eeg_data: np.ndarray):
        """Callback to convert EEG data to music"""
        try:
            # Analyze brainwave bands
            band_powers = self.analyze_eeg_bands(eeg_data)
            
            # Map to musical parameters
            music_params = self.map_brainwaves_to_music(band_powers)
            
            # Generate full musical arrangement (4 seconds for complete progression)
            audio = self.music_generator.generate_full_arrangement(music_params, duration=4.0)
            
            # Add to audio queue
            if not self.audio_queue.full():
                self.audio_queue.put(audio)
                
            # Log current state with neurological dimensions
            logger.info(f"🎵 Arousal={music_params['arousal']:.2f}, "
                       f"Valence={music_params['valence']:.2f}, "
                       f"Load={music_params['cognitive_load']:.2f} | "
                       f"Tempo={music_params['tempo']:.0f} BPM")
            
        except Exception as e:
            logger.error(f"Error generating music: {e}")
    
    def audio_playback_worker(self):
        """Worker thread for audio playback"""
        if not AUDIO_AVAILABLE:
            logger.error("Audio playback not available")
            return
            
        logger.info("🔊 Audio playback started")
        
        while self.is_playing:
            try:
                # Get audio from queue
                audio = self.audio_queue.get(timeout=1.0)
                
                # Play audio
                sd.play(audio, self.sample_rate)
                sd.wait()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Audio playback error: {e}")
                
        logger.info("🔇 Audio playback stopped")
    
    def start_music_generation(self, eeg_stream_manager: EEGStreamManager):
        """Start generating music from EEG stream"""
        if not AUDIO_AVAILABLE:
            logger.error("Cannot start: sounddevice not available")
            return False
            
        self.is_playing = True
        
        # Start audio playback thread
        self.playback_thread = threading.Thread(
            target=self.audio_playback_worker, 
            daemon=True
        )
        self.playback_thread.start()
        
        # Start EEG streaming with music callback
        success = eeg_stream_manager.start_streaming(self.eeg_to_music_callback)
        
        if success:
            logger.info("🎼 Music generation started!")
        else:
            logger.error("Failed to start EEG streaming")
            self.is_playing = False
            
        return success
    
    def stop_music_generation(self, eeg_stream_manager: EEGStreamManager):
        """Stop music generation"""
        self.is_playing = False
        eeg_stream_manager.stop_streaming()
        logger.info("🛑 Music generation stopped")

def main():
    """Main function to run brainwave music generator"""
    print("🧠🎵 Brainwave Music Generator")
    print("=" * 50)
    
    if not AUDIO_AVAILABLE:
        print("❌ Audio not available. Install sounddevice:")
        print("   pip install sounddevice")
        return
    
    # Create EEG stream manager
    eeg_manager = EEGStreamManager()
    
    # Create file stream with test data
    csv_path = "/Users/e.baena/CascadeProjects/test_eeg_data.csv"
    stream = eeg_manager.create_stream(
        'file',
        file_path=csv_path,
        sample_rate=250,
        n_channels=8,
        loop=True
    )
    
    if not stream:
        print("❌ Failed to create EEG stream")
        return
    
    eeg_manager.set_current_stream(stream)
    
    # Create music generator
    music_gen = BrainwaveMusicGenerator()
    
    # Start music generation
    print("\n🎼 Starting music generation from brainwaves...")
    print("   Press Ctrl+C to stop\n")
    
    if music_gen.start_music_generation(eeg_manager):
        try:
            # Keep running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping...")
            music_gen.stop_music_generation(eeg_manager)
            print("✅ Stopped successfully")
    else:
        print("❌ Failed to start music generation")

if __name__ == "__main__":
    main()
