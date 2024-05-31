import sys
from PyQt6.QtWidgets import QApplication, QFileDialog
from PyQt6.QtGui import QPixmap
from VueFirstApp import VueFirstApp
from ModeleFirstApp import ModeleFirstApp
from NewProjectApp import NewProjectApp

class Controller:
    def __init__(self) -> None:
        self.vue = VueFirstApp()
        self.modele = ModeleFirstApp()
        self.new_window = None
        self.update_product_list()

        self.vue.newClicked.connect(self.new)
        self.vue.loadClicked.connect(self.load)
        self.vue.saveClicked.connect(self.modele.save)
        self.vue.saveasClicked.connect(self.modele.save_as)
        self.vue.openClicked.connect(self.open)
        self.vue.main_widget.options.categoryChanged.connect(self.update_product_list)
        self.vue.main_widget.options.drawClicked.connect(self.draw_grid)
        self.vue.main_widget.options.clearClicked.connect(self.clear_grid)

        self.vue.main_widget.options.products.addItem("bruh")
        self.vue.main_widget.options.products.addItem("Poisson")


    def new(self):
        self.new_window = NewProjectApp()
        self.new_window.show()

        self.new_window.infosSignal.connect(self.create_project)

    def create_project(self, d:dict):
        self.modele.current_infos = d
        self.update_vue(self.modele.current_infos["image"], self.modele.current_infos["project_name"], self.modele.current_infos["file_path"])

    def load(self):
        image = QFileDialog.getOpenFileName(caption="Sélectionner un plan", filter="Fichier PNG (*.png) ;; Fichier JPG (*.jpg *.jpeg) ;; Fichier SVG (*.svg)")[0]
        if image:
            self.modele.current_infos["image"] = image
            self.update_vue()

    def open(self):
        if self.modele.open():
            self.update_vue()

    def update_vue(self):
        self.vue.setWindowTitle(self.modele.current_infos["project_name"] + " - " + self.modele.current_infos["file_path"])
        self.vue.main_widget.grid.image = self.modele.current_infos["image"]
        self.vue.main_widget.grid.update()

    def update_product_list(self):
        products = self.modele.get_products(self.vue.main_widget.options.category.currentText())
        self.vue.main_widget.options.products.clear()
        self.vue.main_widget.options.products.addItems(products)

    def draw_grid(self, size:tuple):
        if self.vue.main_widget.grid.grid:
            self.vue.main_widget.grid.clear_grid()

        self.vue.main_widget.grid.width = size[0]
        self.vue.main_widget.grid.height = size[1]
        self.vue.main_widget.grid.draw_grid()

    def clear_grid(self):
        self.vue.main_widget.grid.clear_grid()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    fenetre = Controller()
    sys.exit(app.exec())