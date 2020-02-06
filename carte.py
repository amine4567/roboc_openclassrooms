import copy
import pickle

from consts import OBSTACLES_BLOQUANTS
from outils import calculer_n_pas


class Carte:
    """
    Classe qui correspond à une carte.
    la classe est composée des attributs suivants:
    *grille: un dictionnaire ou chaque clé est un tuple (x, y) de la
    cellule considérée, la valeur associée est le type d'obstacle (ou non).
    *n_lignes: nombre de lignes de la grille.
    *n_cols: nombre de colonnes de la grille.
    *position_robot: liste contenant les coordonnées [x, y] du robot.
    *quitter_partie: booléen qui permet de signaler la fin d'une partie.
    """

    def __init__(self):
        self.grille = {}
        self.n_lignes = 0
        self.n_cols = 0
        self.position_robot = None
        self.quitter_partie = False

    def charger_txt_en_carte(self, carte_txt):
        """
        On passe la carte en chaine de caractères qui est alors convertie
        en grille d'obstacles et position du robot.
        La méthode vérifie aussi que la carte est correcte.
        """
        lignes = carte_txt.split("\n")
        self.n_lignes = len(lignes)
        self.n_cols = len(lignes[0])
        for i, ligne in enumerate(lignes):
            if len(ligne) != self.n_cols:
                raise ValueError(
                    "Il y'a un problème sur la carte. "
                    + "Toutes les lignes n'ont pas le même nombre de colonnes."
                )
            for j, col in enumerate(ligne):
                if col == "X":
                    if self.position_robot is None:
                        self.position_robot = [i, j]
                        # On ne met pas le robot sur la grille
                        self.grille[(i, j)] = " "
                    else:
                        raise ValueError("Il y'a plus d'un seul robot sur la carte.")
                else:
                    self.grille[(i, j)] = col

        if self.position_robot is None:
            raise ValueError("Il n'y'a aucun robot sur la carte.")

    def obtenir_carte(self, mettre_joueur=False):
        """
        Obtenir la carte sous forme d'une chaine de caractères
        """
        grille_actuelle_txt = ""
        for i in range(self.n_lignes):
            for j in range(self.n_cols):
                if mettre_joueur and tuple(self.position_robot) == (i, j):
                    grille_actuelle_txt += "X"
                else:
                    grille_actuelle_txt += self.grille[(i, j)]

            grille_actuelle_txt += "\n"

        return grille_actuelle_txt

    def afficher_carte(self):
        """
        méthode qui affiche la carte de façon élégante avec le
        robot bien positionné.
        """
        grille_actuelle_txt = self.obtenir_carte(mettre_joueur=True)
        print(grille_actuelle_txt)

    def bouger_un_pas(self, direction):
        """
        Méthode qui traite les actions de mouvement du robot par pas.
        C'est au niveau de cette méthode que les obstacles sont traités.
        La fonction retourne un booléen qui est vrai s'il y'a un obstacle
        bloquant.
        """
        new_position = copy.deepcopy(self.position_robot)
        if direction == "n":
            new_position[0] -= 1
        elif direction == "s":
            new_position[0] += 1
        elif direction == "e":
            new_position[1] += 1
        elif direction == "o":
            new_position[1] -= 1

        if self.grille[tuple(new_position)] not in OBSTACLES_BLOQUANTS:
            self.position_robot = new_position
            if self.grille[tuple(self.position_robot)] == "U":
                return True  # Le chemin s'arrête si le robot est sur la porte
            return False
        else:
            print("Il y'a un obstacle bloquant sur le chemin")
            return True  # Le chemin s'arrête si on rencontre un obstacle bloquant

    def bouger_n_pas(self, action):
        """
        Méthode qui traite les actions de mouvement du robot en plusieurs pas.
        Execute la méthode bouger_un_pas en boucle et s'arrête quand nécessaire.
        """
        direction = action[0].lower()
        n_pas = calculer_n_pas(action)
        for i in range(n_pas):
            stop = self.bouger_un_pas(direction)
            if stop:
                break

    def traiter_action(self, action):
        """
        Méthode qui traite les actions de l'utilisateur en faisant appel
        aux fonctions adéquates.
        """
        if action.startswith(("n", "N", "s", "S", "e", "E", "o", "O")):
            self.bouger_n_pas(action)
        elif action in ["q", "Q"]:
            self.quitter_partie = True
            print("Vous allez quitter la partie.\n Partie sauvegardée.")
        else:
            print("Action inconnue.")

        self.sauvegarder_carte()

    def sauvegarder_carte(self):
        """
        Méthode qui sauvegarde l'état actuel de la carte dans un fichier.
        """
        with open("save", "wb") as f:
            pickler = pickle.Pickler(f)
            pickler.dump(self)
