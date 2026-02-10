from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableView, 
    QPushButton, QLabel, QHeaderView, QMessageBox, QAbstractItemView
)
from PySide6.QtCore import Qt
from library_system.models.loan_model import LoanTableModel
from library_system.services.loan_service import LoanService
from library_system.ui.loan_dialog import LoanDialog

from library_system.pages.base_page import BasePage

class LoansPage(BasePage):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(12)

        # -- Toolbar --
        toolbar_layout = QHBoxLayout()
        
        self.title_label = QLabel("Daftar Peminjaman")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        
        # Action Buttons
        self.return_btn = QPushButton("Kembalikan Buku")
        self.return_btn.setCursor(Qt.PointingHandCursor)
        self.return_btn.setObjectName("secondary-btn")
        self.return_btn.setEnabled(False)
        self.return_btn.clicked.connect(self.return_books)

        self.add_btn = QPushButton("+ Peminjaman Baru")
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.setObjectName("primary-btn")
        self.add_btn.clicked.connect(self.open_loan_dialog)
        
        toolbar_layout.addWidget(self.title_label)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.return_btn)
        toolbar_layout.addWidget(self.add_btn)
        
        self.layout.addLayout(toolbar_layout)

        # -- Table View --
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.model = LoanTableModel()
        self.table_view.setModel(self.model)
        self.table_view.selectionModel().selectionChanged.connect(self.on_selection_changed)
        
        self.layout.addWidget(self.table_view)
        
        # Load Data
        self.refresh_data()

    def refresh_data(self):
        loans = LoanService.get_all_loans()
        self.model.update_data(loans)
        self.return_btn.setEnabled(False) # Reset button

    def on_selection_changed(self, selected, deselected):
        rows = self.table_view.selectionModel().selectedRows()
        
        if not rows:
            self.return_btn.setEnabled(False)
            return

        # Check if ALL selected rows are 'borrowed'
        all_borrowed = True
        for idx in rows:
            row_data = self.model._data[idx.row()]
            if row_data.get('status') != 'borrowed':
                all_borrowed = False
                break
        
        self.return_btn.setEnabled(all_borrowed)

    def return_books(self):
        rows = self.table_view.selectionModel().selectedRows()
        if not rows: return
        
        count = len(rows)
        reply = QMessageBox.question(
            self, "Konfirmasi Pengembalian", 
            f"Yakin ingin mengembalikan {count} buku terpilih?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success_count = 0
            for idx in rows:
                loan_data = self.model._data[idx.row()]
                loan_id = loan_data['id']
                
                if LoanService.return_book(loan_id):
                    success_count += 1
            
            self.refresh_data()
            
            if success_count < count:
                QMessageBox.warning(self, "Info", f"Hanya {success_count} dari {count} berhasil diproses")
            else:
                 QMessageBox.information(self, "Sukses", "Buku berhasil dikembalikan")

    def open_loan_dialog(self):
        dialog = LoanDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if not data: return
            
            success, message = LoanService.borrow_book(data['member_id'], data['book_id'])
            
            if success:
                self.refresh_data()
                QMessageBox.information(self, "Sukses", message)
            else:
                QMessageBox.critical(self, "Gagal", message)
