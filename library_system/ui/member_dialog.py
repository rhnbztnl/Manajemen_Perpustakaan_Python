from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QTextEdit, QFormLayout
)
from PySide6.QtCore import Qt
from library_system.services.member_service import MemberService

class MemberDialog(QDialog):
    def __init__(self, parent=None, member_data=None):
        super().__init__(parent)
        self.setWindowTitle("Tambah Anggota" if not member_data else "Edit Anggota")
        self.setFixedSize(450, 450)
        self.member_data = member_data
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Title
        title = QLabel(self.windowTitle())
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(title)

        # Form
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.code_input = QLineEdit()
        if not member_data:
            # Auto generate code
            self.code_input.setText(MemberService.generate_member_code())
            self.code_input.setPlaceholderText("MEM001 (Auto)")
        
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)

        if member_data:
            self.code_input.setText(member_data.get('member_code', ''))
            self.name_input.setText(member_data.get('name', ''))
            self.email_input.setText(member_data.get('email', ''))
            self.phone_input.setText(member_data.get('phone', ''))
            self.address_input.setText(member_data.get('address', ''))

        form_layout.addRow("Kode Anggota:", self.code_input)
        form_layout.addRow("Nama Lengkap:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("No. Telepon:", self.phone_input)
        form_layout.addRow("Alamat:", self.address_input)

        layout.addLayout(form_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Simpan")
        self.save_btn.setObjectName("primary-btn")
        self.save_btn.clicked.connect(self.save_data)
        
        self.cancel_btn = QPushButton("Batal")
        self.cancel_btn.setObjectName("secondary-btn")
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

        self.form_data = {}

    def save_data(self):
        code = self.code_input.text().strip()
        name = self.name_input.text().strip()
        
        if not code or not name:
            QMessageBox.warning(self, "Validasi", "Kode dan Nama wajib diisi!")
            return

        self.form_data = {
            "member_code": code,
            "name": name,
            "email": self.email_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "address": self.address_input.toPlainText().strip()
        }
        self.accept()

    def get_data(self):
        return self.form_data
