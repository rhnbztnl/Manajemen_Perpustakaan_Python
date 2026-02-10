from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

class BookTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []
        self._headers = ["ID", "Judul", "Penulis", "Penerbit", "Tahun", "Stok", "Kategori"]

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            row_data = self._data[index.row()]
            col = index.column()
            # ["ID", "Judul", "Penulis", "Penerbit", "Tahun", "Stok", "Kategori"]
            if col == 0: return str(row_data['id'])
            elif col == 1: return str(row_data['title'])
            elif col == 2: return str(row_data['author'])
            elif col == 3: return str(row_data['publisher'])
            elif col == 4: return str(row_data['year'])
            elif col == 5: return str(row_data['stock'])
            elif col == 6: return str(row_data['category'])
        
        elif role == Qt.TextAlignmentRole:
            # Align numeric columns to the right, others to the left
            if index.column() in [0, 4, 5]:  # ID, Tahun, Stok
                return Qt.AlignVCenter | Qt.AlignRight
            return Qt.AlignVCenter | Qt.AlignLeft

        return None

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
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

    def add_book(self, book):
        self.beginInsertRows(QModelIndex(), self.rowCount(QModelIndex()), self.rowCount(QModelIndex()))
        self._data.append(book)
        self.endInsertRows()

    def remove_book(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._data[row]
        self.endRemoveRows()
