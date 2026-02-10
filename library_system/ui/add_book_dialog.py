from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QLabel, QPushButton, QComboBox, QSpinBox, QMessageBox
)

class AddBookDialog(QDialog):
    def __init__(self, parent=None, book_data=None, categories=None):
        super().__init__(parent)
        self.setWindowTitle("Tambah Buku Baru" if not book_data else "Edit Buku")
        self.setFixedWidth(400)
        self.layout = QVBoxLayout(self)
        self.book_data = book_data
        self.categories = categories or []

        # -- Inputs --
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Judul Buku")
        
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Penulis")
        
        self.publisher_input = QLineEdit()
        self.publisher_input.setPlaceholderText("Penerbit")
        
        self.year_input = QSpinBox()
        self.year_input.setRange(1900, 2100)
        self.year_input.setValue(2024)
        self.year_input.setPrefix("Tahun: ")
        
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 1000)
        self.stock_input.setValue(1)
        self.stock_input.setPrefix("Stok: ")

        self.category_input = QComboBox()
        for cat in self.categories:
            self.category_input.addItem(cat['name'], cat['id'])

        # Add widgets to layout
        self.layout.addWidget(QLabel("Informasi Buku"))
        self.layout.addWidget(self.title_input)
        self.layout.addWidget(self.author_input)
        self.layout.addWidget(self.category_input)
        self.layout.addWidget(self.publisher_input)
        
        row_layout = QHBoxLayout()
        row_layout.addWidget(self.year_input)
        row_layout.addWidget(self.stock_input)
        self.layout.addLayout(row_layout)

        # -- Buttons --
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Simpan")
        self.save_btn.setObjectName("primary-btn")
        self.save_btn.clicked.connect(self.accept)
        
        self.cancel_btn = QPushButton("Batal")
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        self.layout.addLayout(btn_layout)

        # Load data if editing
        if self.book_data:
            self.title_input.setText(self.book_data['title'])
            self.author_input.setText(self.book_data['author'])
            self.publisher_input.setText(self.book_data['publisher'])
            self.year_input.setValue(int(self.book_data['year']))
            self.stock_input.setValue(int(self.book_data['stock']))
            
            # Set category combo box
            # Note: We only have category name in the table list usually, but let's see. 
            # In the service we fetch 'category' name. But for editing we really need category_id.
            # Ideally the service should return category_id as well.
            # For now let's just default to first or try to match text if possible.
            index = self.category_input.findText(str(self.book_data.get('category', '')))
            if index >= 0:
                self.category_input.setCurrentIndex(index)

    def get_data(self):
        return {
            'title': self.title_input.text(),
            'author': self.author_input.text(),
            'publisher': self.publisher_input.text(),
            'year': self.year_input.value(),
            'stock': self.stock_input.value(),
            'category_id': self.category_input.currentData()
        }
