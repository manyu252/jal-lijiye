# -*- mode: python ; coding: utf-8 -*-
import sys

is_windows = sys.platform == 'win32'
is_mac = sys.platform == 'darwin'
icon_path = 'assets/icon.ico' if is_windows else 'assets/icon.png'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt6.QtQml', 'PyQt6.QtQuick', 'PyQt6.QtNetwork', 'PyQt6.QtPdf', 'PyQt6.QtSvg', 'PyQt6.QtDBus', 'PyQt6.QtTest', 'cv2', 'numpy', 'scipy'],
    noarchive=False,
    optimize=0,
)
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
    icon=[icon_path],
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
            'CFBundleShortVersionString': '1.2.0',
            'CFBundleVersion': '1.2.0',
            'NSHumanReadableCopyright': 'Copyright © 2026 Jal Lijiye Team',
        },
    )
