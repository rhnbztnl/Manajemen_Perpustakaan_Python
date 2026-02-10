import json
from library_system.utils.paths import AppPaths

class ConfigManager:
    _instance = None
    _default_config = {
        "theme": "Light",
        "font_size": 13,
        "language": "en"
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.config_file = AppPaths.get_settings_path()
            cls._instance.config = cls._instance.load_config()
        return cls._instance

    def load_config(self):
        if not self.config_file.exists():
            return self._default_config.copy()
        
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._default_config.copy()

    def save_config(self):
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()
