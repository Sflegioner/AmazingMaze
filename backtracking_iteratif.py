import random
import time

n = int(input("Veuillez rentrer un nombre : "))

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


def backtracking(grille, n):
    pile = [(1,1)]
    grille[1][1]="."
    while pile :
        # Ici, pile[-1] regarde le dernier élément de la pile
        y, x = pile[-1]
        voisins = voisins_non_visites(grille, y, x, n)
        # Si la liste contient qq chose : 
        if voisins :
            # Choisir un élément de la liste
            ny, nx = random.choice(voisins)
            # Le mur passe de "#" à "."
            grille [(y+ny)//2][(x+nx)//2] = "."
            # L'élément visité passe de "#" à "."
            grille [(ny)][(nx)] = "."
            pile.append((ny, nx))
        else :
            pile.pop()
    return grille

depart = time.time()
grille_finale = backtracking(grille_generee, n)
grille_finale[0][0] = "."
grille_finale[2*n][2*n] = "."
afficher(grille_finale)
fin = time.time() - depart
print(f"Le temps total de création du labyrinthe avec le backtracking itératif est de {fin} secondes.")
