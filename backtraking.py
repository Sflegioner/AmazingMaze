import random
import time

while True :
    n = int(input("Veuillez rentrer un nombre en dessous de 45 : "))
    if n<=45 :
        break
    else :
        print("Le nombre d'appel récursif sera trop élevé si n>45, et le programme plantera.")


def labyrinthe(n):
    largeur = 2*n+1
    hauteur = 2*n+1

    grille = []
    for x in range(hauteur):
        ligne = ['#' for _ in range(largeur)]
        grille.append(ligne)
    return grille

def afficher(grille) :
    for ligne in grille :
        print(''.join(ligne))

def afficher_dans_fichier(grille) :
    texte = ""
    for ligne in grille : 
        texte +=''.join(ligne) + "\n"
    return texte

grille_generee = labyrinthe(n)

def voisins_non_visites(grille, y, x, n) :
    # Création d'une liste de tuples de direction
    direction = [(-2,0), (2,0),(0,-2),(0, 2)]

    cel_potentielles = []
    for dy, dx in direction : 
        ny, nx = (y+dy), (x+dx)
        if 1 <= ny <= 2*n-1 and 1 <= nx <= 2*n-1 and grille[ny][nx] == "#":
            cel_potentielles.append((ny,nx))
    return cel_potentielles


def backtracking(grille, y, x, n):
    # On marque la cellule courante comme visitée
    grille[y][x] = "."

    voisins = voisins_non_visites(grille, y, x, n)

    # Tant que la cellule courante a encore des voisins à explorer
    while voisins:
        # Choisir une direction au hasard
        ny, nx = random.choice(voisins)
        # Ouvrir le mur entre la cellule courante et la voisine
        grille[(y+ny)//2][(x+nx)//2] = "."
        # Descendre dans la voisine : c'est ici que la pile d'appels grandit
        backtracking(grille, ny, nx, n)
        # Au retour de l'appel, la branche explorée a visité d'autres cellules :
        # il faut recalculer la liste, certains voisins ne sont plus "#"
        voisins = voisins_non_visites(grille, y, x, n)
    # Plus aucun voisin : la fonction se termine, on remonte automatiquement
    # d'un cran dans la pile d'appels (équivalent du pop())

depart = time.time()
backtracking(grille_generee, 1, 1, n)
grille_generee[0][1] = "."
grille_generee[2*n-1][2*n] = "."
afficher(grille_generee)
fin = time.time() - depart
print(f"Le temps total de création du labyrinthe avec le backtracking récursif est de {fin} secondes.")

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
    f.write(f"{afficher_dans_fichier(grille_generee)}")
    print("Fichier généré !")
with open(".gitignore", "a") as f:
  f.write(f"{nom_fichier}.txt")