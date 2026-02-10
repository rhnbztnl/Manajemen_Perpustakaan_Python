from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QPushButton, QMessageBox, QFormLayout
)
from PySide6.QtCore import Qt
from library_system.services.member_service import MemberService
from library_system.services.book_service import BookService

class LoanDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tambah Peminjaman Baru")
        self.setFixedWidth(400)
        self.result_data = None
        
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        # Member Selection
        self.member_combo = QComboBox()
        self.members = []
        self.load_members()
        form_layout.addRow("Anggota:", self.member_combo)
        
        # Book Selection
        self.book_combo = QComboBox()
        self.books = []
        self.load_books()
        form_layout.addRow("Buku:", self.book_combo)
        
        layout.addLayout(form_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Simpan")
        self.save_btn.setObjectName("primary-btn")
        self.save_btn.setStyleSheet("background-color: #2ECC71; color: white;")
        self.save_btn.clicked.connect(self.save)
        
        self.cancel_btn = QPushButton("Batal")
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        
        layout.addLayout(btn_layout)
        
        # Initial validation
        self.validate_input()
        self.member_combo.currentIndexChanged.connect(self.validate_input)
        self.book_combo.currentIndexChanged.connect(self.validate_input)

    def load_members(self):
        # Only active members
        self.members = MemberService.get_all_members(active_only=True)
        self.member_combo.clear()
        for m in self.members:
            self.member_combo.addItem(f"{m['member_code']} - {m['name']}", userData=m['id'])
            
    def load_books(self):
        # All books, but we will visually indicate stock
        all_books = BookService.get_all_books()
        self.books = [] # Filtered list if needed, or just map indices
        self.book_combo.clear()
        
        for b in all_books:
            stock = b['stock']
            title = f"{b['title']} (Stok: {stock})"
            self.book_combo.addItem(title, userData=b['id'])
            
            # Disable item if stock is 0 (User UX: Make it unselectable or show visual cue)
            # QComboBox standard model doesn't easily support disabling individual items visually in a simple way 
            # without a custom model, but we can validate on save.
            # However, for UX, let's keep it in the list but maybe append " [KESEDIAAN HABIS]" if stock is 0
            if stock <= 0:
                self.book_combo.setItemText(self.book_combo.count()-1, f"{b['title']} [HABIS]")
                # We will handle validation in save()
            
            self.books.append(b)

    def validate_input(self):
        # Check if selection is valid
        # For now, just ensure items are selected
        is_valid = self.member_combo.currentIndex() >= 0 and self.book_combo.currentIndex() >= 0
        
        # Check stock
        if self.book_combo.currentIndex() >= 0:
             selected_idx = self.book_combo.currentIndex()
             if selected_idx < len(self.books):
                 if self.books[selected_idx]['stock'] <= 0:
                     is_valid = False
                     self.save_btn.setToolTip("Stok buku habis")
                 else:
                     self.save_btn.setToolTip("")
        
        self.save_btn.setEnabled(is_valid)

    def save(self):
        member_idx = self.member_combo.currentIndex()
        book_idx = self.book_combo.currentIndex()
        
        if member_idx < 0 or book_idx < 0:
            return
            
        member_id = self.member_combo.currentData()
        book_id = self.book_combo.currentData()
        
        self.result_data = {
            'member_id': member_id,
            'book_id': book_id
        }
        self.accept()

    def get_data(self):
        return self.result_data
