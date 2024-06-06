import sys, json
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QStatusBar, \
                            QLabel, QTextEdit, QFileDialog, QDockWidget, QVBoxLayout, \
                            QHBoxLayout, QComboBox, QWidget, QPushButton, QAbstractItemView, \
                            QListWidget
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

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout() ; self.setLayout(layout)

        self.left = Left()
        self.left.setMaximumWidth(800)
        self.image = Image("../images/vide.png")

        layout.addWidget(self.left)
        layout.addWidget(self.image, alignment=Qt.AlignmentFlag.AlignCenter)




    def getProductList(self):
        self.fetchProductList.emit()

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


class Left(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout() ; self.setLayout(layout)

        self.up = Up()
        self.buttons = Buttons()
        self.way_button = QPushButton("Génerer le chemin")

        layout.addWidget(self.up)
        layout.addWidget(self.buttons)
        layout.addSpacing(10)
        layout.addWidget(self.way_button)


class Selection(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout() ; self.setLayout(layout)

        self.label = QLabel("Séletionnez vos articles:")

        self.categories = QComboBox()
        self.categories.addItems(["Légumes", "Poissons", "Viandes", "Épicerie", "Épicerie sucrée", "Petit déjeuner", "Fruits", "Rayon frais", "Crèmerie", "Conserves", "Apéritifs", "Boissons", "Articles Maison", "Hygiène", "Bureau", "Animaux"])

        self.products = QListWidget()
        self.products.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.update_product_list()

        self.categories.currentTextChanged.connect(self.update_product_list)

        layout.addWidget(self.label)
        layout.addWidget(self.categories)
        layout.addWidget(self.products)

    def update_product_list(self):
        products = self.get_products(self.categories.currentText())
        self.products.clear()
        self.products.addItems(products)

        # Check dans la liste de produits et mettre en statue "sélectionné" les articles qui y sont
        # Fraudra probablement déplacer la fonction

    def get_products(self, category:str):
        products = []
        with open("../Liste de produits-20240513/liste_produits.json", encoding="utf-8") as f:
            products = json.load(f)

        return products.get(category, [])

class Liste(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout() ; self.setLayout(layout)

        self.list_label = QLabel("Votre liste de courses:")
        self.liste = QListWidget()
        self.liste.setDisabled(True)
        self.clear_button = QPushButton("Vider la liste")

        layout.addWidget(self.list_label)
        layout.addWidget(self.liste)
        layout.addWidget(self.clear_button)

class Up(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout() ; self.setLayout(layout)

        self.left = Selection()
        self.right = Liste()

        layout.addWidget(self.left)
        layout.addSpacing(20)
        layout.addWidget(self.right)


class Buttons(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout() ; self.setLayout(layout)

        self.pos_button = QPushButton("Choisir une position")
        self.random_pos_button = QPushButton("Position aléatoire")
        self.end_button = QPushButton("Choisir la position d'arrivée")

        layout.addWidget(self.pos_button)
        layout.addWidget(self.random_pos_button)
        layout.addWidget(self.end_button)


class VueSecondApp(QMainWindow):

    loadClicked = pyqtSignal(str)
    infosClicked = pyqtSignal()

    def __init__(self, chemin: str = None):
        super().__init__()

        self.resize(1200, 720)
        self.setWindowTitle('StorePathFinder')
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

        self.mainWidget = MainWidget()
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

    fenetre = VueSecondApp()

    sys.exit(app.exec())