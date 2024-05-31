import json
from PyQt6.QtWidgets import QFileDialog
import random

class ModeleSecondApp:

    def __init__(self) -> None:
        self.current_infos = {
            "project_name": "Sans nom",
            "project_author": "Sans nom",
            "shop_name": "Sans nom",
            "shop_address": "Sans nom",
            "file_path": None,
            "image": "../images/vide.png",
            "x": 0,
            "y": 0,
            "grid": []
        }
        self.current_position = [0, 0]
        self.destination = []
    
    def open(self):
        path = QFileDialog.getOpenFileName(caption="Choisissez un projet", filter="Json Files (*.json)")[0]
        if path:
            with open(path, 'r') as f:
                self.current_infos = json.load(f)
                self.current_infos["file_path"] = path
            return True
        return False

    def getProductList(self):
        pass

    def generatePathToDestination(self):
        pass

    def setPosition(self, random: bool, position: list):
        if random:
            self.current_position = [random.randint(0, len(self.current_infos['grid'][0])- 1), random.randint(0, len(self.current_infos['grid'][1])- 1)]
        else:
            self.current_position = position

    def setDestination(self, destination: list):
        pass

    def loadProject(self, path: str):
        with open(path, 'r') as f:
            self.current_infos = json.load(f)

