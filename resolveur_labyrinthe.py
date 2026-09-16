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

        # f(n) = g(n) + h(n)
        def A_Star(name_of_file:str): 
            #               y,x
            maze = load_maze(name_of_file)

            current_cell = [0,1]
            finish_point = [len(maze) - 2, len(maze[0]) - 1]
            maze[finish_point[0]][finish_point[1]] = "."

            g=0

            while True:
                g = g + 1
                if current_cell == finish_point:
                    # print("FINISH")
                    maze[finish_point[0]][finish_point[1]] = "o"
                    print_maze(maze)
                    return maze
                current_cell = check_next_cell_(maze_to_solve=maze,current_cell=current_cell,finish_point=finish_point,g=g)
            


        def check_next_cell_(maze_to_solve:list,current_cell:list,finish_point:tuple,g:int)->tuple:
            """return best cell to choose """

            posible_ways = []
            directions = {"up":(-1,0), "down":(1,0), "left":(0,-1), "right":(0,1)}

            tryed_steps = 0 # for checking dead end only 4 tries if not go and block by ~
            for d in directions:
                #try to go untill branching(embranchment)
                new_y = current_cell[0] + directions[d][0]
                new_x = current_cell[1] + directions[d][1]
                #add posible cells to go
                if maze_to_solve[new_y][new_x] == "." and maze_to_solve[new_y][new_x] != "o":
                    posible_ways.append((new_y,new_x))
                    maze_to_solve[current_cell[0]][current_cell[1]] = "o"
                

            #go if its only 1 way to go
            if len(posible_ways) == 1:
                current_cell = list(posible_ways[0])
                # print("new point setted")

            #find where is V and bound(assinne)
            elif len(posible_ways) == 0:
                # print("DEAD_END")
                maze_to_solve[current_cell[0]][current_cell[1]] = "*"
                for d in directions:
                    new_y = current_cell[0] + directions[d][0]
                    new_x = current_cell[1] + directions[d][1]
                    
                    if maze_to_solve[new_y][new_x] == "o":
                        current_cell = [new_y, new_x]
                        break
                            
                return current_cell


            else:
                #choose best way
                #mathetan distance to implement
                list_to_find = []
                for way in posible_ways:
                    h = heuristic(way[1], finish_point[1], way[0], finish_point[0])
                    f = h + g
                    list_to_find.append([f,way])
                    # print(list_to_find)
                
                best_y,best_x=take_lovest_cells(list_to_find)
                current_cell = [best_y,best_x]
                # print("new point setted")
                pass

            # print_maze(maze_to_solve)
            return current_cell

        #____________________________________________________________________

        def take_lovest_cells(arr: list) -> tuple:
            if not arr:
                return None  
            best_way = arr[0]
            
            for way in arr:
                if way[0] < best_way[0]:
                    best_way = way
            # print(f'Best way - {best_way[1]} - lowest f - {way}')
            return best_way[1]

        def heuristic(x2,x1,y2,y1):   
            return abs(x2 - x1) + abs(y2 - y1)

        def load_maze(name_of_file: str):
            maze = []
            with open(name_of_file, "r") as f:
                for line in f:
                    line = line.strip()                 
                    if line:                            
                        maze.append(list(line))         
            return maze

        def print_maze(maze):
            print("________________________________")
            for row in maze:
                print("".join(row))
            print()  # Empty line separator

        def afficher_dans_fichier(grille):
            texte = ""
            for ligne in grille:
                texte += ''.join(ligne) + "\n"
            return texte

        def lire_labyrinthe(nom_fichier):
            with open(f"{nom_fichier}.txt", "r") as f:
                lignes = f.read().splitlines()
            return [list(ligne) for ligne in lignes]


        name_of_file = input("Nom du fichier du labyrinthe à résoudre (sans extension) : ")
        start = time.time()
        solution = A_Star(f"{name_of_file}.txt")   # solution = la grille résolue (liste de listes)
        finish = time.time() - start
        name_output = input(f"Le labyrinthe a été résolu en {finish:.5f} seconde(s). Donnez un nom au fichier généré : ")
        with open(f"{name_output}_ar.txt", "w") as f:
            f.write(afficher_dans_fichier(solution))
        break