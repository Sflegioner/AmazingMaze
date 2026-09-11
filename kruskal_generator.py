import random
import time

n = int(input("Veuillez rentrer un nombre : "))


def cellules_voisines(mur):
    y, x = mur
    if y % 2 == 1:   # mur horizontal -> gauche/droite
        return (y, x-1), (y, x+1)
    else:            # mur vertical -> haut/bas
        return (y-1, x), (y+1, x)
    
# Génération de la grille :
def labyrinthe(n):
    grille = []
    for x in range(2*n+1):
        ligne = ['#' for _ in range(2*n+1)]
        grille.append(ligne)
    return grille

def generer_labyrinthe():
    grille = labyrinthe(n)

    murs_conn_h = [(y,x) for y in range(1, 2*n, 2)   for x in range(2, 2*n-1, 2)]   # y impair, x pair → mur horizontal
    murs_conn_v = [(y,x) for y in range(2, 2*n-1, 2) for x in range(1, 2*n, 2)]    # y pair, x impair → mur vertical

    cellules = [(y,x) for y in range (1, 2*n, 2) for x in range (1, 2*n, 2)]
    groupe = {c: c for c in cellules}
    
    for (y, x) in cellules : 
        grille[x][y] = "."

    murs = murs_conn_h + murs_conn_v
    random.shuffle(murs)

    # Kruskal
    for mur in murs : 
        c1, c2 = cellules_voisines(mur)

        # On casse le mur
        if groupe[c1] != groupe[c2]:
            (y, x) = mur
            grille[y][x] = "."
            rep1, rep2 = groupe[c1], groupe[c2]
            # Fusion des groupes
            for c in groupe :
                if groupe[c] == rep2:
                    groupe[c] = rep1
    return grille

def afficher(grille) :
    for ligne in grille :
        print(''.join(ligne))


depart = time.time()
grille_finale = generer_labyrinthe()
grille_finale[0][1] = "."
grille_finale[2*n-1][2*n] = "."
afficher(grille_finale)
fin = time.time() - depart
print(f"Le temps total de création du labyrinthe avec le backtracking récursif est de {fin} secondes.")

###### Affichage et création fichier :
def afficher_dans_fichier(grille) :
    texte = ""
    for ligne in grille : 
        texte +=''.join(ligne) + "\n"
    return texte

while True:                                  
    nom_fichier = input("Veuillez rentrer un nom de fichier : ")
    try:
        # "x" crée le fichier, et lève FileExistsError s'il existe déjà
        with open(f"{nom_fichier}.txt", "x"):
            pass                             # on ne fait rien : on voulait juste créer le fichier
        break                                # aucune erreur -> on sort de la boucle
    except FileExistsError:
        print("Nom déjà utilisé, donnez un autre nom.")


with open(f"{nom_fichier}.txt", "a") as f :
    f.write(f"{afficher_dans_fichier(grille_finale)}")
    print("Fichier généré !")

