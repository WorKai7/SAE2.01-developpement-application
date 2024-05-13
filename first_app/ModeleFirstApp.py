from PyQt6.QtWidgets import QFileDialog, QApplication
from NewProjectApp import NewProjectApp

class ModeleFirstApp:
    def __init__(self) -> None:
        self.new_window = None

    def new(self):
        self.new_window = NewProjectApp()
        self.new_window.show()