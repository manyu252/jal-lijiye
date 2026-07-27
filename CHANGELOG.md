# Changelog

All notable changes to **Jal Lijiye** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
