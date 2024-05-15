import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap
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

        layout = QVBoxLayout() ; self.setLayout(layout)

        self.image = Image("../images/vide.png")

        layout.addStretch()
        layout.addWidget(self.image, alignment=Qt.AlignmentFlag.AlignCenter)


class Image(QLabel):
    '''
        Classe image: cette classe correspond à l'image qui sera associée au plan
    '''

    def __init__(self, chemin:str):
        super().__init__()

        self.image = QPixmap(chemin).scaledToHeight(int(QApplication.screens()[0].size().height()*0.7))
        self.setPixmap(self.image)


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    fenetre = VueFirstApp()
    sys.exit(app.exec())