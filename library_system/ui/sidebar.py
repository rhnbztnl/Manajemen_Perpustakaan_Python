from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel, QWidget
from PySide6.QtCore import Qt, Signal
from library_system.managers.settings_manager import SettingsManager

class Sidebar(QFrame):
    """
    Sidebar component containing navigation buttons and app title.
    """
    page_selected = Signal(int, str) # Emits (index, title) when a button is clicked

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(250)
        self.setObjectName("sidebar")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # App Title
        self.app_title_lbl = QLabel(SettingsManager().get("general/library_name", str).upper())
        # Styling allows it to be targeted by QSS if needed, or we can use the theme manager later
        self.layout.addWidget(self.app_title_lbl)
        
        # Navigation Buttons
        self.btn_labels = ["Dashboard", "Data Buku", "Anggota", "Peminjaman", "Laporan", "Settings"]
        self.sidebar_btns = []
        
        for i, label in enumerate(self.btn_labels):
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            
            # Connect click with index capture
            # We use a closure or partial to capture 'i' and 'label'
            btn.clicked.connect(lambda checked=False, idx=i, title=label: self.on_btn_click(idx, title))
            
            self.layout.addWidget(btn)
            self.sidebar_btns.append(btn)
            
        self.layout.addStretch()

    def on_btn_click(self, index, title):
        # Update UI state (exclusive check)
        self.set_active_index(index)
        # Emit signal
        self.page_selected.emit(index, title)

    def set_active_index(self, index):
        """Allows external control to set the active button (e.g. from Dashboard shortcuts)"""
        if 0 <= index < len(self.sidebar_btns):
            for btn in self.sidebar_btns:
                btn.setChecked(False)
            self.sidebar_btns[index].setChecked(True)

    def update_title(self, title):
        self.app_title_lbl.setText(title.upper())
