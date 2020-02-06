import os
import pickle

from carte import Carte


class Partie:
    """
    Classe qui correspond à une partie, elle contient un ensemble de méthodes
    qui permettent de gérer une partie.
    Attributs:
    *nom_fichier_carte: nom du fichier txt carte à charger.
    *carte: instance de la classe Carte.
    """

    def __init__(self):
        self.nom_fichier_carte = ""
        self.carte = Carte()

    def choisir_carte(self):
        """
        Affiche une petite interface à l'utilisateur pour choisir le fichier
        txt de carte à charger.
        """
        compteur = 0
        cartes = {}
        for nom_fichier in os.listdir("cartes"):
            if nom_fichier.endswith(".txt"):
                compteur += 1
                nom_carte = nom_fichier[:-3].lower()
                cartes[compteur] = nom_carte

        for i, nom_carte in cartes.items():
            print("{}.{}".format(i, nom_carte))

        while True:
            choix_carte = int(input("Veuillez choisir une carte:"))
            if choix_carte in cartes.keys():
                self.nom_fichier_carte = cartes[choix_carte]
                print("Vous avez choisi {}".format(self.nom_fichier_carte))
                break
            else:
                print("Veuillez rentrer un numéro valable.")

    def lire_carte(self):
        """
        Lit le fichier choisi et le convertit en instance de la classe Carte
        """
        chemin = os.path.join("cartes", self.nom_fichier_carte + "txt")
        with open(chemin, "r") as fichier:
            carte_str = fichier.read()
        self.carte.charger_txt_en_carte(carte_str)

    def charger_sauvegarde(self):
        """
        Charge une partie existante
        """
        with open("save", "rb") as f:
            unpickler = pickle.Unpickler(f)
            self.carte = unpickler.load()
        self.carte.quitter_partie = False

    def lancer_partie(self):
        """
        Contient la boucle de jeu principale.
        """
        while not self.carte.quitter_partie:
            self.carte.afficher_carte()
            if self.carte.grille[tuple(self.carte.position_robot)] == "U":
                print("Félicitations ! Vous avez gagné.")
                break
            action = input("Action:")
            self.carte.traiter_action(action)
