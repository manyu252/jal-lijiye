import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
)

class ProfileDialog(QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.setWindowTitle("Switch User")
        self.setFixedSize(360, 180)
        
        # Ensure dialog brings itself to top and gets focus when opened from menu bar
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        self.setStyleSheet("""
            QDialog {
                background-color: #1a242b;
                color: #ffffff;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QComboBox {
                background-color: #24333e;
                color: #ffffff;
                border: 1px solid #2c3e50;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                background-color: #1a242b;
                color: #ffffff;
                selection-background-color: #3498db;
            }
            QPushButton#btn_login {
                background-color: #27ae60;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
                border-radius: 8px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton#btn_login:hover {
                background-color: #2ecc71;
            }
            QPushButton#btn_cancel {
                background-color: #7f8c8d;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
                border-radius: 8px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton#btn_cancel:hover {
                background-color: #95a5a6;
            }
        """)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("Select User", self)
        h_font = QFont()
        h_font.setPointSize(16)
        h_font.setBold(True)
        header.setFont(h_font)
        layout.addWidget(header)

        # Dropdown options: Abhimanyu, Shreya, Default
        self.combo_profile = QComboBox(self)
        
        profiles = ["Abhimanyu", "Shreya", "Default"]
        current = self.config.get_current_user()
        if current and current not in profiles:
            profiles.insert(0, current)
            
        for prof in profiles:
            self.combo_profile.addItem(prof)
            
        if current in profiles:
            self.combo_profile.setCurrentText(current)
        else:
            self.combo_profile.setCurrentIndex(0)
            
        layout.addWidget(self.combo_profile)

        layout.addStretch()

        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = QPushButton("Cancel", self)
        btn_cancel.setObjectName("btn_cancel")
        btn_cancel.clicked.connect(self.reject)

        btn_login = QPushButton("Switch", self)
        btn_login.setObjectName("btn_login")
        btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_login.clicked.connect(self._on_switch_profile)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_login)
        layout.addLayout(btn_layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.raise_()
        self.activateWindow()

    def _on_switch_profile(self):
        name = self.combo_profile.currentText().strip()
        if not name:
            name = "Default"
        self.config.set_current_user(name)
        self.accept()
