import shutil
import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QPushButton, QGroupBox, QFileDialog, QMessageBox, QTabWidget,
    QLineEdit, QSpinBox, QCheckBox, QFormLayout
)
from PySide6.QtCore import Qt, Signal
from library_system.managers.settings_manager import SettingsManager
from library_system.database.db import get_db_path
from pathlib import Path

from library_system.pages.base_page import BasePage

class SettingsPage(BasePage):
    settings_updated = Signal()

    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(20)

        # Title
        header = QLabel("Pengaturan")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50;")
        self.layout.addWidget(header)

        # Tabs
        self.tabs = QTabWidget()
        # Tabs
        self.tabs = QTabWidget()
        # Styles handled by ThemeManager

        self.init_general_tab()
        self.init_appearance_tab()
        self.tabs.setTabEnabled(1, False) # Disable Appearance tab as requested
        self.init_loans_tab()
        self.init_system_tab()

        self.layout.addWidget(self.tabs)
        
        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.save_btn = QPushButton("Simpan Perubahan")
        self.save_btn.setObjectName("primary-btn")
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_settings)
        
        btn_layout.addWidget(self.save_btn)
        self.layout.addLayout(btn_layout)

    def init_general_tab(self):
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.inp_lib_name = QLineEdit(self.settings.get("general/library_name"))
        self.inp_location = QLineEdit(self.settings.get("general/location"))
        self.inp_date_fmt = QComboBox()
        self.inp_date_fmt.addItems(["dd/MM/yyyy", "yyyy-MM-dd", "MM/dd/yyyy"])
        self.inp_date_fmt.setCurrentText(self.settings.get("general/date_format"))

        layout.addRow("Nama Perpustakaan:", self.inp_lib_name)
        layout.addRow("Lokasi / Instansi:", self.inp_location)
        layout.addRow("Format Tanggal:", self.inp_date_fmt)
        
        self.tabs.addTab(tab, "Umum")

    def init_appearance_tab(self):
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.inp_theme = QComboBox()
        self.inp_theme.addItems(["Light", "Dark"])
        
        # Load via ThemeManager
        from library_system.ui.theme_manager import ThemeManager
        current_theme_code = ThemeManager.load_theme() # 'light', 'dark'
        
        # Map code to Display Name
        display_name = "Dark" if current_theme_code == "dark" else "Light"
        
        self.inp_theme.setCurrentText(display_name)
        
        # Connect signal
        self.inp_theme.currentTextChanged.connect(self.on_theme_changed)
        
        self.inp_density = QComboBox()
        self.inp_density.addItems(["Compact", "Comfortable"])
        self.inp_density.setCurrentText(self.settings.get("appearance/density"))

        layout.addRow("Tema:", self.inp_theme)
        layout.addRow("Kepadatan Tabel:", self.inp_density)
        
        self.tabs.addTab(tab, "Tampilan")

    def init_loans_tab(self):
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.inp_loan_duration = QSpinBox()
        self.inp_loan_duration.setRange(1, 365)
        self.inp_loan_duration.setSuffix(" Hari")
        self.inp_loan_duration.setValue(int(self.settings.get("loans/duration_days")))

        self.inp_max_books = QSpinBox()
        self.inp_max_books.setRange(1, 20)
        self.inp_max_books.setSuffix(" Buku")
        self.inp_max_books.setValue(int(self.settings.get("loans/max_books")))

        self.inp_fine_enabled = QCheckBox("Aktifkan Denda")
        self.inp_fine_enabled.setChecked(self.settings.get("loans/fine_enabled", bool))
        
        self.inp_fine_amount = QSpinBox()
        self.inp_fine_amount.setRange(0, 1000000)
        self.inp_fine_amount.setPrefix("Rp ")
        self.inp_fine_amount.setSingleStep(500)
        self.inp_fine_amount.setValue(int(self.settings.get("loans/fine_per_day")))

        layout.addRow("Durasi Peminjaman:", self.inp_loan_duration)
        layout.addRow("Maks Buku / Anggota:", self.inp_max_books)
        layout.addRow("Denda Keterlambatan:", self.inp_fine_enabled)
        layout.addRow("Nominal Denda / Hari:", self.inp_fine_amount)
        
        self.tabs.addTab(tab, "Peminjaman")

    def init_system_tab(self):
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        db_path_lbl = QLabel(str(Path(get_db_path()).absolute()))
        db_path_lbl.setStyleSheet("color: #7F8C8D; font-family: monospace;")
        
        backup_btn = QPushButton("Backup Database")
        backup_btn.setObjectName("secondary-btn")
        backup_btn.clicked.connect(self.backup_database)
        
        restore_btn = QPushButton("Restore Database")
        restore_btn.setObjectName("secondary-btn")
        restore_btn.clicked.connect(self.restore_database)
        restore_btn.setStyleSheet("color: #E67E22;") # Keep warning color hint

        layout.addRow("Lokasi Database:", db_path_lbl)
        layout.addRow("", backup_btn)
        layout.addRow("", restore_btn)
        
        self.tabs.addTab(tab, "Sistem")

    def save_settings(self):
        # General
        self.settings.set("general/library_name", self.inp_lib_name.text())
        self.settings.set("general/location", self.inp_location.text())
        self.settings.set("general/date_format", self.inp_date_fmt.currentText())

        # Appearance
        # Theme is now saved immediately on change via ThemeManager, 
        # but we can ensure it's saved here too if we want bulk save behavior.
        # However, user requested "Apply immediately", so on_theme_changed handles it.
        # We just save other appearance settings here.
        self.settings.set("appearance/density", self.inp_density.currentText())

        # Loans
        self.settings.set("loans/duration_days", self.inp_loan_duration.value())
        self.settings.set("loans/max_books", self.inp_max_books.value())
        self.settings.set("loans/fine_enabled", self.inp_fine_enabled.isChecked())
        self.settings.set("loans/fine_per_day", self.inp_fine_amount.value())

        self.settings_updated.emit()
        QMessageBox.information(self, "Sukses", "Pengaturan berhasil disimpan!")

    def on_theme_changed(self, text):
        from library_system.ui.theme_manager import ThemeManager
        # text is "Light" or "Dark"
        theme_code = text.lower()
        
        # 1. Save immediately
        ThemeManager.save_theme(theme_code)
        
        # 2. Apply immediately
        ThemeManager.apply_theme(theme_code)

    def backup_database(self):
        src = Path(get_db_path())
        if not src.exists():
            QMessageBox.warning(self, "Error", "Database file not found.")
            return
            
        dest, _ = QFileDialog.getSaveFileName(self, "Save Backup", "library_backup.db", "SQLite Database (*.db)")
        if dest:
            try:
                shutil.copy2(src, dest)
                QMessageBox.information(self, "Success", "Database backup created successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to backup: {e}")

    def restore_database(self):
        src, _ = QFileDialog.getOpenFileName(self, "Select Backup", "", "SQLite Database (*.db)")
        if src:
            confirm = QMessageBox.warning(
                self, "Konfirmasi Restore", 
                "Tindakan ini akan MENIMPA data saat ini dengan data dari backup!\nApakah Anda yakin?", 
                QMessageBox.Yes | QMessageBox.No
            )
            
            if confirm == QMessageBox.Yes:
                try:
                    dest = Path(get_db_path())
                    shutil.copy2(src, dest)
                    QMessageBox.information(self, "Sukses", "Database berhasil di-restore. Aplikasi akan ditutup.")
                    sys.exit(0)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Gagal restore: {e}")
