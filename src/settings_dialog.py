import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QFileDialog, QGroupBox, QFormLayout, QLineEdit
)
from src.fonts import font_poppins, font_newsreader, font_work_sans

class SettingsDialog(QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.setWindowTitle("Settings - Jal Lijiye")
        self.setFixedSize(500, 480)
        
        f_pop = font_poppins()
        f_news = font_newsreader()
        f_work = font_work_sans()
        
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #f6f4ee;
                color: #261e1b;
                font-family: "{f_work}", sans-serif;
            }}
            QGroupBox {{
                color: #414f42;
                font-family: "{f_news}", sans-serif;
                font-size: 16px;
                font-weight: bold;
                border: 1.5px solid #414f42;
                border-radius: 10px;
                margin-top: 14px;
                padding-top: 14px;
                background-color: #ffffff;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
                background-color: #f6f4ee;
                border-radius: 4px;
            }}
            QLabel {{
                color: #261e1b;
                font-family: "{f_work}", sans-serif;
                font-size: 13px;
            }}
            QLineEdit {{
                background-color: #ffffff;
                color: #261e1b;
                border: 1px solid #414f42;
                border-radius: 6px;
                padding: 6px 10px;
                font-family: "{f_work}", sans-serif;
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border: 2px solid #89301c;
            }}
            QSpinBox {{
                background-color: #ffffff;
                color: #261e1b;
                border: 1px solid #414f42;
                border-radius: 6px;
                padding: 6px;
                font-family: "{f_work}", sans-serif;
                font-size: 13px;
            }}
            QPushButton {{
                background-color: #414f42;
                color: #ffffff;
                font-family: "{f_work}", sans-serif;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 16px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #546455;
            }}
            QPushButton#btn_save {{
                background-color: #89301c;
                color: #ffffff;
            }}
            QPushButton#btn_save:hover {{
                background-color: #a23b24;
            }}
            QPushButton#btn_reset {{
                background-color: #89301c;
                color: #ffffff;
            }}
            QPushButton#btn_reset:hover {{
                background-color: #a23b24;
            }}
        """)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header (Poppins)
        header = QLabel("App Settings ⚙️", self)
        h_font = QFont(font_poppins(), 18, QFont.Weight.Bold)
        header.setFont(h_font)
        header.setStyleSheet("color: #89301c; border: none;")
        layout.addWidget(header)

        # Profile Group
        profile_group = QGroupBox("User Profile", self)
        p_layout = QFormLayout(profile_group)
        p_layout.setContentsMargins(14, 14, 14, 14)
        p_layout.setSpacing(10)
        
        self.edit_name = QLineEdit(self.config.get_user_name(), profile_group)
        self.edit_name.setPlaceholderText("Enter your name (e.g. Abhimanyu)")
        p_layout.addRow("Your Name:", self.edit_name)
        layout.addWidget(profile_group)

        # Timers Group
        timer_group = QGroupBox("Reminder Timers", self)
        t_layout = QFormLayout(timer_group)
        t_layout.setContentsMargins(14, 14, 14, 14)
        t_layout.setSpacing(10)
        
        self.spin_interval = QSpinBox(timer_group)
        self.spin_interval.setRange(1, 240)
        self.spin_interval.setSuffix(" minutes")
        self.spin_interval.setValue(self.config.get("reminder_interval_minutes", 30))
        
        self.spin_snooze = QSpinBox(timer_group)
        self.spin_snooze.setRange(1, 60)
        self.spin_snooze.setSuffix(" minutes")
        self.spin_snooze.setValue(self.config.get("snooze_duration_minutes", 10))
        
        t_layout.addRow("Reminder Frequency:", self.spin_interval)
        t_layout.addRow("Snooze Duration:", self.spin_snooze)
        layout.addWidget(timer_group)

        # Custom Animation GIFs Group
        asset_group = QGroupBox("Custom Character Animations", self)
        a_layout = QFormLayout(asset_group)
        a_layout.setContentsMargins(14, 14, 14, 14)
        a_layout.setSpacing(10)

        self.edit_walk = self._create_asset_row(a_layout, "Entry GIF (Walk-In):", "asset_walk_gif", "assets/walk.gif")
        self.edit_exit = self._create_asset_row(a_layout, "Exit GIF (Walk-Out):", "asset_exit_gif", "assets/exit.gif")
        
        layout.addWidget(asset_group)

        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_reset = QPushButton("Reset Defaults", self)
        btn_reset.setObjectName("btn_reset")
        btn_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_reset.clicked.connect(self._reset_defaults)
        btn_layout.addWidget(btn_reset)
        
        btn_layout.addStretch()
        
        btn_cancel = QPushButton("Cancel", self)
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.clicked.connect(self.reject)
        
        btn_save = QPushButton("Save Settings", self)
        btn_save.setObjectName("btn_save")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.clicked.connect(self._save_settings)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)

    def _create_asset_row(self, form_layout: QFormLayout, label_text: str, config_key: str, default_val: str) -> QLineEdit:
        row = QHBoxLayout()
        edit = QLineEdit(self.config.get(config_key, default_val), self)
        btn_browse = QPushButton("Browse...", self)
        btn_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_browse.clicked.connect(lambda: self._browse_gif(edit))
        row.addWidget(edit)
        row.addWidget(btn_browse)
        form_layout.addRow(label_text, row)
        return edit

    def _browse_gif(self, line_edit: QLineEdit):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Custom Character GIF", "", "GIF Files (*.gif)")
        if file_path:
            line_edit.setText(file_path)

    def _reset_defaults(self):
        self.config.reset_defaults()
        self.edit_name.setText(self.config.get_user_name())
        self.spin_interval.setValue(self.config.get("reminder_interval_minutes"))
        self.spin_snooze.setValue(self.config.get("snooze_duration_minutes"))
        self.edit_walk.setText(self.config.get("asset_walk_gif"))
        self.edit_exit.setText(self.config.get("asset_exit_gif"))

    def _save_settings(self):
        self.config.set_user_name(self.edit_name.text())
        self.config.set("reminder_interval_minutes", self.spin_interval.value())
        self.config.set("snooze_duration_minutes", self.spin_snooze.value())
        self.config.set("asset_walk_gif", self.edit_walk.text().strip())
        self.config.set("asset_exit_gif", self.edit_exit.text().strip())
        self.accept()
