# Bongo Cat Desktop Buddy

![Bongo Cat](img/cat-rest.png)

A desktop pet that slaps its paws whenever you press a key or click a mouse button. Frameless, always-on-top, draggable. Tracks slap count, builds combos, and unlocks achievements as you use it.

[![Version](https://img.shields.io/github/v/release/luinbytes/bongocat)](https://github.com/luinbytes/bongocat/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Install

Grab a pre-built release for your platform:

- **Windows**: `BongoCat-windows-x64.exe` (unsigned, SmartScreen warns first launch)
- **macOS**: `BongoCat-macos.dmg` (unsigned, right-click → Open first launch)
- **Linux**: `BongoCat-linux-x86_64.AppImage` (`chmod +x` then run)

Latest: https://github.com/luinbytes/bongocat/releases/latest

## Run from source

Requires Python 3.8–3.11 (PyQt5 does not ship wheels for 3.13+).

```bash
git clone https://github.com/luinbytes/bongocat.git
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

## Achievements

14 unlockables, saved to `achievements.json` next to the config.

- **Slap count**: 1, 100, 500, 1,000, 5,000, 10,000
- **Combos**: 10, 25, 50, 100, 200
- **Hidden**: slap between midnight–3 AM, slap between 5–7 AM, hold a 60+ combo

## Troubleshooting

**Cat ignores keys or mouse.** Global hooks need permission:
- Windows: run as Administrator.
- macOS: System Settings → Privacy & Security → Accessibility, allow the app.
- Linux: add yourself to the `input` group.

**`pyinstaller` not found.** Install it (`pip install "pyinstaller>=5.0"`) or invoke via `python -m PyInstaller`.

**Bug report.** Open an issue: https://github.com/luinbytes/bongocat/issues

## Contributing

Fork, branch, open a PR. Run `python -m unittest discover tests -v` before submitting. Pushing a `v*` tag triggers `.github/workflows/release.yml`, which builds and publishes all three platforms.

## License

MIT. See [LICENSE](LICENSE).

---

*Inspired by the original Bongo Cat meme. Not affiliated with its creators.*
