import sys
import json
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QListWidget, QAbstractItemView, QApplication, QLabel
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import QRect, Qt

class Popup(QWidget):
    def __init__(self, coordinates:tuple, max_right:int, max_bottom:int):
        super().__init__()
        
        self.setWindowTitle("Case (" + str(coordinates[0]) + ", " + str(coordinates[1]) + ")")
        
        layout = QHBoxLayout() ; self.setLayout(layout)

        self.left = Left()
        self.right = Right(coordinates, max_right, max_bottom)

        layout.addWidget(self.left)
        layout.addWidget(self.right)


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

        painter = QPainter(self.schema)
        if coordinates[0] > 0:
            self.rect_list.append(QRect(150, 50, 100, 100))

        if coordinates[1] > 0:
            self.rect_list.append(QRect(50, 150, 100, 100))

        self.rect_list.append(QRect(150, 150, 100, 100))

        if coordinates[1] < max_right-1:
            self.rect_list.append(QRect(250, 150, 100, 100))

        if coordinates[0] < max_bottom-1:
            self.rect_list.append(QRect(150, 250, 100, 100))

        painter.drawRects(self.rect_list)

        self.setPixmap(self.schema)

        painter.end()



if __name__ == "__main__":

    app = QApplication(sys.argv)
    fenetre = Popup((24, 625))
    fenetre.show()
    sys.exit(app.exec())