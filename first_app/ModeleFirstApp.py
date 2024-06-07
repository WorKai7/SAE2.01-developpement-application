import json
from PyQt6.QtWidgets import QFileDialog

class ModeleFirstApp:

    def __init__(self) -> None:
        self.current_infos = {
            "project_name": "Sans nom",
            "project_author": "Sans nom",
            "shop_name": "Sans nom",
            "shop_address": "Sans nom",
            "file_path": "",
            "image": "../images/vide.png",
            "case_size": 50,
            "x": 0,
            "y": 0,
            "grid": [],
            "pattern": {}
        }



    def save(self):
        if not self.current_infos["file_path"]:
            self.save_as()
        else:
            with open(self.current_infos["file_path"], 'w', encoding="utf8") as f:
                self.convert_tuples_to_str()
                json.dump(self.current_infos, f, indent=4)
                self.convert_str_to_tuples()


    def save_as(self):
        path = QFileDialog.getSaveFileName(caption="Enregistrer sous", directory="../projets", filter="Projet JSON")[0] + ".json"
        if path:
            self.current_infos["file_path"] = path
            with open(path, 'w', encoding="utf8") as f:
                self.convert_tuples_to_str()
                json.dump(self.current_infos, f, indent=4)
                self.convert_str_to_tuples()

    def open(self):
        path = QFileDialog.getOpenFileName(caption="Choisissez un projet", directory="../projets", filter="Projet JSON (*.json)")[0]
        if path:
            with open(path, 'r', encoding="utf8") as f:
                self.current_infos = json.load(f)
                self.convert_str_to_tuples()
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
        pattern = {}

        for i in range(size[1]):
            row = []
            for j in range(size[0]):
                row.append(None)
                sommet = (i, j)
                pattern[sommet] = {}

                if i > 0:
                    pattern[sommet][(i-1, j)] = 1
                if i < size[1]-1:
                    pattern[sommet][(i+1, j)] = 1
                if j > 0:
                    pattern[sommet][(i, j-1)] = 1
                if j < size[0]-1:
                    pattern[sommet][(i, j+1)] = 1

            grille.append(row)

        self.current_infos["grid"] = grille
        self.current_infos["pattern"] = pattern

    def convert_tuples_to_str(self):
        converted_pattern = {}

        for key, value in self.current_infos["pattern"].items():
            converted_pattern[str(key)] = {}
            for key2, value2 in value.items():
                converted_pattern[str(key)][str(key2)] = value2

        self.current_infos["pattern"] = converted_pattern

    def convert_str_to_tuples(self):
        converted_pattern = {}

        for key, value in self.current_infos["pattern"].items():
            first_value = ""
            i = 1
            while key[i] != ",":
                first_value += key[i]
                i += 1

            second_value = ""
            i = -2
            while key[i] != " ":
                second_value += key[i]
                i -= 1

            second_value = second_value[::-1]

            converted_pattern[(int(first_value), int(second_value))] = {}
            for key2, value2 in value.items():
                first_value2 = ""
                i = 1
                while key2[i] != ",":
                    first_value2 += key2[i]
                    i += 1

                second_value2 = ""
                i = -2
                while key2[i] != " ":
                    second_value2 += key2[i]
                    i -= 1

                second_value2 = second_value2[::-1]

                converted_pattern[(int(first_value), int(second_value))][(int(first_value2), int(second_value2))] = value2

        self.current_infos["pattern"] = converted_pattern