import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np


def afficher_labyrinthe(chemin_fichier, chemin_image_sortie=None):
    # Lecture du fichier texte (grille de caractères #, ., o, *)
    with open(chemin_fichier) as f:
        lignes = [ligne.rstrip("\n") for ligne in f if ligne.strip() != ""]

    hauteur = len(lignes)
    largeur = len(lignes[0])

    # Vérifie si le labytinthe est correct :
    for i, ligne in enumerate(lignes):
        if len(ligne) != largeur:
            raise ValueError(
                f"Ligne {i} de longueur {len(ligne)}, attendu {largeur}"
            )
        
    # Correspondance caractère -> valeur numérique
    # 0 = mur, 1 = case libre, 2 = case explorée, 3 = chemin final
    correspondance = {"#": 0, ".": 1, "*": 2, "o": 3}

    # Grille numérique vide, remplie ensuite case par case
    grille_num = np.zeros((hauteur, largeur), dtype=int)
    for y, ligne in enumerate(lignes):
        for x, caractere in enumerate(ligne):
            if caractere not in correspondance:
                raise ValueError(
                    f"Caractère inattendu '{caractere}' en position ({y}, {x})"
                )
            grille_num[y, x] = correspondance.get(caractere, 1)

    # Une couleur par valeur, dans l'ordre 0, 1, 2, 3
    couleurs = ["black", "white", "orange", "red"]
    cmap = ListedColormap(couleurs)  # import en haut du fichier : from matplotlib.colors import ListedColormap

    plt.figure(figsize=(largeur / 10, hauteur / 10))
    plt.imshow(grille_num, cmap=cmap, vmin=0, vmax=3)
    plt.axis("off")

    plt.savefig(chemin_image_sortie, dpi=150, bbox_inches="tight", pad_inches=0)
    print(f"Image enregistrée dans {chemin_image_sortie}")
    plt.close()  # libère la figure, indispensable si la fonction est appelée en boucle

if __name__ == "__main__":
    chemin_fichier = input("Veuillez rentrer un nom de fichier : ")
    chemin_image_sortie = input("Nom du fichier image de sortie (ex: labyrinthe.png) : ")
    afficher_labyrinthe(chemin_fichier, chemin_image_sortie)

