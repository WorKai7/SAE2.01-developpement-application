import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt6.QtCore import QSize, Qt, pyqtSignal

class NewProjectApp(QWidget):

    infosSignal = pyqtSignal(dict)

    def __init__(self) -> None:
        super().__init__()

        self.infos = {
            "project_name": "Sans nom",
            "project_author": "Sans nom",
            "shop_name": "Sans nom",
            "shop_address": "Sans nom",
            "file_path": None,
            "image": "../images/vide.png"
        }

        self.setMinimumSize(900, 600)
        self.resize(900, 600)
        self.setWindowTitle("Nouveau projet")

        layout = QVBoxLayout() ; self.setLayout(layout)

        self.setStyleSheet("QWidget{ background-color: white; }  QLabel{ font-size: 18px; } QLineEdit { border: 2px solid; border-radius: 8px; padding-left: 10px; height: 20px }") # commun a tous les éléments de la page

        self.project_name_label = QLabel("Nom du projet:")
        self.project_name = Champ("Ex: Projet 1")
        self.project_author_label = QLabel("Nom de l'auteur du projet:")
        self.project_author = Champ("Ex: Rick Astley")
        self.shop_name_label = QLabel("Nom du magasin:")
        self.shop_name = Champ("Ex: Monoprix")
        self.shop_address_label = QLabel("Adresse du magasin:")
        self.shop_address = Champ("Ex: 4894984 Rue de la paix, MontCul")
        self.image_label = QLabel("Plan du magasin")
        self.image_path = Champ("Sélectionnez une image")
        self.image_path.setDisabled(True)
        self.select_image_button = QPushButton("Parcourir")
        self.select_image_button.setFixedWidth(150)
        self.create_button = QPushButton("Créer")
        self.create_button.setFixedWidth(150)
        self.create_button.setStyleSheet("background-color: #5DF07D; color: white; font-size: 16px; border: 2px solid; border-radius: 2px")

        self.create_button.clicked.connect(self.create)
        self.select_image_button.clicked.connect(self.browse)

        layout.addStretch()
        layout.addWidget(self.project_name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.project_name, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(self.project_author_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.project_author, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(self.shop_name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.shop_name, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(self.shop_address_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.shop_address, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_path, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.select_image_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(self.create_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()


    def create(self):
        # valeurs saisies
        self.infos["project_name"] = self.project_name.text()
        self.infos["project_author"] = self.project_author.text()
        self.infos["shop_name"] = self.shop_name.text()
        self.infos["shop_address"] = self.shop_address.text()

        # valeurs par défaut
        self.infos["x"] = 0
        self.infos["y"] = 0
        self.infos["case_size"] = 10
        self.infos["grid"] = [
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ]
        ]


        self.close()
        self.infosSignal.emit(self.infos)


    def browse(self):
        image = QFileDialog.getOpenFileName(self, "Choisissez le plan", "", "Fichier PNG (*.png) ;; Fichier JPG (*.jpg *.jpeg) ;; Fichier SVG (*.svg)")[0]

        if image:
            self.infos["image"] = image
            self.image_path.setText(image)
        else:
            print("Pas de fichier sélectionné")


class Champ(QLineEdit):
    def __init__(self, placeholder:str):
        super().__init__()

        self.setPlaceholderText(placeholder)
        self.setFixedSize(QSize(400, 30))


if __name__ == "__main__":

    app = QApplication(sys.argv)
    fenetre = NewProjectApp()
    fenetre.show()
    sys.exit(app.exec())