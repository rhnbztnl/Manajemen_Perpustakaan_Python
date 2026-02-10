from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableView, 
    QLineEdit, QPushButton, QLabel, QHeaderView, QAbstractItemView, QMessageBox, QMenu
)
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtCore import Qt, QSortFilterProxyModel
from library_system.models.book_model import BookTableModel
from library_system.services.book_service import BookService
from library_system.ui.add_book_dialog import AddBookDialog

from library_system.pages.base_page import BasePage

class BooksPage(BasePage):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24) # Consistent padding
        self.layout.setSpacing(12) # Tighter spacing

        self.layout.setSpacing(12) # Tighter spacing

        # page title removed (handled by Top Bar)
        # title_label = QLabel("Data Buku")
        # title_label.setObjectName("pageTitle")
        # self.layout.addWidget(title_label)

        # -- Toolbar (Search + Actions) --
        toolbar_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari judul, penulis...")
        self.search_input.setFixedWidth(300)
        self.search_input.textChanged.connect(self.on_search_changed)
        
        self.add_btn = QPushButton("+ Tambah Buku")
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.setObjectName("primary-btn")
        self.add_btn.setStyleSheet("background-color: #3498DB; color: white; border-radius: 4px; padding: 8px 16px;")
        self.add_btn.clicked.connect(self.open_add_dialog)

        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        self.edit_btn.setObjectName("secondary-btn")
        self.edit_btn.setEnabled(False)  # Enabled when row selected
        self.edit_btn.clicked.connect(self.open_edit_dialog)

        self.delete_btn = QPushButton("Hapus")
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        self.delete_btn.setObjectName("secondary-btn")
        self.delete_btn.setStyleSheet("color: #E74C3C; border: 1px solid #E74C3C;")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_book)

        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addWidget(self.edit_btn)
        toolbar_layout.addWidget(self.delete_btn)

        self.layout.addLayout(toolbar_layout)

        # -- Table View --
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Setup Model
        self.model = BookTableModel()
        # Proxy model is optional now if we do SQL search, but kept for client-side filtering if needed. 
        # Actually let's do SQL search properly in on_search_changed.
        # But for now, let's keep it simple: load all, filter via SQL if text changes? 
        # Or keeping proxy for fast local filter is better for small datasets.
        # Given "Query pencarian (LIKE)", I should probably use SQL search.
        
        self.table_view.setModel(self.model)
        self.table_view.selectionModel().selectionChanged.connect(self.on_selection_changed)

        self.layout.addWidget(self.table_view)
        
        # Status Bar / Selection Count
        self.status_label = QLabel("0 baris terpilih")
        self.status_label.setStyleSheet("color: #7F8C8D; font-size: 12px;")
        self.layout.addWidget(self.status_label)

        # Actions
        self.setup_actions()
        
        # Load initial data
        self.refresh_data()

    def setup_actions(self):
        # Select All Action
        self.select_all_action = QAction("Select All", self)
        # self.select_all_action.setShortcut(QKeySequence.SelectAll) 
        self.select_all_action.triggered.connect(self.select_all_rows)
        self.addAction(self.select_all_action) 

        # Clear Selection Action
        self.clear_selection_action = QAction("Clear Selection", self)
        self.clear_selection_action.triggered.connect(self.clear_selection)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        menu.addAction(self.select_all_action)
        menu.addAction(self.clear_selection_action)
        menu.addSeparator()
        
        if self.edit_btn.isEnabled():
            edit_action = QAction("Edit", self)
            edit_action.triggered.connect(self.open_edit_dialog)
            menu.addAction(edit_action)
            
        if self.delete_btn.isEnabled():
            delete_action = QAction("Hapus", self)
            delete_action.triggered.connect(self.delete_book)
            menu.addAction(delete_action)
            
        menu.exec(self.table_view.viewport().mapToGlobal(pos))

    def select_all_rows(self):
        self.table_view.selectAll()

    def clear_selection(self):
        self.table_view.clearSelection()

    def refresh_data(self):
        books = BookService.get_all_books()
        self.model.update_data(books)
        self.status_label.setText(f"{len(books)} total data")
        self.clear_selection()

    def on_search_changed(self, text):
        if len(text) > 0:
            books = BookService.search_books(text)
        else:
            books = BookService.get_all_books()
        self.model.update_data(books)
        self.status_label.setText(f"{len(books)} data ditemukan")

    def on_selection_changed(self, selected, deselected):
        selected_rows = self.table_view.selectionModel().selectedRows()
        count = len(selected_rows)
        
        self.status_label.setText(f"{count} baris terpilih")
        
        # Edit only if exactly 1 row is selected
        self.edit_btn.setEnabled(count == 1)
        # Delete if 1 or more rows are selected
        self.delete_btn.setEnabled(count > 0)

    def open_add_dialog(self):
        categories = BookService.get_categories()
        dialog = AddBookDialog(self, categories=categories)
        if dialog.exec():
            data = dialog.get_data()
            if BookService.add_book(
                data['title'], data['author'], data['publisher'], 
                data['year'], data['stock'], data['category_id']
            ):
                self.refresh_data()
            else:
                QMessageBox.critical(self, "Error", "Gagal menyimpan buku")

    def open_edit_dialog(self):
        # Ensure single selection logic
        selected_rows = self.table_view.selectionModel().selectedRows()
        if len(selected_rows) != 1: return
        
        index = selected_rows[0]
        
        # Get raw data from model
        book_data = self.model._data[index.row()]
        categories = BookService.get_categories()
        
        dialog = AddBookDialog(self, book_data=book_data, categories=categories)
        if dialog.exec():
            data = dialog.get_data()
            if BookService.update_book(
                book_data['id'],
                data['title'], data['author'], data['publisher'], 
                data['year'], data['stock'], data['category_id']
            ):
                self.refresh_data()
            else:
                QMessageBox.critical(self, "Error", "Gagal mengupdate buku")

    def delete_book(self):
        selected_rows = self.table_view.selectionModel().selectedRows()
        if not selected_rows: return
        
        count = len(selected_rows)
        msg = f"Yakin ingin menghapus {count} buku terpilih?"
        if count == 1:
            # Show specific title if only one
            book_data = self.model._data[selected_rows[0].row()]
            msg = f"Yakin ingin menghapus '{book_data['title']}'?"
            
        reply = QMessageBox.question(
            self, "Konfirmasi Hapus", 
            msg,
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success_count = 0
            for index in selected_rows:
                book_data = self.model._data[index.row()]
                if BookService.delete_book(book_data['id']):
                    success_count += 1
            
            if success_count > 0:
                self.refresh_data()
                if success_count < count:
                    QMessageBox.warning(self, "Partial Success", f"Hanya {success_count} dari {count} buku berhasil dihapus.")
            else:
                QMessageBox.critical(self, "Error", "Gagal menghapus buku")
