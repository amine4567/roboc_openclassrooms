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

    def traiter_action(self, action):
        # TODO: checker les obstacles, etc
        # TODO: gérer les déplacements multiples
        # TODO: sauvegarder avant de quitter
        if action == "n":
            self.position_robot[0] -= 1
        elif action == "s":
            self.position_robot[0] += 1
        elif action == "e":
            self.position_robot[1] += 1
        elif action == "o":
            self.position_robot[1] -= 1
        elif action == "q":
            self.quitter_partie = True