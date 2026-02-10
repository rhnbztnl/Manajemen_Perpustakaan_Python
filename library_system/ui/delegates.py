from PySide6.QtWidgets import QStyledItemDelegate, QStyle
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QBrush, QPen

class StatusDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option, index):
        # Save painter state
        painter.save()
        
        # Enable Antialiasing for smooth rounded corners
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get status text
        status_text = index.data(Qt.DisplayRole)
        
        # Determine Check State or Value
        is_active = status_text == "AKTIF"
        
        # Setup Colors
        if is_active:
            bg_color = QColor("#2ECC71") # Strong Green
            text_color = QColor("white")
        else:
            bg_color = QColor("#E74C3C") # Strong Red
            text_color = QColor("white")
            
        # Draw Background (Optional: if we want to override selection color for the badge itself)
        # But usually we let the table draw the cell background (row color) 
        # and we just draw the badge on top.
        
        # Define Badge Rect
        rect = option.rect
        # add padding
        badge_width = 80
        badge_height = 22
        
        # Center the badge
        x = rect.x() + (rect.width() - badge_width) / 2
        y = rect.y() + (rect.height() - badge_height) / 2
        
        badge_rect = QRectF(x, y, badge_width, badge_height)
        
        # Draw Badge Background
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bg_color))
        painter.drawRoundedRect(badge_rect, 10, 10) # 10px radius
        
        # Draw Text
        painter.setPen(text_color)
        painter.drawText(badge_rect, Qt.AlignCenter, status_text)
        
        painter.restore()
        
    def sizeHint(self, option, index):
        return super().sizeHint(option, index)
