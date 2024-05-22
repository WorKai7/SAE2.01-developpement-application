import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtWidgets import QWidget


class VueFirstApp(QMainWindow):
    '''
        Classe VueFirstApp: correpond à la classe de la vue de la première application pour la création de magasins.
        Elle ne représente que le visuel et est liée au modèle dans le fichier Controller.py
    '''

    newClicked = pyqtSignal()
    loadClicked = pyqtSignal()
    saveClicked = pyqtSignal()
    saveasClicked = pyqtSignal()
    openClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.resize(int(QApplication.screens()[0].size().width()), int(QApplication.screens()[0].size().height()))
        self.setWindowTitle("Projet sans nom")

        # Barre de menu et catégories
        menu_bar = self.menuBar()

        menu_fichier = menu_bar.addMenu("&Fichier")
        menu_fichier.addAction("Nouveau", self.new)
        menu_fichier.addAction("Ouvrir", self.open)
        menu_fichier.addAction("Enregistrer", self.save)
        menu_fichier.addAction("Enregistrer sous..", self.save_as)

        menu_edition = menu_bar.addMenu("&Edition")
        menu_edition.addAction("Charger un plan de magasin", self.load)

        menu_theme = menu_bar.addMenu("&Thèmes")
        menu_theme.addAction("Clair", self.applyBrightTheme)
        menu_theme.addAction("Sombre", self.applyDarkTheme)
        menu_theme.addAction("Défaut", self.resetTheme)

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        self.show()
        

    def applyBrightTheme(self):
        '''
            Méthode applyBrightTheme: permet à l'utilisateur de basculer vers le thème clair
        '''

        fichier_style = open("../fichiers_qss/lightstyle.qss", 'r')
        with fichier_style:
            qss = fichier_style.read()
            self.setStyleSheet(qss)

    def applyDarkTheme(self):
        '''
            Méthode applyDarkTheme: permet à l'utilisateur de basculer vers le thème sombre
        '''

        fichier_style = open("../fichiers_qss/darkstyle.qss", 'r')
        with fichier_style:
            qss = fichier_style.read()
            self.setStyleSheet(qss)

    def resetTheme(self):
        '''
            Méthode resetTheme: permet à l'utilisateur de basculer vers le thème par défaut
        '''

        self.setStyleSheet('')

    def new(self):
        '''
            Méthode new: permet à l'utilisateur de créer un nouveau magasin
            Elle émet simplement un signal vers l'extérieur
        '''
        
        self.newClicked.emit()

    def open(self):
        '''
            Méthode open: permet à l'utilisateur d'ouvrir un fichier de magasin
            Elle émet simplement un signal vers l'extérieur
        '''

        self.openClicked.emit()

    def save(self):
        '''
            Méthode save: permet à l'utilisateur d'enregistrer le magasin courant
            Elle émet simplement un signal vers l'extérieur
        '''

        self.saveClicked.emit()

    def save_as(self):
        '''
            Méthode save_as: permet à l'utilisateur d'enregistrer le magasin courant à l'emplacement choisi
            Elle émet simplement un signal vers l'extérieur
        '''

        self.saveasClicked.emit()

    def load(self):
        '''
            Méthode load: permet à l'utilisateur de charger le plan d'un magasin
            Elle émet simplement un signal vers l'extérieur
        '''

        self.loadClicked.emit()


class MainWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QHBoxLayout() ; self.setLayout(layout)

        self.options = Options()
        self.grid = Grid()

        layout.addWidget(self.options)
        layout.addWidget(self.grid)

class Grid(QLabel):
    def __init__(self) -> None:
        super().__init__()
        self.image = "../images/vide.png"
        self.grid = []
        self.pixmap = QPixmap(self.image)
        self.setPixmap(self.pixmap)

    def draw_grid(self, grid:list):
        width = len(grid[0])
        height = len(grid)
        pixmap = self.pixmap
        painter = QPainter(pixmap)

        for i in range(height):
            row = []
            for j in range(width):
                case = QRect(i*30, j*30, 30, 30)
                painter.drawRect(case)
                row.append(case)
            self.grid.append(row)
        self.setPixmap(pixmap)
        painter.end()

    def clear_grid(self):
        self.grid.clear()
        self.pixmap = QPixmap(self.image)
        self.setPixmap(self.pixmap)



class Options(QWidget):

    drawClicked = pyqtSignal(tuple)
    clearClicked = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self.setFixedSize(int(QApplication.screens()[0].size().width()*0.3), int(QApplication.screens()[0].size().height()*0.3))

        layout = QVBoxLayout() ; self.setLayout(layout)

        self.row_label = QLabel("Nombre de lignes")
        self.row_number = QSpinBox()
        self.column_label = QLabel("Nombre de colonnes")
        self.column_number = QSpinBox()
        self.draw_grid_button = QPushButton("Dessiner la grille")
        self.clear_grid_button = QPushButton("Effacer la grille")

        layout.addWidget(self.row_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.row_number, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.column_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.column_number, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.draw_grid_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.clear_grid_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.draw_grid_button.clicked.connect(self.dessinClicked)
        self.clear_grid_button.clicked.connect(self.effaceClicked)


    def dessinClicked(self):
        self.drawClicked.emit((self.column_number.value(), self.row_number.value()))

    def effaceClicked(self):
        self.clearClicked.emit()




if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    fenetre = VueFirstApp()
    sys.exit(app.exec())