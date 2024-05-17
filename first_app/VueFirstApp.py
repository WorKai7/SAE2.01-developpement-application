import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtWidgets import QWidget


class VueFirstApp(QMainWindow):
    '''
        Classe VueFirstApp: correpond à la classe de la vue de la première application pour la création de magasins.
        Elle ne représente que le visuel et est liée au modèle dans le fichier Controller.py
    '''

    newClicked = pyqtSignal()
    loadClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.resize(int(QApplication.screens()[0].size().width()), int(QApplication.screens()[0].size().height()))
        self.setWindowTitle("Sans nom")

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

        pass

    def save(self):
        '''
            Méthode save: permet à l'utilisateur d'enregistrer le magasin courant
            Elle émet simplement un signal vers l'extérieur
        '''

        pass

    def save_as(self):
        '''
            Méthode save_as: permet à l'utilisateur d'enregistrer le magasin courant à l'emplacement choisi
            Elle émet simplement un signal vers l'extérieur
        '''

        pass

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

class Grid(QWidget):
    def __init__(self, width:int=0, height:int=0) -> None:
        super().__init__()

        self.layout = QGridLayout() ; self.setLayout(self.layout)

        self.image = "../images/vide.png"
        self.width = width
        self.height = height

        self.grid = []

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.image)
        painter.drawPixmap(self.rect(), pixmap)
        super().paintEvent(event)

    def draw_grid(self):
        for i in range(self.height):
            row = []
            for j in range(self.width):
                case = QCheckBox()
                row.append(case)
                self.layout.addWidget(case, i, j)
            self.grid.append(row)

    def clear_grid(self):
        for i in range(self.height-1, -1, -1):
            for j in range(self.width-1, -1, -1):
                self.layout.removeWidget(self.grid[i][j])
                del self.grid[i][j]
        self.grid.clear()


class Options(QWidget):

    drawClicked = pyqtSignal(tuple)
    clearClicked = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self.setFixedWidth(int(QApplication.screens()[0].size().width()*0.3))

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