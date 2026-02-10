from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor

class MemberTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []
        # Columns: ID, Kode, Nama, Email, Phone, Status (Hidden/Active) -> Now Visible
        self._headers = ["ID", "Kode Anggota", "Nama", "Email", "No. Telp", "Alamat", "Status"]

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def data(self, index, role):
        if not index.isValid():
            return None
        
        row_data = self._data[index.row()]
        is_active = str(row_data.get('is_active', 1)) == '1'
        
        if role == Qt.ForegroundRole:
            # Row Coloring (Text)
            if not is_active:
                return QColor("#E74C3C") # Red for Inactive
            else:
                return None # Default text color (handled by theme)

        if role == Qt.DisplayRole:
            col = index.column()
            
            if col == 0: return str(row_data.get('id', ''))
            elif col == 1: return str(row_data.get('member_code', ''))
            elif col == 2: return str(row_data.get('name', ''))
            elif col == 3: return str(row_data.get('email', ''))
            elif col == 4: return str(row_data.get('phone', ''))
            elif col == 5: return str(row_data.get('address', ''))
            elif col == 6: return "AKTIF" if is_active else "NONAKTIF"
        
        elif role == Qt.TextAlignmentRole:
            # ID right aligned
            if index.column() == 0:
                return Qt.AlignVCenter | Qt.AlignRight
            # Status center aligned
            if index.column() == 6:
                return Qt.AlignCenter
            return Qt.AlignVCenter | Qt.AlignLeft
        
        return None

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            else:
                return str(section + 1)
        return None

    def update_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()
