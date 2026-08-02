# -*- mode: python ; coding: utf-8 -*-
import sys

is_mac = sys.platform == 'darwin'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt6.QtQml', 'PyQt6.QtQuick', 'PyQt6.QtNetwork', 'PyQt6.QtPdf',
        'PyQt6.QtSvg', 'PyQt6.QtDBus', 'PyQt6.QtTest', 'PyQt6.QtPositioning',
        'PyQt6.QtSensors', 'PyQt6.QtBluetooth', 'PyQt6.QtLocation',
        'PyQt6.QtMultimedia', 'PyQt6.QtWebEngineCore', 'PyQt6.QtDesigner',
        'PyQt6.QtHelp', 'cv2', 'numpy', 'scipy', 'matplotlib'
    ],
    noarchive=False,
    optimize=0,
)

# Filter out Qt location permission plugins that cause dyld launch crashes on macOS
a.binaries = [
    x for x in a.binaries
    if 'qdarwinpermissionplugin' not in x[0].lower()
    and 'positioning' not in x[0].lower()
    and 'location' not in x[0].lower()
]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Jal Lijiye',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/icon.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Jal Lijiye',
)
if is_mac:
    app = BUNDLE(
        coll,
        name='Jal Lijiye.app',
        icon='assets/icon.png',
        bundle_identifier='com.jallijiye.app',
        info_plist={
            'CFBundleName': 'Jal Lijiye',
            'CFBundleDisplayName': 'Jal Lijiye',
            'CFBundleIdentifier': 'com.jallijiye.app',
            'CFBundleShortVersionString': '1.3.1',
            'CFBundleVersion': '1.3.1',
            'NSHighResolutionCapable': 'True',
            'NSHumanReadableCopyright': 'Copyright © 2026 Jal Lijiye Team',
        },
    )
