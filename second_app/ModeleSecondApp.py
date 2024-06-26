import json, copy
from PyQt6.QtWidgets import QFileDialog
from pile import Pile

class ModeleSecondApp:

    def __init__(self) -> None:
        self.current_infos = {
            "project_name": "Sans nom",
            "project_author": "Sans nom",
            "shop_name": "Sans nom",
            "shop_address": "Sans nom",
            "file_path": None,
            "image": "../images/vide.png",
            "case_size": 50,
            "x": 0,
            "y": 0,
            "grid": [],
            "pattern": {}
        }

        self.current_position = ()
        self.destination = ()
        self.product_list = []
    

    def open(self):
        """
            Demande a l'utilisateur de selectionner un projet et l'ouvre
        """
        path = QFileDialog.getOpenFileName(caption="Choisissez un projet", filter="Json Files (*.json)")[0]

        if path:
            with open(path, 'r') as f:
                self.current_infos = json.load(f)
                self.current_infos["file_path"] = path
            return True
        return False

    def getProductList(self):
        pass

    def generateAllPaths(self):
        if self.current_position and self.destination:
            final_path = []
            position = self.current_position
            liste_course = copy.deepcopy(self.product_list)
            for i in range(len(liste_course)):
                path_list=  []
                for produit in liste_course:
                    for ligne in self.current_infos["grid"]:
                        for product in ligne:
                            if product and product[1] == produit:
                                path_list.append([produit, self.parcours(self.current_infos["pattern"], position, (self.current_infos["grid"].index(ligne), ligne.index(product))), (self.current_infos["grid"].index(ligne), ligne.index(product))])
                min_path = path_list[0][1]
                min_produit = path_list[0][0]
                min_position = path_list[0][2]
                for produit, path, position in path_list:
                    if len(path) < len(min_path):
                        min_path = path
                        min_produit = produit
                        min_position = position
                final_path += min_path
                position = min_position
                liste_course.remove(min_produit)

            final_path += self.parcours(self.current_infos["pattern"], position, self.destination)

            return final_path

    def parcours(self, dico_graphe:dict, depart:tuple, arrivee:tuple):
        """
            Vieux parcours en profodeur tout nul (manque de temps pour implémenter un truc bien comme un a star par exemple)
        """
        p1:Pile = Pile()
        p1.empiler(depart)

        parcours = []

        while arrivee not in parcours:
            sommet = p1.depiler()
            if sommet:
                parcours.append(sommet)
                for voisin in dico_graphe[sommet].keys():
                    if voisin not in parcours and not p1.contient(voisin):
                        p1.empiler(voisin)
            else:
                print("Erreur, position bloquée")
                return []

        return parcours

    def open_project(self):
        """
            Ouvre un projet 
        """
        path = QFileDialog.getOpenFileName(caption='Ouvrir plan', directory="../projets/", filter="Json Files (*.json)")[0]

        if path:
            with open(path, 'r') as f:
                self.current_infos = json.load(f)
                self.convert_str_to_tuples()
                self.current_infos["file_path"] = path


    def convert_str_to_tuples(self):
        """
            Convertis les chaines de caractere du pattern en tuples
        """
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

