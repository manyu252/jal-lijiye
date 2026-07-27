import sys
import json
import re
from pathlib import Path
from typing import Any, Dict, Optional, Union

is_windows = sys.platform == 'win32'
default_icon_asset = "assets/icon.ico" if is_windows else "assets/icon.png"

def resolve_asset_path(relative_path: Union[str, Path]) -> str:
    """
    Resolves relative path to assets working for both development environment
    and packaged PyInstaller bundle (.app / .exe).
    """
    if not relative_path:
        return str(relative_path)

    rel_path = Path(relative_path)
    if hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent
    
    full_path = base_path / rel_path
    if full_path.exists():
        return str(full_path)
    
    # Fallback to absolute or current working directory path
    if rel_path.exists():
        return str(rel_path.resolve())
        
    return str(rel_path)

DEFAULT_CONFIG: Dict[str, Any] = {
    "user_name": "Abhimanyu",
    "reminder_interval_minutes": 30,
    "snooze_duration_minutes": 10,
    "focus_mode": False,
    "asset_walk_gif": "assets/walk.gif",
    "asset_exit_gif": "assets/exit.gif",
    "asset_icon": default_icon_asset,
}

class ConfigManager:
    def __init__(self, config_path: Optional[Union[str, Path]] = None) -> None:
        if config_path is None:
            config_dir = Path.home() / ".jal_lijiye"
            config_dir.mkdir(parents=True, exist_ok=True)
            self.config_path = config_dir / "config.json"
        else:
            self.config_path = Path(config_path)
            
        self._config: Dict[str, Any] = {}
        self.load()

    def load(self) -> Dict[str, Any]:
        """Loads configuration from JSON file or initializes defaults."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self._config = {**DEFAULT_CONFIG, **loaded}
            except Exception as e:
                print(f"[ConfigManager] Error reading config, using defaults: {e}")
                self._config = DEFAULT_CONFIG.copy()
        else:
            self._config = DEFAULT_CONFIG.copy()
            self.save()
        return self._config

    def save(self) -> None:
        """Saves current configuration to JSON file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=4)
        except Exception as e:
            print(f"[ConfigManager] Error saving config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Gets a configuration value."""
        return self._config.get(key, default if default is not None else DEFAULT_CONFIG.get(key))

    def set(self, key: str, value: Any) -> None:
        """Sets a configuration value and saves to disk."""
        self._config[key] = value
        self.save()

    def get_user_name(self) -> str:
        """Returns the configured user name."""
        return self.get("user_name", self.get("current_user", "Abhimanyu")).strip()

    def set_user_name(self, name: str) -> None:
        """Sets user name."""
        clean_name = name.strip() if name else ""
        self.set("user_name", clean_name)
        self.set("current_user", clean_name)

    def get_current_user(self) -> str:
        """Alias for get_user_name for compatibility."""
        return self.get_user_name()

    def set_current_user(self, name: str) -> None:
        """Alias for set_user_name for compatibility."""
        self.set_user_name(name)

    def get_user_gif(self, asset_type: str) -> str:
        """
        Returns file path for user-configured entry ('walk') or exit ('exit') GIF.
        Falls back to configured asset path or default assets/walk.gif / assets/exit.gif.
        """
        asset_key = f"asset_{asset_type}_gif"
        default_val = f"assets/{asset_type}.gif"
        configured_path = self.get(asset_key, default_val)
        
        # Check if absolute/direct file exists
        direct_path = Path(configured_path)
        if direct_path.exists():
            return str(direct_path)
            
        # Fallback to resolved asset path
        return resolve_asset_path(configured_path)

    def reset_defaults(self) -> None:
        """Resets configuration to default values."""
        self._config = DEFAULT_CONFIG.copy()
        self.save()
