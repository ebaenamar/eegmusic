# 🎮 Pixel Dashboard Guide

## 🚀 Quick Start

### 1. Start Backend Server
```bash
cd /Users/e.baena/CascadeProjects/eeg-music-generator
source venv/bin/activate
python pixel_backend_server.py
```

### 2. Open Dashboard
```bash
open pixel_dashboard.html
```
Or navigate to: `file:///Users/e.baena/CascadeProjects/eeg-music-generator/pixel_dashboard.html`

## 🎯 Using the Dashboard

### Data Source Selection

#### Option 1: CSV File
1. Click **"📁 CSV FILE"** button
2. Click **"CLICK TO LOAD FILE"**
3. Select your CSV file (e.g., `/Users/e.baena/Desktop/eeg_stream.csv`)
4. File name will appear below

#### Option 2: Neurable URL
1. Click **"🌐 NEURABLE URL"** button
2. URL is pre-filled: `wss://stream2.mindfulmakers.xyz`
3. Connection status will show when streaming starts

**⚠️ Important**: Sources are **exclusive** - only one can be active at a time!

### Configuration

#### Smoothing Window (5-30)
- **Low (5-10)**: Responsive, follows EEG changes quickly
- **Medium (15)**: Balanced (default)
- **High (20-30)**: Very stable, slow transitions

#### Tempo Stability (0.5-0.95)
- **Low (0.5-0.6)**: Dynamic tempo changes
- **Medium (0.85)**: Balanced (default)
- **High (0.9-0.95)**: Very stable tempo

#### Phrase Duration (3-10 sec)
- **Short (3-4s)**: Quick changes, more variety
- **Medium (6s)**: Balanced (default)
- **Long (8-10s)**: Longer, more developed phrases

#### Presets
- **MEDITATION**: Smoothing=20, Tempo=0.9, Duration=8 (very stable)
- **BALANCED**: Smoothing=15, Tempo=0.85, Duration=6 (default)
- **RESPONSIVE**: Smoothing=10, Tempo=0.6, Duration=4 (dynamic)
- **CUSTOM**: Manual configuration

### Controls

#### ▶ START
- Starts music generation from selected source
- Button glows green when active
- Status changes to "PLAYING"
- Active source is displayed

#### ⏹ STOP
- Stops current playback
- Closes WebSocket if using URL source
- Status changes to "STOPPED"

## 📊 Visualizations

### EEG Oscilloscope
- **Green line**: Left hemisphere alpha activity
- **Cyan line**: Right hemisphere alpha activity
- Real-time waveform display
- Grid background for reference

### Musical State
- **TEMPO**: Current BPM (60-140)
- **SCALE**: Major/Minor/Pentatonic
- **AROUSAL**: Energy level (0-1)
- **VALENCE**: Emotional tone (0-1)
- **ENERGY**: Overall energy (0-1)
- **QUALITY**: Signal quality (0-1)

### Brain Activity
- **DELTA**: 0.5-4 Hz (deep sleep)
- **THETA**: 4-8 Hz (meditation)
- **ALPHA**: 8-13 Hz (relaxed)
- **BETA**: 13-30 Hz (active)
- **GAMMA**: 30-50 Hz (peak)
- **FOCUS**: Alpha/Theta ratio

## 🎨 Visual Indicators

### Status Dots
- **Red**: Inactive/Disconnected
- **Green (blinking)**: Active/Connected
- **Yellow**: Connecting

### Button States
- **Normal**: Dark background, green border
- **Hover**: Green background
- **Active**: Green background with pulse animation

## 🔧 Troubleshooting

### Backend Not Connecting
```bash
# Check if server is running
ps aux | grep pixel_backend_server

# Restart server
pkill -f pixel_backend_server
python pixel_backend_server.py
```

### No Audio
- Check that sounddevice is installed
- Verify audio device in system settings
- Check console for errors (F12 in browser)

### CSV Not Loading
- Ensure file is in Neurable format (27 columns)
- Check file path is accessible
- Look for errors in browser console

### WebSocket Connection Failed
- Verify URL is correct
- Check internet connection
- Ensure Neurable stream is active
- Check backend server logs

### Oscilloscope Not Updating
- Refresh browser page
- Check backend connection
- Verify data is being received (check sample count)

## 📝 Tips

1. **Start with Balanced preset** - Good for most use cases
2. **Use CSV for testing** - More predictable than live stream
3. **Monitor signal quality** - Should be > 0.3 for good results
4. **Watch the oscilloscope** - Visual feedback of EEG activity
5. **Adjust smoothing first** - Has biggest impact on stability

## 🎵 Expected Behavior

### Good Signal (Quality > 0.5)
- Smooth musical transitions
- Consistent tempo and scale
- Rich harmonic content
- Oscilloscope shows clear patterns

### Poor Signal (Quality < 0.3)
- ⚠️ More random musical output
- System still works but less accurate
- Oscilloscope may show noise
- Consider adjusting electrodes

## 🔄 Workflow Example

### Testing with CSV
1. Start backend server
2. Open dashboard
3. Select "CSV FILE"
4. Load `/Users/e.baena/Desktop/eeg_stream.csv`
5. Choose "BALANCED" preset
6. Click "START"
7. Observe oscilloscope and metrics
8. Adjust smoothing if needed
9. Click "STOP" when done

### Live Streaming from Neurable
1. Start backend server
2. Open dashboard
3. Select "NEURABLE URL"
4. Verify URL: `wss://stream2.mindfulmakers.xyz`
5. Choose preset (try "MEDITATION" for stable)
6. Click "START"
7. Wait for connection (status dot turns green)
8. Monitor real-time data
9. Click "STOP" to disconnect

## 🎮 Keyboard Shortcuts

Currently none - use mouse/trackpad for all controls

## 🌐 Browser Compatibility

- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ⚠️ Older browsers may have issues with WebSocket

## 📊 Performance

- **CPU**: Moderate (audio synthesis + visualization)
- **Memory**: ~200-300 MB
- **Network**: Minimal (WebSocket only)
- **Latency**: ~100-200ms end-to-end

## 🎨 Customization

### Change Colors
Edit `pixel_style.css`:
```css
/* Primary color */
color: #00ff41; /* Green */

/* Change to blue */
color: #00ffff;
```

### Adjust Oscilloscope
Edit `pixel_dashboard.js`:
```javascript
// Change line thickness
ctx.lineWidth = 2; // Default

// Change colors
ctx.strokeStyle = '#00ff41'; // Left channel
ctx.strokeStyle = '#00ffff'; // Right channel
```

---

**Enjoy your pixel art EEG music experience! 🧠🎵🎮**
