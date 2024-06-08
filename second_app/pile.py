# Fichier contenant la classe pile adaptée pour que la méthode contient fonctionne correctement avec le type tuple

class Pile():
    def __init__(self) -> None:
        self.elements = []
        self.nb_elements = 0
        
    
    def empiler(self, element):
        """
            Empile un element dans la pile

            Keyword arguments:
            element -- L'element a empiler
        """
        self.elements.append(element)
        self.nb_elements += 1
    

    def depiler(self):
        """
            Supprile l'element au sommet de la pile et le renvoie
        """
        self.nb_elements -= 1
        return self.elements.pop(self.nb_elements)


    def contient(self, element):
        """
            Renvoie la presence d'un element ou non dans la liste

            Keyword arguments:
            element -- L'element dont on verifie la presence
        """
        return element in self.elements