import sys
import json
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QListWidget, QAbstractItemView, QApplication, QLabel, QPushButton
from PyQt6.QtGui import QMouseEvent, QPixmap, QPainter
from PyQt6.QtCore import QRect, Qt

class Popup(QWidget):
    def __init__(self, coordinates:tuple, max_right:int, max_bottom:int):
        super().__init__()
        
        self.setWindowTitle("Case (" + str(coordinates[0]) + ", " + str(coordinates[1]) + ")")
        
        layout = QHBoxLayout()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.info = QLabel("⬇️ Sélectionnez l'article à placer dans la case et définissez les murs ⬇️")
        self.left = Left()
        self.right = Right(coordinates, max_right, max_bottom)
        self.ajout = QLabel("Article ajouté : Aucun")
        self.confirm_button = QPushButton("Confirmer")
        self.confirm_button.setFixedWidth(350)

        main_layout.addWidget(self.info, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.left)
        layout.addWidget(self.right)
        main_layout.addLayout(layout)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.ajout, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.confirm_button, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(10)

        self.left.products.currentItemChanged.connect(self.update_label)


    def update_label(self):
        self.ajout.setText("Article ajouté : " + self.left.products.currentItem().text())


class Left(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout() ; self.setLayout(layout)

        self.category = QComboBox()
        self.category.addItems(["Légumes", "Poissons", "Viandes", "Épicerie", "Épicerie sucrée", "Petit déjeuner", "Fruits", "Rayon frais", "Crèmerie", "Conserves", "Apéritifs", "Boissons", "Articles Maison", "Hygiène", "Bureau", "Animaux"])

        self.products = QListWidget()
        self.products.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.update_product_list()

        self.category.currentTextChanged.connect(self.update_product_list)

        layout.addWidget(self.category)
        layout.addWidget(self.products)

    def update_product_list(self):
        products = self.get_products(self.category.currentText())
        self.products.clear()
        self.products.addItems(products)

    def get_products(self, category:str):
        products = []
        with open("../Liste de produits-20240513/liste_produits.json", encoding="utf-8") as f:
            products = json.load(f)

        return products.get(category, [])


class Right(QLabel):
    def __init__(self, coordinates:tuple, max_right:int, max_bottom:int):
        super().__init__()

        self.schema = QPixmap(400, 400)
        self.schema.fill(Qt.GlobalColor.transparent)
        self.rect_list = []
        self.rect_names = []

        painter = QPainter(self.schema)
        if coordinates[0] > 0:
            self.rect_list.append(QRect(150, 50, 100, 100))
            self.rect_names.append("up")

        if coordinates[1] > 0:
            self.rect_list.append(QRect(50, 150, 100, 100))
            self.rect_names.append("left")

        self.rect_list.append(QRect(150, 150, 100, 100))
        self.rect_names.append("current")

        if coordinates[1] < max_right-1:
            self.rect_list.append(QRect(250, 150, 100, 100))
            self.rect_names.append("right")

        if coordinates[0] < max_bottom-1:
            self.rect_list.append(QRect(150, 250, 100, 100))
            self.rect_names.append("down")

        painter.drawRects(self.rect_list)

        self.setPixmap(self.schema)

        painter.end()


    def mousePressEvent(self, event):
        for i in range(len(self.rect_list)):
            if self.rect_list[i].contains(event.pos()):
                print("clic dans ", self.rect_names[i])


if __name__ == "__main__":

    app = QApplication(sys.argv)
    fenetre = Popup((24, 625), 24, 625)
    fenetre.show()
    sys.exit(app.exec())