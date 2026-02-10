import sys
from pathlib import Path
from PySide6.QtCore import QStandardPaths, QCoreApplication

class AppPaths:
    APP_NAME = "SistemManajemenPerpustakaan"
    ORG_NAME = "Antigravity"

    @staticmethod
    def get_data_dir() -> Path:
        """Returns the cross-platform data directory."""
        path = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)
        if not path:
            # Fallback for some systems
            path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        
        # QStandardPaths returns a string, convert to Path
        # On Linux: ~/.local/share/SistemManajemenPerpustakaan usually
        # On Windows: C:/Users/<User>/AppData/Local/Antigravity/SistemManajemenPerpustakaan or similar
        data_dir = Path(path) / AppPaths.APP_NAME
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir

    @staticmethod
    def get_config_dir() -> Path:
        """Returns the cross-platform config directory."""
        path = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)
        config_dir = Path(path) / AppPaths.APP_NAME
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    @staticmethod
    def get_db_path():
        # Ensure app name is set for QStandardPaths
        if not QCoreApplication.applicationName():
            QCoreApplication.setApplicationName("SistemManajemenPerpustakaan")
            QCoreApplication.setOrganizationName("Rhnbztnl")

        data_dir = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)
        
        # Clean up path if it accidentally includes the script name (common issue with python scripts)
        if "main_app.py" in data_dir:
            data_dir = data_dir.replace("/main_app.py", "")
            
        path = Path(data_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path / "library.db"

    @staticmethod
    def get_settings_path() -> Path:
        """Returns the full path to the settings file."""
        return AppPaths.get_config_dir() / "settings.json"
