import json
from PyQt6.QtWidgets import QFileDialog, QApplication
from NewProjectApp import NewProjectApp

class ModeleFirstApp:

    def __init__(self) -> None:
        self.new_window = None
        self.current_infos = {}
        self.image_path = None
        self.grid = []
        self.grid_width = 0
        self.grid_height = 0


    def new(self):
        self.new_window = NewProjectApp()
        self.new_window.show()

        self.new_window.infosSignal.connect(self.create_file)

    def create_file(self, d:dict):
        self.current_infos = d

        with open(self.current_infos["file_path"], 'w') as f:
            json.dump(self.current_infos, f, indent=4)