from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
    QTableView, QHeaderView, QAbstractItemView, QPushButton, QGridLayout, QListWidget
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor
from library_system.services.dashboard_service import DashboardService

class DashCard(QFrame):
    clicked = Signal()

    def __init__(self, title, value, icon_char="📦", color="#3498DB"):
        super().__init__()
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("dashCard")
        self.setObjectName("dashCard")
        # Styles moved to ThemeManager
        
        layout = QVBoxLayout(self)
        
        # Header (Icon + Title)
        header_layout = QHBoxLayout()
        icon = QLabel(icon_char)
        icon.setStyleSheet(f"font-size: 24px; color: {color};")
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #7F8C8D; font-size: 14px; font-weight: 500;")
        
        header_layout.addWidget(icon)
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        
        self.lbl_value = QLabel(str(value))
        self.lbl_value.setStyleSheet(f"color: {color}; font-size: 32px; font-weight: bold;")
        self.lbl_value.setAlignment(Qt.AlignRight)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.lbl_value)
    
    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)
    
    def update_value(self, value):
        self.lbl_value.setText(str(value))

from library_system.pages.base_page import BasePage

class DashboardPage(BasePage):
    # Signal to request page switch: index, tab_name (optional)
    # navigate_to = Signal(int) # Inherited from BasePage 

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(20)

        # -- Header --
        header_lbl = QLabel("Dashboard Overview")
        header_lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50;")
        self.layout.addWidget(header_lbl)

        # -- KPI Cards --
        cards_layout = QHBoxLayout()
        self.card_books = DashCard("Buku Tersedia", "0", "📚", "#3498DB")
        self.card_borrowed = DashCard("Sedang Dipinjam", "0", "📖", "#E67E22")
        self.card_overdue = DashCard("Terlambat", "0", "⚠️", "#E74C3C")
        self.card_members = DashCard("Anggota Aktif", "0", "👥", "#2ECC71")
        
        # Navigate on click (Optional Logic)
        self.card_books.clicked.connect(lambda: self.navigate_to.emit(1)) # Data Buku
        self.card_borrowed.clicked.connect(lambda: self.navigate_to.emit(2)) # Peminjaman
        self.card_overdue.clicked.connect(lambda: self.navigate_to.emit(2)) # Peminjaman (or Reports)
        self.card_members.clicked.connect(lambda: self.navigate_to.emit(1)) # Members
        
        cards_layout.addWidget(self.card_books)
        cards_layout.addWidget(self.card_borrowed)
        cards_layout.addWidget(self.card_overdue)
        cards_layout.addWidget(self.card_members)
        
        self.layout.addLayout(cards_layout)

        # -- Middle Section: Urgent Tasks & Activity --
        mid_layout = QHBoxLayout()
        
        # Left: Urgent Tasks
        urgent_frame = QFrame()
        urgent_frame.setObjectName("contentFrame")
        # urgent_frame.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #E0E0E0;")
        u_layout = QVBoxLayout(urgent_frame)
        u_lbl = QLabel("🔥 Perlu Perhatian (Terlambat)")
        u_lbl.setStyleSheet("font-weight: bold; font-size: 16px; color: #C0392B;")
        u_layout.addWidget(u_lbl)
        
        self.urgent_table = QTableView()
        self.urgent_table.verticalHeader().setVisible(False)
        self.urgent_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.urgent_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.urgent_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setup_urgent_model()
        
        u_layout.addWidget(self.urgent_table)
        mid_layout.addWidget(urgent_frame, stretch=2)
        
        # Right: Recent Activity
        activity_frame = QFrame()
        activity_frame.setObjectName("contentFrame")
        # activity_frame.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #E0E0E0;")
        a_layout = QVBoxLayout(activity_frame)
        a_lbl = QLabel("🕒 Aktivitas Terakhir")
        a_lbl.setStyleSheet("font-weight: bold; font-size: 16px; color: #2C3E50;")
        a_layout.addWidget(a_lbl)
        
        self.activity_list = QListWidget()
        self.activity_list.setStyleSheet("border: none;")
        a_layout.addWidget(self.activity_list)
        
        mid_layout.addWidget(activity_frame, stretch=1)
        self.layout.addLayout(mid_layout)

        # -- Shortcuts --
        shortcuts_layout = QHBoxLayout()
        shortcuts_layout.setSpacing(10)
        
        btn_loan = QPushButton("+ Pinjam Buku")
        btn_loan.setStyleSheet("background-color: #3498DB; color: white; padding: 10px; border-radius: 5px;")
        btn_loan.clicked.connect(lambda: self.navigate_to.emit(2)) # To Loans
        
        btn_book = QPushButton("+ Data Buku")
        btn_book.setStyleSheet("background-color: #2ECC71; color: white; padding: 10px; border-radius: 5px;")
        btn_book.clicked.connect(lambda: self.navigate_to.emit(0)) # To Books
        
        btn_member = QPushButton("+ Anggota Baru")
        btn_member.setStyleSheet("background-color: #9B59B6; color: white; padding: 10px; border-radius: 5px;")
        btn_member.clicked.connect(lambda: self.navigate_to.emit(1)) # To Members
        
        shortcuts_layout.addWidget(btn_loan)
        shortcuts_layout.addWidget(btn_book)
        shortcuts_layout.addWidget(btn_member)
        shortcuts_layout.addStretch()
        
        self.layout.addLayout(shortcuts_layout)

        # Load Data
        self.refresh_data()

    def setup_urgent_model(self):
        self.urgent_model = QStandardItemModel()
        self.urgent_model.setHorizontalHeaderLabels(["Anggota", "Buku", "Jatuh Tempo"])
        self.urgent_table.setModel(self.urgent_model)

    def refresh_data(self):
        # 1. KPI Stats
        stats = DashboardService.get_kpi_stats()
        self.card_books.update_value(stats['books_available'])
        self.card_borrowed.update_value(stats['books_borrowed'])
        self.card_overdue.update_value(stats['total_overdue'])
        self.card_members.update_value(stats['active_members'])
        
        # 2. Urgent Tasks
        tasks = DashboardService.get_urgent_tasks()
        self.urgent_model.removeRows(0, self.urgent_model.rowCount())
        for t in tasks:
            row = [
                QStandardItem(t['member_name']),
                QStandardItem(t['book_title']),
                QStandardItem(str(t['due_date']))
            ]
            for item in row: item.setForeground(QColor("#C0392B")) # Red text
            self.urgent_model.appendRow(row)
            
        # 3. Recent Activity
        activity = DashboardService.get_recent_activity()
        self.activity_list.clear()
        for a in activity:
            icon = "📤" if a['type'] == 'Pinjam' else "📥"
            text = f"{icon} {a['member_name']} {a['type']} '{a['book_title']}' ({a['activity_date']})"
            self.activity_list.addItem(text)
