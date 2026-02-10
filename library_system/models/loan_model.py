from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor

class LoanTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []
        self._headers = ["ID", "Member", "Buku", "Tgl Pinjam", "Tgl Kembali", "Status"]

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def data(self, index, role):
        if not index.isValid():
            return None
        
        row_data = self._data[index.row()]
        status = row_data.get('status', 'borrowed')
        
        if role == Qt.DisplayRole:
            col = index.column()
            # ID, Member, Book, Loan Date, Return Date, Status
            if col == 0: return str(row_data.get('id', ''))
            elif col == 1: 
                # Combine Name + Code
                return f"{row_data.get('member_name', '')} ({row_data.get('member_code', '')})"
            elif col == 2: return str(row_data.get('book_title', ''))
            elif col == 3: return str(row_data.get('loan_date', ''))
            elif col == 4: return str(row_data.get('return_date') or '-')
            elif col == 5: 
                if status == 'borrowed': return "DIPINJAM"
                elif status == 'returned': return "KEMBALI"
                elif status == 'overdue': return "TERLAMBAT"
                return status.upper()
        
        elif role == Qt.ForegroundRole:
            # Color code status text
            if status == 'borrowed':
                return QColor("#F1C40F") # Vivid Yellow/Orange
            elif status == 'returned':
                return QColor("#2ECC71") # Vivid Green
            elif status == 'overdue':
                return QColor("#E74C3C") # Vivid Red
            return None
        
        elif role == Qt.TextAlignmentRole:
            if index.column() == 0: return Qt.AlignRight | Qt.AlignVCenter
            if index.column() == 5: return Qt.AlignCenter | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter

        return None

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None

    def update_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()
