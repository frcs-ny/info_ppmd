# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 11:33:33 2026

@author: franc
"""

"""
Les instructions pour jouer s'affichent dans le terminal.
A chaque tour, on a le choix entre miner ou poser un drapeau. 
Il faut entrer m pour miner et d pour poser un drapeau.
On doit ensuite entrer le numéro de la ligne et colonne où l'on veut agir.
"""
import numpy as np
import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
from interface import Interface_Grille

class JeuDeDemineur():
    def __init__(self,grille,etat='en cours'):
        self.g = grille
        self.etat = etat
        
    def Jeu(self):
        while self.etat == "en cours":
            self.g.afficher()
            self.g.afficher_mines()
            a = str(input('que veux tu faire ? d = drapeau/m = miner').strip())
            ligne = int(input('sur quelle ligne ?').strip())
            colonne = int(input('sur quelle colonne ?').strip())
            if a == 'm' :
                action = [ligne,colonne]
                self.g.devoiler(ligne,colonne)
                
                #on vérifie si il y a une mine
                if self.g.cases[ligne,colonne].mine != None :
                    self.g.afficher()
                    print( 'Perdu' )
                    break
                else :
                    self.g.afficher()
            if a == 'd':
                self.g.placer_drapeau(ligne, colonne)
            
  
    
        
class Grille():
    def __init__(self, colonnes, lignes):
        self.colonnes = colonnes
        self.lignes = lignes
        # Initialisation des mines
        mines = []
        while len(mines) < lignes:
            pos = Position(random.randint(0, colonnes - 1),random.randint(0, lignes - 1))                               
            # Vérification que la position n'est pas déjà utilisée
            if not any(m.position == pos for m in mines):
                mines.append(Mine(pos))
                
        #On crée ensuite les cases
        cases = np.zeros((lignes,colonnes),dtype = Case)
        for i in range(lignes):
            for j in range(colonnes):
                cases[i,j] = Case(None,'caché',None)
                for k in range(len(mines)):
                    if (j,i) == (mines[k].position.x,mines[k].position.y):
                        cases[i,j].mine = mines[k]
        self.cases = cases
        
        # Calcul des mines adjacentes
        for i in range(lignes):
            for j in range(colonnes):
                self.cases[i][j].mines_adjacentes = (
                    self.compter_mines(i, j)
                )
    def est_valide(self, ligne, colonne):
        return (
            0 <= ligne < self.lignes
            and 0 <= colonne < self.colonnes
        )

    def voisins(self, ligne, colonne):
        voisins = []
        for i in range(ligne - 1, ligne + 2):
            for j in range(colonne - 1, colonne + 2):
                if self.est_valide(i, j):
                    if (i, j) != (ligne, colonne):
                        voisins.append((i, j))
        return voisins

    def compter_mines(self, ligne, colonne):
        compteur = 0
        for i, j in self.voisins(ligne, colonne):
            if self.cases[i][j].mine is not None:
                compteur += 1
        return compteur

    def devoiler(self, ligne, colonne):
        # Dévoilement automatique des cases voisines
        a_visiter = [(ligne, colonne)]
        while a_visiter:
            i, j = a_visiter.pop()
            case = self.cases[i][j]
            if case.etat != "caché":
                continue
            if case.mine is not None:
                continue
            case.etat = "dévoilé"
            # Si la case ne touche aucune mine,
            # on dévoile également ses voisines.
            if case.mines_adjacentes == 0:
                for x, y in self.voisins(i, j):
                    if self.cases[x][y].etat == "caché":
                        a_visiter.append((x, y))
    
        
    def afficher(self):
        affichage = ""
        for i in range(self.lignes):
            for j in range(self.colonnes):
                if self.cases[i,j].etat == "dévoilé":
                    if self.cases[i,j].mine == None:
                        affichage += '[' + str(self.cases[i,j].mines_adjacentes) + ']'
                    else:
                        affichage += '[X]'
    
                elif self.cases[i,j].etat == "drapeau":
                    affichage += '[F]'
    
                else:
                    affichage += '[ ]'
    
            affichage += '\n'
    
        print(affichage)
        
    def afficher_mines(self):
        affichage = ""
        for i in range(self.lignes):
            for j in range(self.colonnes):
                if self.cases[i,j].mine == None:
                        affichage += '[ ]'
                else:
                        affichage += '[X]'
    
    
            affichage += '\n'
    
        print(affichage)

    def placer_drapeau(self, ligne, colonne):
        case = self.cases[ligne][colonne]
        #cliquer sur un case ajouter un drapeau
        if case.etat == "caché":
            case.etat = "drapeau"
            print("Drapeau posé !\n")
        #recliquer sur cette même case enleve le drapeau
        elif case.etat == "drapeau":
            case.etat = "caché"
            print("Drapeau retiré !\n")

        else:
            print("Impossible de poser un drapeau ici.\n")
        
        
class Case():
    def __init__(self,mine,etat,mines_adjacentes):
        self.mine = mine
        self.etat = etat
        self.mines_adjacentes = mines_adjacentes
     
        
class Mine():
    def __init__(self,position):
        self.position = position
        
class Position():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
class Drapeau():
    def __init__(self,etat,position):
        self.etat = etat
        self.position = position
        
        
        
if __name__ == "__main__":
    
    # ---- Jouer dans la console ---- #
    '''
    g = Grille(10,10)
    J = JeuDeDemineur(g)
    J.Jeu()
    '''
    
    # ---- Jouer avec l'interface graphique ---- #
    app = QApplication.instance() or QApplication(sys.argv)
    g = Grille(10, 10)
    fen = Interface_Grille(g)
    fen.show()
    app.exec_()
    
        
        
        
        
        