import sys, json
from random import randint
from PyQt6.QtWidgets import QApplication
from VueSecondApp import VueSecondApp
from ModeleSecondApp import ModeleSecondApp
from Popup import Popup
from ProjectInfos import ProjectInfos

class Controller():
    def __init__(self):
        
        self.vue = VueSecondApp()
        self.modele = ModeleSecondApp()
        self.popup = None
        self.project_infos = None

        self.vue.loadClicked.connect(self.open_project)
        self.vue.mainWidget.left.up.selection.addClicked.connect(self.add_article)
        self.vue.mainWidget.left.up.liste.deleteClicked.connect(self.delete_article)
        self.vue.mainWidget.left.buttons.randomStart.connect(self.select_random_pos)
        self.vue.mainWidget.left.buttons.selectStart.connect(self.set_select_start)
        self.vue.mainWidget.left.buttons.selectEnd.connect(self.set_select_end)
        self.vue.mainWidget.image.startClicked.connect(self.select_start)
        self.vue.mainWidget.image.endClicked.connect(self.select_end)
        self.vue.mainWidget.left.generateClicked.connect(self.generate_path)
        self.vue.mainWidget.left.eraseClicked.connect(self.update_vue)
        self.vue.mainWidget.left.up.selection.updateList.connect(self.update_list)
        self.vue.mainWidget.left.buttons.infoClicked.connect(self.set_info_mode)
        self.vue.mainWidget.image.rectClicked.connect(self.show_product_info)
        self.vue.infosClicked.connect(self.show_project_info)


    def add_article(self):
        """
            Ajoute un article
        """
        item = self.vue.mainWidget.left.up.selection.products.currentItem()
        if item:
            if item.text() not in self.modele.product_list:
                self.modele.product_list.append(item.text())
                self.vue.mainWidget.left.up.liste.liste.addItem(item.text())


    def delete_article(self):
        """
            Supprime un article    
        """
        item = self.vue.mainWidget.left.up.liste.liste.currentItem()
        if item:
            self.modele.product_list.remove(item.text())
            self.vue.mainWidget.left.up.liste.liste.takeItem(self.vue.mainWidget.left.up.liste.liste.row(item))
            self.vue.mainWidget.left.up.liste.liste.setCurrentItem(None)


    def update_list(self):
        """
            Modifie la liste d'articles en fonction de la categorie selectionnee
        """
        products = self.get_products(self.vue.mainWidget.left.up.selection.categories.currentText())
        self.vue.mainWidget.left.up.selection.products.clear()
        self.vue.mainWidget.left.up.selection.products.addItems(products)


    def get_products(self, category:str):
        """
            Obtient la liste de produits de la categorie choisie, a partir du fichier liste de produits

            Keyword arguments:
            category -- La categorie dont on doit recuperer les produits
        """
        liste = []
        with open("../Liste de produits-20240513/liste_produits.json", encoding="utf-8") as f:
            products = json.load(f)

        if self.modele.current_infos["grid"]:
            for product in products[category]:
                for ligne in self.modele.current_infos["grid"]:
                    for produit in ligne:
                        if produit and produit[1] == product:
                            liste.append(product)

        return liste


    def open_project(self):
        """
            Ouvre un nouveau projet en lancant la selection du fichier en appelant la foction correspondante du modele
            et en mettant la vue a jour
        """
        self.modele.open_project()
        self.update_vue()


    def select_random_pos(self):
        """
            Choisi une position aleatoire dans la grille
        """
        if self.modele.current_infos["grid"]:
            self.modele.current_position = (randint(1, len(self.modele.current_infos["grid"]))-1, randint(1, len(self.modele.current_infos["grid"][0]))-1)
            self.update_vue()


    def set_select_start(self):
        """
            Active la selection de la position de depart
        """
        self.vue.mainWidget.image.selecting_start = True
        self.vue.mainWidget.left.label.show()


    def set_select_end(self):
        """
            Active la selection de la position d'arrivee
        """
        self.vue.mainWidget.image.selecting_end = True
        self.vue.mainWidget.left.label.show()

    def set_info_mode(self):
        """
            Active le mode informations
        """

        if self.vue.mainWidget.image.info_mode:
            self.vue.mainWidget.image.info_mode = False
            self.vue.mainWidget.left.info_label.hide()
        else:
            self.vue.mainWidget.image.info_mode = True
            self.vue.mainWidget.left.info_label.show()

    def select_start(self, coordinates:tuple):
        """
            Met a jour le modele en changeant la position de depart

            Keyword arguments:
            coordinates -- les coordonnes de la nouvelle position
        """
        if self.modele.current_infos["grid"]:
            self.modele.current_position = coordinates
            self.update_vue()
            self.vue.mainWidget.left.label.hide()

    def select_end(self, coordinates:tuple):
        """
            Met a jour le modele en changeant la position d'arrivee

            Keyword arguments:
            coordinates -- les coordonnes de la nouvelle position
        """
        if self.modele.current_infos["grid"]:
            self.modele.destination = coordinates
            self.update_vue()
            self.vue.mainWidget.left.label.hide()

    def show_product_info(self, coordinates:tuple):
        """
            Affiche une fenêtre d'information sur le produit aux coordonnées données

            Keyword arguments:
            coordinates -- les coordonnees de la case cliquée
        """
        try:
            if self.modele.current_infos["grid"][coordinates[0]][coordinates[1]]:
                self.popup = Popup(coordinates, self.modele.current_infos["grid"][coordinates[0]][coordinates[1]][1])
                self.popup.show()
        except:
            pass

    def show_project_info(self):
        self.project_infos = ProjectInfos(self.modele.current_infos)
        self.project_infos.show()


    def update_vue(self):
        """
            Met a jour la vue a partir des informations du modele
        """
        self.vue.setWindowTitle("StorePathFinder - " + self.modele.current_infos["project_name"])

        # Actualisation de l'image du plan
        self.vue.mainWidget.image.image = self.modele.current_infos["image"]
        self.vue.mainWidget.image.update_image()

        # Actualisation de la grille
        self.vue.mainWidget.image.draw_grid(self.modele.current_infos["grid"], self.modele.current_infos["x"],
                                            self.modele.current_infos["y"], self.modele.current_infos["case_size"])

        # Actualisation des cases d'entrée et de sortie
        if not self.modele.current_position or not self.modele.destination:
            for i in range(len(self.modele.current_infos["grid"])):
                for j in range(len(self.modele.current_infos["grid"][i])):
                    if self.modele.current_infos["grid"][i][j]:
                        if self.modele.current_infos["grid"][i][j][1] == "Entrée":
                            if not self.modele.current_position:
                                self.modele.current_position = (i, j)
                                self.modele.current_infos["grid"][i][j] = None
                        elif self.modele.current_infos["grid"][i][j][1] == "Sortie":
                            if not self.modele.destination:
                                self.modele.destination = (i, j)
                                self.modele.current_infos["grid"][i][j] = None

        # Actualisation du dessin des cases d'entrée et de sortie
        if self.modele.current_position:
            self.vue.mainWidget.image.draw_rect(self.modele.current_position, self.modele.current_infos["x"], self.modele.current_infos["y"],
                                                self.modele.current_infos["case_size"], (0, 0, 255, 200))

        if self.modele.destination:
            self.vue.mainWidget.image.draw_rect(self.modele.destination, self.modele.current_infos["x"], self.modele.current_infos["y"],
                                                self.modele.current_infos["case_size"], (255, 0, 0, 200))

        self.update_list()


    def generate_path(self):
        """
            Genere le chemin
        """
        path = self.modele.generateAllPaths()

        if path:
            self.vue.mainWidget.image.draw_path(path, self.modele.current_infos["x"], self.modele.current_infos["y"],
                                                self.modele.current_infos["case_size"])



if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Controller()
    sys.exit(app.exec())