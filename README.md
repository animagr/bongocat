# Bongo Cat Desktop Buddy

![Bongo Cat](img/cat-rest.png)

A desktop pet that slaps its paws whenever you press a key or click a mouse button. Frameless, always-on-top, draggable. Tracks slap count, grows a daily sunflower companion, builds combos, and unlocks achievements as you use it.

This fork removes sounds and associated dependencies, adds slap history by day saved in `slap_history.json`, and adds plant progress saved in `plant_state.json` in `%AppData%/BongoCat`.

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![GitHub last commit](https://img.shields.io/github/last-commit/animagr/bongocat/main)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/animagr/bongocat/main)

## Install

Grab a pre-built release for your platform:

- **Windows**: `BongoCat-windows-x64.exe` (unsigned, SmartScreen warns first launch)
- **macOS**: `BongoCat-macos.dmg` (unsigned, right-click → Open first launch)
- **Linux**: `BongoCat-linux-x86_64.AppImage` (`chmod +x` then run)

Latest: https://github.com/animagr/bongocat/releases/latest

## Run from source

Requires Python 3.8–3.11 (PyQt5 does not ship wheels for 3.13+).

```bash
git clone https://github.com/animagr/bongocat.git
cd bongocat
pip install -r requirements.txt
python -m bongo_cat
```

If your system Python is too new, use a virtual environment with an older version:

**Windows** (assuming Python 3.11 is installed alongside a newer version):

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m bongo_cat
```

**macOS / Linux**:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m bongo_cat
```

## Build a standalone

Same path CI uses (run inside the venv if applicable):

```bash
pip install -r requirements.txt "pyinstaller>=5.0" "Pillow>=10"
pyinstaller --clean --noconfirm bongo_cat.spec
```

Output lands in `dist/` as `BongoCat.exe`, `BongoCat.app`, or `BongoCat` depending on platform.

Linux needs xcb runtime libs first:

```bash
sudo apt install libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
  libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-sync1 libxcb-xfixes0 \
  libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0 libfuse2
```

## Configure

Hover the cat → ⚙ Settings opens the GUI. Click 📄 to open the ini directly.

Config file lives at:

- **Windows**: `%APPDATA%/BongoCat/bongo.ini`
- **macOS**: `~/.config/BongoCat/bongo.ini`
- **Linux**: `~/.config/BongoCat/bongo.ini`

| Key | Effect | Default |
|-----|--------|---------|
| `hidden_footer` | hide footer until you hover | `true` |
| `footer_alpha` | footer opacity (0–100) | `50` |
| `always_show_points` | always show total slaps | `false` |
| `floating_points` | "+1" animation per slap | `true` |
| `invert_cat` | mirror horizontally | `false` |
| `startup_with_windows` | autostart on login | `false` |
| `max_slaps` | counter cap (0 = unlimited) | `0` |
| `current_skin` | active skin folder name | `default` |

## Custom skins

Drop a folder under `skins/`:

```
skins/your-skin/
├── skin.json
├── cat-rest.png
├── cat-left.png
└── cat-right.png
```

`skin.json`:

```json
{
  "name": "Your Skin",
  "author": "you",
  "version": "1.0.0",
  "images": {
    "idle": "cat-rest.png",
    "left": "cat-left.png",
    "right": "cat-right.png"
  },
  "rotation_degrees": -13
}
```

PNGs with transparency, any size (default art is ~200×200). All three poses required. Restart, then pick it from Settings.

## Slap history

Daily slap counts are tracked automatically and saved to `slap_history.json` in the same directory as the config:

- **Windows**: `%APPDATA%/BongoCat/slap_history.json`
- **macOS**: `~/Library/Application Support/BongoCat/slap_history.json`
- **Linux**: `~/.config/BongoCat/slap_history.json`

History is saved when you quit the app. Format is `{"2026-05-15": 42, "2026-05-16": 108}`.

## Plant companion

Bongo Cat includes a small sunflower companion to the right of the cat. The plant grows from today's slap activity and resets to a seed each new day.

Growth stages are saved separately in `plant_state.json` next to the config and slap history files. The plant does not use the lifetime slap count, so long-running installs still get a fresh daily growth loop.

Current sunflower stages:

- `seed`: 0 daily slaps
- `seedling`: 1,000 daily slaps
- `growing1`: 2,500 daily slaps
- `young`: 5,000 daily slaps
- `growing2`: 8,000 daily slaps
- `growing3`: 12,500 daily slaps
- `mature`: 16,000 daily slaps
- `flowering`: 20,000 daily slaps
- `seed-bearing`: 25,000 daily slaps

Stage changes show a brief sparkle animation. Watering, wilting, harvesting, and multiple species are not implemented yet.

## Achievements

70 unlockables, saved to `achievements.json` next to the config.

- **Slap count**: 1, 7, 8, 12, 32, 42, 46, 99, 100, 128, 206, 212, 314, 366, 460, 500, 767, 1,000, 1,024, 1,618, 1,760, 3,220, 3,959, 5,000, 5,280, 6,022, 6,371, 7,917, 8,760, 10,000, 10,080, 14,700, 24,901, 25,000, 27,182, 31,415, 32,768, 50,000, 65,536, 86,400, 100,000, 186,282, 238,855, 384,400, 524,288, 1,000,000, 1,048,576, 1,618,034, 2,718,282, 3,141,593, 5,280,000, 5,865,696, 10,000,000
- **Combos**: 10, 25, 50, 100, 200, 300, 500, 1,000
- **Hidden and special**: late-night, early-morning, weekend, launch-count, overload, speed, and marathon achievements

## Troubleshooting

**Cat ignores keys or mouse.** Global hooks need permission:
- Windows: run as Administrator.
- macOS: System Settings → Privacy & Security → Accessibility, allow the app.
- Linux: add yourself to the `input` group.

**`pyinstaller` not found.** Install it (`pip install "pyinstaller>=5.0"`) or invoke via `python -m PyInstaller`.

**Bug report.** Open an issue: https://github.com/animagr/bongocat/issues

## Contributing

Fork, branch, open a PR. Run `python -m unittest discover tests -v` before submitting. Pushing a `v*` tag triggers `.github/workflows/release.yml`, which builds and publishes all three platforms.

## License

MIT. See [LICENSE](LICENSE).

---

*Inspired by the original Bongo Cat meme. Not affiliated with its creators.*
