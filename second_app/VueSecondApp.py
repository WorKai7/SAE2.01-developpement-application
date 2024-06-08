import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, \
                            QHBoxLayout, QComboBox, QWidget, QPushButton, QAbstractItemView, \
                            QListWidget
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt, pyqtSignal, QRect

class Image(QLabel):

    startClicked = pyqtSignal(tuple)
    endClicked = pyqtSignal(tuple)
    rectClicked = pyqtSignal(tuple)

    def __init__(self, chemin: str):
        super().__init__()

        self.image = chemin
        self.pixmap = QPixmap(self.image)
        self.setPixmap(self.pixmap)
        self.grid = []
        self.selecting_start = False
        self.selecting_end = False
        self.info_mode = False


    def update_image(self):
        """
            Modifie l'image actuellement affichee par la nouvelle image
        """
        self.pixmap = QPixmap(self.image)

        if self.pixmap.width() >= 1100:
            self.pixmap = QPixmap(self.image).scaledToWidth(1100)

        if self.pixmap.height() >= 800:
            self.pixmap = QPixmap(self.image).scaledToHeight(800)

        self.setPixmap(self.pixmap)


    def draw_grid(self, grid:list, x:int, y:int, case_size:int):
        """
            Dessine la grille selon les informations passees en parametre

            Keyword arguments:
            grid -- Les dimensions de la grille (verticale et horizontale)
            x -- L'abcisse a laquelle doit commencer la grille
            y -- L'ordonnee a laquelle doit commencer la grille
            case_size -- La taille de chaque case
        """

        # Determination des dimensions de la grille
        if grid:
            width = len(grid[0])
        else:
            width = 0

        height = len(grid)


        # Initialisation du dessin
        painter = QPainter(self.pixmap)

        for i in range(height):

            # Création d'une ligne
            row = []

            for j in range(width):

                # Initialisation des cases
                case = QRect(j*case_size+x, i*case_size+y, case_size, case_size)
                row.append(case)

                # Dessin des cases
                if grid[i][j]:
                    painter.setBrush(QColor(0, 0, 0, 128))
                    painter.drawRect(case)
                    painter.setBrush(QColor(0, 0, 0, 0))
                else:
                    painter.drawRect(case)

            self.grid.append(row)

        # Mise à jour du dessin
        self.setPixmap(self.pixmap)
        painter.end()


    def draw_rect(self, pos:tuple, x:int, y:int, case_size:int, color:tuple):
        """
            Colore une case sur la grille

            Keywrod arguments:
            pos -- Les coordonnees de la case a colorer
            x -- L'abcisse a partir de laquelle commencer la coloration
            y -- L'ordonnee a partir de laquelle commencer la coloration
            case_size -- La taille de la case a colorer
            color -- La couleur a appliquer sur la case (en format RVB)
        """
        rect = QRect(pos[1]*case_size+x, pos[0]*case_size+y, case_size, case_size)
        painter = QPainter(self.pixmap)
        painter.setBrush(QColor(color[0], color[1], color[2], color[3]))
        painter.drawRect(rect)
        painter.end()
        self.setPixmap(self.pixmap)


    def draw_path(self, path:list, x:int, y:int, case_size:int):
        """
            Dessine le chemin a suivre
        """
        pas = 255/len(path)
        rouge = 0
        bleu = 255

        for i in range(len(path)):
            self.draw_rect(path[i], x, y, case_size, (int(rouge), 0, int(bleu), 200))
            rouge += pas
            bleu -= pas


    def mousePressEvent(self, event):
        """
            Emet un click event avec les bonnes valeurs
        """

        # Gère les clics sur la grille: trois types de clics possibles:
        # - Selection de la position de départ
        # - Sélection de la position d'arrivée
        # - Sélection d'une case pour voir le produit à l'intérieur
        if self.selecting_start or self.selecting_end or self.info_mode:
            if event.button() == Qt.MouseButton.LeftButton:
                for i in range(len(self.grid)):
                    for j in range(len(self.grid[i])):
                        rect = self.grid[i][j]
                        if rect.contains(event.pos()):
                            if self.selecting_start and not self.info_mode:
                                self.startClicked.emit((i, j))
                                self.selecting_start = False
                            elif self.selecting_end and not self.info_mode:
                                self.endClicked.emit((i, j))
                                self.selecting_end = False
                            elif self.info_mode:
                                self.rectClicked.emit((i, j))


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
        self.info_label = QLabel("Vous êtes en mode informations : cliquez sur une case pour voir son produit associé")
        self.label.hide()
        self.info_label.hide()
        self.buttons = Buttons()
        self.way_button = QPushButton("Génerer le chemin")
        self.erase_way_button = QPushButton("Effacer le chemin")

        layout.addWidget(self.up)
        layout.addSpacing(10)
        layout.addWidget(self.label)
        layout.addWidget(self.info_label)
        layout.addWidget(self.buttons)
        layout.addSpacing(10)
        layout.addWidget(self.way_button)
        layout.addWidget(self.erase_way_button)

        self.way_button.clicked.connect(self.generate)
        self.erase_way_button.clicked.connect(self.erase)


    def generate(self):
        """
            Emet un evenement de click sur le bouton generer
        """
        self.generateClicked.emit()

    def erase(self):
        """
            Emet un evenement de click sur le bouton effacer
        """
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
        """
            Emet un evenement de click sur le bouton ajouter un produit
        """
        self.addClicked.emit()

    def update_product_list(self):
        """
            Emet un evenement d'update de la liste
        """
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
        """
            Emet l'evenement de suppression de la liste
        """
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
    infoClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout() ; self.setLayout(layout)

        self.random_pos_button = QPushButton("Position de départ aléatoire")
        self.pos_button = QPushButton("Sélectionner le départ")
        self.end_button = QPushButton("Sélectionner l'arrivée")
        self.info_button = QPushButton("Activer/Désactiver le mode informations")

        layout.addWidget(self.random_pos_button)
        layout.addWidget(self.pos_button)
        layout.addWidget(self.end_button)
        layout.addWidget(self.info_button)

        self.random_pos_button.clicked.connect(self.random_pos)
        self.pos_button.clicked.connect(self.select_pos)
        self.end_button.clicked.connect(self.select_end)
        self.info_button.clicked.connect(self.info_mode)


    def random_pos(self):
        """
            Emet l'evenement de click sur le bouton position aleatoire
        """
        self.randomStart.emit()

    def select_pos(self):
        """
            Emet l'evenement de click sur le bouton selection de position
        """
        self.selectStart.emit()

    def select_end(self):
        """
            Emet l'evenement de click sur le bouton selection de sortie
        """
        self.selectEnd.emit()

    def info_mode(self):
        """
            Emet l'evenement de click sur le bouton de passage en mode info
        """
        self.infoClicked.emit()


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

        menu_theme = menu_bar.addMenu("&Thèmes")
        menu_theme.addAction("Clair", self.applyBrightTheme)
        menu_theme.addAction("Sombre", self.applyDarkTheme)
        menu_theme.addAction("Material Dark", self.applyMaterialDark)
        menu_theme.addAction("Défaut", self.resetTheme)

        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)

        self.show()


    def applyBrightTheme(self):
        """
            Bascule vers le theme clair
        """

        fichier_style = open("../fichiers_qss/lightstyle.qss", 'r')
        with fichier_style:
            qss = fichier_style.read()
            self.setStyleSheet(qss)


    def applyDarkTheme(self):
        """
            Bascule vers le theme sombre
        """

        fichier_style = open("../fichiers_qss/darkstyle.qss", 'r')
        with fichier_style:
            qss = fichier_style.read()
            self.setStyleSheet(qss)


    def applyMaterialDark(self):
        """
            Bascule vers le theme Material Dark
        """

        fichier_style = open("../fichiers_qss/materialdark.qss", 'r')
        with fichier_style:
            qss = fichier_style.read()
            self.setStyleSheet(qss)

    def resetTheme(self):
        """
            Bascule sur le theme par defaut du systeme
        """
        self.setStyleSheet('')


    def getPathToProduct(self):
        """
            Emet le signal pour génerer et afficher le chemin
        """
        self.mainWidget.left.generateClicked.emit()


    def setPos(self):
        """
            Emet le signal pour sélectionner la position de départ
        """
        self.mainWidget.left.buttons.selectStart.emit()


    def setGoal(self):
        """
            Emet le signal pour sélectionner la position d'arrivée
        """
        self.mainWidget.left.buttons.selectEnd.emit()


    def setProject(self):
        """
            Emet le signal pour ouvrir un nouveau projet
        """
        self.loadClicked.emit()


    def viewInfos(self):
        """
            Emet le signal pour afficher les informations du projet ouvert
        """
        self.infosClicked.emit()


## -----------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = VueSecondApp()
    sys.exit(app.exec())