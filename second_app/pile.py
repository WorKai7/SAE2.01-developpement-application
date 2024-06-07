# Fichier contenant la classe pile adaptée pour que la méthode contient fonctionne correctement avec le type tuple

class Pile():
    def __init__(self) -> None:
        self.elements = []
        self.nb_elements = 0
        
    
    def empiler(self, element):
        self.elements.append(element)
        self.nb_elements += 1
    
    def depiler(self):
        self.nb_elements -= 1
        return self.elements.pop(self.nb_elements)

    def contient(self, element):
        return element in self.elements