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

        self.resize(1600, 900)
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
        self.right = Right()

        layout.addWidget(self.options, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.right, alignment=Qt.AlignmentFlag.AlignCenter)


class Right(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QGridLayout() ; self.setLayout(layout)

        self.grid = Grid()
        self.w_slider = WidthSlider(self.grid.pixmap.width())
        self.h_slider = HeightSlider(self.grid.pixmap.height())

        layout.addWidget(self.w_slider, 0, 1)
        layout.addWidget(self.h_slider, 1, 0)
        layout.addWidget(self.grid, 1, 1)


class WidthSlider(QSlider):

    gridMoved = pyqtSignal(int)

    def __init__(self, max_width:int):
        super().__init__(Qt.Orientation.Horizontal)

        self.setMaximum(max_width)
        self.setProperty("type", "x")

        self.valueChanged.connect(self.move_grid)


    def move_grid(self, value:int):
        self.gridMoved.emit(value)


class HeightSlider(QSlider):

    gridMoved = pyqtSignal(int)

    def __init__(self, max_height:int):
        super().__init__(Qt.Orientation.Vertical)

        self.setMaximum(max_height)
        self.setInvertedAppearance(True)
        self.setProperty("type", "y")

        self.valueChanged.connect(self.move_grid)


    def move_grid(self, value:int):
        self.gridMoved.emit(value)


class Grid(QLabel):

    rectClicked = pyqtSignal(tuple)

    def __init__(self) -> None:
        super().__init__()
        self.image = "../images/vide.png"
        self.grid = []
        self.x = 0
        self.y = 0
        self.update_image()

    def update_image(self):
        self.pixmap = QPixmap(self.image)

        if self.pixmap.width() >= 1100:
            self.pixmap = QPixmap(self.image).scaledToWidth(1100)

        if self.pixmap.height() >= 800:
            self.pixmap = QPixmap(self.image).scaledToHeight(800)

        self.blank_pixmap = self.pixmap

        self.setPixmap(self.pixmap)

    def draw_grid(self, grid:list, case_size:int):
        if grid:
            width = len(grid[0])
        else:
            width = 0

        height = len(grid)
        pixmap = self.blank_pixmap.copy()
        painter = QPainter(pixmap)

        for i in range(height):
            row = []
            for j in range(width):
                case = QRect(j*case_size+self.x, i*case_size+self.y, case_size, case_size)
                painter.drawRect(case)
                row.append(case)
            self.grid.append(row)
        self.setPixmap(pixmap)
        painter.end()

    def clear_grid(self):
        self.grid.clear()
        self.setPixmap(self.blank_pixmap)


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    rect = self.grid[i][j]
                    if rect.contains(event.pos()):
                        self.rectClicked.emit((i, j))



class Options(QWidget):

    drawClicked = pyqtSignal(tuple)
    clearClicked = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout() ; self.setLayout(layout)

        self.row_label = QLabel("Nombre de lignes")
        self.row_number = QSpinBox()
        self.column_label = QLabel("Nombre de colonnes")
        self.column_number = QSpinBox()
        self.case_size_label = QLabel("Taille des cases")
        self.case_size = QSpinBox()
        self.case_size.setValue(50)
        self.case_size.setSingleStep(10)
        self.draw_grid_button = QPushButton("Dessiner la grille")
        self.clear_grid_button = QPushButton("Effacer la grille")

        layout.addWidget(self.row_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.row_number, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.column_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.column_number, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.case_size_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.case_size, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.draw_grid_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.clear_grid_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.draw_grid_button.clicked.connect(self.dessinClicked)
        self.clear_grid_button.clicked.connect(self.effaceClicked)


    def dessinClicked(self):
        self.drawClicked.emit((self.column_number.value(), self.row_number.value(), self.case_size.value()))

    def effaceClicked(self):
        self.clearClicked.emit()




if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    fenetre = VueFirstApp()
    sys.exit(app.exec())