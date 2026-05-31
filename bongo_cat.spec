# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for Bongo Cat."""

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all data files
datas = []

# Add required directories
if os.path.exists('img'):
    datas += [('img', 'img')]
if os.path.exists('skins'):
    datas += [('skins', 'skins')]
if os.path.exists('plant'):
    datas += [('plant', 'plant')]

# Add config file if it exists
if os.path.exists('bongo.ini'):
    datas += [('bongo.ini', '.')]

# Collect PySide6 data files
datas += collect_data_files('PySide6')

# Collect hidden imports
hiddenimports = []
hiddenimports += collect_submodules('PySide6')
hiddenimports += ['pynput.keyboard', 'pynput.mouse']

a = Analysis(
    ['bongo_cat/main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BongoCat',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='img/cat-rest.png' if os.path.exists('img/cat-rest.png') else None,
)

# macOS app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='BongoCat.app',
        icon='img/cat-rest.png' if os.path.exists('img/cat-rest.png') else None,
        bundle_identifier='com.animagr.bongocat',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': 'True',
            'LSBackgroundOnly': 'False',
        },
    )
