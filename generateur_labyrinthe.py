import random
import time
import sys

while True :
    choix_utilisateur = input(
        "Afin de générer un labyrinthe, choisissez un algorithme :\n"
        " - Tapez 1 pour le backtracking itératif\n"
        " - Tapez 2 pour le backtracking récursif\n"
        " - Tapez 3 pour l'algorithme de Kruskal\n"
        " - Tapez q pour quitter\n"
        "Entrez votre choix : "
    )



# Backtracking itératif :
    if choix_utilisateur == "1" :
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
        grille_finale[0][1] = "."
        grille_finale[2*n-1][2*n] = "."
        afficher(grille_finale)
        fin = time.time() - depart
        print(f"Le temps total de création du labyrinthe avec le backtracking itératif est de {fin} secondes.")
    
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
                with open(f"{nom_fichier}.txt", "a") as f :
                    f.write(f"{afficher_dans_fichier(grille_finale)}")
                    print("Fichier généré !")
                    pass                             # on ne fait rien : on voulait juste créer le fichier
                break                                # aucune erreur -> on sort de la boucle
            except FileExistsError:
                print("Nom déjà utilisé, donnez un autre nom.")
        break
    
    
    elif choix_utilisateur == "2":
        n = int(input("Veuillez rentrer un nombre : "))

        sys.setrecursionlimit((2*n+1)**2)

            # if n<=45 :
            #     break
            # else :
            #     print("Le nombre d'appel récursif sera trop élevé si n>45, et le programme plantera.")


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
        grille_generee[1][0] = "."
        grille_generee[2*n-1][2*n] = "."
        afficher(grille_generee)
        fin = time.time() - depart
        print(f"Le temps total de création du labyrinthe avec le backtracking récursif est de {fin} secondes.")

        ###### Affichage et création fichier :
        while True:                                  
            nom_fichier = input("Veuillez rentrer un nom de fichier : ")
            try:
                # "x" crée le fichier, et lève FileExistsError s'il existe déjà
                with open(f"{nom_fichier}_btrg.txt", "x"):
                    pass                             # on ne fait rien : on voulait juste créer le fichier
                break                                # aucune erreur -> on sort de la boucle
            except FileExistsError:
                print("Nom déjà utilisé, donnez un autre nom.")


        with open(f"{nom_fichier}_btrg.txt", "a") as f :
            f.write(f"{afficher_dans_fichier(grille_generee)}")
            print("Fichier généré !")
        break

# Kruskal :
    elif choix_utilisateur == "3":
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

        def find(groupe, c):
            # Remonte jusqu'à la racine, en compressant le chemin au passage
            while groupe[c] != c:
                groupe[c] = groupe[groupe[c]]  # saute un niveau (compression partielle)
                c = groupe[c]
            return c

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
            for mur in murs:
                c1, c2 = cellules_voisines(mur)          # un seul argument, comme défini plus haut
                r1, r2 = find(groupe, c1), find(groupe, c2)
                if r1 != r2:
                    (y, x) = mur
                    grille[y][x] = "."
                    groupe[r2] = r1   # une seule affectation, pas de boucle sur tout le dict
                # (ancien bloc naïf supprimé : il refaisait le même travail en O(n²))

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
        print(f"Le temps total de création du labyrinthe avec Kruskal est de {fin} secondes.")

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


        with open(f"{nom_fichier}_kg.txt", "a") as f :
            f.write(f"{afficher_dans_fichier(grille_finale)}")
            print("Fichier généré !")
        break
    
    elif choix_utilisateur == "q":
            print("Fin du programme.")
            break