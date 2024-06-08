import sys
import json
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QListWidget, QAbstractItemView, QApplication, QLabel, QPushButton
from PyQt6.QtGui import QMouseEvent, QPixmap, QPainter, QBrush, QColor
from PyQt6.QtCore import QRect, Qt, pyqtSignal


class Popup(QWidget):

    confirmClicked = pyqtSignal()

    def __init__(self, coordinates:tuple, pattern:dict, product_infos:list|None):
        super().__init__()
        
        self.x = coordinates[1]
        self.y = coordinates[0]

        if product_infos:
            self.category = product_infos[0]
            self.product = product_infos[1]
        else:
            self.category = None
            self.product = None

        self.setWindowTitle("Case (" + str(self.y) + ", " + str(self.x) + ")")
        
        layout = QHBoxLayout()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.info = QLabel("⬇️ Sélectionnez l'article à placer dans la case et définissez les murs ⬇️")
        self.right = Right(coordinates, pattern)
        self.left = Left()

        if self.category:
            self.left.categories.setCurrentText(self.category)

        if self.product:
            self.ajout = QLabel("Article : " + self.product)
            item = self.left.products.findItems(self.product, Qt.MatchFlag.MatchExactly)
            self.left.products.setCurrentItem(item[0])
        else:
            self.ajout = QLabel("Article : Aucun")


        self.delete_button = QPushButton("Supprimer l'article")
        self.delete_button.setFixedWidth(350)

        self.confirm_button = QPushButton("Confirmer")
        self.confirm_button.setFixedWidth(350)

        main_layout.addWidget(self.info, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.left)
        layout.addWidget(self.right)
        main_layout.addLayout(layout)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.ajout, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.delete_button, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.confirm_button, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(10)

        self.left.products.currentItemChanged.connect(self.update_label)
        self.confirm_button.clicked.connect(self.confirm)
        self.delete_button.clicked.connect(self.delete)


    def update_label(self):
        """
            Modifie le label de selection de produit pour qu'il corresponde au produit actuellement
            selectionne par l'utilisareur
        """
        if self.left.products.currentItem():
            self.ajout.setText("Article : " + self.left.products.currentItem().text())
        else:
            self.ajout.setText("Article: Aucun")


    def confirm(self):
        """
            envoie le signal de confirmation de modification de la case
        """
        self.confirmClicked.emit()


    def delete(self):
        """
            Supprime le produit actuellement selectionne par l'utilisateur
        """
        self.left.products.setCurrentItem(None)


    def closeEvent(self):
        """
            Ferme la fenetre
        """
        self.right.painter.end()
        self.close()


class Left(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout() ; self.setLayout(layout)

        self.categories = QComboBox()
        self.categories.addItems(["Entrée/Sortie", "Légumes", "Poissons", "Viandes", "Épicerie", "Épicerie sucrée", "Petit déjeuner", "Fruits", "Rayon frais", "Crèmerie", "Conserves", "Apéritifs", "Boissons", "Articles Maison", "Hygiène", "Bureau", "Animaux"])

        self.products = QListWidget()
        self.products.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.update_product_list()

        self.categories.currentTextChanged.connect(self.update_product_list)

        layout.addWidget(self.categories)
        layout.addWidget(self.products)


    def update_product_list(self):
        """
            Met a jour la liste de produits en fonction de la categorie selectionnee
        """
        products = self.get_products(self.categories.currentText())
        self.products.clear()
        self.products.addItems(products)


    def get_products(self, category:str):
        """
            Recupere les produits de la categorie choisie dans le fichier liste de produits

            Keyword arguments:
            category -- La categorie dont on recupere les produits
        """
        products = []
        with open("../Liste de produits-20240513/liste_produits.json", encoding="utf-8") as f:
            products = json.load(f)

        return products.get(category, [])


class Right(QLabel):
    def __init__(self, coordinates:tuple, pattern:dict):
        super().__init__()

        self.schema = QPixmap(400, 400)
        self.schema.fill(Qt.GlobalColor.transparent)
        self.rect_list = []
        self.rect_infos = []
        max_right = max([key[1] for key in pattern.keys()])
        max_bottom = max([key[0] for key in pattern.keys()])

        self.painter = QPainter(self.schema)
        if coordinates[0] > 0:
            rect = QRect(150, 50, 100, 100)
            self.rect_list.append(rect)

            if (coordinates[0]-1, coordinates[1]) in pattern[(coordinates[0], coordinates[1])].keys():
                self.rect_infos.append(["up", "green"])
                self.painter.setBrush(QBrush(QColor(Qt.GlobalColor.green)))
            else:
                self.rect_infos.append(["up", "red"])
                self.painter.setBrush(QBrush(QColor(Qt.GlobalColor.red)))

            self.painter.drawRect(rect)

        if coordinates[1] > 0:
            rect = QRect(50, 150, 100, 100)
            self.rect_list.append(rect)

            if (coordinates[0], coordinates[1]-1) in pattern[(coordinates[0], coordinates[1])].keys():
                self.rect_infos.append(["left", "green"])
                self.painter.setBrush(QBrush(QColor(Qt.GlobalColor.green)))
            else:
                self.rect_infos.append(["left", "red"])
                self.painter.setBrush(QBrush(QColor(Qt.GlobalColor.red)))

            self.painter.drawRect(rect)

        mid_rect = QRect(150, 150, 100, 100)
        self.rect_list.append(mid_rect)
        self.rect_infos.append(["current", "black"])

        if coordinates[1] < max_right:
            rect = QRect(250, 150, 100, 100)
            self.rect_list.append(rect)

            if (coordinates[0], coordinates[1]+1) in pattern[(coordinates[0], coordinates[1])].keys():
                self.rect_infos.append(["right", "green"])
                self.painter.setBrush(QBrush(QColor(Qt.GlobalColor.green)))
            else:
                self.rect_infos.append(["right", "red"])
                self.painter.setBrush(QBrush(QColor(Qt.GlobalColor.red)))

            self.painter.drawRect(rect)

        if coordinates[0] < max_bottom:
            rect = QRect(150, 250, 100, 100)
            self.rect_list.append(rect)

            if (coordinates[0]+1, coordinates[1]) in pattern[(coordinates[0], coordinates[1])].keys():
                self.rect_infos.append(["down", "green"])
                self.painter.setBrush(QBrush(QColor(Qt.GlobalColor.green)))
            else:
                self.rect_infos.append(["down", "red"])
                self.painter.setBrush(QBrush(QColor(Qt.GlobalColor.red)))

            self.painter.drawRect(rect)

        self.painter.setBrush(QBrush(QColor(Qt.GlobalColor.black)))
        self.painter.drawRect(mid_rect)

        self.setPixmap(self.schema)


    def mousePressEvent(self, event):
        """
            Appelee lorsque la grille est cliquee afin de traiter le click
        """
        for i in range(len(self.rect_list)):

            if self.rect_list[i].contains(event.pos()):
                if self.rect_infos[i][1] == "green":
                    self.painter.setBrush(QColor(Qt.GlobalColor.red))
                    self.painter.drawRect(self.rect_list[i])
                    self.rect_infos[i][1] = "red"

                elif self.rect_infos[i][1] == "red":
                    self.painter.setBrush(QColor(Qt.GlobalColor.green))
                    self.painter.drawRect(self.rect_list[i])
                    self.rect_infos[i][1] = "green"

                self.setPixmap(self.schema)
