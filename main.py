import sys
from pathlib import Path
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
    
    is_windows = sys.platform == 'win32'
    default_icon = "assets/icon.ico" if is_windows else "assets/icon.png"
    icon_path = Path(resolve_asset_path(config_manager.get("asset_icon", default_icon)))
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
        
    tray = WaterBuddyTray(config_manager, db_manager)
    tray.show()
    
    print("Jal Lijiye (Drinking Water Buddy) is running in the Menu Bar!")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
