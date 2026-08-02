import os
import tempfile
import pytest
from PyQt6.QtCore import Qt
from src.config import ConfigManager
from src.overlay import CharacterOverlayWindow

def test_overlay_creation(qtbot):
    with tempfile.TemporaryDirectory() as tmpdir:
        cfg = ConfigManager(os.path.join(tmpdir, "config.json"))
        overlay = CharacterOverlayWindow(cfg)
        qtbot.addWidget(overlay)
        
        assert overlay.windowFlags() & Qt.WindowType.FramelessWindowHint
        assert overlay.windowFlags() & Qt.WindowType.WindowStaysOnTopHint

def test_overlay_signals(qtbot):
    with tempfile.TemporaryDirectory() as tmpdir:
        cfg = ConfigManager(os.path.join(tmpdir, "config.json"))
        overlay = CharacterOverlayWindow(cfg)
        qtbot.addWidget(overlay)
        
        with qtbot.waitSignal(overlay.drink_confirmed, timeout=1000):
            overlay._on_drink_clicked()

def test_overlay_snooze_signal(qtbot):
    with tempfile.TemporaryDirectory() as tmpdir:
        cfg = ConfigManager(os.path.join(tmpdir, "config.json"))
        overlay = CharacterOverlayWindow(cfg)
        qtbot.addWidget(overlay)
        
        with qtbot.waitSignal(overlay.snooze_requested, timeout=1000):
            overlay._on_snooze_clicked()

def test_overlay_custom_message_and_screen_positions(qtbot):
    with tempfile.TemporaryDirectory() as tmpdir:
        cfg = ConfigManager(os.path.join(tmpdir, "config.json"))
        cfg.set("custom_message", "Time to hydrate, {name}! 💧")
        cfg.set_current_user("Abhimanyu")
        
        for pos in ["bottom_left", "top_left", "bottom_right", "top_right"]:
            cfg.set("screen_position", pos)
            overlay = CharacterOverlayWindow(cfg)
            qtbot.addWidget(overlay)
            overlay.show_reminder()
            overlay._on_walk_in_finished()
            
            assert overlay.lbl_title.text() == "Time to hydrate, Abhimanyu! 💧"
