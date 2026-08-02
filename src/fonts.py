from typing import Dict
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import QFontDatabase, QFont

_FONT_CACHE: Dict[str, str] = {}

def get_font_family(preferred_family: str, fallback_family: str = "Helvetica Neue") -> str:
    """
    Returns preferred_family if installed on the host system QFontDatabase,
    otherwise returns fallback_family to prevent Qt 198ms missing font warnings.
    Safely checks QCoreApplication.instance() before querying QFontDatabase.
    """
    if preferred_family in _FONT_CACHE:
        return _FONT_CACHE[preferred_family]

    if QCoreApplication.instance() is not None:
        try:
            families = QFontDatabase.families()
            if preferred_family in families:
                _FONT_CACHE[preferred_family] = preferred_family
                return preferred_family
            else:
                _FONT_CACHE[preferred_family] = fallback_family
                return fallback_family
        except Exception:
            pass

    return preferred_family

def font_poppins() -> str:
    return get_font_family("Poppins", "Helvetica Neue")

def font_newsreader() -> str:
    return get_font_family("Newsreader", "Georgia")

def font_work_sans() -> str:
    return get_font_family("Work Sans", "Helvetica Neue")

def get_system_font(point_size: int = 13, bold: bool = False) -> QFont:
    """Returns a native system QFont with preferred fallbacks."""
    family = get_font_family("Helvetica Neue", "Segoe UI")
    font = QFont(family, point_size)
    font.setBold(bold)
    return font

