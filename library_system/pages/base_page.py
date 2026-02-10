from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

class BasePage(QWidget):
    """
    Base class for all pages in the application.
    Enforces a common interface.
    """
    # Signal to request navigation to another page (by index or name)
    navigate_to = Signal(int) 

    def __init__(self):
        super().__init__()

    def refresh_data(self):
        """
        Called when the page is shown to refresh its data.
        Should be overridden by subclasses.
        """
        pass
