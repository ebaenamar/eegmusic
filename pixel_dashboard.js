// State management
const state = {
    source: 'csv',
    isPlaying: false,
    ws: null,
    backendWs: null,
    csvData: null,
    csvIndex: 0,
    config: {
        smoothing: 15,
        tempoStability: 0.85,
        duration: 6.0,
        baseScale: 'auto'
    },
    sampleCount: 0,
    lastSampleTime: Date.now()
};

// Oscilloscope setup
const canvas = document.getElementById('oscilloscope-canvas');
const ctx = canvas.getContext('2d');
canvas.width = canvas.offsetWidth;
canvas.height = canvas.offsetHeight;

const oscilloscopeData = {
    left: new Array(canvas.width).fill(canvas.height / 3),
    right: new Array(canvas.width).fill(canvas.height * 2 / 3)
};

// UI Elements
const elements = {
    btnCsvSource: document.getElementById('btn-csv-source'),
    btnUrlSource: document.getElementById('btn-url-source'),
    csvSourcePanel: document.getElementById('csv-source-panel'),
    urlSourcePanel: document.getElementById('url-source-panel'),
    csvFileInput: document.getElementById('csv-file-input'),
    csvFileName: document.getElementById('csv-file-name'),
    wsUrl: document.getElementById('ws-url'),
    wsStatusDot: document.getElementById('ws-status-dot'),
    wsStatusText: document.getElementById('ws-status-text'),
    smoothingSlider: document.getElementById('smoothing-slider'),
    smoothingValue: document.getElementById('smoothing-value'),
    tempoSlider: document.getElementById('tempo-slider'),
    tempoValue: document.getElementById('tempo-value'),
    durationSlider: document.getElementById('duration-slider'),
    durationValue: document.getElementById('duration-value'),
    baseScaleSelect: document.getElementById('base-scale-select'),
    presetSelect: document.getElementById('preset-select'),
    btnStart: document.getElementById('btn-start'),
    btnStop: document.getElementById('btn-stop'),
    playbackStatusDot: document.getElementById('playback-status-dot'),
    playbackStatusText: document.getElementById('playback-status-text'),
    activeSource: document.getElementById('active-source'),
    sampleCount: document.getElementById('sample-count'),
    sampleRate: document.getElementById('sample-rate')
};

// Connect to backend server
function connectBackend() {
    state.backendWs = new WebSocket('ws://localhost:8766');
    
    state.backendWs.onopen = () => {
        console.log('✅ Connected to backend server');
    };
    
    state.backendWs.onmessage = (event) => {
        const data = JSON.parse(event.data);
        updateUI(data);
    };
    
    state.backendWs.onerror = (error) => {
        console.error('❌ Backend connection error:', error);
    };
    
    state.backendWs.onclose = () => {
        console.log('🔌 Backend disconnected');
        setTimeout(connectBackend, 2000); // Reconnect
    };
}

// Source selection
elements.btnCsvSource.addEventListener('click', () => {
    state.source = 'csv';
    elements.btnCsvSource.classList.add('active');
    elements.btnUrlSource.classList.remove('active');
    elements.csvSourcePanel.style.display = 'block';
    elements.urlSourcePanel.style.display = 'none';
});

elements.btnUrlSource.addEventListener('click', () => {
    state.source = 'url';
    elements.btnUrlSource.classList.add('active');
    elements.btnCsvSource.classList.remove('active');
    elements.urlSourcePanel.style.display = 'block';
    elements.csvSourcePanel.style.display = 'none';
});

// CSV file selection
elements.csvFileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        elements.csvFileName.textContent = file.name;
        loadCSVFile(file);
    }
});

function loadCSVFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const text = e.target.result;
        parseCSV(text);
    };
    reader.readAsText(file);
}

function parseCSV(text) {
    const lines = text.trim().split('\n');
    const headers = lines[0].split(',');
    state.csvData = lines.slice(1).map(line => {
        const values = line.split(',');
        const row = {};
        headers.forEach((header, i) => {
            row[header.trim()] = parseFloat(values[i]) || 0;
        });
        return row;
    });
    state.csvIndex = 0;
    console.log(`✅ Loaded ${state.csvData.length} samples from CSV`);
}

// Configuration sliders
elements.smoothingSlider.addEventListener('input', (e) => {
    state.config.smoothing = parseInt(e.target.value);
    elements.smoothingValue.textContent = state.config.smoothing;
    elements.presetSelect.value = 'custom';
});

elements.tempoSlider.addEventListener('input', (e) => {
    state.config.tempoStability = parseFloat(e.target.value);
    elements.tempoValue.textContent = state.config.tempoStability.toFixed(2);
    elements.presetSelect.value = 'custom';
});

elements.durationSlider.addEventListener('input', (e) => {
    state.config.duration = parseFloat(e.target.value);
    elements.durationValue.textContent = state.config.duration.toFixed(1);
    elements.presetSelect.value = 'custom';
});

// Base scale selection
elements.baseScaleSelect.addEventListener('change', (e) => {
    state.config.baseScale = e.target.value;
    console.log(`🎼 Base scale set to: ${state.config.baseScale}`);
    
    // If playing, send update to backend
    if (state.isPlaying && state.backendWs && state.backendWs.readyState === WebSocket.OPEN) {
        state.backendWs.send(JSON.stringify({
            action: 'update_config',
            config: state.config
        }));
        console.log('📤 Sent scale update to backend');
    }
});

// Presets
elements.presetSelect.addEventListener('change', (e) => {
    const presets = {
        meditation: { smoothing: 20, tempoStability: 0.9, duration: 8 },
        balanced: { smoothing: 15, tempoStability: 0.85, duration: 6 },
        responsive: { smoothing: 10, tempoStability: 0.6, duration: 4 },
        dynamic: { smoothing: 5, tempoStability: 0.5, duration: 3 },
        ultra: { smoothing: 1, tempoStability: 0.2, duration: 2 }
    };
    
    if (e.target.value !== 'custom') {
        const preset = presets[e.target.value];
        state.config.smoothing = preset.smoothing;
        state.config.tempoStability = preset.tempoStability;
        state.config.duration = preset.duration;
        elements.smoothingSlider.value = preset.smoothing;
        elements.smoothingValue.textContent = preset.smoothing;
        elements.tempoSlider.value = preset.tempoStability;
        elements.tempoValue.textContent = preset.tempoStability.toFixed(2);
        elements.durationSlider.value = preset.duration;
        elements.durationValue.textContent = preset.duration.toFixed(1);
        console.log(`🎛️ Preset applied: ${e.target.value}`, state.config);
    }
});

// Start/Stop controls
elements.btnStart.addEventListener('click', startPlayback);
elements.btnStop.addEventListener('click', stopPlayback);

function startPlayback() {
    if (state.isPlaying) return;
    
    if (state.source === 'csv') {
        if (!state.csvData) {
            alert('Please load a CSV file first!');
            return;
        }
        startCSVPlayback();
    } else {
        startURLPlayback();
    }
}

function startCSVPlayback() {
    // Send CSV data to backend
    if (state.backendWs && state.backendWs.readyState === WebSocket.OPEN) {
        const command = {
            action: 'start_csv',
            config: state.config,
            data: state.csvData
        };
        
        state.backendWs.send(JSON.stringify(command));
        
        state.isPlaying = true;
        state.csvIndex = 0;
        elements.btnStart.classList.add('active');
        elements.playbackStatusDot.classList.add('active');
        elements.playbackStatusText.textContent = 'PLAYING';
        elements.activeSource.textContent = 'CSV FILE';
        
        console.log('▶ Started CSV playback');
    } else {
        alert('Backend not connected! Please refresh the page.');
    }
}

function startURLPlayback() {
    const url = elements.wsUrl.value;
    
    if (state.backendWs && state.backendWs.readyState === WebSocket.OPEN) {
        const command = {
            action: 'start_url',
            config: state.config,
            wsUrl: url
        };
        
        state.backendWs.send(JSON.stringify(command));
        
        state.isPlaying = true;
        elements.btnStart.classList.add('active');
        elements.playbackStatusDot.classList.add('active');
        elements.playbackStatusText.textContent = 'PLAYING';
        elements.activeSource.textContent = 'NEURABLE URL';
        elements.wsStatusDot.classList.add('active');
        elements.wsStatusText.textContent = 'CONNECTING...';
        
        console.log('▶ Started URL playback');
    } else {
        alert('Backend not connected! Please refresh the page.');
    }
}

function stopPlayback() {
    if (!state.isPlaying) return;
    
    // Send stop command to backend
    if (state.backendWs && state.backendWs.readyState === WebSocket.OPEN) {
        state.backendWs.send(JSON.stringify({ action: 'stop' }));
    }
    
    state.isPlaying = false;
    elements.btnStart.classList.remove('active');
    elements.playbackStatusDot.classList.remove('active');
    elements.playbackStatusText.textContent = 'STOPPED';
    elements.activeSource.textContent = 'NONE';
}

// Update UI with data from backend
function updateUI(data) {
    state.sampleCount++;
    elements.sampleCount.textContent = state.sampleCount;
    
    // Update sample rate
    const now = Date.now();
    const elapsed = (now - state.lastSampleTime) / 1000;
    if (elapsed > 0) {
        const rate = 1 / elapsed;
        elements.sampleRate.textContent = rate.toFixed(1);
    }
    state.lastSampleTime = now;
    
    // Update oscilloscope
    if (data.left_alpha !== undefined && data.right_alpha !== undefined) {
        updateOscilloscope(data.left_alpha, data.right_alpha);
    }
    
    // Update musical parameters
    if (data.tempo) document.getElementById('metric-tempo').textContent = Math.round(data.tempo);
    if (data.scale) document.getElementById('metric-scale').textContent = data.scale.toUpperCase();
    if (data.arousal !== undefined) document.getElementById('metric-arousal').textContent = data.arousal.toFixed(2);
    if (data.valence !== undefined) document.getElementById('metric-valence').textContent = data.valence.toFixed(2);
    if (data.energy !== undefined) document.getElementById('metric-energy').textContent = data.energy.toFixed(2);
    if (data.signal_quality !== undefined) document.getElementById('metric-quality').textContent = data.signal_quality.toFixed(2);
    
    // Update band powers
    if (data.delta !== undefined) document.getElementById('band-delta').textContent = data.delta.toFixed(2);
    if (data.theta !== undefined) document.getElementById('band-theta').textContent = data.theta.toFixed(2);
    if (data.alpha !== undefined) document.getElementById('band-alpha').textContent = data.alpha.toFixed(2);
    if (data.beta !== undefined) document.getElementById('band-beta').textContent = data.beta.toFixed(2);
    if (data.gamma !== undefined) document.getElementById('band-gamma').textContent = data.gamma.toFixed(2);
    if (data.focus !== undefined) document.getElementById('cognitive-focus').textContent = data.focus.toFixed(2);
}

// Oscilloscope rendering
function updateOscilloscope(leftValue, rightValue) {
    // Shift data
    oscilloscopeData.left.shift();
    oscilloscopeData.right.shift();
    
    // Add new values (normalized to canvas height)
    oscilloscopeData.left.push(canvas.height / 3 + leftValue * 50);
    oscilloscopeData.right.push(canvas.height * 2 / 3 + rightValue * 50);
    
    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid
    ctx.strokeStyle = '#003311';
    ctx.lineWidth = 1;
    for (let i = 0; i < canvas.height; i += 30) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(canvas.width, i);
        ctx.stroke();
    }
    
    // Draw left channel (green)
    ctx.strokeStyle = '#00ff41';
    ctx.lineWidth = 2;
    ctx.beginPath();
    oscilloscopeData.left.forEach((y, x) => {
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();
    
    // Draw right channel (cyan)
    ctx.strokeStyle = '#00ffff';
    ctx.lineWidth = 2;
    ctx.beginPath();
    oscilloscopeData.right.forEach((y, x) => {
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();
}

// Initialize
connectBackend();

// Animation loop for oscilloscope
function animate() {
    requestAnimationFrame(animate);
}
animate();
