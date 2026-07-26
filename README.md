# 💧 Jal Lijiye - macOS Drinking Water Buddy

**Jal Lijiye** (*"Water, please!"*) is a cute, lightweight, team-friendly macOS desktop app that reminds you to stay hydrated while working. An animated pixel-art character walks onto the bottom of your screen with a glass, prompts you to drink water, celebrates on confirmation, snoozes for 10 minutes when deferred, and maintains local hydration statistics over time.

---

## ✨ Features

- 🚶 **Animated Screen Overlay**: Your character walks onto the bottom edge of your screen, holds up a glass, and asks: *"Did you drink water?"*
- 🎉 **Interactive Prompts**: 
  - Click **🥤 Drank Water!** to trigger a happy celebration animation and log a drink entry.
  - Click **⏰ Snooze 10m** to send the character away and get reminded in 10 minutes.
- 🍏 **macOS Menu Bar Icon**: Sits in top menu bar with quick options for triggering test reminders, toggling **Focus Mode**, opening **Hydration Stats**, and configuring settings.
- 📊 **Local SQLite Hydration Tracker**: Records daily drink count, laptop active hours, and calculates your hydration ratio (drinks per active hour).
- 🎨 **Custom Character Assets**: Drop in your own animated GIF pixel character (`walk.gif`, `ask.gif`, `happy.gif`, `exit.gif`) or use the built-in pixel companion!
- 👥 **Team Distribution Ready**: Super easy setup with a simple `./run.sh` script or standalone `.app` bundle via PyInstaller.

---

## 🚀 Quick Start (Team Setup)

### Option 1: Run via Shell Script

1. Open Terminal in the repository directory:
   ```bash
   cd /path/to/jal_lijiye
   ```
2. Run the launch script:
   ```bash
   ./run.sh
   ```
   *(The script automatically sets up the Python virtualenv, installs required packages, generates default pixel assets if missing, and launches the app!)*

---

### Option 2: Manual Installation

1. Create a Python 3 virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Generate default assets:
   ```bash
   python3 scripts/generate_assets.py
   ```
4. Run the application:
   ```bash
   python3 main.py
   ```

---

## 🎨 Customizing Your Pixel Character

You can use your own custom pixel-art animated character!

1. Prepare your animated `.gif` files (recommended resolution: 96x96 to 128x128 pixels with transparent background):
   - `walk.gif`: Character walking horizontally with a glass
   - `ask.gif`: Character standing, asking question / holding glass
   - `happy.gif`: Celebration / jumping animation
   - `exit.gif`: Character walking away off screen
2. Click the **Jal Lijiye icon** in your macOS Menu Bar -> Select **⚙️ Settings...**
3. Browse and select your custom GIF files, then click **Save Settings**!

---

## 📊 Viewing Hydration Stats

Click the **Jal Lijiye icon** in your macOS Menu Bar -> Select **📊 Hydration Stats...**

You'll see:
- Today's Total Water Drunk Count
- Active Laptop Working Hours Today
- Hydration Efficiency Ratio (Drinks per Active Hour)
- 7-Day Historical Breakdown Table

---

## 🏗️ Building Standalone macOS `.app` Bundle

To package the app into a standalone macOS `.app` for easy sharing with team members:

```bash
source venv/bin/activate
pyinstaller JalLijiye.spec
```

The resulting `JalLijiye.app` will be created inside the `dist/` directory!

---

## 🧪 Running Tests

To execute unit and GUI component integration tests:

```bash
./venv/bin/python -m pytest tests/
```

---

## 📜 License
MIT License - Created with ❤️ for teams to stay hydrated while building great software!
