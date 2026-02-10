from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableView, 
    QLineEdit, QPushButton, QLabel, QHeaderView, QAbstractItemView, QMessageBox, QMenu
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from library_system.models.member_model import MemberTableModel
from library_system.services.member_service import MemberService
from library_system.ui.member_dialog import MemberDialog
from library_system.ui.delegates import StatusDelegate

from library_system.pages.base_page import BasePage

class MembersPage(BasePage):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(12)

        # -- Toolbar --
        toolbar_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari nama, kode, email...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self.on_search_changed)
        
        # Actions Buttons
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.setCursor(Qt.PointingHandCursor)
        self.select_all_btn.setObjectName("secondary-btn")
        self.select_all_btn.clicked.connect(self.select_all_rows)

        self.clear_select_btn = QPushButton("Clear")
        self.clear_select_btn.setCursor(Qt.PointingHandCursor)
        self.clear_select_btn.setObjectName("secondary-btn")
        self.clear_select_btn.clicked.connect(self.clear_selection)

        self.add_btn = QPushButton("+ Anggota Baru")
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.setObjectName("primary-btn")
        self.add_btn.setStyleSheet("background-color: #2ECC71; color: white; border: none;") # Green for members
        self.add_btn.clicked.connect(self.open_add_dialog)

        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        self.edit_btn.setObjectName("secondary-btn")
        self.edit_btn.setEnabled(False)
        self.edit_btn.clicked.connect(self.open_edit_dialog)

        self.status_btn = QPushButton("Nonaktifkan")
        self.status_btn.setCursor(Qt.PointingHandCursor)
        self.status_btn.setObjectName("secondary-btn")
        self.status_btn.setStyleSheet("color: #E67E22; border: 1px solid #E67E22;") # Default warning color
        self.status_btn.setEnabled(False)
        self.status_btn.clicked.connect(self.toggle_member_status)

        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(self.select_all_btn)
        toolbar_layout.addWidget(self.clear_select_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addWidget(self.edit_btn)
        toolbar_layout.addWidget(self.status_btn)

        self.layout.addLayout(toolbar_layout)

        # -- Table View --
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.show_context_menu)

        self.model = MemberTableModel()
        self.table_view.setModel(self.model)
        self.table_view.selectionModel().selectionChanged.connect(self.on_selection_changed)

        # Set Delegates
        self.table_view.setItemDelegateForColumn(6, StatusDelegate(self.table_view))
        
        self.layout.addWidget(self.table_view)

        # Status Bar
        self.status_label = QLabel("0 anggota")
        self.status_label.setStyleSheet("color: #7F8C8D; font-size: 12px;")
        self.layout.addWidget(self.status_label)
        
        # Initialize Actions
        self.setup_actions()

        # Load Data
        self.refresh_data()

    def setup_actions(self):
        self.select_all_action = QAction("Select All", self)
        self.select_all_action.triggered.connect(self.select_all_rows)
        self.addAction(self.select_all_action)
        
        self.clear_selection_action = QAction("Clear Selection", self)
        self.clear_selection_action.triggered.connect(self.clear_selection)

    def refresh_data(self):
        # Fetch ALL members to show inactive ones too
        members = MemberService.get_all_members(active_only=False)
        self.model.update_data(members)
        
        # Count active vs inactive
        active_count = sum(1 for m in members if str(m.get('is_active', 1)) == '1')
        self.status_label.setText(f"{active_count} Aktif / {len(members)} Total")
        self.clear_selection()

    def on_search_changed(self, text):
        if len(text) > 0:
            members = MemberService.search_members(text, active_only=False)
        else:
            members = MemberService.get_all_members(active_only=False)
        self.model.update_data(members)
        self.status_label.setText(f"{len(members)} data ditemukan")

    def on_selection_changed(self, selected, deselected):
        rows = self.table_view.selectionModel().selectedRows()
        count = len(rows)
        self.status_label.setText(f"{count} baris terpilih")
        
        # Analyze Selection Status
        all_active = True
        all_inactive = True
        
        if count > 0:
            for idx in rows:
                row_data = self.model._data[idx.row()]
                is_active = str(row_data.get('is_active', 1)) == '1'
                if is_active:
                    all_inactive = False
                else:
                    all_active = False
        else:
            all_active = False
            all_inactive = False

        # Edit: Only if 1 selected AND it is active
        self.edit_btn.setEnabled(count == 1 and all_active)
        
        # Status Button Logic
        self.status_btn.setEnabled(count > 0 and (all_active or all_inactive))
        
        if count > 0:
            if all_active:
                self.status_btn.setText("Nonaktifkan")
                self.status_btn.setStyleSheet("color: #E67E22; border: 1px solid #E67E22;")
                self.status_btn.setToolTip("Nonaktifkan anggota terpilih")
                self.status_action_mode = "deactivate"
            elif all_inactive:
                self.status_btn.setText("Aktifkan")
                self.status_btn.setStyleSheet("color: #27AE60; border: 1px solid #27AE60;")
                self.status_btn.setToolTip("Aktifkan kembali anggota terpilih")
                self.status_action_mode = "activate"
            else:
                self.status_btn.setText("Status")
                self.status_btn.setToolTip("Pilih anggota dengan status yang sama")
                self.status_btn.setEnabled(False)
        else:
            self.status_btn.setText("Nonaktifkan")
            self.status_btn.setStyleSheet("color: #BDC3C7; border: 1px solid #BDC3C7;")


    def select_all_rows(self):
        self.table_view.selectAll()

    def clear_selection(self):
        self.table_view.clearSelection()

    def show_context_menu(self, pos):
        menu = QMenu(self)
        menu.addAction(self.select_all_action)
        menu.addAction(self.clear_selection_action)
        menu.addSeparator()
        
        if self.edit_btn.isEnabled():
            menu.addAction("Edit", self.open_edit_dialog)
        
        if self.status_btn.isEnabled():
            menu.addAction(self.status_btn.text(), self.toggle_member_status)
            
        menu.exec(self.table_view.viewport().mapToGlobal(pos))

    def open_add_dialog(self):
        dialog = MemberDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if MemberService.add_member(
                data['member_code'], data['name'], data['email'], 
                data['phone'], data['address']
            ):
                self.refresh_data()
            else:
                QMessageBox.critical(self, "Error", "Gagal menyimpan anggota (Kode mungkin duplikat)")

    def open_edit_dialog(self):
        rows = self.table_view.selectionModel().selectedRows()
        if len(rows) != 1: return
        
        member_data = self.model._data[rows[0].row()]
        dialog = MemberDialog(self, member_data=member_data)
        if dialog.exec():
            data = dialog.get_data()
            if MemberService.update_member(
                member_data['id'],
                data['member_code'], data['name'], data['email'], 
                data['phone'], data['address']
            ):
                self.refresh_data()
            else:
                QMessageBox.critical(self, "Error", "Gagal mengupdate anggota")

    def toggle_member_status(self):
        rows = self.table_view.selectionModel().selectedRows()
        if not rows: return
        
        count = len(rows)
        mode = getattr(self, "status_action_mode", "deactivate")
        
        action_verb = "menonaktifkan" if mode == "deactivate" else "mengaktifkan"
        
        reply = QMessageBox.question(
            self, "Konfirmasi", 
            f"Yakin ingin {action_verb} {count} anggota terpilih?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success_count = 0
            for idx in rows:
                member_data = self.model._data[idx.row()]
                member_id = member_data['id']
                
                if mode == "deactivate":
                    if MemberService.delete_member(member_id):
                        success_count += 1
                else:
                    if MemberService.activate_member(member_id):
                        success_count += 1
                        
            self.refresh_data()
            
            if success_count < count:
                QMessageBox.warning(self, "Info", f"Hanya {success_count} dari {count} berhasil diproses")
