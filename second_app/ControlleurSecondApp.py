import sys
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


    def update_vue(self):
        self.vue.setWindowTitle("StorePathFinder - " + self.modele.current_infos["project_name"])

        self.vue.mainWidget.image.image = self.modele.current_infos["image"]
        self.vue.mainWidget.image.update_image()

        self.vue.mainWidget.image.draw_grid(self.modele.current_infos["grid"], self.modele.current_infos["x"],
                                            self.modele.current_infos["y"], self.modele.current_infos["case_size"])



if __name__ == "__main__":

    app = QApplication(sys.argv)

    fenetre = Controller()

    sys.exit(app.exec())