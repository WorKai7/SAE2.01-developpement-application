import sys
from PyQt6.QtWidgets import QApplication
from ModeleSecondApp import ModeleSecondApp
from VueSecondApp import VueSecondApp, ProjectInfos

class Controller:
    def __init__(self) -> None:

            #Composants
            self.vue = VueSecondApp("../images/vide.png")
            self.modele = ModeleSecondApp()
            self.new_window = None

            #Signaux
            self.vue.mainWidget.selectedPosition.connect(self.modele.setPosition)
            self.vue.mainWidget.selectedDestination.connect(self.modele.addDestination)
            self.vue.mainWidget.generatePathClicked.connect(self.getPath)
            self.vue.mainWidget.fetchProductList.connect(self.getProductList)
            self.vue.loadClicked.connect(self.loadProject)
            self.vue.infosClicked.connect(self.show_infos)

    def show_infos(self):
          self.new_window = ProjectInfos(self.modele.current_infos)
          self.new_window.show()

    def getPath(self):
          path = self.modele.generateFullPath(self.modele.current_position, self.modele.destinations)

    def getProductList(self):
          self.vue.mainWidget.fillProductList(self.modele.getProductList())

    def loadProject(self):
          if self.modele.open():
                self.vue.updateInfos(self.modele.current_infos)

#-----------------------------------------------------

if __name__ == "__main__":

    app = QApplication(sys.argv)
    fenetre = Controller()
    sys.exit(app.exec())