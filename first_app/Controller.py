import sys
from PyQt6.QtWidgets import QApplication, QFileDialog
from PyQt6.QtGui import QPixmap
from VueFirstApp import VueFirstApp
from ModeleFirstApp import ModeleFirstApp

class Controller:
    def __init__(self) -> None:
        self.vue = VueFirstApp()
        self.modele = ModeleFirstApp()

        self.vue.newClicked.connect(self.modele.new)
        self.vue.loadClicked.connect(self.load)
        self.vue.main_widget.options.drawClicked.connect(self.draw_grid)
        self.vue.main_widget.options.clearClicked.connect(self.clear_grid)


    def load(self):
        image = QFileDialog.getOpenFileName()[0]
        if image:
            if image[-4:] == ".png" or image[-4:] == ".jpg" or image[-4:] == ".svg" or image[-5:] == ".jpeg":
                self.modele.image_path = image
                self.vue.main_widget.grid.image = image
                self.vue.main_widget.grid.update()

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