import json
from PyQt6.QtWidgets import QFileDialog
import random
from filepile import File, Pile
import copy

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
        self.current_position = []
        self.destination = []
        self.product_list = []
    
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

    def generatePathToDestination(self, dico_graphe: dict, depart: tuple, arrivee: tuple):
        '''La fonction effectue un parcours en profondeur et retourne un chemin entre le départ & l'arrivée'''

        assert isinstance(dico_graphe, dict), "L'argument utilisé n'est pas conforme : type dict() attendu."   # vérification de l'argument

        voisins = Pile(64)
        voisins.empiler(depart)
        parcours = []
        liste_parcours = []
        while voisins.est_vide() == False:
            sommet = voisins.depiler()
            parcours.append(sommet)
            if sommet == arrivee:
                parcours2 = copy.deepcopy(parcours)
                liste_parcours.append(parcours2)

            for voisin in dico_graphe[sommet].keys():
                if (voisin not in parcours):
                    voisins.empiler(voisin)
                elif len(dico_graphe[sommet].keys()) == 1 and voisin in parcours and sommet != arrivee:
                    old_sommet = parcours[parcours.index(sommet)-1]
                    parcours.remove(sommet)
                    sommet = old_sommet
                    while len(dico_graphe[sommet].keys()) == 2:
                        old_sommet = parcours[parcours.index(old_sommet)-1]
                        parcours.remove(sommet)
                        sommet = old_sommet

        return liste_parcours

    def setPosition(self, random: bool, position: list):
        if random:
            self.current_position = [random.randint(0, len(self.current_infos['grid'][0])- 1), random.randint(0, len(self.current_infos['grid'][1])- 1)]
        else:
            self.current_position = position

    def setDestination(self, destination: list):
        pass

    def open_project(self):
        path = QFileDialog.getOpenFileName(caption='Ouvrir plan', directory="../projets/", filter="Json Files (*.json)")[0]
        with open(path, 'r') as f:
            self.current_infos = json.load(f)

