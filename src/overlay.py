from pathlib import Path
from typing import Optional
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QTimer, pyqtSignal
from PyQt6.QtGui import QMovie, QGuiApplication, QFont
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
)
from src.config import resolve_asset_path
from src.fonts import get_system_font

class ComicSpeechBubble(QFrame):
    """Custom speech bubble widget with comic style border and pointing tail."""
    def __init__(self, parent=None):
        super().__init__(parent)
        app_font = get_system_font(13)
        bold_font = get_system_font(14, bold=True)
        btn_font = get_system_font(13, bold=True)

        font_family = app_font.family()

        self.setStyleSheet(f"""
            QFrame {{
                background-color: #ffffff;
                border: 2.5px solid #2c3e50;
                border-radius: 14px;
            }}
            QLabel {{
                color: #1a242b;
                font-family: "{font_family}", sans-serif;
                font-size: 14px;
                font-weight: bold;
                border: none;
                background: transparent;
            }}
            QPushButton#btn_drink {{
                background-color: #27ae60;
                color: #ffffff;
                font-family: "{font_family}", sans-serif;
                font-weight: bold;
                font-size: 13px;
                border-radius: 8px;
                padding: 6px 12px;
                border: none;
            }}
            QPushButton#btn_drink:hover {{
                background-color: #2ecc71;
            }}
            QPushButton#btn_snooze {{
                background-color: #7f8c8d;
                color: #ffffff;
                font-family: "{font_family}", sans-serif;
                font-weight: bold;
                font-size: 13px;
                border-radius: 8px;
                padding: 6px 12px;
                border: none;
            }}
            QPushButton#btn_snooze:hover {{
                background-color: #95a5a6;
            }}
        """)

class CharacterOverlayWindow(QWidget):
    drink_confirmed = pyqtSignal()
    snooze_requested = pyqtSignal()

    def __init__(self, config_manager, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.config = config_manager
        
        # Transparent, frameless, always-on-top window hints
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        
        self._init_ui()

    def _init_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(6)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        # 1. Comic Speech Bubble (Top)
        self.bubble = ComicSpeechBubble(self)
        bubble_layout = QVBoxLayout(self.bubble)
        bubble_layout.setContentsMargins(12, 10, 12, 10)
        bubble_layout.setSpacing(8)

        # Text: "Jal lijiye! 💧"
        self.lbl_title = QLabel("Jal lijiye! 💧", self.bubble)
        self.lbl_title.setWordWrap(True)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bubble_layout.addWidget(self.lbl_title)

        # Drink / Snooze buttons inside comic bubble
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(8)

        self.btn_drink = QPushButton("Drink", self.bubble)
        self.btn_drink.setObjectName("btn_drink")
        self.btn_drink.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_drink.clicked.connect(self._on_drink_clicked)

        self.btn_snooze = QPushButton("Snooze", self.bubble)
        self.btn_snooze.setObjectName("btn_snooze")
        self.btn_snooze.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_snooze.clicked.connect(self._on_snooze_clicked)

        btn_layout.addWidget(self.btn_drink)
        btn_layout.addWidget(self.btn_snooze)
        bubble_layout.addLayout(btn_layout)

        main_layout.addWidget(self.bubble)
        self.bubble.hide()  # Hidden initially while character walks

        # 2. Transparent Character GIF (Bottom)
        self.char_label = QLabel(self)
        self.char_label.setFixedSize(210, 210)
        self.char_label.setScaledContents(True)
        self.char_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.char_label.setStyleSheet("background: transparent; border: none;")
        self.char_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        main_layout.addWidget(self.char_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.movie: Optional[QMovie] = None

    def _play_gif(self, asset_key: str) -> None:
        try:
            asset_type = "exit" if "exit" in asset_key else "walk"
            gif_path = Path(resolve_asset_path(self.config.get_user_gif(asset_type)))
            
            if not gif_path.exists():
                raw_default = self.config.get(asset_key, f"assets/{asset_type}.gif")
                gif_path = Path(resolve_asset_path(raw_default))
                
            if not gif_path.exists():
                print(f"[Overlay] Asset missing: {gif_path}")
                return
                
            if self.movie:
                self.movie.stop()
                
            self.movie = QMovie(str(gif_path))
            self.char_label.setMovie(self.movie)
            self.movie.start()
        except Exception as e:
            print(f"[Overlay] Error playing GIF: {e}")

    def _get_gif_duration_ms(self) -> int:
        """Calculates total GIF duration in milliseconds. Defaults to 3000 ms if invalid."""
        if not self.movie or not self.movie.isValid():
            return 3000
        frame_count = self.movie.frameCount()
        if frame_count <= 0:
            return 3000
        total_ms = 0
        for i in range(frame_count):
            self.movie.jumpToFrame(i)
            delay = self.movie.nextFrameDelay()
            total_ms += delay if delay > 0 else 100
        self.movie.jumpToFrame(0)
        return total_ms if total_ms > 0 else 3000

    def show_reminder(self) -> None:
        """Starts the walk-in animation from configured screen corner."""
        try:
            screen = QGuiApplication.primaryScreen()
            if not screen:
                return
                
            geo = screen.availableGeometry()
            width = 330
            height = 310
            self.resize(width, height)
            
            position = self.config.get("screen_position", "bottom_left")
            
            if position == "top_left":
                start_x = geo.x() - width
                target_x = geo.x() + 30
                y_pos = geo.y() + 10
            elif position == "bottom_right":
                start_x = geo.x() + geo.width()
                target_x = geo.x() + geo.width() - width - 30
                y_pos = geo.y() + geo.height() - height - 10
            elif position == "top_right":
                start_x = geo.x() + geo.width()
                target_x = geo.x() + geo.width() - width - 30
                y_pos = geo.y() + 10
            else:  # bottom_left (Default)
                start_x = geo.x() - width
                target_x = geo.x() + 30
                y_pos = geo.y() + geo.height() - height - 10

            self.move(start_x, y_pos)
            self.bubble.hide()
            
            self._play_gif("walk")
            self.show()
            self.raise_()
            self.activateWindow()

            # Dynamic duration: If GIF < 3s, use GIF length; if GIF > 3s, cut at 3s
            gif_duration = self._get_gif_duration_ms()
            anim_duration = min(gif_duration, 3000)

            self.pos_anim = QPropertyAnimation(self, b"pos")
            self.pos_anim.setDuration(anim_duration)
            self.pos_anim.setStartValue(QPoint(start_x, y_pos))
            self.pos_anim.setEndValue(QPoint(target_x, y_pos))
            self.pos_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
            self.pos_anim.finished.connect(self._on_walk_in_finished)
            self.pos_anim.start()
        except Exception as e:
            print(f"[Overlay] Error showing reminder: {e}")

    def _on_walk_in_finished(self) -> None:
        try:
            if self.movie:
                self.movie.setPaused(True)
                
            user_name = self.config.get_current_user()
            custom_msg = self.config.get("custom_message", "").strip()
            
            if custom_msg:
                final_text = custom_msg.replace("{name}", user_name)
            else:
                if user_name and user_name.lower() != "default":
                    final_text = f"Jal lijiye, {user_name}! 💧"
                else:
                    final_text = "Jal lijiye! 💧"

            self.lbl_title.setText(final_text)
            self.bubble.show()
        except Exception as e:
            print(f"[Overlay] Error in walk-in finished: {e}")

    def _on_drink_clicked(self) -> None:
        try:
            self.bubble.hide()
            self.drink_confirmed.emit()
            self._walk_out()
        except Exception as e:
            print(f"[Overlay] Error in drink clicked: {e}")

    def _on_snooze_clicked(self) -> None:
        try:
            self.bubble.hide()
            self.snooze_requested.emit()
            self._walk_out()
        except Exception as e:
            print(f"[Overlay] Error in snooze clicked: {e}")

    def _walk_out(self) -> None:
        try:
            self.bubble.hide()
            self._play_gif("asset_exit_gif")
            screen = QGuiApplication.primaryScreen()
            if not screen:
                self.hide()
                return
                
            geo = screen.availableGeometry()
            current_pos = self.pos()
            position = self.config.get("screen_position", "bottom_left")
            
            if "right" in position:
                end_x = geo.x() + geo.width() + 10
            else:
                end_x = geo.x() - self.width() - 10
            
            # Dynamic duration for exit GIF
            gif_duration = self._get_gif_duration_ms()
            anim_duration = min(gif_duration, 2500)

            self.pos_anim = QPropertyAnimation(self, b"pos")
            self.pos_anim.setDuration(anim_duration)
            self.pos_anim.setStartValue(current_pos)
            self.pos_anim.setEndValue(QPoint(end_x, current_pos.y()))
            self.pos_anim.setEasingCurve(QEasingCurve.Type.InQuad)
            self.pos_anim.finished.connect(self.hide)
            self.pos_anim.start()
        except Exception as e:
            print(f"[Overlay] Error in walk out: {e}")
            self.hide()
