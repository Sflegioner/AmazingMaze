import math
import random
import time 
import sys
import heapq   # module standard pour gérer une file de priorité (l'"open set")



while True :
    choix_utilisateur = input(
        "Choisissez une methode de résolution de labyrinthe :\n"
        " - Tapez 1 pour le backtracking récursif\n"
        " - Tapez 2 pour l'algorithme Astar\n"
        " - Tapez q pour quitter\n"
        "Entrez votre choix : "
    )

# Backtracking récursif :
    if choix_utilisateur == "1" :
        def lire_labyrinthe(nom_fichier):
            with open(f"{nom_fichier}.txt", "r") as f:
                lignes = f.read().splitlines()
            return [list(ligne) for ligne in lignes]

        def deduire_n(grille):
            # La grille fait toujours (2n+1) x (2n+1) : n s'en déduit directement
            hauteur = len(grille)
            largeur = len(grille[0])
            assert hauteur == largeur, "la grille n'est pas carrée"
            return (hauteur - 1) // 2

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
            global compteur
            if (y, x) == (y_sortie, x_sortie):
                grille[y][x] = "o"
                return True

            visite.add((y, x))

            direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dy, dx in direction:
                compteur += 1
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
            compteur = 0
            nom_fichier = input("Nom du fichier du labyrinthe a resoudre : ")
            grille = lire_labyrinthe(nom_fichier)
            n = deduire_n(grille)
            sys.setrecursionlimit((2*n+1)**2)

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
            nom_sortie = input(f"La solution a été générée en {arrivee:.6f} secondes pour un coût de {compteur} opérations (test de voisins). Nom du fichier de sortie (labyrinthe + solution) : ")
            with open(f"{nom_sortie}_btr.txt", "w") as f:
                f.write(afficher_dans_fichier(grille))
        break


# Astar :
    if choix_utilisateur== "2":

        def A_Star(name_of_file: str):
            maze = load_maze(name_of_file)

            start = (1, 0)
            finish = (len(maze)-2, len(maze[0])-1)  # attention: -1 et non -2 comme avant
            maze[finish[0]][finish[1]] = "."

            # open_set : file de priorité (f, position) -> on prend toujours la case
            # au f le plus bas, où qu'elle soit dans le labyrinthe (pas seulement voisine)
            open_set = [(heuristic(start, finish), start)]

            # g_score : coût réel connu pour atteindre chaque case depuis le départ
            g_score = {start: 0}

            # came_from : pour chaque case, la case depuis laquelle on y est arrivé
            # -> permet de reconstruire le chemin final une fois la sortie trouvée
            came_from = {}

            # closed_set : cases déjà définitivement traitées (évite de les retraiter)
            closed_set = set()

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            while open_set:
                _, current = heapq.heappop(open_set)

                if current in closed_set:
                    continue
                closed_set.add(current)

                if current == finish:
                    path = reconstruct_path(came_from, current)
                    mark_path(maze, path, closed_set)
                    print_maze(maze)
                    return

                for dy, dx in directions:
                    ny, nx = current[0] + dy, current[1] + dx
                    neighbor = (ny, nx)

                    if not (0 <= ny < len(maze) and 0 <= nx < len(maze[0])):
                        continue
                    if maze[ny][nx] == "#":
                        continue
                    if neighbor in closed_set:
                        continue

                    tentative_g = g_score[current] + 1

                    # si on n'a jamais vu cette case, ou si on a trouvé un chemin
                    # moins coûteux pour l'atteindre, on met à jour
                    if tentative_g < g_score.get(neighbor, float("inf")):
                        g_score[neighbor] = tentative_g
                        came_from[neighbor] = current
                        f = tentative_g + heuristic(neighbor, finish)
                        heapq.heappush(open_set, (f, neighbor))

            print("Pas de solution trouvée")


        def reconstruct_path(came_from, current):
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path


        def mark_path(maze, path, closed_set):
            # "*" pour les cases explorées mais hors chemin final
            for (y, x) in closed_set:
                if maze[y][x] == ".":
                    maze[y][x] = "*"
            # "o" pour le chemin final (écrase les "*" éventuels sur ce chemin)
            for (y, x) in path:
                maze[y][x] = "o"


        def heuristic(a, b):
            # distance de Manhattan
            return abs(a[0] - b[0]) + abs(a[1] - b[1])


        def load_maze(name_of_file: str):
            maze = []
            with open(name_of_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        maze.append(list(line))
            return maze


        def print_maze(maze):
            for row in maze:
                print("".join(row))
            print()

        def afficher(grille):
            for ligne in grille:
                print(''.join(ligne))

        def afficher_dans_fichier(grille):
            texte = ""
            for ligne in grille:
                texte += ''.join(ligne) + "\n"
            return texte


        name_of_file = input("Nom du fichier du labyrinthe à résoudre : ")
        start = time.time()
        A_Star(name_of_file)
        finish = time.time() - start
        name_output = input(f"Le labyrinthe a été résolu en {finish:.5f} seconde(s). Donnez un nom au fichier généré : ")
        with open(f"{name_output}_ar.txt", "w") as f:
            f.write(afficher_dans_fichier(name_of_file))
        break
