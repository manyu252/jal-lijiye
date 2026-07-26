#!/usr/bin/env bash
# Script to build lightweight standalone macOS executable app bundle for Jal Lijiye

set -e

echo "Building standalone macOS Application Bundle..."
export PYINSTALLER_CONFIG_DIR="$(pwd)/build/pyinstaller_config"

./venv/bin/pyinstaller --noconfirm --onedir --windowed \
  --name "Jal Lijiye" \
  --icon "assets/icon.png" \
  --add-data "assets:assets" \
  --exclude-module "PyQt6.QtQml" \
  --exclude-module "PyQt6.QtQuick" \
  --exclude-module "PyQt6.QtNetwork" \
  --exclude-module "PyQt6.QtPdf" \
  --exclude-module "PyQt6.QtSvg" \
  --exclude-module "PyQt6.QtDBus" \
  --exclude-module "PyQt6.QtTest" \
  --exclude-module "cv2" \
  --exclude-module "numpy" \
  --exclude-module "scipy" \
  main.py

echo "Build complete! Your app is ready at: dist/Jal Lijiye.app"
