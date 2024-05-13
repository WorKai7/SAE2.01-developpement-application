import sys
from PyQt6.QtWidgets import QApplication
from VueFirstApp import VueFirstApp
from ModeleFirstApp import ModeleFirstApp

class Controller:
    def __init__(self) -> None:
        self.vue = VueFirstApp()
        self.modele = ModeleFirstApp()

        self.vue.newClicked.connect(self.modele.new)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    fenetre = Controller()
    sys.exit(app.exec())