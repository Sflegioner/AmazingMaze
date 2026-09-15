# **Amazing Maze**    

## **Création de labirynthe**

### **1) Création de labytrinthe avec le backtracking itératif et le backtracking récursif**      
L'algorithme de backtracking a la particularité de pouvoir revenir sur ses pas afin de choisir un autre chemin que celui qui vient de le mener dans une impasse. Contrairement à une recherche bruteforce (qui parcours toutes les solutions jusqu'à  trouver la bonne), le backtracking construit des solutions potentielles et peut revenir sur ses pas si la solution candidate en cours n'est pas effective.

Dans cette première phase, nous avons créé des labyrinthes à l'aide de l'algorithme de backtracking, qui nous a permis de produire des labyrinthes parfaits dans un temps relativement réduit.     

**Test pour chacun des algorithmes :**     
Backtracking récursif :      
- Pour n=10, le temps total de création du labyrinthe avec le backtracking récursif est de 0.000344 secondes.     
- Pour n=20, Le temps total de création du labyrinthe avec le backtracking récursif est de 0.001026 secondes.    
- Pour n=50, capacité d'appel récursif de Python dépassé, python ne fini pas le labyrinthe.     

Backtracking itératif :      
- Pour n=10, le temps total de création du labyrinthe avec le backtracking itératif est de 0.00046 secondes.     
- Pour n=20, le temps total de création du labyrinthe avec le backtracking itératif est de 0.00091 secondes.     
- Pour n=50, le temps total de création du labyrinthe avec le backtracking itératif est de 0.00559 secondes.     
- Pour n=100, le temps total de création du labyrinthe avec le backtracking itératif est de 0.22217 secondes.     
- Pour n=500, le temps total de création du labyrinthe avec le backtracking itératif est de 1.14411 secondes.     
- Pour n=1000, le temps total de création du labyrinthe avec le backtracking itératif est de 3.25933 secondes.     
- Pour n=10000, VSCode a planté.     

Nous constatons que le backtracking récursif trouve ses limites relativement rapidement par rapport à l'itératif.


### **2) Création de labyrinthe avec l'algorithme de Kruskal**     
L'algorithme de Kruskal est algorithme de recherche de l'arbre couvrant minimum dans un graphe connexe.    
Il construit une forêt d'arbres couvrant.     

- Pour n=10, le temps total de création du labyrinthe avec l'algorithme de Kruskal est de 0.00058 secondes.     
- Pour n=20, le temps total de création du labyrinthe avec l'algorithme de Kruskal est de 0.00217 secondes.     
- Pour n=50, le temps total de création du labyrinthe avec l'algorithme de Kruskal est de 0.01870 secondes.     
- Pour n=100, le temps total de création du labyrinthe avec l'algorithme de Kruskal est de 0.06191 secondes.     
- Pour n=500, le temps total de création du labyrinthe avec l'algorithme de Kruskal est de 2.55623 secondes.     
- Pour n=1000, le temps total de création du labyrinthe avec l'algorithme de Kruskal est de 11.27484 secondes.     
- Pour n=10000, VSCode a planté.

## **Résolution de labyrinthe**

### **1) Le backtracking**   
Pour n= 100 :    
Le backtracking récursif a prit 0.05318 seconde pour résoudre le labyrinthe.   
Pour n= 500 :     
Le backtracking récursif a prit 1.59909 secondes pour résoudre le labyrinthe.  
Pour n= 1000 :     
Le backtracking récursif a prit 6.26718 secondes pour résoudre le labyrinthe.      
Pour n= 5000 :     
VSCode a planté.      


### **2) Astar**     
Pour cet algorithme, nous allons parler de coût (nombre de moouvement effectués pour arriver jusqu'à la solution) et de temps.

Pour n= 100 :    
L'algorithme Astar a prit 0.01359 seconde pour résoudre le labyrinthe.   
Pour n= 500 :     
L'algorithme Astar a prit 0.52785 secondes pour résoudre le labyrinthe.  
Pour n= 1000 :     
L'algorithme Astar a prit 1.67852 secondes pour résoudre le labyrinthe.      
Pour n= 5000 :     
L'algorithme Astar a prit 350.23740 (presque 6 minutes) secondes pour résoudre le labyrinthe.      

