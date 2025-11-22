#!/usr/bin/env python3
"""
Neurable EEG Music Generator
Real-time music generation from Neurable 12-channel EEG device
"""

import numpy as np
import queue
import threading
import logging
from typing import Dict
from neurable_adapter import NeurableEEGAdapter
from advanced_music_generator import AdvancedMusicGenerator

# Check for audio availability
try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️ sounddevice not available - audio playback disabled")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NeurableMusicGenerator:
    """Generate music from Neurable EEG data"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.is_playing = False
        self.audio_queue = queue.Queue(maxsize=10)
        
        # Neurable adapter
        self.neurable_adapter = NeurableEEGAdapter(smoothing_window=5)
        
        # Advanced music generator
        self.music_generator = AdvancedMusicGenerator(sample_rate=sample_rate)
        
    def music_generation_callback(self, music_params: Dict[str, float]):
        """Callback to generate music from Neurable parameters"""
        try:
            # Generate full musical arrangement
            audio = self.music_generator.generate_full_arrangement(
                music_params, 
                duration=4.0
            )
            
            # Add to audio queue
            if not self.audio_queue.full():
                self.audio_queue.put(audio)
            else:
                logger.warning("⚠️ Audio queue full, skipping")
                
            # Log current state
            logger.info(
                f"🎵 Arousal={music_params['arousal']:.2f}, "
                f"Valence={music_params['valence']:.2f}, "
                f"Focus={music_params['focus']:.2f}, "
                f"Tempo={music_params['tempo']:.0f} BPM"
            )
            
        except Exception as e:
            logger.error(f"❌ Error generating music: {e}")
    
    def audio_playback_worker(self):
        """Worker thread for audio playback"""
        if not AUDIO_AVAILABLE:
            logger.error("❌ Audio playback not available")
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
                logger.error(f"❌ Audio playback error: {e}")
                
        logger.info("🔇 Audio playback stopped")
    
    def start_from_csv(self, csv_path: str, delay: float = 4.0):
        """
        Start music generation from Neurable CSV file.
        
        Args:
            csv_path: Path to Neurable CSV file
            delay: Delay between samples (seconds) - should match arrangement duration
        """
        if not AUDIO_AVAILABLE:
            logger.error("❌ Cannot start - audio not available")
            return
        
        # Start playback thread
        self.is_playing = True
        playback_thread = threading.Thread(target=self.audio_playback_worker)
        playback_thread.daemon = True
        playback_thread.start()
        
        logger.info("🎵 Music generation started!")
        logger.info(f"📂 Reading from: {csv_path}")
        logger.info("Press Ctrl+C to stop")
        
        try:
            # Stream from CSV
            self.neurable_adapter.stream_from_csv(
                csv_path,
                self.music_generation_callback,
                delay=delay
            )
        except KeyboardInterrupt:
            logger.info("⏹️ Stopping music generation...")
        finally:
            self.is_playing = False
            playback_thread.join(timeout=2.0)
            logger.info("✅ Music generation stopped")

def main():
    """Main entry point"""
    import sys
    
    # Default CSV path
    default_csv = "/Users/e.baena/CascadeProjects/mindfulmakers/neurable-eeg-stream/eeg_data_20251122_143416.csv"
    
    csv_path = sys.argv[1] if len(sys.argv) > 1 else default_csv
    
    print("=" * 60)
    print("🧠🎵 Neurable EEG Music Generator")
    print("=" * 60)
    print(f"\n📂 CSV File: {csv_path}")
    print(f"🎼 Sample Rate: 44.1kHz")
    print(f"⏱️  Arrangement Duration: 4 seconds")
    print(f"🎹 Instruments: Chords, Bass, Melody, Drums, Pads")
    print(f"\n🧠 Neurological Mapping:")
    print(f"   - Left Hemisphere → Tempo, Rhythm")
    print(f"   - Right Hemisphere → Melody, Harmony")
    print(f"   - Cognitive Ratios → Energy, Complexity")
    print("\n" + "=" * 60 + "\n")
    
    # Create generator
    generator = NeurableMusicGenerator()
    
    # Start generation
    generator.start_from_csv(csv_path, delay=4.0)

if __name__ == "__main__":
    main()
