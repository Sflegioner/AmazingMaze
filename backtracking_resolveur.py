import sys
import time


def lire_labyrinthe(nom_fichier):
    with open(f"{nom_fichier}.txt", "r") as f:
        lignes = f.read().splitlines()
    return [list(ligne) for ligne in lignes]


def afficher(grille):
    for ligne in grille:
        print(''.join(ligne))


def afficher_dans_fichier(grille):
    texte = ""
    for ligne in grille:
        texte += ''.join(ligne) + "\n"
    return texte


def trouver_ouverture(grille, bord):
    """Cherche la case '.' percee sur un bord donne de la grille.
    Renvoie (y, x) de la premiere case ouverte trouvee sur ce bord, ou None."""
    hauteur, largeur = len(grille), len(grille[0])
    if bord == "haut":
        return next(((0, x) for x in range(largeur) if grille[0][x] == "."), None)
    if bord == "bas":
        return next(((hauteur - 1, x) for x in range(largeur) if grille[hauteur - 1][x] == "."), None)
    if bord == "gauche":
        return next(((y, 0) for y in range(hauteur) if grille[y][0] == "."), None)
    if bord == "droite":
        return next(((y, largeur - 1) for y in range(hauteur) if grille[y][largeur - 1] == "."), None)


def trouver_entree_sortie(grille):
    """L'entree est percee soit sur le bord du haut, soit sur le bord gauche.
    La sortie est percee soit sur le bord du bas, soit sur le bord droit.
    On ne suppose plus que ce sont forcement les coins (0,0) / (2n,2n)."""
    entree = trouver_ouverture(grille, "haut") or trouver_ouverture(grille, "gauche")
    sortie = trouver_ouverture(grille, "bas") or trouver_ouverture(grille, "droite")
    return entree, sortie


def resoudre(grille, y, x, y_sortie, x_sortie, visite):
    if (y, x) == (y_sortie, x_sortie):
        grille[y][x] = "o"
        return True

    visite.add((y, x))

    direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dy, dx in direction:
        ny, nx = y + dy, x + dx
        deplacement_valide = (
            0 <= ny < len(grille)
            and 0 <= nx < len(grille[0])
            and grille[ny][nx] != "#"
            and (ny, nx) not in visite
        )
        if deplacement_valide:
            if resoudre(grille, ny, nx, y_sortie, x_sortie, visite):
                grille[y][x] = "o"
                return True

    grille[y][x] = "*"
    return False


if __name__ == "__main__":
    
    nom_fichier = input("Nom du fichier du labyrinthe a resoudre : ")
    grille = lire_labyrinthe(nom_fichier)

    entree, sortie = trouver_entree_sortie(grille)
    if entree is None or sortie is None:
        print("Impossible de trouver l'entree ou la sortie sur les bords de la grille.")
        sys.exit()

    y_entree, x_entree = entree
    y_sortie, x_sortie = sortie

    depart = time.time()
    try:
        trouve = resoudre(grille, y_entree, x_entree, y_sortie, x_sortie, set())
    except RecursionError:
        print("Labyrinthe trop grand pour le backtracking recursif (limite de recursion Python atteinte).")
        sys.exit()

    if not trouve:
        print("Aucun chemin trouve entre l'entree et la sortie.")

    afficher(grille)
    arrivee = time.time() - depart
    nom_sortie = input(f"La solution a été générée en {arrivee:.6f} secondes. Nom du fichier de sortie (labyrinthe + solution) : ")
    with open(f"{nom_sortie}_btr.txt", "w") as f:
        f.write(afficher_dans_fichier(grille))