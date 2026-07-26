import os
from typing import Optional
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QTimer, pyqtSignal
from PyQt6.QtGui import QMovie, QGuiApplication, QFont
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
)

class ComicSpeechBubble(QFrame):
    """Custom speech bubble widget with comic style border and pointing tail."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 2.5px solid #2c3e50;
                border-radius: 14px;
            }
            QLabel {
                color: #1a242b;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 15px;
                font-weight: bold;
                border: none;
                background: transparent;
            }
            QPushButton#btn_drink {
                background-color: #27ae60;
                color: #ffffff;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-weight: bold;
                font-size: 13px;
                border-radius: 8px;
                padding: 6px 12px;
                border: none;
            }
            QPushButton#btn_drink:hover {
                background-color: #2ecc71;
            }
            QPushButton#btn_snooze {
                background-color: #7f8c8d;
                color: #ffffff;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-weight: bold;
                font-size: 13px;
                border-radius: 8px;
                padding: 6px 12px;
                border: none;
            }
            QPushButton#btn_snooze:hover {
                background-color: #95a5a6;
            }
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
        asset_type = "exit" if "exit" in asset_key else "walk"
        gif_path = self.config.get_user_gif(asset_type)
        
        if not os.path.exists(gif_path):
            # Fallback to config or default assets
            gif_path = self.config.get(asset_key, f"assets/{asset_type}.gif")
            
        if not os.path.exists(gif_path):
            print(f"[Overlay] Asset missing: {gif_path}")
            return
            
        if self.movie:
            self.movie.stop()
            
        self.movie = QMovie(gif_path)
        self.char_label.setMovie(self.movie)
        self.movie.start()

    def show_reminder(self) -> None:
        """Starts the walk-in animation from the far left screen edge."""
        screen = QGuiApplication.primaryScreen()
        if not screen:
            return
            
        geo = screen.availableGeometry()
        
        width = 330
        height = 310
        self.resize(width, height)
        
        # Start at left screen boundary
        start_x = geo.x()
        target_x = geo.x() + 30  # Resting position near left edge
        y_pos = geo.y() + geo.height() - height - 10  # Bottom of screen
        
        self.move(start_x, y_pos)
        self.bubble.hide()  # Speech bubble hidden during walk-in
        
        self._play_gif("walk")
        self.show()
        self.raise_()
        self.activateWindow()

        # Slide in from left screen edge to target_x
        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setDuration(3000)  # 3 seconds walk-in
        self.pos_anim.setStartValue(QPoint(start_x, y_pos))
        self.pos_anim.setEndValue(QPoint(target_x, y_pos))
        self.pos_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.pos_anim.finished.connect(self._on_walk_in_finished)
        self.pos_anim.start()

    def _on_walk_in_finished(self) -> None:
        # Pause/freeze movie on last frame of walk-in video
        if self.movie:
            self.movie.setPaused(True)
            
        # Update personalized title
        user_name = self.config.get_current_user()
        if user_name and user_name.lower() != "default":
            self.lbl_title.setText(f"Jal lijiye, {user_name}! 💧")
        else:
            self.lbl_title.setText("Jal lijiye! 💧")

        # Pop up comic speech bubble above character
        self.bubble.show()

    def _on_drink_clicked(self) -> None:
        self.bubble.hide()
        self.drink_confirmed.emit()
        self._walk_out()

    def _on_snooze_clicked(self) -> None:
        self.bubble.hide()
        self.snooze_requested.emit()
        self._walk_out()

    def _walk_out(self) -> None:
        self.bubble.hide()
        self._play_gif("asset_exit_gif")
        screen = QGuiApplication.primaryScreen()
        if not screen:
            self.hide()
            return
            
        geo = screen.availableGeometry()
        current_pos = self.pos()
        end_x = geo.x() - self.width() - 10
        
        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setDuration(2500)  # 2.5 seconds walk-out
        self.pos_anim.setStartValue(current_pos)
        self.pos_anim.setEndValue(QPoint(end_x, current_pos.y()))
        self.pos_anim.setEasingCurve(QEasingCurve.Type.InQuad)
        self.pos_anim.finished.connect(self.hide)
        self.pos_anim.start()
