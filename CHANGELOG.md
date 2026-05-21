# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.6] - 2026-05-20

### Added

- Daily plant companion displayed to the right of Bongo Cat.
- Random daily plant species selection from subfolders under `plant/`, with the same plant stage image naming conventions.
- Separate `plant_state.json` progress file for daily plant growth, independent of the lifetime slap counter.
- Slap-driven plant stages: seed, seedling, growing transitions, young, mature, flowering, and seed-bearing.
- Sparkle transition overlay when the plant reaches a new stage.
- Plant assets are included in package manifests and PyInstaller build data.
- Plant state regression tests for thresholds, daily reset behavior, persistence, and corrupt-state fallback.

## [2.0.5] - 2026-05-18

### Fixed

- `UpdateLayeredWindowIndirect` error on Windows caused by child widgets (combo pop, overload wobble/shake, floating +1 labels, achievement notifications) being positioned outside the translucent window bounds.

## [2.0.4] - 2026-05-18

### Added

- Science, measurement, and computing themed slap-count achievements, bringing the total achievement count to 70 and extending slap milestones to 10,000,000.
- `RUN.bat` for launching the app from the repo root with the local virtual environment and keeping the console open.
- Achievement regression tests for milestone ordering, uniqueness, total count, and high-tier unlock coverage.

### Fixed

- Footer graphics effect lifecycle issues when dragging the footer or applying footer settings.
- macOS release workflow DMG creation now retries transient `hdiutil` failures.

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
