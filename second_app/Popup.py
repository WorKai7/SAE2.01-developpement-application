import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class Popup(QWidget):
    def __init__(self, x:int, y:int, article:str):
        super().__init__()

        self.resize(600, 300)
        self.setWindowTitle("Case (" + str(x) + ", " + str(y) + ")")

        layout = QVBoxLayout() ; self.setLayout(layout)

        font = QFont()
        font.setPointSize(16)
        self.label = QLabel("Article positionné dans cette case : " + article)
        self.label.setFont(font)

        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    fenetre = Popup(1, 2, "test")
    fenetre.show()
    sys.exit(app.exec())