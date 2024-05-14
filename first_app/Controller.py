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


    def load(self):
        image = QFileDialog.getOpenFileName()[0]
        if image:
            if image[-4:] == ".png" or image[-4:] == ".jpg" or image[-4:] == ".svg" or image[-5:] == ".jpeg":
                self.modele.image_path = image
                self.vue.main_widget.image.setPixmap(QPixmap(image).scaledToHeight(int(QApplication.screens()[0].size().height()*0.7)))




if __name__ == "__main__":

    app = QApplication(sys.argv)
    fenetre = Controller()
    sys.exit(app.exec())