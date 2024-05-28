import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QStatusBar, \
                            QLabel, QTextEdit, QFileDialog, QDockWidget, QVBoxLayout, \
                            QHBoxLayout, QComboBox, QWidget, QPushButton
from PyQt6.QtGui import QIcon, QAction, QPixmap
from PyQt6.QtCore import Qt
from pathlib import Path
import json

class Image(QLabel):

    def __init__(self, chemin: str):
        super().__init__()

        self.image = QPixmap(chemin)
        self.setPixmap(self.image)

class MainWidget(QWidget):

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
        self.menu_layout.addWidget(self.product_list)
        self.menu_layout.addSpacing(30)
        self.pick_location_button = QPushButton("Sélectionner Position")
        self.menu_layout.addWidget(self.pick_location_button)
        self.random_location_button = QPushButton("Position Aléatoire")
        self.menu_layout.addWidget(self.random_location_button)
        self.menu_layout.addSpacing(30)
        self.generate_path_button = QPushButton("Générer chemin")
        self.menu_layout.addWidget(self.generate_path_button)
        self.main_layout.addLayout(self.menu_layout)
        self.menu_layout.addStretch()

        if not image_path is None:
            self.showPlan()

    def showPlan(self):
        self.image = Image(self.__imagePath)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.image)

class VueSecondApp(QMainWindow):
    def __init__(self, chemin: str = None):
        super().__init__()
        self.setWindowTitle('StorePathFinder')
        self.__imagePath = chemin
        menu_bar = self.menuBar()

        menu_fichier = menu_bar.addMenu('&Fichier')
        menu_nav = menu_bar.addMenu('&Navigation')

        menu_fichier.addAction('Ouvrir Plan', self.setProject)
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
        pass

    def setPos(self):
        pass

    def setGoal(self):
        pass

    def updatePlan(self):
        self.new_product_list = QComboBox()
        self.mainWidget.main_layout.replaceWidget(self.mainWidget.product_list, self.new_product_list)
        self.mainWidget.main_layout.removeWidget(self.mainWidget.image)
        self.mainWidget.showPlan()

    def setProject(self):
        filepath = QFileDialog.getOpenFileName(self, 'Ouvrir plan', str(Path.cwd()), "Json Files (*.json)")
        with open(filepath, 'r') as f:
            self.project_infos = json.load(f)
            self.__imagePath = self.project_infos.image

## -----------------------------------------------------------------------------

if __name__ == "__main__":

    app = QApplication(sys.argv)

    fenetre = VueSecondApp("../images/vide.png")

    sys.exit(app.exec())