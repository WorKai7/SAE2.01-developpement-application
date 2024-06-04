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
        self.destinations = []
    
    def open(self):
        path = QFileDialog.getOpenFileName(caption="Choisissez un projet", filter="Json Files (*.json)")[0]
        if path:
            with open(path, 'r') as f:
                self.current_infos = json.load(f)
                self.current_infos["file_path"] = path
            return True
        return False

    def getProductList(self) -> list:
        pass

    def generateFullPath(self, start, product_list: list) ->list:
        full_path = []
        while len(product_list) != 0:
            min_path = self.generatePathToDestination(start, product_list[0])
            min_path_len = len(min_path)
            product_to_remove = product_list[0]
            for product in product_list:
                path = self.generatePathToDestination(start, product)
                path_len = len(path)
                if len(path) < min_path_len:
                    min_path = path
                    min_path_len = path_len
                    product_to_remove = product
            full_path.append(path)
            product_list.remove(product_to_remove)
            start = product_to_remove
        return full_path

    def generatePathToDestination(self, start, end) -> list:
        pass

    def setPosition(self, randomness: bool, position: list):
        if randomness:
            self.current_position = [random.randint(0, len(self.current_infos['grid'][0])- 1), random.randint(0, len(self.current_infos['grid'][1])- 1)]
        else:
            self.current_position = position

    def addDestination(self, destination: list):
        self.destinations.append(destination)

