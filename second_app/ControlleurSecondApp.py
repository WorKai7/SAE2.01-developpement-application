import sys
from random import randint
from PyQt6.QtWidgets import QApplication
from VueSecondApp import VueSecondApp
from ModeleSecondApp import ModeleSecondApp
from Popup import Popup
import json

class Controller():
    def __init__(self):
        
        self.vue = VueSecondApp()
        self.modele = ModeleSecondApp()
        self.popup = None

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


    def add_article(self):
        item = self.vue.mainWidget.left.up.selection.products.currentItem()
        if item:
            if item.text() not in self.modele.product_list:
                self.modele.product_list.append(item.text())
                self.vue.mainWidget.left.up.liste.liste.addItem(item.text())


    def delete_article(self):
        item = self.vue.mainWidget.left.up.liste.liste.currentItem()
        if item:
            self.modele.product_list.remove(item.text())
            self.vue.mainWidget.left.up.liste.liste.takeItem(self.vue.mainWidget.left.up.liste.liste.row(item))
            self.vue.mainWidget.left.up.liste.liste.setCurrentItem(None)


    def update_list(self):
        products = self.get_products(self.vue.mainWidget.left.up.selection.categories.currentText())
        self.vue.mainWidget.left.up.selection.products.clear()
        self.vue.mainWidget.left.up.selection.products.addItems(products)

    def get_products(self, category:str):
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
        self.modele.open_project()
        self.update_vue()


    def select_random_pos(self):
        if self.modele.current_infos["grid"]:
            self.modele.current_position = (randint(1, len(self.modele.current_infos["grid"]))-1, randint(1, len(self.modele.current_infos["grid"][0]))-1)
            self.update_vue()


    def set_select_start(self):
        self.vue.mainWidget.image.selecting_start = True
        self.vue.mainWidget.left.label.show()


    def set_select_end(self):
        self.vue.mainWidget.image.selecting_end = True
        self.vue.mainWidget.left.label.show()


    def select_start(self, coordinates:tuple):
        if self.modele.current_infos["grid"]:
            self.modele.current_position = coordinates
            self.update_vue()
            self.vue.mainWidget.left.label.hide()


    def select_end(self, coordinates:tuple):
        if self.modele.current_infos["grid"]:
            self.modele.destination = coordinates
            self.update_vue()
            self.vue.mainWidget.left.label.hide()


    def update_vue(self):
        self.vue.setWindowTitle("StorePathFinder - " + self.modele.current_infos["project_name"])

        self.vue.mainWidget.image.image = self.modele.current_infos["image"]
        self.vue.mainWidget.image.update_image()

        self.vue.mainWidget.image.draw_grid(self.modele.current_infos["grid"], self.modele.current_infos["x"],
                                            self.modele.current_infos["y"], self.modele.current_infos["case_size"])

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

        if self.modele.current_position:
            self.vue.mainWidget.image.draw_rect(self.modele.current_position, self.modele.current_infos["x"], self.modele.current_infos["y"],
                                                self.modele.current_infos["case_size"], (0, 0, 255, 200))

        if self.modele.destination:
            self.vue.mainWidget.image.draw_rect(self.modele.destination, self.modele.current_infos["x"], self.modele.current_infos["y"],
                                                self.modele.current_infos["case_size"], (255, 0, 0, 200))

        self.update_list()

    def generate_path(self):
        path = self.modele.generateAllPaths()

        if path:
            self.vue.mainWidget.image.draw_path(path, self.modele.current_infos["x"], self.modele.current_infos["y"],
                                                self.modele.current_infos["case_size"])



if __name__ == "__main__":

    app = QApplication(sys.argv)

    fenetre = Controller()

    sys.exit(app.exec())