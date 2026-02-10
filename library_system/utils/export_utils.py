import csv
from PySide6.QtWidgets import QFileDialog, QMessageBox, QTableView
from PySide6.QtCore import QAbstractItemModel

class ExportUtils:
    @staticmethod
    def export_table_to_csv(parent, table_view: QTableView, filename="export.csv"):
        """
        Export QTableView model data to CSV.
        """
        model = table_view.model()
        if not model:
            return

        filepath, _ = QFileDialog.getSaveFileName(parent, "Export to CSV", filename, "CSV Files (*.csv)")
        if not filepath:
            return

        try:
            with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Write Headers
                headers = []
                for col in range(model.columnCount()):
                    headers.append(model.headerData(col, 1).title()) # 1 = Horizontal
                writer.writerow(headers)
                
                # Write Rows
                for row in range(model.rowCount()):
                    row_data = []
                    for col in range(model.columnCount()):
                        index = model.index(row, col)
                        row_data.append(str(model.data(index)))
                    writer.writerow(row_data)
                    
            QMessageBox.information(parent, "Sukses", f"Data berhasil diexport ke:\n{filepath}")
            
        except Exception as e:
            QMessageBox.critical(parent, "Error", f"Gagal export data: {e}")
