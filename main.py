import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from src.config import ConfigManager, resolve_asset_path
from src.db import DatabaseManager
from src.tray import WaterBuddyTray

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Jal Lijiye")
    app.setOrganizationName("JalLijiye")
    app.setQuitOnLastWindowClosed(False)
    
    config_manager = ConfigManager()
    db_manager = DatabaseManager()
    
    icon_path = resolve_asset_path(config_manager.get("asset_icon", "assets/icon.png"))
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        
    tray = WaterBuddyTray(config_manager, db_manager)
    tray.show()
    
    print("Jal Lijiye (Drinking Water Buddy) is running in the Menu Bar!")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
