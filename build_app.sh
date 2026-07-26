#!/usr/bin/env bash
# Script to build standalone macOS executable app bundle for Jal Lijiye

set -e

echo "Building standalone macOS Application Bundle..."
export PYINSTALLER_CONFIG_DIR="$(pwd)/build/pyinstaller_config"

./venv/bin/pyinstaller --noconfirm --onedir --windowed \
  --name "Jal Lijiye" \
  --icon "assets/icon.png" \
  --add-data "assets:assets" \
  --add-data "character_data:character_data" \
  main.py

echo "Build complete! Your app is ready at: dist/Jal Lijiye.app"
