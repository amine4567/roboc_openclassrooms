"""
Module qui contient des fonctions utiles pour les autres classes.
"""


def calculer_n_pas(action):
    """
    Une fonction qui permet d'extraire le nombre de pas d'une action
    de mouvement. par exemple si l'utilisateur rentre "n3", la fonction
    renvoie 3.
    Elle vérifie aussi que l'utilisateur rentre un entier positif.
    """
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
