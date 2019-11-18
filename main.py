import os

from carte import Carte


def lire_carte(nom_carte):
    chemin = os.path.join("cartes", nom_carte + "txt")
    with open(chemin, "r") as fichier:
        carte_base = fichier.read()
    return carte_base


def choisir_carte():
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
            nom_carte_choisie = cartes[choix_carte]
            print("Vous avez choisi {}".format(nom_carte_choisie))
            break
        else:
            print("Veuillez rentrer un numéro valable.")

    return nom_carte_choisie


if __name__ == "__main__":
    print(
        "Bienvenue à roboc.\n"
        + "1. Nouvelle partie\n"
        + "2. Continuer une partie existante"
    )
    while True:
        choix = int(input("Votre choix:"))
        if choix == 1:
            print("\nNouvelle partie")
            nom_carte_choisie = choisir_carte()
            carte_base_txt = lire_carte(nom_carte_choisie)
            carte_actuelle = Carte(carte_base_txt)
            while not carte_actuelle.quitter_partie:
                carte_actuelle.afficher_carte()
                action = input("Action:")
                carte_actuelle.traiter_action(action)
            break
        elif choix == 2:
            print("\nContinuer u1ne partie existante")
            break
        else:
            print("\nVeuillez choisir 1 ou 2")
