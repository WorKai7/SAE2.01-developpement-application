import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QSize, Qt

class NewProjectApp(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.resize(800, 500)

        layout = QVBoxLayout() ; self.setLayout(layout)

        self.project_name_label = QLabel("Nom du projet:")
        self.project_name = Champ("Ex: Projet 1")
        self.project_author_label = QLabel("Nom de l'auteur du projet:")
        self.project_author = Champ("Ex: Rick Astley")
        self.shop_name_label = QLabel("Nom du magasin:")
        self.shop_name = Champ("Ex: Monoprix")
        self.shop_address_label = QLabel("Adresse du magasin:")
        self.shop_address = Champ("Ex: 4894984 Rue de la paix, MontCul")
        self.create_button = QPushButton("Créer")
        self.create_button.setFixedWidth(150)

        self.create_button.clicked.connect(self.create)

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
        layout.addWidget(self.create_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()


    def create(self):
        infos = {
            "project_name": self.project_name.text(),
        }

        self.close()
        print(infos)

        # Faudra voir pour renvoyer les infos au modele pour pouvoir les traiter après
        return infos


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