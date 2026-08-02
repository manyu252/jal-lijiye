from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QSpinBox,
    QPushButton, QFileDialog, QGroupBox, QFormLayout, QLineEdit,
    QRadioButton, QButtonGroup
)
from src.fonts import get_system_font

class SettingsDialog(QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.setWindowTitle("Settings - Jal Lijiye")
        self.setFixedSize(520, 560)
        
        app_font = get_system_font(13)
        bold_font = get_system_font(14, bold=True)
        title_font = get_system_font(16, bold=True)
        font_family = app_font.family()

        self.setStyleSheet(f"""
            QDialog {{
                background-color: #1a242b;
                color: #ffffff;
                font-family: "{font_family}", sans-serif;
            }}
            QGroupBox {{
                color: #aed6f1;
                font-weight: bold;
                border: 1px solid rgba(52, 152, 219, 100);
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
            QLabel {{
                color: #ffffff;
            }}
            QLineEdit {{
                background-color: #24333e;
                color: #ffffff;
                border: 1px solid #2c3e50;
                border-radius: 6px;
                padding: 6px;
            }}
            QSpinBox {{
                background-color: #24333e;
                color: #ffffff;
                border: 1px solid #2c3e50;
                border-radius: 6px;
                padding: 6px;
            }}
            QRadioButton {{
                color: #ffffff;
                font-size: 13px;
            }}
            QPushButton {{
                background-color: #3498db;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 6px 12px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
            QPushButton#btn_reset {{
                background-color: #e74c3c;
            }}
            QPushButton#btn_reset:hover {{
                background-color: #c0392b;
            }}
        """)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        # Header
        header = QLabel("App Settings ⚙️", self)
        h_font = get_system_font(16, bold=True)
        header.setFont(h_font)
        layout.addWidget(header)

        # 1. Reminder Timers & Speech Text Group
        timer_group = QGroupBox("Reminder Timers & Message", self)
        t_layout = QFormLayout(timer_group)
        
        self.spin_interval = QSpinBox(timer_group)
        self.spin_interval.setRange(1, 240)
        self.spin_interval.setSuffix(" minutes")
        self.spin_interval.setValue(self.config.get("reminder_interval_minutes", 30))
        
        self.spin_snooze = QSpinBox(timer_group)
        self.spin_snooze.setRange(1, 60)
        self.spin_snooze.setSuffix(" minutes")
        self.spin_snooze.setValue(self.config.get("snooze_duration_minutes", 10))
        
        self.edit_message = QLineEdit(timer_group)
        self.edit_message.setMaxLength(100)
        self.edit_message.setPlaceholderText("Jal lijiye, {name}! 💧")
        self.edit_message.setText(self.config.get("custom_message", ""))
        
        t_layout.addRow("Reminder Frequency:", self.spin_interval)
        t_layout.addRow("Snooze Duration:", self.spin_snooze)
        t_layout.addRow("Speech Bubble Text:", self.edit_message)
        layout.addWidget(timer_group)

        # 2. Screen Position Group (Exclusive Selection)
        pos_group = QGroupBox("Screen Corner Position", self)
        pos_layout = QGridLayout()
        
        self.pos_button_group = QButtonGroup(self)
        self.pos_button_group.setExclusive(True)
        
        self.radio_bl = QRadioButton("Bottom Left (Default)", pos_group)
        self.radio_tl = QRadioButton("Top Left", pos_group)
        self.radio_br = QRadioButton("Bottom Right", pos_group)
        self.radio_tr = QRadioButton("Top Right", pos_group)
        
        self.pos_button_group.addButton(self.radio_bl, 1)
        self.pos_button_group.addButton(self.radio_tl, 2)
        self.pos_button_group.addButton(self.radio_br, 3)
        self.pos_button_group.addButton(self.radio_tr, 4)
        
        current_pos = self.config.get("screen_position", "bottom_left")
        if current_pos == "top_left":
            self.radio_tl.setChecked(True)
        elif current_pos == "bottom_right":
            self.radio_br.setChecked(True)
        elif current_pos == "top_right":
            self.radio_tr.setChecked(True)
        else:
            self.radio_bl.setChecked(True)
            
        pos_layout.addWidget(self.radio_bl, 0, 0)
        pos_layout.addWidget(self.radio_tl, 0, 1)
        pos_layout.addWidget(self.radio_br, 1, 0)
        pos_layout.addWidget(self.radio_tr, 1, 1)
        pos_group.setLayout(pos_layout)
        layout.addWidget(pos_group)

        # 3. Custom Assets Group
        asset_group = QGroupBox("Custom Character GIFs", self)
        a_layout = QFormLayout(asset_group)
        self.edit_walk = self._create_asset_row(a_layout, "Walk-In GIF:", "asset_walk_gif")
        self.edit_exit = self._create_asset_row(a_layout, "Walk-Out GIF:", "asset_exit_gif")
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
        self.edit_message.setText(self.config.get("custom_message", ""))
        self.radio_bl.setChecked(True)
        self.edit_walk.setText(self.config.get("asset_walk_gif"))
        self.edit_exit.setText(self.config.get("asset_exit_gif"))

    def _get_selected_position(self) -> str:
        if self.radio_tl.isChecked():
            return "top_left"
        elif self.radio_br.isChecked():
            return "bottom_right"
        elif self.radio_tr.isChecked():
            return "top_right"
        return "bottom_left"

    def _save_settings(self):
        self.config.set("reminder_interval_minutes", self.spin_interval.value())
        self.config.set("snooze_duration_minutes", self.spin_snooze.value())
        self.config.set("custom_message", self.edit_message.text().strip())
        self.config.set("screen_position", self._get_selected_position())
        self.config.set("asset_walk_gif", self.edit_walk.text())
        self.config.set("asset_exit_gif", self.edit_exit.text())
        self.accept()
