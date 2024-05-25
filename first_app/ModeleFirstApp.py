import json
from PyQt6.QtWidgets import QFileDialog

class ModeleFirstApp:

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



    def save(self):
        if not self.current_infos["file_path"]:
            self.save_as()
        else:
            with open(self.current_infos["file_path"], 'w') as f:
                json.dump(self.current_infos, f, indent=4)


    def save_as(self):
        path = QFileDialog.getSaveFileName(caption="Enregistrer sous", directory="../projets", filter="Projet JSON")[0]
        if path:
            self.current_infos["file_path"] = path
            with open(path, 'w') as f:
                json.dump(self.current_infos, f, indent=4)

    def open(self):
        path = QFileDialog.getOpenFileName(caption="Choisissez un projet", filter="Projet JSON (*.json)")[0]
        if path:
            with open(path, 'r') as f:
                self.current_infos = json.load(f)
                self.current_infos["file_path"] = path
            return True
        return False


    def load_image(self):
        image = QFileDialog.getOpenFileName(caption="Sélectionner un plan", directory="../images", filter="Images (*.png *.jpg *.jpeg *.svg)")[0]
        if image:
            self.current_infos["image"] = image
            return True
        return False


    def create_grid(self, size:tuple):
        grille = []

        for i in range(size[1]):
            row = []
            for j in range(size[0]):
                row.append(size[2])
            grille.append(row)

        self.current_infos["grid"] = grille