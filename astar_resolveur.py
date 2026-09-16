import heapq
import time

def charger_labyrinthe(chemin_fichier):
    with open(chemin_fichier) as f:
        lignes = [ligne.rstrip("\n") for ligne in f]
    lignes = [ligne for ligne in lignes if ligne != ""]  # ignore une éventuelle ligne vide en fin de fichier
    return [list(ligne) for ligne in lignes]


def deduire_n(grille):
    # La grille fait toujours (2n+1) x (2n+1) : n s'en déduit directement
    hauteur = len(grille)
    largeur = len(grille[0])
    assert hauteur == largeur, "la grille n'est pas carrée"
    return (hauteur - 1) // 2


def voisins_accessibles(grille, y, x, n):
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    voisins = []

    for dx, dy in directions:
        nx, ny = x+dx, y+dy
        # Mur entre les deux cellules
        # my, mx = y + dy // 2, x + dx // 2
        if 1 <= ny <= 2*n - 1 and 1 <= nx <= 2*n - 1 and grille[ny][nx] == ".":
            voisins.append((ny, nx))
    return voisins


def astar(grille, debut, fin, n):
    tas_a_voir = []
    g_score = {debut: 0}
    h_score = {debut: abs(debut[0]-fin[0]) + abs(debut[1]-fin[1])}
    parent = {}
    deja_vu = set()
    heapq.heappush(tas_a_voir, (g_score[debut] + h_score[debut], debut))

    while tas_a_voir:
        f_actuel, actuel = heapq.heappop(tas_a_voir)

        if actuel in deja_vu:
            continue
        deja_vu.add(actuel)

        if actuel == fin:
            chemin = [actuel]
            while chemin[-1] in parent:
                chemin.append(parent[chemin[-1]])
            chemin.reverse()
            return chemin, g_score[fin], deja_vu

        for voisin in voisins_accessibles(grille, actuel[0], actuel[1], n):
            if voisin in deja_vu:
                continue
            g_tentatif = g_score[actuel] + 2
            if voisin not in g_score or g_tentatif < g_score[voisin]:
                g_score[voisin] = g_tentatif
                h = abs(voisin[0]-fin[0]) + abs(voisin[1]-fin[1])
                parent[voisin] = actuel
                heapq.heappush(tas_a_voir, (g_tentatif + h, voisin))
    return None, None, deja_vu

def sauvegarder_solution(grille, chemin, explores, chemin_sortie):
    # copie de la grille pour ne pas modifier l'originale en mémoire
    grille_solution = [ligne.copy() for ligne in grille]

    chemin_set = set(chemin) 

    # accès rapide (O(1)) pour tester l'appartenance au chemin
    # 1) on marque d'abord les cases explorées mais hors chemin final
    for (y, x) in explores:
        if (y, x) not in chemin_set :
            grille_solution[y][x] = '*'

    # 2) puis le chemin final, en dernier pour qu'il ne soit jamais écrasé
    for (y, x) in chemin:
        grille_solution[y][x] = 'o'

    # Les cases de départ et d'arrivée :
    grille_solution[1][0] = 'o'
    grille_solution[2*n-1][2*n] = 'o'

    with open(chemin_sortie, "w") as f:
        for ligne in grille_solution:
            f.write("".join(ligne) + "\n")

chemin_fichier = input("Choisissez le fichier à traiter : ")
if not chemin_fichier.endswith(".txt"):
    chemin_fichier += ".txt"
grille = charger_labyrinthe(chemin_fichier)
n = deduire_n(grille)
debut = (1, 1)
fin = (2*n - 1, 2*n - 1)   # corrigé

depart = time.time()
chemin, cout, explores = astar(grille, debut, fin, n)
fin = time.time() - depart


if chemin is None:
    print("Aucun chemin trouvé entre le départ et l'arrivée.")
else:
    while True:
        nom_fichier = input("Veuillez rentrer un nom de fichier de sauvegarde : ")
        chemin_sortie = f"{nom_fichier}_ar.txt"
        try:
            with open(chemin_sortie, "x"):
                pass
            sauvegarder_solution(grille, chemin, explores, chemin_sortie)
            print(f"Chemin trouvé (coût = {cout}) en {fin} secondes. Résultat écrit dans {chemin_sortie}.")
            break
        except FileExistsError:
            print("Nom déjà utilisé, donnez un autre nom.")

