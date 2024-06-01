from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QListWidget

class Popup(QWidget):
    def __init__(self, coordinates:tuple):
        super().__init__()
        
        self.setWindowTitle("Case (" + str(coordinates[0]) + ", " + str(coordinates[1]) + ")")
        
        layout = QHBoxLayout() ; self.setLayout(layout)

        self.left = Left()

        self.show()


class Left(QWidget):
    def __init__(self, coordinates:tuple):
        super().__init__()

        layout = QVBoxLayout() ; self.setLayout(layout)

