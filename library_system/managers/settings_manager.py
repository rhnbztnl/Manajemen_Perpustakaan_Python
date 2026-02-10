from PySide6.QtCore import QSettings

class SettingsManager:
    _instance = None
    
    DEFAULTS = {
        "general/library_name": "Perpustakaan Daerah",
        "general/location": "Jakarta, Indonesia",
        "general/language": "Indonesia",
        "general/date_format": "dd/MM/yyyy",
        
        "appearance/theme": "Light",
        "appearance/font_size": "Normal",
        "appearance/density": "Comfortable",
        
        "loans/duration_days": 7,
        "loans/max_books": 3,
        "loans/fine_enabled": True,
        "loans/fine_per_day": 2000,
        
        "system/db_path": "library.db" # Relative path default
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            cls._instance.settings = QSettings("MyCompany", "LibrarySystem")
        return cls._instance

    def get(self, key, type_cls=None):
        """
        Get setting value. 
        key: 'category/setting_name'
        type_cls: int, bool, str (optional type casting)
        """
        default = self.DEFAULTS.get(key)
        val = self.settings.value(key, default)
        
        if type_cls:
            if type_cls == bool:
                return str(val).lower() == 'true'
            try:
                return type_cls(val)
            except:
                return default
        return val

    def set(self, key, value):
        self.settings.setValue(key, value)
        # Sync immediately
        self.settings.sync()

    def get_all(self):
        """Debug method to see all stored settings"""
        return self.settings.allKeys()
