import sys, time
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QStatusBar, \
                            QLabel, QTextEdit, QFileDialog, QDockWidget, QVBoxLayout, \
                            QHBoxLayout, QComboBox, QWidget, QPushButton, QAbstractItemView, \
                            QListWidget
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt, pyqtSignal, QRect

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

    startClicked = pyqtSignal(tuple)
    endClicked = pyqtSignal(tuple)

    def __init__(self, chemin: str):
        super().__init__()

        self.image = chemin
        self.pixmap = QPixmap(self.image)
        self.setPixmap(self.pixmap)
        self.grid = []
        self.selecting_start = False
        self.selecting_end = False

    def update_image(self):
        self.pixmap = QPixmap(self.image)

        if self.pixmap.width() >= 1100:
            self.pixmap = QPixmap(self.image).scaledToWidth(1100)

        if self.pixmap.height() >= 800:
            self.pixmap = QPixmap(self.image).scaledToHeight(800)

        self.setPixmap(self.pixmap)


    def draw_grid(self, grid:list, x:int, y:int, case_size:int):
        if grid:
            width = len(grid[0])
        else:
            width = 0

        height = len(grid)
        painter = QPainter(self.pixmap)

        for i in range(height):
            row = []
            for j in range(width):
                case = QRect(j*case_size+x, i*case_size+y, case_size, case_size)
                row.append(case)

                if grid[i][j]:
                    painter.setBrush(QColor(0, 0, 0, 128))
                    painter.drawRect(case)
                    painter.setBrush(QColor(0, 0, 0, 0))
                else:
                    painter.drawRect(case)

            self.grid.append(row)
        self.setPixmap(self.pixmap)
        painter.end()


    def draw_rect(self, pos:tuple, x:int, y:int, case_size:int, color:tuple):
        rect = QRect(pos[1]*case_size+x, pos[0]*case_size+y, case_size, case_size)
        painter = QPainter(self.pixmap)
        painter.setBrush(QColor(color[0], color[1], color[2], color[3]))
        painter.drawRect(rect)
        painter.end()
        self.setPixmap(self.pixmap)


    def draw_path(self, path:list, x:int, y:int, case_size:int):
        pas = 255//len(path)
        rouge = 0
        bleu = 255

        for i in range(len(path)):
            self.draw_rect(path[i], x, y, case_size, (rouge, 0, bleu, 128))
            rouge += pas
            bleu -= pas


    def mousePressEvent(self, event):
        if self.selecting_start or self.selecting_end:
            if event.button() == Qt.MouseButton.LeftButton:
                for i in range(len(self.grid)):
                    for j in range(len(self.grid[i])):
                        rect = self.grid[i][j]
                        if rect.contains(event.pos()):
                            if self.selecting_start:
                                self.startClicked.emit((i, j))
                                self.selecting_start = False
                            elif self.selecting_end:
                                self.endClicked.emit((i, j))
                                self.selecting_end = False

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout() ; self.setLayout(layout)

        self.left = Left()
        self.left.setMaximumWidth(800)
        self.image = Image("../images/vide.png")

        layout.addWidget(self.left)
        layout.addWidget(self.image, alignment=Qt.AlignmentFlag.AlignCenter)



class Left(QWidget):

    generateClicked = pyqtSignal()
    eraseClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout() ; self.setLayout(layout)

        self.up = Up()
        self.label = QLabel("Sélectionnez une case en cliquant dans la grille")
        self.label.hide()
        self.buttons = Buttons()
        self.way_button = QPushButton("Génerer le chemin")
        self.erase_way_button = QPushButton("Effacer le chemin")

        layout.addWidget(self.up)
        layout.addSpacing(10)
        layout.addWidget(self.label)
        layout.addWidget(self.buttons)
        layout.addSpacing(10)
        layout.addWidget(self.way_button)
        layout.addWidget(self.erase_way_button)

        self.way_button.clicked.connect(self.generate)
        self.erase_way_button.clicked.connect(self.erase)


    def generate(self):
        self.generateClicked.emit()

    def erase(self):
        self.eraseClicked.emit()


class Selection(QWidget):

    addClicked = pyqtSignal()
    updateList = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout() ; self.setLayout(layout)

        self.label = QLabel("Séletionnez vos articles:")

        self.categories = QComboBox()
        self.categories.addItems(["Légumes", "Poissons", "Viandes", "Épicerie", "Épicerie sucrée", "Petit déjeuner", "Fruits", "Rayon frais", "Crèmerie", "Conserves", "Apéritifs", "Boissons", "Articles Maison", "Hygiène", "Bureau", "Animaux"])

        self.products = QListWidget()
        self.products.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.add_button = QPushButton("Ajouter l'article sélectionné")

        self.categories.currentTextChanged.connect(self.update_product_list)

        layout.addWidget(self.label)
        layout.addWidget(self.categories)
        layout.addWidget(self.products)
        layout.addWidget(self.add_button)

        self.add_button.clicked.connect(self.add)


    def add(self):
        self.addClicked.emit()

    def update_product_list(self):
        self.updateList.emit()


class Liste(QWidget):

    deleteClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout() ; self.setLayout(layout)

        self.list_label = QLabel("Votre liste de courses:")
        self.liste = QListWidget()
        self.del_button = QPushButton("Supprimer l'article sélectionné")

        layout.addWidget(self.list_label)
        layout.addWidget(self.liste)
        layout.addWidget(self.del_button)

        self.del_button.clicked.connect(self.delete)


    def delete(self):
        self.deleteClicked.emit()

class Up(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout() ; self.setLayout(layout)

        self.selection = Selection()
        self.liste = Liste()

        layout.addWidget(self.selection)
        layout.addSpacing(20)
        layout.addWidget(self.liste)


class Buttons(QWidget):

    randomStart = pyqtSignal()
    selectStart = pyqtSignal()
    selectEnd = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout() ; self.setLayout(layout)

        self.random_pos_button = QPushButton("Sélectionner une position de départ aléatoire")
        self.pos_button = QPushButton("Sélectionner la position de départ")
        self.end_button = QPushButton("Sélectionner la position d'arrivée")

        layout.addWidget(self.random_pos_button)
        layout.addWidget(self.pos_button)
        layout.addWidget(self.end_button)

        self.random_pos_button.clicked.connect(self.random_pos)
        self.pos_button.clicked.connect(self.select_pos)
        self.end_button.clicked.connect(self.select_end)


    def random_pos(self):
        self.randomStart.emit()

    def select_pos(self):
        self.selectStart.emit()

    def select_end(self):
        self.selectEnd.emit()


class VueSecondApp(QMainWindow):

    loadClicked = pyqtSignal()
    infosClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.resize(1600, 900)
        self.setWindowTitle('StorePathFinder - Aucun projet ouvert')
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
        self.loadClicked.emit()

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