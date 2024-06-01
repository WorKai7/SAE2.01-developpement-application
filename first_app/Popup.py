import sys
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QListWidget, QAbstractItemView, QApplication

class Popup(QWidget):
    def __init__(self, coordinates:tuple):
        super().__init__()
        
        self.setWindowTitle("Case (" + str(coordinates[0]) + ", " + str(coordinates[1]) + ")")
        
        layout = QHBoxLayout() ; self.setLayout(layout)

        self.left = Left()

        layout.addWidget(self.left)

        self.show()


class Left(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout() ; self.setLayout(layout)

        self.category = QComboBox()
        self.category.addItems(["Légumes", "Poissons", "Viandes", "Épicerie", "Épicerie sucrée", "Petit déjeuner", "Fruits", "Rayon frais", "Crèmerie", "Conserves", "Apéritifs", "Boissons", "Articles Maison", "Hygiène", "Bureau", "Animaux"])

        self.products = QListWidget()
        self.products.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.category.currentTextChanged.connect(self.update_product_list)

        layout.addWidget(self.category)
        layout.addWidget(self.products)

    def update_product_list(self):
        products = self.get_products(self.category.currentText())
        self.products.clear()
        self.products.addItems(products)

    def get_products(self, category:str):
        pass


if __name__ == "__main__":

    app = QApplication(sys.argv)
    fenetre = Popup((24, 625))
    sys.exit(app.exec())