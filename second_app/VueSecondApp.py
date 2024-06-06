import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QStatusBar, \
                            QLabel, QTextEdit, QFileDialog, QDockWidget, QVBoxLayout, \
                            QHBoxLayout, QComboBox, QWidget, QPushButton
from PyQt6.QtGui import QIcon, QAction, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from pathlib import Path

class ProjectInfos(QWidget):
    def __init__(self, infos: dict):
        super().__init__()
        self.projectInfos = infos

        self.author = QLabel(self.projectInfos['project_author'])
        self.project_name = QLabel(self.projectInfos["project_name"])
        self.shop_name = QLabel("shop_name")
        self.shop_address = QLabel(self.projectInfos["shop_address"])

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(self.author)
        self.main_layout.addWidget(self.project_name)
        self.main_layout.addWidget(self.shop_name)
        self.main_layout.addWidget(self.shop_address)

        self.show()

class Image(QLabel):

    def __init__(self, chemin: str):
        super().__init__()

        self.image = QPixmap(chemin)
        self.setPixmap(self.image)

class MainWidget(QWidget):

    selectedPosition = pyqtSignal(bool, list)
    selectedDestination = pyqtSignal()
    generatePathClicked = pyqtSignal()
    fetchProductList = pyqtSignal()

    def __init__(self, image_path: str):
        super().__init__()

        self.__imagePath = image_path
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.menu_layout = QVBoxLayout()

        self.menu_layout.addStretch()

        self.product_list_label = QLabel("Produit Destination")
        self.menu_layout.addWidget(self.product_list_label)
        self.product_list = QComboBox()
        self.product_list.currentIndexChanged.connect(self.destinationPicked)
        self.menu_layout.addWidget(self.product_list)

        self.menu_layout.addSpacing(30)

        self.pick_location_button = QPushButton("Sélectionner Position")
        self.pick_location_button.clicked.connect(self.setLocation)
        self.menu_layout.addWidget(self.pick_location_button)

        self.random_location_button = QPushButton("Position Aléatoire")
        self.random_location_button.clicked.connect(self.setRandomPosition)
        self.menu_layout.addWidget(self.random_location_button)

        self.menu_layout.addSpacing(30)

        self.generate_path_button = QPushButton("Générer chemin")
        self.generate_path_button.clicked.connect(self.generatePath)
        self.menu_layout.addWidget(self.generate_path_button)

        self.menu_layout.addStretch()

        self.main_layout.addLayout(self.menu_layout)

        if not image_path is None:
            self.showPlan()

    def getProductList(self):
        self.fetchProductList.emit()

    def fillProductList(self, product_list: list):
        for product in product_list:
            self.product_list.addItem(product)

    def showPlan(self, image_path = None):
        if image_path != None:
            self.__imagePath = image_path
        self.image = Image(self.__imagePath)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.main_layout.count() != 0:
            self.main_layout.addWidget(self.image)
        else:
            self.main_layout.removeWidget(self.main_layout.itemAt(0))
            self.main_layout.addWidget(self.image)

    def setRandomPosition(self):
        self.selectedPosition.emit(True, [])

    def setLocation(self):
        location = [0,0] ##Récupérer endroit cliqué par l'utilisateur puis envoyer dans signal
        self.selectedPosition.emit(False, location)

    def destinationPicked(self):
        self.selectedDestination.emit()

    def generatePath(self):
        self.generatePathClicked.emit()

    def showPathToDestination(self, path: list):
        pass

class VueSecondApp(QMainWindow):

    loadClicked = pyqtSignal(str)
    infosClicked = pyqtSignal()

    def __init__(self, chemin: str = None):
        super().__init__()
        self.setWindowTitle('StorePathFinder')
        self.__imagePath = chemin
        menu_bar = self.menuBar()

        menu_fichier = menu_bar.addMenu('&Fichier')
        menu_nav = menu_bar.addMenu('&Navigation')

        menu_fichier.addAction('Ouvrir Plan', self.setProject)
        menu_fichier.addAction('Infos Plan', self.viewInfos)
        menu_fichier.addSeparator()
        menu_fichier.addAction('Quitter', self.destroy)

        menu_nav.addAction('Sélectionner Position', self.setPos)
        menu_nav.addAction('Sélectionner Destination', self.setGoal)
        menu_fichier.addSeparator()
        menu_nav.addAction('Générer chemin', self.getPathToProduct)

        self.mainWidget = MainWidget(self.__imagePath)
        self.setCentralWidget(self.mainWidget)

        self.show()

    def getPathToProduct(self):
        self.mainWidget.generatePath()

    def setPos(self):
        self.mainWidget.setLocation()

    def setGoal(self):
        self.mainWidget.destinationPicked()

    def updatePlan(self, image_path = None):
        self.new_product_list = QComboBox()
        self.mainWidget.main_layout.replaceWidget(self.mainWidget.product_list, self.new_product_list)
        self.mainWidget.getProductList()
        self.mainWidget.main_layout.removeWidget(self.mainWidget.image)
        self.mainWidget.showPlan(image_path)

    def setProject(self):
        filepath = QFileDialog.getOpenFileName(self, 'Ouvrir plan', str(Path.cwd()), "Json Files (*.json)")
        self.loadClicked.emit(filepath[0])

    def viewInfos(self):
        self.infosClicked.emit()

    def updateInfos(self, infos: dict):
        self.project_infos = infos
        self.__imagePath = self.project_infos["image"]
        self.updatePlan(self.__imagePath)


## -----------------------------------------------------------------------------

if __name__ == "__main__":

    app = QApplication(sys.argv)

    fenetre = VueSecondApp("../images/vide.png")

    sys.exit(app.exec())