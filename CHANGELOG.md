# Changelog

All notable changes to **Jal Lijiye** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.5] - 2026-08-03

### Fixed
- **macOS Zip Symlink Preservation**: Added `-y` flag (`zip -r -y`) in GitHub Actions release workflow to preserve macOS Framework symlinks. Prevents recursive framework file duplication (which bloated zips from 50 MB to 394 MB) and resolves dyld launch crash.

## [1.3.4] - 2026-08-03

### Fixed
- **PyInstaller Binary Framework Stripping**: Added explicit `EXCLUDED_BINARIES` list in `Jal Lijiye.spec` filtering both `a.binaries` and `a.datas` to purge unused Qt frameworks (`QtWebEngineCore`, `Qt3D`, `QtQuick`) and macOS permission plugins (`qdarwinpermissionplugin_location`).
- **CI Build Cache Cleanliness**: Added `--clean` and `--no-cache-dir` flags to `.github/workflows/release.yml` with environment diagnostics.

## [1.3.3] - 2026-08-03

### Fixed
- **CI/CD Build Command Alignment**: Replaced `.spec` file build step in GitHub Actions `.github/workflows/release.yml` with explicit PyInstaller CLI flags matching `build_app.sh`, ensuring GitHub Releases produce the exact same working 50-70 MB executable bundles as local builds.

## [1.3.2] - 2026-08-03

### Fixed
- **macOS Qt Permissions Plugin Stripping**: Expanded PyInstaller `.spec` filters to strip Qt permission plugins (`qdarwinpermissionplugin`) from both `a.binaries` and `a.datas` arrays across all Python versions (Python 3.12/3.13), completely resolving the `dyld` launch crash (`SIGSEGV 11`).
- **Qt Permissions Logging Guard**: Added early environment rule `QT_LOGGING_RULES="*.debug=false;qt.permissions=false"` at startup in `main.py`.

## [1.3.1] - 2026-08-03

### Fixed
- **macOS `dyld` Permission Crash (`SIGSEGV 11`)**: Filtered out `qdarwinpermissionplugin` and `QtPositioning` shared libraries from PyInstaller bundle analysis to prevent static initializer launch crashes.
- **Bundle Size Optimization**: Separated production runtime dependencies from heavy dev packages (`opencv-python`), reducing release zips down to minimal footprint (~70 MB).
- **Windows Release Zip Fix**: Fixed PowerShell archive path handling in GitHub Actions release workflow.

## [1.3.0] - 2026-08-02

### Added
- **Dynamic Walk-In GIF Timing**: Walk-in animation automatically syncs duration with character GIF length (auto-cut at 3.0s max).
- **Exclusive 4-Corner Screen Position Picker**: Choose screen entry/exit location in Settings (Bottom-Left, Top-Left, Bottom-Right, Top-Right).
- **Custom Speech Bubble Text**: Support for custom reminder text with `{name}` template replacement.
- **Brand Palette Restoration**: Restored warm paper light theme `#f6f4ee`, terracotta red `#89301c`, and sage green `#414f42`.

## [1.2.1] - 2026-07-28

### Fixed
- **Qt Font Family Inspection Warning**: Added dynamic runtime font inspection (`src/fonts.py`) via `QFontDatabase` to safely resolve font families at runtime, eliminating the 198ms Qt font alias population warning.
- **Robust Exception Handling**: Wrapped PyQt6 timer slots and dialog callbacks in `try...except` guards to prevent uncaught Python exceptions from raising `SIGABRT` crashes.

## [1.2.0] - 2026-07-28

### Added
- **Brand Palette & Design System**: Full application UI styling using brand tokens (`#89301c` Accent, `#414f42` Secondary, `#f6f4ee` Primary).
- **Typography Hierarchy**: Integrated **Poppins** for main headers, **Newsreader 14pt** for section subheadings, and **Work Sans** for body text, form fields, and buttons.
- **Single User Name Setting**: Added customizable user name configuration field (`user_name`) in Settings.
- **Personalized Speech Bubble Greetings**: Animated character dynamically greets the user with `"Jal lijiye, <name>! 💧"`.
- **Custom Animation File Pickers**: Added Entry GIF (`Walk-In`) and Exit GIF (`Walk-Out`) file pickers allowing users to load any local GIF animations.

### Removed
- **Multi-User Dropdown**: Removed legacy multi-user profile switcher dialog in favor of single configurable user profile settings.

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
