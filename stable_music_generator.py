#!/usr/bin/env python3
"""
Stable Neurable Music Generator
Enhanced musical stability and coherence
"""

import numpy as np
import queue
import threading
import logging
from typing import Dict
from stable_neurable_adapter import StableNeurableAdapter
from advanced_music_generator import AdvancedMusicGenerator

try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️ sounddevice not available")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StableMusicGenerator:
    """Generate stable, coherent music from Neurable EEG data"""
    
    def __init__(self, 
                 sample_rate: int = 44100,
                 smoothing_window: int = 15,
                 tempo_stability: float = 0.8,
                 arrangement_duration: float = 6.0):
        """
        Args:
            sample_rate: Audio sample rate
            smoothing_window: EEG smoothing window size
            tempo_stability: Tempo stability factor (0-1)
            arrangement_duration: Duration of each musical phrase (seconds)
        """
        self.sample_rate = sample_rate
        self.arrangement_duration = arrangement_duration
        self.is_playing = False
        self.audio_queue = queue.Queue(maxsize=10)
        
        # Stable Neurable adapter
        self.neurable_adapter = StableNeurableAdapter(
            smoothing_window=smoothing_window,
            tempo_stability=tempo_stability,
            scale_stability_samples=8
        )
        
        # Advanced music generator
        self.music_generator = AdvancedMusicGenerator(sample_rate=sample_rate)
        
        logger.info(f"🎼 Stable Music Generator initialized")
        logger.info(f"   Arrangement duration: {arrangement_duration}s")
        logger.info(f"   Smoothing window: {smoothing_window}")
        logger.info(f"   Tempo stability: {tempo_stability}")
        
    def music_generation_callback(self, music_params: Dict[str, float]):
        """Callback to generate music from stable parameters"""
        try:
            # Generate full musical arrangement
            audio = self.music_generator.generate_full_arrangement(
                music_params, 
                duration=self.arrangement_duration
            )
            
            # Add to audio queue
            if not self.audio_queue.full():
                self.audio_queue.put(audio)
            else:
                logger.warning("⚠️ Audio queue full, skipping")
                
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
                audio = self.audio_queue.get(timeout=1.0)
                sd.play(audio, self.sample_rate)
                sd.wait()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"❌ Audio playback error: {e}")
                
        logger.info("🔇 Audio playback stopped")
    
    def start_from_csv(self, csv_path: str):
        """Start stable music generation from Neurable CSV"""
        if not AUDIO_AVAILABLE:
            logger.error("❌ Cannot start - audio not available")
            return
        
        # Start playback thread
        self.is_playing = True
        playback_thread = threading.Thread(target=self.audio_playback_worker)
        playback_thread.daemon = True
        playback_thread.start()
        
        logger.info("🎵 Stable music generation started!")
        logger.info(f"📂 Reading from: {csv_path}")
        logger.info("Press Ctrl+C to stop")
        
        try:
            self.neurable_adapter.stream_from_csv(
                csv_path,
                self.music_generation_callback,
                delay=self.arrangement_duration
            )
        except KeyboardInterrupt:
            logger.info("⏹️ Stopping music generation...")
        finally:
            self.is_playing = False
            playback_thread.join(timeout=2.0)
            logger.info("✅ Music generation stopped")

def main():
    """Main entry point with configuration options"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Stable Neurable EEG Music Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default settings
  python stable_music_generator.py /path/to/eeg_data.csv
  
  # High stability (smoother, slower changes)
  python stable_music_generator.py --smoothing 20 --tempo-stability 0.9 data.csv
  
  # More responsive (faster changes)
  python stable_music_generator.py --smoothing 10 --tempo-stability 0.6 data.csv
  
  # Longer musical phrases
  python stable_music_generator.py --duration 8 data.csv
        """
    )
    
    parser.add_argument('csv_file', 
                       nargs='?',
                       default='/Users/e.baena/Desktop/eeg_stream.csv',
                       help='Path to Neurable CSV file')
    
    parser.add_argument('--smoothing', '-s',
                       type=int,
                       default=15,
                       help='Smoothing window size (default: 15, range: 5-30)')
    
    parser.add_argument('--tempo-stability', '-t',
                       type=float,
                       default=0.8,
                       help='Tempo stability factor (default: 0.8, range: 0.5-0.95)')
    
    parser.add_argument('--duration', '-d',
                       type=float,
                       default=6.0,
                       help='Arrangement duration in seconds (default: 6.0)')
    
    args = parser.parse_args()
    
    # Validate arguments
    args.smoothing = max(5, min(30, args.smoothing))
    args.tempo_stability = max(0.5, min(0.95, args.tempo_stability))
    args.duration = max(3.0, min(10.0, args.duration))
    
    print("=" * 70)
    print("🧠🎵 Stable Neurable EEG Music Generator")
    print("=" * 70)
    print(f"\n📂 CSV File: {args.csv_file}")
    print(f"🎼 Sample Rate: 44.1kHz")
    print(f"⏱️  Arrangement Duration: {args.duration}s")
    print(f"📊 Smoothing Window: {args.smoothing} samples")
    print(f"🎯 Tempo Stability: {args.tempo_stability}")
    print(f"\n🎹 Features:")
    print(f"   • Temporal smoothing for stable transitions")
    print(f"   • Scale stability (no abrupt changes)")
    print(f"   • Smooth tempo transitions")
    print(f"   • Harmonic consistency")
    print(f"   • Multi-instrument arrangements")
    print(f"\n🧠 Neurological Mapping:")
    print(f"   • Left Hemisphere → Tempo, Rhythm")
    print(f"   • Right Hemisphere → Melody, Harmony")
    print(f"   • Cognitive Ratios → Energy, Complexity")
    print("\n" + "=" * 70 + "\n")
    
    # Create generator
    generator = StableMusicGenerator(
        smoothing_window=args.smoothing,
        tempo_stability=args.tempo_stability,
        arrangement_duration=args.duration
    )
    
    # Start generation
    generator.start_from_csv(args.csv_file)

if __name__ == "__main__":
    main()
