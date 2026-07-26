import os
import sys
import json
import re
from typing import Any, Dict

def resolve_asset_path(relative_path: str) -> str:
    """
    Resolves relative path to assets working for both development environment
    and packaged macOS PyInstaller bundle (.app).
    """
    if not relative_path:
        return relative_path

    if hasattr(sys, "_MEIPASS"):
        # PyInstaller bundle directory
        base_path = sys._MEIPASS
    else:
        # Development environment root directory
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    full_path = os.path.join(base_path, relative_path)
    if os.path.exists(full_path):
        return full_path
    
    # Fallback to current working directory
    return os.path.abspath(relative_path)

DEFAULT_CONFIG: Dict[str, Any] = {
    "reminder_interval_minutes": 30,
    "snooze_duration_minutes": 10,
    "focus_mode": False,
    "current_user": "Default",
    "asset_walk_gif": "assets/walk.gif",
    "asset_exit_gif": "assets/exit.gif",
    "asset_icon": "assets/icon.png",
}

class ConfigManager:
    def __init__(self, config_path: str = None) -> None:
        if config_path is None:
            config_dir = os.path.expanduser("~/.jal_lijiye")
            os.makedirs(config_dir, exist_ok=True)
            self.config_path = os.path.join(config_dir, "config.json")
        else:
            self.config_path = config_path
            
        self._config: Dict[str, Any] = {}
        self.load()

    def load(self) -> Dict[str, Any]:
        """Loads configuration from JSON file or initializes defaults."""
        if os.path.exists(self.config_path):
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
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
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

    def get_current_user(self) -> str:
        """Returns the active user profile name."""
        return self.get("current_user", "Default")

    def set_current_user(self, name: str) -> None:
        """Sets active user profile name."""
        clean_name = name.strip() if name and name.strip() else "Default"
        self.set("current_user", clean_name)

    def get_user_gif(self, asset_type: str) -> str:
        """
        Returns absolute file path for user-specific GIF (e.g. assets/<name>_walk.gif)
        Fallback order:
        1. assets/<slug>_<asset_type>.gif (e.g. assets/shreya_walk.gif)
        2. assets/<slug>/<asset_type>.gif
        3. Configured default (assets/walk.gif or assets/exit.gif)
        """
        user_name = self.get_current_user()
        slug = re.sub(r'[^a-zA-Z0-9_-]', '', user_name.lower().replace(' ', '_'))
        
        if slug and slug != "default":
            candidate1 = resolve_asset_path(os.path.join("assets", f"{slug}_{asset_type}.gif"))
            candidate2 = resolve_asset_path(os.path.join("assets", slug, f"{asset_type}.gif"))
            if os.path.exists(candidate1):
                return candidate1
            if os.path.exists(candidate2):
                return candidate2

        # Default asset key
        default_key = f"asset_{asset_type}_gif"
        raw_path = self.get(default_key, f"assets/{asset_type}.gif")
        return resolve_asset_path(raw_path)

    def reset_defaults(self) -> None:
        """Resets configuration to default values."""
        self._config = DEFAULT_CONFIG.copy()
        self.save()
