import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class ProjectInfos(QWidget):
    def __init__(self, infos: dict):
        super().__init__()

        self.resize(300, 200)
        self.move(500, 200)

        self.projectInfos = infos

        font = QFont()
        font.setPointSize(18)

        self.project_name = QLabel("Nom du projet: " + self.projectInfos["project_name"])
        self.author = QLabel("Auteur du projet: " + self.projectInfos['project_author'])
        self.shop_name = QLabel("Nom du magasin: " + self.projectInfos["shop_name"])
        self.shop_address = QLabel("Adresse du magasin: " + self.projectInfos["shop_address"])

        self.project_name.setFont(font)
        self.author.setFont(font)
        self.shop_name.setFont(font)
        self.shop_address.setFont(font)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(self.author, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.project_name, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.shop_name, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.shop_address, alignment=Qt.AlignmentFlag.AlignCenter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = ProjectInfos({
            "project_name": "Sans nom",
            "project_author": "Sans nom",
            "shop_name": "Sans nom",
            "shop_address": "Sans nom",
            "file_path": None,
            "image": "../images/vide.png",
            "case_size": 50,
            "x": 0,
            "y": 0,
            "grid": [],
            "pattern": {}
        })
    fenetre.show()
    sys.exit(app.exec())