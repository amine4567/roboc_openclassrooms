"""
Le fichier python à exécuter avec python pour lancer le jeu
"""

import os

from partie import Partie

if __name__ == "__main__":
    print(
        "Bienvenue à roboc.\n"
        + "1. Nouvelle partie\n"
        + "2. Continuer une partie existante"
    )
    while True:
        choix = int(input("Votre choix:"))
        jeu = Partie()
        if choix == 1:
            print("\nNouvelle partie")
            jeu.choisir_carte()
            jeu.lire_carte()
            jeu.lancer_partie()
            break
        elif choix == 2:
            print("\nContinuer une partie existante")
            if os.path.exists("save"):
                jeu.charger_sauvegarde()
                jeu.lancer_partie()
                break
            else:
                print("Il n'y'a aucune partie sauvegardée.")
        else:
            print("\nVeuillez choisir 1 ou 2")
