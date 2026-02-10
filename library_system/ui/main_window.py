from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QStackedWidget, QLabel, QFrame
)
from library_system.pages.books_page import BooksPage
from library_system.pages.members_page import MembersPage
from library_system.pages.loans_page import LoansPage
from library_system.pages.reports_page import ReportsPage
from library_system.pages.dashboard_page import DashboardPage
from library_system.pages.settings_page import SettingsPage
from library_system.managers.settings_manager import SettingsManager
from library_system.ui.theme_manager import ThemeManager
from library_system.ui.sidebar import Sidebar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Apply Saved Theme
        settings = SettingsManager()
        theme = settings.get("appearance/theme", "Light")
        ThemeManager.apply_theme(theme)

        self.setWindowTitle("Sistem Manajemen Perpustakaan")
        self.resize(1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_selected.connect(self.switch_page)
        main_layout.addWidget(self.sidebar)
        
        # Right Side (Content)
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Top Bar
        self.create_top_bar()
        content_layout.addWidget(self.top_bar_frame)
        
        # Page Stack
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)
        
        main_layout.addLayout(content_layout)
        
        # Init Pages
        self.init_pages()
        
        # Default Page
        self.switch_page(0, "Dashboard")
        self.sidebar.set_active_index(0)

    def create_top_bar(self):
        self.top_bar_frame = QFrame()
        self.top_bar_frame.setFixedHeight(60)
        self.top_bar_frame.setStyleSheet("background-color: white; border-bottom: 1px solid #ECF0F1;")
        
        top_bar_layout = QHBoxLayout(self.top_bar_frame)
        top_bar_layout.setContentsMargins(24, 0, 24, 0) # Match QSS padding
        top_bar_layout.setSpacing(15)
        
        # Breadcrumb / Page Info
        self.header_label = QLabel("Overview")
        self.header_label.setStyleSheet("font-size: 16px; color: #7F8C8D;")
        top_bar_layout.addWidget(self.header_label)
        
        top_bar_layout.addStretch()
        
        user_lbl = QLabel("Admin User")
        user_lbl.setStyleSheet("color: #95A5A6;")
        top_bar_layout.addWidget(user_lbl)

    def init_pages(self):
        # 0: Dashboard
        self.dashboard_page = DashboardPage()
        # Connect navigate_to signal (inherited from BasePage)
        self.dashboard_page.navigate_to.connect(self.navigate_from_dashboard)
        self.stack.addWidget(self.dashboard_page)

        # 1: Data Buku
        self.books_page = BooksPage()
        self.stack.addWidget(self.books_page)
        
        # 2: Anggota
        self.members_page = MembersPage()
        self.stack.addWidget(self.members_page)
        
        # 3: Peminjaman
        self.loans_page = LoansPage()
        self.stack.addWidget(self.loans_page)
        
        # 4: Reports
        self.reports_page = ReportsPage()
        self.stack.addWidget(self.reports_page)
        
        # 5: Settings
        self.settings_page = SettingsPage()
        self.settings_page.settings_updated.connect(self.refresh_ui_text)
        self.stack.addWidget(self.settings_page)

    def refresh_ui_text(self):
        # Update App Titles from Settings
        settings = SettingsManager()
        name = settings.get("general/library_name", str)
        self.setWindowTitle(name)
        
        # Update Sidebar
        self.sidebar.update_title(name)

    def navigate_from_dashboard(self, index):
        # Helper to map dashboard request to sidebar click
        # Indices in stack: 0=Dash, 1=Books, 2=Members, 3=Loans, 4=Reports, 5=Settings
        page_titles = ["Dashboard", "Data Buku", "Anggota", "Peminjaman", "Laporan", "Settings"]
        if 0 <= index < len(page_titles):
            title = page_titles[index]
            self.switch_page(index, title)
            # Sync Sidebar visual state
            self.sidebar.set_active_index(index)

    def switch_page(self, index, title):
        self.stack.setCurrentIndex(index)
        self.header_label.setText(title)
        
        # Polymorphic refresh
        current_page = self.stack.widget(index)
        if hasattr(current_page, 'refresh_data'):
            current_page.refresh_data()
