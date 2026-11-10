# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 09:11:57 2026

@author: franc
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QMessageBox

"""
Commandes :
Clique droit pour poser un drapeau
Clique Gauche pour miner
"""

class BoutonCase(QPushButton):
    '''case cliquable'''
    def __init__(self, ligne, colonne, interface):
        super().__init__("")
        self.ligne = ligne
        self.colonne = colonne
        self.interface = interface
        self.setFixedSize(40, 40)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.interface.clic_gauche(self.ligne, self.colonne)
        elif event.button() == Qt.RightButton:
            self.interface.clic_droit(self.ligne, self.colonne)


class Interface_Grille(QWidget):
    '''Interface graphique du démineur'''
    def __init__(self, grille):
        super().__init__()
        self.grille = grille
        self.fini = False
        self.setWindowTitle("Démineur")
        layout = QGridLayout()
        layout.setSpacing(0)
        self.boutons = []
        for i in range(self.grille.lignes):
            ligne_boutons = []
            for j in range(self.grille.colonnes):
                bouton = BoutonCase(i, j, self)
                layout.addWidget(bouton, i, j)
                ligne_boutons.append(bouton)
            self.boutons.append(ligne_boutons)
        self.setLayout(layout)

    def clic_gauche(self, ligne, colonne):
        #on ne fait rien si le jeu est fini
        if self.fini == True:
            return
        case = self.grille.cases[ligne, colonne]
        #on ne peut pas cliquer sur un drapeau
        if case.etat == "drapeau":
            return
        #on perd si on clique sur une mine
        if case.mine is not None:
            self.perdre()
            return
        self.grille.devoiler(ligne, colonne)
        self.mettre_a_jour()
        if self.victoire():
            self.fini = True
            QMessageBox.information(self, "Démineur", "Gagné !")

    def clic_droit(self, ligne, colonne):
        #le clique droit gère les drapeau
        if self.fini == True:
            return
        self.grille.placer_drapeau(ligne, colonne)
        self.mettre_a_jour()

    def victoire(self):
        return all(
            c.mine is not None or c.etat == "dévoilé"
            for c in self.grille.cases.flat
        )

    def perdre(self):
        self.fini = True
        for c in self.grille.cases.flat:
            if c.mine is not None:
                c.etat = "dévoilé"
        self.mettre_a_jour()
        QMessageBox.information(self, "Démineur", "Perdu !")

    def mettre_a_jour(self):
        for i in range(self.grille.lignes):
            for j in range(self.grille.colonnes):
                case = self.grille.cases[i, j]
                bouton = self.boutons[i][j]
                #si la case est dévoilée, on vérifie si c'est une mine, sinon on affiche le nombre de mines ajacentes
                if case.etat == "dévoilé":
                    if case.mine is not None:
                        bouton.setText("X")
                        bouton.setStyleSheet("background-color: red;")
                    else:
                        n = case.mines_adjacentes
                        if n > 0 :
                            bouton.setText(str(n))
                            bouton.setStyleSheet("background-color: white;")
                        else : 
                            bouton.setText("")
                            bouton.setStyleSheet("background-color: white;")
                #si la case n'est pas dévoilée, on verifie si c'est un drapeau, et sinon on affiche rien
                elif case.etat == "drapeau":
                    bouton.setText("F")
                    bouton.setStyleSheet("color: red")
                else:
                    bouton.setText("")
                    bouton.setStyleSheet("")
            
    
    




















