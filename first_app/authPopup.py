from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal


class AuthPopup(QWidget):
    """Implémente la Popup d'autenthification"""

    cancelClickedEvent = pyqtSignal()
    confirmClickedEvent = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Authentification")
        self.resize(300, 100)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.passfield = QLineEdit()
        self.passfield.setPlaceholderText("Mot de passe")
        self.passfield.setEchoMode(QLineEdit.EchoMode.Password)
        self.mainLayout.addWidget(self.passfield)

        self.bottomwidget = QWidget()
        self.bottomLayout = QHBoxLayout()
        self.bottomwidget.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.bottomwidget)

        self.cancel = QPushButton("Annuler")
        self.bottomLayout.addWidget(self.cancel)

        self.confirm = QPushButton("Se connecter")
        self.bottomLayout.addWidget(self.confirm)

        self.cancel.clicked.connect(self.cancelClicked)
        self.confirm.clicked.connect(self.confirmClicked)
        
        self.show()

    
    def cancelClicked(self):
        self.cancelClickedEvent.emit()

    
    def confirmClicked(self, passwd: str):
        self.confirmClickedEvent.emit(self.passfield.text())
