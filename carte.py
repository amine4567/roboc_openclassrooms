import copy
import pickle


def calculer_n_pas(action):
    if len(action) != 1:
        try:
            n_pas = int(action[1:])
            assert n_pas >= 0
            return n_pas
        except (ValueError, AssertionError):
            print("Il faut que le nombre de pas soit un entier positif.")
        return 0
    else:
        return 1


class Carte:
    def __init__(self, carte_txt):
        self.grille = {}
        self.n_lignes = 0
        self.n_cols = 0
        self.position_robot = None
        self.quitter_partie = False

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

    def afficher_carte(self):
        grille_actuelle_txt = ""
        for i in range(self.n_lignes):
            for j in range(self.n_cols):
                if tuple(self.position_robot) == (i, j):
                    grille_actuelle_txt += "X"
                else:
                    grille_actuelle_txt += self.grille[(i, j)]
            grille_actuelle_txt += "\n"

        print(grille_actuelle_txt)

    def bouger_un_pas(self, direction):
        new_position = copy.deepcopy(self.position_robot)
        if direction == "n":
            new_position[0] -= 1
        elif direction == "s":
            new_position[0] += 1
        elif direction == "e":
            new_position[1] += 1
        elif direction == "o":
            new_position[1] -= 1

        if self.grille[tuple(new_position)] != "O":
            self.position_robot = new_position
            if self.grille[tuple(self.position_robot)] == "U":
                return True  # Le chemin s'arrête si le robot est sur la porte
            return False
        else:
            print("Il y'a un mur sur le chemin")
            return True  # Le chemin s'arrête si on rencontre un mur

    def bouger_n_pas(self, action):
        direction = action[0].lower()
        n_pas = calculer_n_pas(action)
        for i in range(n_pas):
            stop = self.bouger_un_pas(direction)
            if stop:
                break

    def traiter_action(self, action):
        if action.startswith(("n", "N", "s", "S", "e", "E", "o", "O")):
            self.bouger_n_pas(action)
        elif action in ["q", "Q"]:
            self.quitter_partie = True
            self.sauvegarder_carte()
            print("Vous allez quitter la partie.\n Partie sauvegardée.")
        else:
            print("Action inconnue.")

    def sauvegarder_carte(self):
        with open("save", "wb") as f:
            pickler = pickle.Pickler(f)
            pickler.dump(self)
