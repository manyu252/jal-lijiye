import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QFileDialog, QGroupBox, QFormLayout, QLineEdit
)

class SettingsDialog(QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.setWindowTitle("Settings - Jal Lijiye")
        self.setFixedSize(480, 420)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a242b;
                color: #ffffff;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QGroupBox {
                color: #aed6f1;
                font-weight: bold;
                border: 1px solid rgba(52, 152, 219, 100);
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                background-color: #24333e;
                color: #ffffff;
                border: 1px solid #2c3e50;
                border-radius: 6px;
                padding: 6px;
            }
            QSpinBox {
                background-color: #24333e;
                color: #ffffff;
                border: 1px solid #2c3e50;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 6px 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton#btn_reset {
                background-color: #e74c3c;
            }
            QPushButton#btn_reset:hover {
                background-color: #c0392b;
            }
        """)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(16, 16, 16, 16)

        # Header
        header = QLabel("App Settings ⚙️", self)
        h_font = QFont()
        h_font.setPointSize(16)
        h_font.setBold(True)
        header.setFont(h_font)
        layout.addWidget(header)

        # Timers Group
        timer_group = QGroupBox("Reminder Timers", self)
        t_layout = QFormLayout(timer_group)
        
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

        # Assets Group
        asset_group = QGroupBox("Custom Pixel Character GIFs", self)
        a_layout = QFormLayout(asset_group)

        self.edit_walk = self._create_asset_row(a_layout, "Walk GIF:", "asset_walk_gif")
        self.edit_ask = self._create_asset_row(a_layout, "Ask GIF:", "asset_ask_gif")
        self.edit_happy = self._create_asset_row(a_layout, "Happy GIF:", "asset_happy_gif")
        
        layout.addWidget(asset_group)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_reset = QPushButton("Reset Defaults", self)
        btn_reset.setObjectName("btn_reset")
        btn_reset.clicked.connect(self._reset_defaults)
        btn_layout.addWidget(btn_reset)
        
        btn_layout.addStretch()
        
        btn_cancel = QPushButton("Cancel", self)
        btn_cancel.clicked.connect(self.reject)
        
        btn_save = QPushButton("Save Settings", self)
        btn_save.clicked.connect(self._save_settings)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)

    def _create_asset_row(self, form_layout: QFormLayout, label_text: str, config_key: str) -> QLineEdit:
        row = QHBoxLayout()
        edit = QLineEdit(self.config.get(config_key, ""), self)
        btn_browse = QPushButton("Browse...", self)
        btn_browse.clicked.connect(lambda: self._browse_gif(edit))
        row.addWidget(edit)
        row.addWidget(btn_browse)
        form_layout.addRow(label_text, row)
        return edit

    def _browse_gif(self, line_edit: QLineEdit):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Character GIF", "", "GIF Files (*.gif)")
        if file_path:
            line_edit.setText(file_path)

    def _reset_defaults(self):
        self.config.reset_defaults()
        self.spin_interval.setValue(self.config.get("reminder_interval_minutes"))
        self.spin_snooze.setValue(self.config.get("snooze_duration_minutes"))
        self.edit_walk.setText(self.config.get("asset_walk_gif"))
        self.edit_ask.setText(self.config.get("asset_ask_gif"))
        self.edit_happy.setText(self.config.get("asset_happy_gif"))

    def _save_settings(self):
        self.config.set("reminder_interval_minutes", self.spin_interval.value())
        self.config.set("snooze_duration_minutes", self.spin_snooze.value())
        self.config.set("asset_walk_gif", self.edit_walk.text())
        self.config.set("asset_ask_gif", self.edit_ask.text())
        self.config.set("asset_happy_gif", self.edit_happy.text())
        self.accept()
