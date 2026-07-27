# Changelog

All notable changes to **Jal Lijiye** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-07-27

### Added
- **Full Cross-Platform Support**: Native execution and packaging support for both Windows and macOS.
- **Windows System Tray Integration**: Application icon automatically docks into the Windows taskbar notification area (System Tray).
- **Windows Transparent Window Support**: Added `WA_NoSystemBackground` flag to frameless overlay window initialization for clean transparent rendering on Windows.
- **OS-Specific Icon Handling**: Dynamic icon resolution using `assets/icon.ico` on Windows and `assets/icon.png` on macOS.

### Changed
- **Path Management**: Refactored asset, database, and configuration path handling across `config.py`, `db.py`, `overlay.py`, `tray.py`, and `main.py` using Python `pathlib.Path`.
- **Screen Geometry Calculation**: Refined screen bounds calculation to use `availableGeometry()` ensuring character positioning sits directly above the taskbar on Windows.
- **PyInstaller Specification**: Updated `Jal Lijiye.spec` to conditionally target Windows and macOS builds with OS-specific icon extensions and conditional `BUNDLE` packaging.

## [1.0.0] - 2026-07-27

### Added
- **Multi-User Profile System**: Switch profiles between `Abhimanyu`, `Shreya`, and `Default` directly from the system tray menu.
- **Custom Character Animations**: Support for user-specific companion GIFs (`<name>_walk.gif` and `<name>_exit.gif`) with personalized speech bubble greetings.
- **Standalone macOS Application Bundle**: Compiled native macOS `.app` bundle (`dist/Jal Lijiye.app`) and Finder double-clickable launcher script (`Jal Lijiye.command`).
- **Hydration & Laptop Session Analytics**: Daily drink count tracking, active screen hours calculation, and hydration ratio computation per profile.
- **Automatic Database Migrations**: Seamless schema inspection and auto-migration for pre-existing SQLite databases.

### Fixed
- **App Bundle Size**: Reduced standalone `.app` size from `190 MB` down to `73 MB` (>60% reduction).
- **Resource Resolution**: Fixed menu bar icon and character GIF resolution inside macOS `.app` bundles (`resolve_asset_path()`).
- **Crash Prevention**: Added exception guards across PyQt6 timer slots to prevent `SIGABRT` / `qFatal()` crashes.
- **Menu Bar Styling**: Cleaned system tray dropdown items (removed emojis, trailing `...`, and positioned Switch User below Settings).

### Changed
- Reorganized video processing utilities under a clean master converter: `scripts/mp4_to_gif.py`.
- Optimized SQLite query performance using standard `LEFT JOIN` operations.
