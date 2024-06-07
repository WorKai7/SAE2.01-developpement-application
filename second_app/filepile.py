# -*- coding: utf-8 -*-
'''
:Titre : Implémentation de classes d'objets : File, Pile
:Auteur : L. Conoir
:Date : 10/2020
:Outils : tableau de la bibliothèque numpy
'''

import numpy as np


###########################################################################
## Déclaration de la classe File
###########################################################################

class File(object):        # en anglais : queue
    
    def __init__(self, capacite : int = 6):
        'Constructeur de la classe'
        self.__elements : np.array = np.array([None for _ in range(capacite)])
        self.__nb_elements : int  = 0
        self.__capacite : int = capacite           # par défaut, la capacité est fixée à 6 éléments
        self.__tete : int = 0                      # indice de la tête de file

    @property
    def nombre_elements(self) -> int:
        "Méthode publique, renvoie le nombre d'éléments dans la file."
        return self.__nb_elements
    
    @property
    def capacite(self) -> int:
        '''Méthode publique, renvoie la capacité de la file.'''
        return self.__capacite


    def contient(self, element: any) -> bool:
        '''Méthode publique, précise si l'élément est dans la file.'''
        return element in self.__elements


    def est_vide(self) -> bool:
        '''Méthode publique, précise si la file est vide.'''
        return self.__nb_elements == 0


    def est_pleine(self) -> bool:
        '''Méthode publique, précise si la file est pleine.'''
        return self.__nb_elements == self.__capacite
    
    
    def enfiler(self, element: any) -> None:
        '''Méthode publique, enfile un nouvel element.'''
        if not self.est_pleine():
            indice : int = (self.__tete + self.__nb_elements) % self.__capacite
            self.__elements[indice] = element
            self.__nb_elements += 1
        else:
            print('M.I.1 : La file est pleine.')    # Queue Overflow
    

    def defiler(self) -> any:
        '''Méthode publique, défile le premier et le renvoie.'''
        if not self.est_vide() :
            self.__nb_elements -= 1
            indice: int = self.__tete
            self.__tete = (self.__tete + 1) % self.__capacite
            return self.__elements[indice]
        else:
            print('M.I.2 : La file est vide.')


    def __str__(self) -> str:
        '''Méthode spéciale, renvoie l'affichage du contenu de la file.'''
        if self.est_vide():
            affichage = 'La file est vide'
        else:
            affichage : str = 'Contenu de la file :\n\n   '
            for numero in range(self.__nb_elements):
                indice : int = (self.__tete + numero) % self.__capacite
                affichage = affichage + ' | ' + str(self.__elements[indice])
        return affichage + ' |\n'



###########################################################################
## Déclaration de la classe Pile
###########################################################################

class Pile(object):        # en anglais : stack
    
    def __init__(self, capacite :int = 6):
        '''Constructeur de la classe'''
        self.__elements  : np.array = np.array([None for _ in range(capacite)])
        self.__nb_elements : int  = 0
        self.__capacite : int = capacite           # par défaut, la capacité est fixée à 6 éléments


    @property
    def nombre_elements(self) -> int:
        '''Méthode publique, renvoie le nombre d'éléments dans la pile.'''
        return self.__nb_elements

    @property
    def capacite(self) -> int:
        '''Méthode publique, renvoie la capacité de la pile.'''
        return self.__capacite


    def contient(self, element: any) -> bool:
        '''Méthode publique, précise si l'élément est dans la pile.'''
        return element in self.__elements


    def est_vide(self) -> bool:
        '''Méthode publique, précise si la pile est vide.'''
        return self.__nb_elements == 0


    def est_pleine(self) -> bool:
        '''Méthode publique, précise si la pile est pleine.'''
        return self.__nb_elements == self.__capacite
    
    
    def empiler(self, element: any) -> None:
        '''Méthode publique, empile un nouvel element.'''
        if not self.est_pleine():
            self.__elements[self.__nb_elements] = element
            self.__nb_elements += 1
        else:
            print('M.I.1 : La pile est pleine.')    # Stack Overflow
    

    def depiler(self) -> any:
        '''Méthode publique, dépile le sommet et le renvoie.'''
        if not self.est_vide() :
            self.__nb_elements -= 1
            return self.__elements[self.__nb_elements]
        else:
            print('M.I.2 : La pile est vide.')


    def __str__(self) -> str:
        '''Méthode spéciale, renvoie l'affichage du contenu de la pile.'''
        if self.est_vide():
            affichage: str = 'La pile est vide'
        else:
            affichage : str = 'Contenu de la pile :\n\n   ---\n   '
            for indice in range(self.__nb_elements - 1, -1, -1):
                affichage = affichage + str(self.__elements[indice]) + '\n   ---\n   '
        return affichage



## Test des classes crées
if __name__ == '__main__':
    pile1 = Pile(10)                # création d'un objet de la classe Pile
    pile1.empiler('A')
    pile1.empiler('B')

   
    file1 = File(5)                # création d'un objet de la classe File
    for caract in 'ABCDE': file1.enfiler(caract)
    quantite = 7
    print(file1)
    for _ in range(quantite): file1.defiler()
    print(file1)
    for nombre in range(quantite): file1.enfiler(nombre)
    print(file1)
    for _ in range(quantite): file1.defiler()
    print(file1)
    for nombre in range(quantite): file1.enfiler(nombre)
    #print(pile1)
    print(file1)
