import sys
import os
from PySide6.QtWidgets import QApplication
from library_system.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Initialize Database
    try:
        from library_system.database.db import initialize_db
        initialize_db()
    except Exception as e:
        print(f"Failed to init DB: {e}")

    # Init Config & Theme
    from library_system.managers.settings_manager import SettingsManager
    from library_system.ui.theme_manager import ThemeManager
    
    # Ensure settings are initialized (instance created)
    SettingsManager()
    
    # Load and Apply Theme
    saved_theme = ThemeManager.load_theme()
    ThemeManager.apply_theme(saved_theme)

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
