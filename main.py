import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from src.config import ConfigManager
from src.db import DatabaseManager
from src.tray import WaterBuddyTray

def main():
    # Pass explicit config and DB paths within local environment or default
    config_manager = ConfigManager()
    db_manager = DatabaseManager()
    
    app = QApplication(sys.argv)
    app.setApplicationName("Jal Lijiye")
    app.setOrganizationName("JalLijiye")
    
    # Crucial for macOS tray apps so closing dialogs doesn't terminate app
    app.setQuitOnLastWindowClosed(False)
    
    icon_path = config_manager.get("asset_icon", "assets/icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        
    tray = WaterBuddyTray(config_manager, db_manager)
    tray.show()
    
    print("Jal Lijiye (macOS Drinking Water Buddy) is running in the Menu Bar!")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
