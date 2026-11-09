# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 09:11:57 2026

@author: franc
"""



import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout


class Interface_Grille(QWidget):

    def __init__(self, grille):
        super().__init__()

        self.grille = grille

        self.setWindowTitle("Démineur")

        # Création du gestionnaire de mise en forme
        layout = QGridLayout()

        # Liste qui contiendra tous les boutons
        self.boutons = []

        # Création d'un bouton pour chaque case
        for i in range(self.grille.hauteur):

            ligne_boutons = []

            for j in range(self.grille.largeur):

                bouton = QPushButton("")
                bouton.setFixedSize(40, 40)

                # Connexion du bouton à une fonction
                bouton.clicked.connect(
                    lambda checked, x=i, y=j: self.appui_bouton(x, y)
                )

                layout.addWidget(bouton, i, j)

                ligne_boutons.append(bouton)

            self.boutons.append(ligne_boutons)

        self.setLayout(layout)

    def appui_bouton(self, ligne, colonne):

        print("Appui sur la case :", ligne, colonne)
            
    
    




















