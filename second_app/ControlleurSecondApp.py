import sys
from random import randint
from PyQt6.QtWidgets import QApplication
from VueSecondApp import VueSecondApp
from ModeleSecondApp import ModeleSecondApp

class Controller():
    def __init__(self):
        
        self.vue = VueSecondApp()
        self.modele = ModeleSecondApp()

        self.vue.loadClicked.connect(self.open_project)
        self.vue.mainWidget.left.up.selection.addClicked.connect(self.add_article)
        self.vue.mainWidget.left.up.liste.deleteClicked.connect(self.delete_article)
        self.vue.mainWidget.left.buttons.randomStart.connect(self.select_random_pos)
        self.vue.mainWidget.left.buttons.selectStart.connect(self.set_select_start)
        self.vue.mainWidget.left.buttons.selectEnd.connect(self.set_select_end)
        self.vue.mainWidget.image.startClicked.connect(self.select_start)
        self.vue.mainWidget.image.endClicked.connect(self.select_end)


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


    def open_project(self):
        self.modele.open_project()
        self.update_vue()


    def select_random_pos(self):
        if self.modele.current_infos["grid"]:
            self.modele.current_position = [randint(1, len(self.modele.current_infos["grid"]))-1, randint(1, len(self.modele.current_infos["grid"][0]))-1]
            self.update_vue()


    def set_select_start(self):
        self.vue.mainWidget.image.selecting_start = True
        self.vue.mainWidget.left.label.show()


    def set_select_end(self):
        self.vue.mainWidget.image.selecting_end = True
        self.vue.mainWidget.left.label.show()

    def select_start(self, coordinates:tuple):
        if self.modele.current_infos["grid"]:
            self.modele.current_position = [coordinates[0], coordinates[1]]
            self.update_vue()
            self.vue.mainWidget.left.label.hide()

    def select_end(self, coordinates:tuple):
        if self.modele.current_infos["grid"]:
            self.modele.destination = [coordinates[0], coordinates[1]]
            self.update_vue()
            self.vue.mainWidget.left.label.hide()


    def update_vue(self):
        self.vue.setWindowTitle("StorePathFinder - " + self.modele.current_infos["project_name"])

        self.vue.mainWidget.image.image = self.modele.current_infos["image"]
        self.vue.mainWidget.image.update_image()

        self.vue.mainWidget.image.draw_grid(self.modele.current_infos["grid"], self.modele.current_infos["x"],
                                            self.modele.current_infos["y"], self.modele.current_infos["case_size"])

        if self.modele.current_position:
            self.vue.mainWidget.image.draw_rect(self.modele.current_position, self.modele.current_infos["x"], self.modele.current_infos["y"],
                                                self.modele.current_infos["case_size"], (0, 0, 255, 200))

        if self.modele.destination:
            self.vue.mainWidget.image.draw_rect(self.modele.destination, self.modele.current_infos["x"], self.modele.current_infos["y"],
                                                self.modele.current_infos["case_size"], (255, 0, 0, 200))


if __name__ == "__main__":

    app = QApplication(sys.argv)

    fenetre = Controller()

    sys.exit(app.exec())