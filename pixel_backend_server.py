#!/usr/bin/env python3
"""
Pixel Dashboard Backend Server
Connects the pixel frontend with the stable music generator pipeline
"""

import asyncio
import json
import ssl
import websockets
import logging
from pathlib import Path
import threading
import queue

# Import the stable music generator components
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

class PixelBackendServer:
    """Backend server for pixel dashboard"""
    
    def __init__(self, host='localhost', port=8766):
        self.host = host
        self.port = port
        self.clients = set()
        self.is_playing = False
        self.audio_queue = queue.Queue(maxsize=10)
        self.neurable_adapter = None
        self.music_generator = None
        self.playback_thread = None
        self.source_type = None
        self.source_ws = None
        self.current_config = {}
        
    async def register(self, websocket):
        """Register a new client"""
        self.clients.add(websocket)
        logger.info(f"✅ Client connected: {websocket.remote_address}")
        
    async def unregister(self, websocket):
        """Unregister a client"""
        self.clients.remove(websocket)
        logger.info(f"❌ Client disconnected: {websocket.remote_address}")
        
    async def broadcast(self, message):
        """Broadcast message to all connected clients"""
        if self.clients:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.clients],
                return_exceptions=True
            )
    
    def music_generation_callback(self, music_params):
        """Callback for music generation"""
        try:
            # Generate audio
            if self.music_generator:
                audio = self.music_generator.generate_full_arrangement(
                    music_params,
                    duration=music_params.get('duration', 6.0)
                )
                
                # Add to audio queue
                if not self.audio_queue.full():
                    self.audio_queue.put(audio)
            
            # Broadcast parameters to frontend (schedule in event loop)
            loop = asyncio.get_event_loop()
            loop.create_task(self.broadcast({
                'tempo': music_params.get('tempo', 0),
                'scale': music_params.get('scale', 'unknown'),
                'arousal': music_params.get('arousal', 0),
                'valence': music_params.get('valence', 0),
                'energy': music_params.get('energy', 0),
                'signal_quality': music_params.get('signal_quality', 0),
                'delta': music_params.get('delta', 0),
                'theta': music_params.get('theta', 0),
                'alpha': music_params.get('alpha', 0),
                'beta': music_params.get('beta', 0),
                'gamma': music_params.get('gamma', 0),
                'focus': music_params.get('focus', 0),
                'left_alpha': music_params.get('Left__alpha', music_params.get('alpha', 0)),
                'right_alpha': music_params.get('Right__alpha', music_params.get('alpha', 0))
            }))
            
        except Exception as e:
            logger.error(f"❌ Error in music generation callback: {e}")
            import traceback
            traceback.print_exc()
    
    def audio_playback_worker(self):
        """Worker thread for audio playback"""
        if not AUDIO_AVAILABLE:
            logger.error("❌ Audio playback not available")
            return
            
        logger.info("🔊 Audio playback started")
        
        while self.is_playing:
            try:
                audio = self.audio_queue.get(timeout=1.0)
                sd.play(audio, 44100)
                sd.wait()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"❌ Audio playback error: {e}")
                
        logger.info("🔇 Audio playback stopped")
    
    async def start_csv_playback(self, csv_data, config):
        """Start playback from CSV data"""
        logger.info(f"📂 Starting CSV playback with {len(csv_data)} samples")
        
        # Save config
        self.current_config = config
        
        # Initialize adapter and generator
        self.neurable_adapter = StableNeurableAdapter(
            smoothing_window=config['smoothing'],
            tempo_stability=config['tempoStability'],
            scale_stability_samples=8
        )
        
        self.music_generator = AdvancedMusicGenerator(sample_rate=44100)
        
        # Start audio playback thread
        self.is_playing = True
        self.playback_thread = threading.Thread(target=self.audio_playback_worker)
        self.playback_thread.daemon = True
        self.playback_thread.start()
        
        # Stream from CSV data
        try:
            for idx, row_data in enumerate(csv_data):
                if not self.is_playing:
                    break
                    
                # Extract hemisphere data
                left_data = {
                    'delta': row_data.get('Left__delta', 0),
                    'theta': row_data.get('Left__theta', 0),
                    'alpha': row_data.get('Left__alpha', 0),
                    'beta': row_data.get('Left__beta', 0),
                    'gamma': row_data.get('Left__gamma', 0),
                    'focus': row_data.get('Left__a_ta', 0),
                    'alertness': row_data.get('Left__b_tb', 0),
                    'cognitive_load': row_data.get('Left__b_ab', 0),
                    'engagement': row_data.get('Left__mab_tmab', 0),
                    'signal_quality': 1.0 - row_data.get('Left__p_bad', 0)
                }
                
                right_data = {
                    'delta': row_data.get('Right__delta', 0),
                    'theta': row_data.get('Right__theta', 0),
                    'alpha': row_data.get('Right__alpha', 0),
                    'beta': row_data.get('Right__beta', 0),
                    'gamma': row_data.get('Right__gamma', 0),
                    'focus': row_data.get('Right__a_ta', 0),
                    'alertness': row_data.get('Right__b_tb', 0),
                    'cognitive_load': row_data.get('Right__b_ab', 0),
                    'engagement': row_data.get('Right__mab_tmab', 0),
                    'signal_quality': 1.0 - row_data.get('Right__p_bad', 0)
                }
                
                # Process through adapter
                music_params = self.neurable_adapter.map_to_music_parameters(left_data, right_data)
                music_params['duration'] = self.current_config.get('duration', config['duration'])
                
                # Override scale if base scale is set (use current_config for live updates)
                base_scale = self.current_config.get('baseScale', config.get('baseScale'))
                if base_scale and base_scale != 'auto':
                    music_params['scale'] = base_scale
                    logger.info(f"🎼 Forcing scale: {base_scale}")
                
                # Add hemisphere data for visualization
                music_params['Left__alpha'] = left_data['alpha']
                music_params['Right__alpha'] = right_data['alpha']
                
                self.music_generation_callback(music_params)
                
                # Wait for duration
                await asyncio.sleep(config['duration'])
                
        except Exception as e:
            logger.error(f"❌ CSV playback error: {e}")
            import traceback
            traceback.print_exc()
            self.is_playing = False
    
    async def start_url_playback(self, ws_url, config):
        """Start playback from WebSocket URL"""
        logger.info(f"🌐 Starting URL playback: {ws_url}")
        
        # Initialize adapter and generator
        self.neurable_adapter = StableNeurableAdapter(
            smoothing_window=config['smoothing'],
            tempo_stability=config['tempoStability'],
            scale_stability_samples=8
        )
        
        self.music_generator = AdvancedMusicGenerator(sample_rate=44100)
        
        # Start audio playback thread
        self.is_playing = True
        self.playback_thread = threading.Thread(target=self.audio_playback_worker)
        self.playback_thread.daemon = True
        self.playback_thread.start()
        
        # Connect to Neurable WebSocket
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        try:
            async with websockets.connect(
                ws_url,
                ssl=ssl_context,
                ping_interval=20,
                ping_timeout=10
            ) as ws:
                self.source_ws = ws
                logger.info("✅ Connected to Neurable stream")
                
                async for msg in ws:
                    if not self.is_playing:
                        break
                        
                    eeg_data = json.loads(msg)
                    
                    # Process through adapter
                    # Convert to pandas Series-like dict
                    music_params = self.neurable_adapter.process_neurable_row(eeg_data)
                    self.music_generation_callback(music_params)
                    
        except Exception as e:
            logger.error(f"❌ WebSocket error: {e}")
            self.is_playing = False
    
    def stop_playback(self):
        """Stop playback"""
        logger.info("⏹ Stopping playback")
        self.is_playing = False
        
        if self.source_ws:
            asyncio.create_task(self.source_ws.close())
            self.source_ws = None
        
        if self.playback_thread:
            self.playback_thread.join(timeout=2.0)
            self.playback_thread = None
    
    async def handle_client(self, websocket):
        """Handle client connection"""
        await self.register(websocket)
        
        try:
            async for message in websocket:
                data = json.loads(message)
                action = data.get('action')
                
                if action == 'start_csv':
                    csv_data = data.get('data', [])
                    config = data.get('config', {})
                    asyncio.create_task(self.start_csv_playback(csv_data, config))
                    
                elif action == 'start_url':
                    ws_url = data.get('wsUrl')
                    config = data.get('config', {})
                    asyncio.create_task(self.start_url_playback(ws_url, config))
                        
                elif action == 'stop':
                    self.stop_playback()
                    
                elif action == 'update_config':
                    new_config = data.get('config', {})
                    self.current_config.update(new_config)
                    logger.info(f"🔄 Config updated: {new_config}")
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)
    
    async def start(self):
        """Start the server"""
        logger.info(f"🚀 Starting Pixel Backend Server on {self.host}:{self.port}")
        
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()  # Run forever

def main():
    """Main entry point"""
    print("=" * 70)
    print("🎮 Pixel Dashboard Backend Server")
    print("=" * 70)
    print(f"\n🌐 Server: ws://localhost:8766")
    print(f"📂 Frontend: Open pixel_dashboard.html in browser")
    print(f"\n✨ Features:")
    print(f"   • CSV file streaming")
    print(f"   • Neurable WebSocket streaming")
    print(f"   • Real-time music generation")
    print(f"   • Live parameter visualization")
    print("\n" + "=" * 70 + "\n")
    
    server = PixelBackendServer()
    
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\n⏹ Server stopped by user")

if __name__ == "__main__":
    main()
