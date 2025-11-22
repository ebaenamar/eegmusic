#!/usr/bin/env python3
"""
WebSocket Server for Brainwave Music Generator
Connects EEG stream to web dashboard and audio generation
"""

import asyncio
import json
import logging
import numpy as np
import websockets
from typing import Set
import threading
import time

# Import components
import sys
sys.path.append('/Users/e.baena/CascadeProjects')
from eeg_stream_handler import EEGStreamManager
from brainwave_music_generator import BrainwaveMusicGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MusicGeneratorServer:
    """WebSocket server for brainwave music generation"""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.is_running = False
        
        # EEG and music components
        self.eeg_manager = EEGStreamManager()
        self.music_generator = BrainwaveMusicGenerator()
        
        # Current state
        self.current_band_powers = {}
        self.current_music_params = {}
        self.current_eeg_sample = None
        
    async def register_client(self, websocket):
        """Register a new client"""
        self.clients.add(websocket)
        logger.info(f"✅ Client connected. Total clients: {len(self.clients)}")
        
    async def unregister_client(self, websocket):
        """Unregister a client"""
        self.clients.discard(websocket)
        logger.info(f"❌ Client disconnected. Total clients: {len(self.clients)}")
        
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if self.clients:
            message_json = json.dumps(message)
            await asyncio.gather(
                *[client.send(message_json) for client in self.clients],
                return_exceptions=True
            )
    
    def eeg_callback(self, eeg_data: np.ndarray):
        """Callback for EEG data - generates music and updates dashboard"""
        try:
            # Analyze brainwave bands
            band_powers = self.music_generator.analyze_eeg_bands(eeg_data)
            self.current_band_powers = band_powers
            
            # Map to musical parameters
            music_params = self.music_generator.map_brainwaves_to_music(band_powers)
            self.current_music_params = music_params
            
            # Store sample for visualization (first channel, last 50 samples)
            if eeg_data.shape[1] >= 50:
                self.current_eeg_sample = eeg_data[0, -50:].tolist()
            
            # Generate music (this happens in the music generator's callback)
            self.music_generator.eeg_to_music_callback(eeg_data)
            
            # Prepare data for dashboard
            dashboard_data = {
                'type': 'update',
                'band_powers': band_powers,
                'music_params': music_params,
                'eeg_sample': self.current_eeg_sample[-1] if self.current_eeg_sample else 0,
                'timestamp': time.time()
            }
            
            # Schedule broadcast
            asyncio.create_task(self.broadcast(dashboard_data))
            
        except Exception as e:
            logger.error(f"Error in EEG callback: {e}")
    
    async def handle_client_message(self, websocket, message: str):
        """Handle messages from clients"""
        try:
            data = json.loads(message)
            command = data.get('command')
            
            if command == 'start':
                await self.start_music_generation(data)
                await websocket.send(json.dumps({
                    'type': 'status',
                    'status': 'started',
                    'message': 'Music generation started'
                }))
                
            elif command == 'stop':
                await self.stop_music_generation()
                await websocket.send(json.dumps({
                    'type': 'status',
                    'status': 'stopped',
                    'message': 'Music generation stopped'
                }))
                
            elif command == 'configure':
                await self.configure_generator(data)
                await websocket.send(json.dumps({
                    'type': 'status',
                    'status': 'configured',
                    'message': 'Configuration updated'
                }))
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def start_music_generation(self, config: dict):
        """Start music generation with given configuration"""
        csv_path = config.get('csv_file', '/Users/e.baena/CascadeProjects/test_eeg_data.csv')
        scale = config.get('scale', 'pentatonic')
        base_freq = config.get('base_frequency', 220)
        
        # Update music generator configuration
        self.music_generator.current_scale = scale
        self.music_generator.base_frequency = base_freq
        
        # Create EEG stream
        stream = self.eeg_manager.create_stream(
            'file',
            file_path=csv_path,
            sample_rate=250,
            n_channels=8,
            loop=True
        )
        
        if stream:
            self.eeg_manager.set_current_stream(stream)
            
            # Start music generation
            success = self.music_generator.start_music_generation(self.eeg_manager)
            
            # Also set our callback for dashboard updates
            if success:
                self.is_running = True
                logger.info("🎵 Music generation started")
            else:
                logger.error("Failed to start music generation")
        else:
            logger.error("Failed to create EEG stream")
    
    async def stop_music_generation(self):
        """Stop music generation"""
        self.is_running = False
        self.music_generator.stop_music_generation(self.eeg_manager)
        logger.info("🛑 Music generation stopped")
    
    async def configure_generator(self, config: dict):
        """Update generator configuration"""
        if 'scale' in config:
            self.music_generator.current_scale = config['scale']
        if 'base_frequency' in config:
            self.music_generator.base_frequency = config['base_frequency']
        
        logger.info(f"⚙️ Configuration updated: {config}")
    
    async def handle_websocket(self, websocket, path):
        """Handle WebSocket connection"""
        await self.register_client(websocket)
        
        try:
            async for message in websocket:
                await self.handle_client_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_client(websocket)
    
    async def start_server(self):
        """Start the WebSocket server"""
        logger.info(f"🌐 Starting WebSocket server on ws://{self.host}:{self.port}")
        
        async with websockets.serve(self.handle_websocket, self.host, self.port):
            logger.info("✅ Server started successfully")
            logger.info(f"📱 Open web_dashboard.html in your browser")
            await asyncio.Future()  # Run forever

def main():
    """Main function"""
    print("🧠🎵 Brainwave Music Generator Server")
    print("=" * 50)
    
    server = MusicGeneratorServer()
    
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        print("✅ Server stopped")

if __name__ == "__main__":
    main()
