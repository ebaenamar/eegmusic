# Changelog

All notable changes to the Brainwave Music Generator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-22

### Added
- Initial release of Brainwave Music Generator
- Neurologically-grounded EEG to music mapping system
- Multi-instrument music generation:
  - Chord progressions (4-chord patterns)
  - Bass lines (steady and pulsing patterns)
  - Melodic lines with stepwise motion
  - Drum patterns (kick, snare, hi-hat)
  - Ambient pads
- Psychological dimension mapping:
  - Arousal (activation level)
  - Valence (emotional tone)
  - Cognitive load (mental effort)
- Temporal smoothing (5-sample window) for consistency
- Real-time EEG streaming from CSV files
- WebSocket server for dashboard integration
- Interactive web dashboard
- Complete technical documentation
- Quick start guide
- Setup and run scripts

### Features
- FFT-based frequency band extraction (Delta, Theta, Alpha, Beta, Gamma)
- Scientifically-based arousal/valence model
- Automatic cognitive state detection (deep rest, meditation, relaxed focus, active focus, high performance)
- Musical scale selection based on emotional state
- Dynamic tempo adjustment (60-180 BPM)
- ADSR envelope generation for natural sound
- Audio mixing and normalization
- Support for 8-channel EEG input at 250Hz

### Technical Details
- Sample rate: 44.1kHz
- Arrangement duration: 4 seconds
- Update latency: ~1.5 seconds
- Frequency resolution: 1Hz
- Smoothing window: 5 samples

### Documentation
- README.md: Project overview and quick start
- TECHNICAL_DOCUMENTATION.md: Complete technical specifications
- QUICKSTART.md: Step-by-step usage guide
- Inline code documentation

### Dependencies
- numpy >= 1.21.0
- sounddevice >= 0.4.5
- websockets >= 10.0
- pandas >= 1.3.0
- scipy >= 1.7.0

## [Unreleased]

### Planned Features
- MIDI output support
- Real-time EEG device integration (OpenBCI, Muse)
- Channel-specific mapping (frontal, central, posterior)
- Advanced signal processing (notch filter, artifact rejection)
- Audio effects (reverb, delay, chorus)
- Recording and export functionality
- Machine learning for personalized mappings
- Multiple instrument timbres
- User preference learning
- Style transfer capabilities

### Known Issues
- None reported

---

## Version History

- **1.0.0** (2025-11-22): Initial release with complete neurological mapping system
