# **Amazing Maze**    

## **Création de labirynthe**

### **1) Création de labytrinthe avec le backtracking itératif et le backtracking récursif**      
L'algorithme de backtracking a la particularité de pouvoir revenir sur ses pas afin de choisir un autre chemin que celui qui vient de le mener dans une impasse. Contrairement à une recherche bruteforce (qui parcours toutes les solutions jusqu'à trouver la bonne), le backtracking construit des solutions potentielles et peut revenir sur ses pas si la solution candidate en cours n'est pas effective.

Dans cette première phase, nous avons créé des labyrinthes à l'aide de l'algorithme de backtracking, qui nous a permis de produire des labyrinthes parfaits dans un temps relativement réduit.     

**Test pour chacun des algorithmes :**     
Backtracking récursif : dans un premier temps noous avons laissé la limite de python pour les appel récusifs, pui nous avons déterminé la limite d'appels récursif en fonction de n, avec la formule : sys.setrecursionlimit((2*n+1)**2)        

<u>Limite appels récursif python :</u>      
- Pour n=10, le temps total de création du labyrinthe avec le backtracking récursif est de 0.000344 secondes.     
- Pour n=20, Le temps total de création du labyrinthe avec le backtracking récursif est de 0.001026 secondes.    
- Pour n=50, capacité d'appel récursif de Python dépassé, python ne fini pas le labyrinthe.     

<u>Limite appels récursif (2n+1)² :</u>       
- Pour n=1000, le temps total de création du labyrinthe avec le backtracking récursif est de 4.42895 secondes.
- Pour n=5000, VSCode a planté.

Backtracking itératif :      
- Pour n=10, le temps total de création du labyrinthe avec le backtracking itératif est de 0.00046 secondes.     
- Pour n=20, le temps total de création du labyrinthe avec le backtracking itératif est de 0.00091 secondes.     
- Pour n=50, le temps total de création du labyrinthe avec le backtracking itératif est de 0.00559 secondes.     
- Pour n=100, le temps total de création du labyrinthe avec le backtracking itératif est de 0.22217 secondes.     
- Pour n=500, le temps total de création du labyrinthe avec le backtracking itératif est de 1.14411 secondes.     
- Pour n=1000, le temps total de création du labyrinthe avec le backtracking itératif est de 3.25933 secondes.     
- Pour n=10000, Le temps total de création du labyrinthe avec le backtracking itératif est de 317.75809 secondes.    
- Pour n=100000, VSCode a planté.

Le backtracking itératif peut supporter de plus grandes valeurs de n que le backtracking récursif.


### **2) Création de labyrinthe avec l'algorithme de Kruskal**     
L'algorithme de Kruskal est algorithme de recherche de l'arbre couvrant minimum dans un graphe connexe.    
Il construit une forêt d'arbres couvrant.    
Il casse des murs entre les cellules uniquement si celles ci ne sont pas déjà connectées via un autre chemin : les cellules sont rangées en groupe, si les groupes ne sont pas reliés, on les fusionne lorsqu'on casse un mur.     
Dans le contexte de notre recherche du code le plus efficace, nous avons pu optimiser l'algorithme grâce à une amélioration du processus Union-Find. En effet, mon code, à chaque fusion de deux groupes, parcourait l'ensemble des cellules du labyrinthe pour réassigner celles du groupe perdant au groupe gagnant, alors que le code du collègue ne modifie qu'un seul pointeur (celui du chef du groupe perdant) et se contente de remonter le chemin de la cellule concernée pour retrouver son chef, sans toucher au reste de la structure.    
Dans ce contexte, les poids des arrêtes (murs) étant tous équivalent, on implémente un choix random dans un liste de coordonnées de murs pour enclencher le processus : détermine si les cellules autour de ce mur sont déjà  connectées afin de ne pas créer de boucles.


- Pour n=10, le temps total de création du labyrinthe avec l'algorithme de Kruskal est de 0.00058 secondes.     
- Pour n=20, le temps total de création du labyrinthe avec l'algorithme de Kruskal est de 0.00217 secondes.     
- Pour n=50, le temps total de création du labyrinthe avec l'algorithme de Kruskal est de 0.01870 secondes.     
- Pour n=100, le temps total de création du labyrinthe avec l'algorithme de Kruskal est de 0.06191 secondes.     
- Pour n=500, le temps total de création du labyrinthe avec l'algorithme de Kruskal est de 2.55623 secondes.     
- Pour n=1000, le temps total de création du labyrinthe avec l'algorithme de Kruskal est de 11.27484 secondes.     
- Pour n=10000, VSCode a planté.

## **Résolution de labyrinthe**

### **1) Le backtracking**   
Nous rappelons que le nombre d'appel récursifs autorisés dans python on une limite donnée qui dépend de n : sys.setrecursionlimit((2*n+1)**2)     

**Résolution pour un labyrinthe produit en backtracking récursif :**    
Pour n= 100 :    
Le backtracking récursif a prit 0.05318 seconde pour résoudre le labyrinthe.   
Pour n= 500 :     
Le backtracking récursif a prit 1.59909 secondes pour résoudre le labyrinthe.  
Pour n= 1000 :     
Le backtracking récursif a prit 6.26718 secondes pour résoudre le labyrinthe.      
Pour n= 5000 :     
VSCode a planté.      

**Résolution pour un labyrinthe crée avec l'algorithme de Kruskal :**     
Pour n=100 :    
La solution a été générée en 0.033625 secondes.     
Pour n= 500 :
La solution a été générée en 0.692699 secondes.
Pour n= 1000 :      
La solution a été générée en 2.835056 secondes.    
Pour n=5000 :     
La solution a été générée en 4.103943 secondes.    


### **2) Astar**     
Pour cet algorithme, nous allons parler de coût (nombre de mouvement effectués pour arriver jusqu'à la solution) et de temps.    
     
**Résolution pour un labyrinthe produit en backtracking récursif :**    
Pour n= 100 :    
L'algorithme Astar a prit 0.01359 seconde pour résoudre le labyrinthe.   
Pour n= 500 :     
L'algorithme Astar a prit 0.52785 secondes pour résoudre le labyrinthe.  
Pour n= 1000 :     
L'algorithme Astar a prit 1.67852 secondes pour résoudre le labyrinthe.      
Pour n= 5000 :     
L'algorithme Astar a prit 350.23740 (presque 6 minutes) secondes pour résoudre le labyrinthe.      
Pour n=10000 :     
L'algorithme Astar a fait planter VSCode.      

**Résolution pour un labyrinthe crée avec l'algorithme de Kruskal :**     
Pour n=100 :    
La solution a été générée en 0.046972 secondes.     
Pour n= 500 :
La solution a été générée en 1.688090 secondes.
Pour n= 1000 :      
La solution a été générée en 6.326489 secondes.    
Pour n=5000 :     
La solution a été générée en 6.475189 secondes.    
