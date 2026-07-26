import os
import glob
import re
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QFrame
)

class ProfileDialog(QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.setWindowTitle("User Login & Profile - Jal Lijiye")
        self.setFixedSize(440, 320)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a242b;
                color: #ffffff;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QLabel {
                color: #ffffff;
            }
            QLabel#lbl_info {
                color: #aed6f1;
                font-size: 12px;
            }
            QComboBox, QLineEdit {
                background-color: #24333e;
                color: #ffffff;
                border: 1px solid #2c3e50;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton#btn_login {
                background-color: #27ae60;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
                border-radius: 8px;
                padding: 10px 18px;
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
                padding: 10px 18px;
                border: none;
            }
            QPushButton#btn_cancel:hover {
                background-color: #95a5a6;
            }
        """)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("Who is drinking water today? 👤", self)
        h_font = QFont()
        h_font.setPointSize(16)
        h_font.setBold(True)
        header.setFont(h_font)
        layout.addWidget(header)

        # Subtitle / Info
        lbl_info = QLabel(
            "Enter your name to switch profiles. Your companion GIFs will load from:\n"
            "• assets/<name>_walk.gif\n"
            "• assets/<name>_exit.gif",
            self
        )
        lbl_info.setObjectName("lbl_info")
        layout.addWidget(lbl_info)

        # Combo box / Input line edit
        layout.addWidget(QLabel("Profile Name / Login:", self))
        
        self.combo_profile = QComboBox(self)
        self.combo_profile.setEditable(True)
        
        # Populate detected profiles from assets/
        existing_profiles = self._detect_profiles()
        current = self.config.get_current_user()
        if current not in existing_profiles:
            existing_profiles.insert(0, current)
            
        for prof in existing_profiles:
            self.combo_profile.addItem(prof)
            
        self.combo_profile.setCurrentText(current)
        layout.addWidget(self.combo_profile)

        layout.addStretch()

        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = QPushButton("Cancel", self)
        btn_cancel.setObjectName("btn_cancel")
        btn_cancel.clicked.connect(self.reject)

        btn_login = QPushButton("Switch Profile", self)
        btn_login.setObjectName("btn_login")
        btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_login.clicked.connect(self._on_switch_profile)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_login)
        layout.addLayout(btn_layout)

    def _detect_profiles(self) -> list:
        """Scans assets/ for <name>_walk.gif patterns."""
        profiles = ["Abhimanyu", "Friend", "Default"]
        if os.path.exists("assets"):
            for filepath in glob.glob("assets/*_walk.gif"):
                basename = os.path.basename(filepath)
                slug = basename[:-9]  # remove _walk.gif
                name = slug.replace('_', ' ').title()
                if name not in profiles:
                    profiles.append(name)
        return profiles

    def _on_switch_profile(self):
        name = self.combo_profile.currentText().strip()
        if not name:
            name = "Default"
        self.config.set_current_user(name)
        self.accept()
