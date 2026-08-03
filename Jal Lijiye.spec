# -*- mode: python ; coding: utf-8 -*-
import sys

is_mac = sys.platform == 'darwin'
asset_sep = ';' if sys.platform == 'win32' else ':'
icon_file = 'assets/icon.ico' if sys.platform == 'win32' else 'assets/icon.png'

# Heavy or crashing native Qt frameworks and permission plugins to strip from release builds
EXCLUDED_BINARIES = [
    'qdarwinpermissionplugin_location',
    'qdarwinpermissionplugin',
    'QtWebEngineCore',
    'Qt3D',
    'QtQuick',
    'QtQml',
    'QtMultimedia',
    'QtDesigner',
    'QtPdf',
    'QtPositioning',
    'QtSensors',
    'QtBluetooth',
    'QtLocation',
    'QtTest',
    'QtDBus',
    'QtSvg',
    'QtNetwork',
]

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

# Strip native libraries and plugin binaries matching excluded list
a.binaries = [
    b for b in a.binaries 
    if not any(excluded.lower() in b[0].lower() for excluded in EXCLUDED_BINARIES)
]

# Strip data/plugin entries matching excluded list
a.datas = [
    d for d in a.datas 
    if not any(excluded.lower() in d[0].lower() for excluded in EXCLUDED_BINARIES)
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
    icon=[icon_file],
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
            'CFBundleShortVersionString': '1.3.4',
            'CFBundleVersion': '1.3.4',
            'NSHighResolutionCapable': 'True',
            'NSHumanReadableCopyright': 'Copyright © 2026 Jal Lijiye Team',
        },
    )
