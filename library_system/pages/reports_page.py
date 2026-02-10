from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
    QTabWidget, QTableView, QHeaderView, QAbstractItemView, QPushButton,
    QDateEdit, QFormLayout, QGroupBox, QSplitter
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor
from library_system.pages.base_page import BasePage
from library_system.services.report_service import ReportService
from library_system.managers.settings_manager import SettingsManager
from library_system.utils.export_utils import ExportUtils

class ReportsPage(BasePage):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(15)

        # Header
        # header = QLabel("Laporan Perpustakaan")
        # header.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50;")
        # self.layout.addWidget(header)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #E0E0E0; background: white; border-radius: 4px; }
            QTabBar::tab { background: #ECF0F1; padding: 10px 20px; border-radius: 4px 4px 0 0; margin-right: 2px; }
            QTabBar::tab:selected { background: white; border-bottom: 2px solid #3498DB; font-weight: bold; }
        """)
        
        self.init_summary_tab()
        self.init_loans_tab()
        self.init_overdue_tab()
        self.init_members_tab()
        self.init_books_tab()
        
        self.layout.addWidget(self.tabs)

    def init_members_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Top Borrowers
        gb = QGroupBox("Anggota Teraktif (Top 10)")
        l = QVBoxLayout(gb)
        
        self.members_table = QTableView()
        self.setup_table(self.members_table)
        self.members_model = QStandardItemModel()
        self.members_model.setHorizontalHeaderLabels(["Nama", "Kode Anggota", "Total Peminjaman"])
        self.members_table.setModel(self.members_model)
        
        l.addWidget(self.members_table)
        layout.addWidget(gb)
        
        self.tabs.addTab(tab, "Analisa Anggota")

    def init_summary_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Grid for cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)
        
        self.card_total_books = self.create_card("Total Buku", "0", "#2980B9")
        self.card_active_members = self.create_card("Anggota Aktif", "0", "#27AE60")
        self.card_active_loans = self.create_card("Sedang Dipinjam", "0", "#F39C12")
        self.card_overdue = self.create_card("Terlambat", "0", "#C0392B")
        self.card_fines = self.create_card("Est. Denda", "Rp 0", "#8E44AD")
        
        cards_layout.addWidget(self.card_total_books)
        cards_layout.addWidget(self.card_active_members)
        cards_layout.addWidget(self.card_active_loans)
        cards_layout.addWidget(self.card_overdue)
        cards_layout.addWidget(self.card_fines)
        
        layout.addLayout(cards_layout)
        layout.addStretch()
        
        self.tabs.addTab(tab, "Ringkasan")

    def create_card(self, title, value, color):
        frame = QFrame()
        frame.setStyleSheet(f"background-color: white; border: 1px solid {color}; border-radius: 8px;")
        l = QVBoxLayout(frame)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #7F8C8D; font-size: 14px;")
        
        lbl_value = QLabel(value)
        lbl_value.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        lbl_value.setAlignment(Qt.AlignRight)
        
        l.addWidget(lbl_title)
        l.addWidget(lbl_value)
        
        # Store reference to label for updates. We attach it to the frame for easy access.
        frame.value_label = lbl_value
        return frame

    def init_loans_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Filter Controls
        filter_group = QGroupBox("Filter Tanggal")
        filter_layout = QHBoxLayout(filter_group)
        
        self.date_start = QDateEdit(QDate.currentDate().addMonths(-1))
        self.date_start.setCalendarPopup(True)
        self.date_start.setDisplayFormat("yyyy-MM-dd")
        
        self.date_end = QDateEdit(QDate.currentDate())
        self.date_end.setCalendarPopup(True)
        self.date_end.setDisplayFormat("yyyy-MM-dd")
        
        btn_filter = QPushButton("Terapkan")
        btn_filter.clicked.connect(self.load_loans_report)
        
        btn_export = QPushButton("Export CSV")
        btn_export.clicked.connect(lambda: ExportUtils.export_table_to_csv(self, self.loans_table, "laporan_peminjaman.csv"))
        
        filter_layout.addWidget(QLabel("Dari:"))
        filter_layout.addWidget(self.date_start)
        filter_layout.addWidget(QLabel("Sampai:"))
        filter_layout.addWidget(self.date_end)
        filter_layout.addWidget(btn_filter)
        filter_layout.addStretch()
        filter_layout.addWidget(btn_export)
        
        layout.addWidget(filter_group)
        
        # Table
        self.loans_table = QTableView()
        self.setup_table(self.loans_table)
        self.loans_model = QStandardItemModel()
        self.loans_model.setHorizontalHeaderLabels(["ID", "Buku", "Anggota", "Tgl Pinjam", "Tgl Kembali", "Status"])
        self.loans_table.setModel(self.loans_model)
        
        layout.addWidget(self.loans_table)
        self.tabs.addTab(tab, "Laporan Peminjaman")

    def init_overdue_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Actions
        action_layout = QHBoxLayout()
        btn_export = QPushButton("Export CSV")
        btn_export.clicked.connect(lambda: ExportUtils.export_table_to_csv(self, self.overdue_table, "laporan_keterlambatan.csv"))
        action_layout.addStretch()
        action_layout.addWidget(btn_export)
        layout.addLayout(action_layout)
        
        # Table
        self.overdue_table = QTableView()
        self.setup_table(self.overdue_table)
        self.overdue_model = QStandardItemModel()
        self.overdue_model.setHorizontalHeaderLabels(["ID", "Member", "Buku", "Tgl Pinjam", "Hari Terlambat", "Est. Denda"])
        self.overdue_table.setModel(self.overdue_model)
        
        layout.addWidget(self.overdue_table)
        self.tabs.addTab(tab, "Keterlambatan")

    def init_books_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        splitter = QSplitter(Qt.Vertical)
        
        # Top: Popular Books
        gb_pop = QGroupBox("Buku Terpopuler")
        l_pop = QVBoxLayout(gb_pop)
        self.pop_table = QTableView()
        self.setup_table(self.pop_table)
        self.pop_model = QStandardItemModel()
        self.pop_model.setHorizontalHeaderLabels(["Judul", "Penulis", "Total Peminjaman"])
        self.pop_table.setModel(self.pop_model)
        l_pop.addWidget(self.pop_table)
        
        # Bottom: Never Borrowed
        gb_dead = QGroupBox("Buku Belum Pernah Dipinjam")
        l_dead = QVBoxLayout(gb_dead)
        self.dead_table = QTableView()
        self.setup_table(self.dead_table)
        self.dead_model = QStandardItemModel()
        self.dead_model.setHorizontalHeaderLabels(["Judul", "Penulis", "Kategori", "Stok"])
        self.dead_table.setModel(self.dead_model)
        l_dead.addWidget(self.dead_table)
        
        splitter.addWidget(gb_pop)
        splitter.addWidget(gb_dead)
        
        layout.addWidget(splitter)
        self.tabs.addTab(tab, "Analisa Buku")

    def setup_table(self, table):
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)

    def refresh_data(self):
        # 1. Summary Stats
        settings = SettingsManager()
        fine_per_day = settings.get("loans/fine_per_day", int)
        stats = ReportService.get_summary_stats(fine_per_day)
        
        self.card_total_books.value_label.setText(str(stats['total_books']))
        self.card_active_members.value_label.setText(str(stats['active_members']))
        self.card_active_loans.value_label.setText(str(stats['active_loans']))
        self.card_overdue.value_label.setText(str(stats['overdue_count']))
        
        # Format Currency
        fines = stats.get('total_fines', 0)
        self.card_fines.value_label.setText(f"Rp {fines:,}")
        
        # 2. Tabs Data
        self.load_loans_report()
        self.load_overdue_report(fine_per_day)
        self.load_members_report()
        self.load_books_report()

    def load_members_report(self):
        active_members = ReportService.get_active_members(10)
        self.members_model.removeRows(0, self.members_model.rowCount())
        for m in active_members:
            row = [
                QStandardItem(m['name']),
                QStandardItem(m['member_code']),
                QStandardItem(str(m['borrow_count']))
            ]
            self.members_model.appendRow(row)

    def load_loans_report(self):
        s_date = self.date_start.date().toString("yyyy-MM-dd")
        e_date = self.date_end.date().toString("yyyy-MM-dd")
        
        loans = ReportService.get_loans_by_period(s_date, e_date)
        self.loans_model.removeRows(0, self.loans_model.rowCount())
        
        for l in loans:
            row = [
                QStandardItem(str(l['id'])),
                QStandardItem(l['title']),
                QStandardItem(l['name']),
                QStandardItem(l['loan_date']),
                QStandardItem(l['return_date'] or "-"),
                QStandardItem(l['status'])
            ]
            self.loans_model.appendRow(row)

    def load_overdue_report(self, fine_per_day):
        overdue = ReportService.get_overdue_loans()
        self.overdue_model.removeRows(0, self.overdue_model.rowCount())
        
        for o in overdue:
            days = o['days_overdue']
            est_fine = days * fine_per_day
            
            row = [
                QStandardItem(str(o['id'])),
                QStandardItem(o['member_name']),
                QStandardItem(o['book_title']),
                QStandardItem(o['loan_date']),
                QStandardItem(str(days)),
                QStandardItem(f"Rp {est_fine:,}")
            ]
            # Color red
            for item in row: item.setForeground(QColor("#C0392B"))
            
            self.overdue_model.appendRow(row)

    def load_books_report(self):
        # Popular
        popular = ReportService.get_popular_books(20)
        self.pop_model.removeRows(0, self.pop_model.rowCount())
        for p in popular:
            row = [
                QStandardItem(p['title']),
                QStandardItem(p['author']),
                QStandardItem(str(p['borrow_count']))
            ]
            self.pop_model.appendRow(row)
            
        # Never Borrowed
        dead_stock = ReportService.get_never_borrowed_books()
        self.dead_model.removeRows(0, self.dead_model.rowCount())
        for d in dead_stock:
            row = [
                QStandardItem(d['title']),
                QStandardItem(d['author']),
                QStandardItem(d.get('category') or "-"),
                QStandardItem(str(d['stock']))
            ]
            self.dead_model.appendRow(row)
