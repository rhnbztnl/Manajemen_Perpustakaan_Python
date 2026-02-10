from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
from library_system.managers.settings_manager import SettingsManager

class ThemeManager:
    @staticmethod
    def load_theme():
        """
        Load theme from settings.
        Returns: 'light', 'dark', or 'system'
        """
        settings = SettingsManager()
        # Default to 'light' if not set
        return settings.get("ui.theme", str) or "light"

    @staticmethod
    def save_theme(theme_name):
        """
        Save theme to settings.
        theme_name: 'light', 'dark', or 'system'
        """
        settings = SettingsManager()
        # Ensure we save lowercase
        settings.set("ui.theme", theme_name.lower())

    @staticmethod
    def apply_theme(theme_name):
        """
        Apply the specified theme to the global QApplication instance.
        theme_name: 'light', 'dark', or 'system' (case-insensitive)
        """
        app = QApplication.instance()
        if not app:
            return

        mode = theme_name.lower()

        if mode == "dark":
            ThemeManager.set_dark_theme(app)
        elif mode == "light":
            ThemeManager.set_light_theme(app)
        elif mode == "system":
            # For now, default to light or implement system detection later
            # Ideally: detect dark mode from OS
            ThemeManager.set_light_theme(app) # Fallback to light
        else:
            # Fallback
            ThemeManager.set_light_theme(app)

    @staticmethod
    def set_light_theme(app):
        # Reset to default style/palette often works, 
        # but let's be explicit for "Light" to ensure return from Dark
        app.setStyle("Fusion")
        
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, Qt.white)
        palette.setColor(QPalette.AlternateBase, QColor(233, 233, 233))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.black)
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        
        app.setPalette(palette)
        
        # Global Stylesheet tweaks for Light Mode
        app.setStyleSheet("""
            /* --- SIDEBAR --- */
            #sidebar { background-color: #FFFFFF; border-right: 1px solid #ECF0F1; }
            #sidebar QPushButton {
                text-align: left;
                padding: 12px 20px;
                border: none;
                color: #2C3E50;
                font-size: 14px;
                background-color: transparent;
            }
            #sidebar QPushButton:hover { background-color: #F0F2F5; color: #3498DB; }
            #sidebar QPushButton:checked { background-color: #EBF5FB; color: #2C3E50; border-left: 4px solid #3498DB; font-weight: bold; }
            #sidebar QLabel { color: #2C3E50; font-weight: bold; font-size: 18px; padding: 20px; }

            /* --- GENERIC --- */
            QMainWindow { background-color: #F8F9FA; }
            QLabel { color: #2C3E50; }
            QGroupBox { border: 1px solid #BDC3C7; border-radius: 4px; margin-top: 10px; font-weight: bold; color: #2C3E50; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; }
            
            /* --- TABLES --- */
            QTableView { 
                background-color: white; 
                gridline-color: #ECF0F1; 
                border: 1px solid #BDC3C7; 
                border-radius: 4px;
            }
            QHeaderView::section { 
                background-color: #ECF0F1; 
                padding: 8px; 
                border: none; 
                font-weight: bold; 
                color: #2C3E50; 
                border-bottom: 2px solid #BDC3C7;
            }
            QHeaderView::section:horizontal { border-right: 1px solid white; }
            
            /* --- INPUTS --- */
            QLineEdit, QComboBox, QSpinBox { 
                background-color: white; 
                color: #2C3E50;
                border: 1px solid #BDC3C7; 
                padding: 8px; 
                border-radius: 4px; 
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus { 
                border: 1px solid #3498DB; 
                background-color: #FFFFFF;
            }

            /* --- BUTTONS --- */
            QPushButton { 
                background-color: white; 
                border: 1px solid #BDC3C7; 
                padding: 8px 16px; 
                border-radius: 4px; 
                color: #2C3E50; 
                font-weight: bold; 
            }
            QPushButton:hover { background-color: #F4F6F6; border-color: #A6ACAF; }
            QPushButton:pressed { background-color: #ECF0F1; }
            
            /* Primary Button */
            QPushButton#primary-btn { background-color: #3498DB; color: white; border: none; }
            QPushButton#primary-btn:hover { background-color: #2980B9; }
            QPushButton#primary-btn:pressed { background-color: #1F618D; }
            
            /* Secondary Button */
            QPushButton#secondary-btn { background-color: white; border: 1px solid #BDC3C7; color: #7F8C8D; }
            QPushButton#secondary-btn:hover { background-color: #FDFEFE; border-color: #7F8C8D; color: #2C3E50; }
            
            /* --- TABS (DISABLED FOR DEBUG) --- */
            /*
            QTabWidget::pane { border: 1px solid #ECF0F1; background: white; border-radius: 4px; }
            QTabBar::tab { 
                background: #F4F6F6;
                padding: 10px 20px; 
                color: #7F8C8D; 
                border: 1px solid #ECF0F1;
                border-bottom: none;
                margin-right: 2px;
                border-top-left-radius: 4px; 
                border-top-right-radius: 4px; 
            }
            QTabBar::tab:selected { 
                color: #2C3E50; 
                background: white;
                font-weight: bold; 
                border-top: 3px solid #3498DB; 
                border-bottom: 1px solid white;
            }
            QTabBar::tab:!selected { margin-top: 2px; }
            #reportsTabs QTabBar::tab { color: #2C3E50; }
            #reportsTabs QTabBar::tab:!selected { color: #7F8C8D; }
            */
            
            /* --- CARDS --- */
            #contentFrame, #dashCard, #statCard { background-color: white; border: 1px solid #E0E0E0; border-radius: 10px; }
            #dashCard:hover { border: 1px solid #3498DB; background-color: #FDFEFE; }
            
            /* --- SCROLLBAR --- */
            QScrollBar:vertical { border: none; background: #F0F3F4; width: 12px; margin: 0px; }
            QScrollBar::handle:vertical { background: #BDC3C7; min-height: 20px; border-radius: 6px; margin: 2px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
            QScrollBar::handle:vertical:hover { background: #95A5A6; }
        """)

    @staticmethod
    def set_dark_theme(app):
        app.setStyle("Fusion")
        
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(44, 62, 80)) # Dark Blue-Grey
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(34, 49, 63)) # Darker for inputs
        palette.setColor(QPalette.AlternateBase, QColor(44, 62, 80))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(52, 73, 94))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(52, 152, 219))
        palette.setColor(QPalette.Highlight, QColor(52, 152, 219))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        
        app.setPalette(palette)
        
        # Global Stylesheet tweaks for Dark Mode
        app.setStyleSheet("""
            /* --- SIDEBAR --- */
            #sidebar { background-color: #2C3E50; }
            #sidebar QPushButton {
                text-align: left;
                padding: 12px 20px;
                border: none;
                color: #BDC3C7;
                font-size: 14px;
                background-color: transparent;
            }
            #sidebar QPushButton:hover { background-color: #34495E; color: white; }
            #sidebar QPushButton:checked { background-color: #34495E; color: white; border-left: 4px solid #3498DB; }
            #sidebar QLabel { color: white; font-weight: bold; font-size: 18px; padding: 20px; }

            /* --- GENERIC WIDGETS --- */
            QMainWindow { background-color: #2C3E50; }
            QLabel { color: #ECF0F1; }
            QGroupBox { border: 1px solid #7F8C8D; border-radius: 4px; margin-top: 10px; font-weight: bold; color: #ECF0F1; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; }
            
            /* --- TABLES --- */
            QTableView { 
                background-color: #2C3E50; 
                color: white; 
                gridline-color: #34495E; 
                selection-background-color: #3498DB; 
                alternate-background-color: #34495E; 
                border: 1px solid #7F8C8D;
                border-radius: 4px;
            }
            QHeaderView::section { 
                background-color: #34495E; 
                color: white; 
                padding: 8px; 
                border: none; 
                font-weight: bold; 
                border-bottom: 2px solid #7F8C8D;
            }
            QHeaderView::section:horizontal { border-right: 1px solid #2C3E50; }
            
            /* --- INPUTS --- */
            QLineEdit, QComboBox, QSpinBox { 
                background-color: #34495E; 
                color: white; 
                border: 1px solid #7F8C8D; 
                padding: 8px; 
                border-radius: 4px; 
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus { 
                border: 1px solid #3498DB; 
                background-color: #3E5871;
            }
            
            /* --- BUTTONS --- */
            QPushButton { 
                background-color: #34495E; 
                color: white; 
                border: 1px solid #7F8C8D; 
                padding: 8px 16px; 
                border-radius: 4px; 
                font-weight: bold;
            }
            QPushButton:hover { background-color: #3E5871; border-color: #95A5A6; }
            QPushButton:pressed { background-color: #2980B9; border-color: #3498DB; }
            
            /* Primary */
            QPushButton#primary-btn { background-color: #3498DB; border: none; color: white; }
            QPushButton#primary-btn:hover { background-color: #2980B9; }
            
            /* Secondary */
            QPushButton#secondary-btn { background-color: #34495E; border: 1px solid #7F8C8D; color: #BDC3C7; }
            QPushButton#secondary-btn:hover { background-color: #3E5871; color: white; }
            
            /* --- TABS (DISABLED FOR DEBUG) --- */
            /*
            QTabWidget::pane { border: 1px solid #7F8C8D; background: #2C3E50; border-radius: 4px; }
            QTabBar::tab { 
                background: #34495E; 
                color: #BDC3C7; 
                padding: 10px 20px; 
                border-top-left-radius: 4px; 
                border-top-right-radius: 4px; 
                margin-right: 2px;
                border: 1px solid #7F8C8D;
                border-bottom: none;
            }
            QTabBar::tab:selected { 
                background: #2C3E50; 
                color: white; 
                border-bottom: 2px solid #2C3E50;
                font-weight: bold; 
                border-top: 3px solid #3498DB;
            }
            QTabBar::tab:!selected { margin-top: 2px; }
            #reportsTabs QTabBar::tab { color: white; }
            #reportsTabs QTabBar::tab:!selected { color: #BDC3C7; }
            */
            
            /* --- CARDS --- */
            #contentFrame, #dashCard, #statCard { background-color: #34495E; border: 1px solid #7F8C8D; border-radius: 10px; }
            #dashCard:hover { border: 1px solid #3498DB; }
            
            /* --- SCROLLBAR --- */
            QScrollBar:vertical { border: none; background: #2C3E50; width: 12px; margin: 0px; }
            QScrollBar::handle:vertical { background: #5D6D7E; min-height: 20px; border-radius: 6px; margin: 2px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
            QScrollBar::handle:vertical:hover { background: #3498DB; }
            
            /* --- DIALOGS --- */
            QDialog { background-color: #2C3E50; }
            QDialog QLabel { color: #ECF0F1; }
        """)
