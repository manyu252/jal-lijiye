import os
from typing import Optional
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
)
from src.fonts import font_poppins, font_newsreader, font_work_sans

class StatsDialog(QDialog):
    def __init__(self, db_manager, user_name: Optional[str] = None, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.user_name = user_name
        
        title_user = f" ({user_name})" if user_name else ""
        self.setWindowTitle(f"Hydration Statistics{title_user} - Jal Lijiye")
        self.setFixedSize(540, 460)
        
        f_pop = font_poppins()
        f_news = font_newsreader()
        f_work = font_work_sans()
        
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #f6f4ee;
                color: #261e1b;
                font-family: "{f_work}", sans-serif;
            }}
            QFrame.card {{
                background-color: #ffffff;
                border-radius: 10px;
                border: 1.5px solid #414f42;
                padding: 10px;
            }}
            QLabel.val {{
                color: #89301c;
                font-family: "{f_pop}", sans-serif;
                font-size: 22px;
                font-weight: bold;
            }}
            QLabel.lbl {{
                color: #414f42;
                font-family: "{f_news}", sans-serif;
                font-size: 12px;
                font-weight: bold;
            }}
            QTableWidget {{
                background-color: #ffffff;
                color: #261e1b;
                gridline-color: #eae6dc;
                border-radius: 8px;
                border: 1px solid #414f42;
                font-family: "{f_work}", sans-serif;
                font-size: 13px;
            }}
            QHeaderView::section {{
                background-color: #414f42;
                color: #ffffff;
                font-family: "{f_work}", sans-serif;
                font-weight: bold;
                padding: 6px;
                border: none;
            }}
            QPushButton {{
                background-color: #89301c;
                color: white;
                font-family: "{f_work}", sans-serif;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 18px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #a23b24;
            }}
        """)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header (Poppins)
        user_header = f" for {self.user_name}" if self.user_name else ""
        header = QLabel(f"Hydration Dashboard{user_header} 📊", self)
        h_font = QFont(font_poppins(), 18, QFont.Weight.Bold)
        header.setFont(h_font)
        header.setStyleSheet("color: #89301c; border: none;")
        layout.addWidget(header)

        # Top 3 Metric Cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        # 1. Drink Count Card
        card1 = QFrame(self)
        card1.setProperty("class", "card")
        c1_layout = QVBoxLayout(card1)
        val1 = QLabel(f"{self.db.get_today_drink_count(self.user_name)} 💧", card1)
        val1.setProperty("class", "val")
        lbl1 = QLabel("Glasses Drunk Today", card1)
        lbl1.setProperty("class", "lbl")
        c1_layout.addWidget(val1)
        c1_layout.addWidget(lbl1)
        cards_layout.addWidget(card1)

        # 2. Active Hours Card
        card2 = QFrame(self)
        card2.setProperty("class", "card")
        c2_layout = QVBoxLayout(card2)
        val2 = QLabel(f"{self.db.get_today_active_hours(self.user_name)} hrs", card2)
        val2.setProperty("class", "val")
        lbl2 = QLabel("Active Laptop Time", card2)
        lbl2.setProperty("class", "lbl")
        c2_layout.addWidget(val2)
        c2_layout.addWidget(lbl2)
        cards_layout.addWidget(card2)

        # 3. Ratio Card
        card3 = QFrame(self)
        card3.setProperty("class", "card")
        c3_layout = QVBoxLayout(card3)
        val3 = QLabel(f"{self.db.get_today_hydration_ratio(self.user_name)} /hr", card3)
        val3.setProperty("class", "val")
        lbl3 = QLabel("Hydration Ratio", card3)
        lbl3.setProperty("class", "lbl")
        c3_layout.addWidget(val3)
        c3_layout.addWidget(lbl3)
        cards_layout.addWidget(card3)

        layout.addLayout(cards_layout)

        # History Title (Newsreader 14pt)
        hist_lbl = QLabel("Past 7 Days History", self)
        hist_font = QFont(font_newsreader(), 14, QFont.Weight.Bold)
        hist_lbl.setFont(hist_font)
        hist_lbl.setStyleSheet("color: #414f42;")
        layout.addWidget(hist_lbl)

        # Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Glasses Drunk", "Active Hours", "Hydration Ratio"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        self._populate_table()
        layout.addWidget(self.table)

        # Close Button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_close = QPushButton("Close", self)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)

    def _populate_table(self):
        summary = self.db.get_daily_summary(7, user_name=self.user_name)
        self.table.setRowCount(len(summary))
        for row_idx, item in enumerate(summary):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(item["date"])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(f"{item['drinks']} 💧"))
            self.table.setItem(row_idx, 2, QTableWidgetItem(f"{item['active_hours']} hrs"))
            self.table.setItem(row_idx, 3, QTableWidgetItem(f"{item['hydration_ratio']} /hr"))
