# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.3]

### Added

- Daily slap history tracking, saved to `slap_history.json` in app data directory.
- Quit button in the settings panel.
- Virtual environment (`.venv/`) instructions in README for running with older Python versions.

### Fixed

- Unicode logging errors on Windows consoles (emoji in achievement log messages).

### Removed

- Sound effects system (`SoundManager`, `generate_sounds.py`, `sounds/` directory) and all related UI settings (enable toggle, volume slider).
- Controller/gamepad input support (`ControllerListener`) and pygame dependency.
- `sound_enabled`, `sound_volume` config options from `bongo.ini`.
