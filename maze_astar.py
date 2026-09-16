import heapq
import random
import sys
import time
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D
import networkx as nx
import numpy as np

# Augmentation de la limite de récursion par défaut pour les grands labyrinthes
sys.setrecursionlimit(5_000_000)

# Taille maximale autorisée pour éviter la saturation mémoire et les dépassements de capacité
MAX_SIZE = 100000


def create_maze(n):
    """
    Génération d'un labyrinthe parfait (arbre couvrant) avec l'algorithme de Kruskal aléatoire (Union-Find).
    Principe :
      - Chaque case (x, y) démarre dans son propre ensemble disjoint.
      - On liste tous les murs intérieurs séparant deux cellules adjacentes.
      - On mélange aléatoirement la liste des murs.
      - Pour chaque mur entre A et B :
          Si Find(A) != Find(B) (pas de cycle) -> Union(A, B) et on abat le mur.
          Sinon (même composante connexe) -> On conserve le mur pour éviter tout cycle.
    """
    if n < 0:
        raise ValueError("La taille du labyrinthe ne peut pas être négative.")
    if n == 0:
        raise ValueError("La taille du labyrinthe ne peut pas être égale à 0 (minimum 1).")
    if n > MAX_SIZE:
        raise ValueError(f"La taille du labyrinthe est trop importante (maximum autorisé : {MAX_SIZE}).")

    # Ajustement dynamique de la limite de récursion selon la taille n
    needed_limit = (2 * n + 1) ** 2
    if needed_limit > sys.getrecursionlimit():
        sys.setrecursionlimit(needed_limit)

    size = 2 * n + 1

    # Tout est mur au départ
    maze = [['#' for _ in range(size)] for _ in range(size)]

    # Ouvrir toutes les cellules (chambres)
    for y in range(n):
        for x in range(n):
            maze[2 * y + 1][2 * x + 1] = '.'

    # Initialisation de la structure Union-Find (Disjoint-Set) avec compression de chemin
    parent = {(x, y): (x, y) for y in range(n) for x in range(n)}

    def find(cell):
        # Recherche itérative avec compression de chemin (évite les dépassements de pile)
        curr = cell
        while parent[curr] != curr:
            curr = parent[curr]
        root = curr
        curr = cell
        while curr != root:
            nxt = parent[curr]
            parent[curr] = root
            curr = nxt
        return root

    def union(cell_a, cell_b):
        root_a = find(cell_a)
        root_b = find(cell_b)
        if root_a != root_b:
            parent[root_b] = root_a
            return True
        return False

    # Liste de tous les murs intérieurs
    walls = []
    for y in range(n):
        for x in range(n):
            # Mur horizontal (vers la droite)
            if x + 1 < n:
                wall_x = 2 * x + 2
                wall_y = 2 * y + 1
                walls.append(((x, y), (x + 1, y), wall_x, wall_y))

            # Mur vertical (vers le bas)
            if y + 1 < n:
                wall_x = 2 * x + 1
                wall_y = 2 * y + 2
                walls.append(((x, y), (x, y + 1), wall_x, wall_y))

    random.shuffle(walls)

    for cell_a, cell_b, wall_x, wall_y in walls:
        if find(cell_a) != find(cell_b):
            union(cell_a, cell_b)
            maze[wall_y][wall_x] = '.'

    # Entrée
    maze[1][0] = '.'

    # Sortie
    maze[size - 2][size - 1] = '.'

    return maze


def solve_maze(maze, start=None, end=None):
    """
    Résolution du labyrinthe avec l'algorithme A* (A-Star).
    Utilise la distance de Manhattan comme fonction heuristique admissible et consistante.
    
    Principe :
      - f(n) = g(n) + h(n)
        * g(n) : coût réel du chemin depuis le point de départ jusqu'à n
        * h(n) : estimation heuristique (distance de Manhattan) du coût de n jusqu'à la sortie
      - Une file de priorité (min-heap) sélectionne toujours le nœud avec le score f(n) minimal.
      - En cas d'égalité sur f(n), on privilégie le nœud avec la plus faible valeur de h(n) (le plus proche de l'objectif).
    
    Marquage des cellules dans la matrice :
      - 'o' : Cases participant au chemin optimal trouvé par A* menant à la sortie.
      - '*' : Cases explorées/visitées par A* lors de la recherche (impasses ou alternatives non retenues).
      - '.' : Passages libres jamais explorés grâce à l'efficacité du guidage heuristique.
    """
    height = len(maze)
    width = len(maze[0])

    # Détection automatique de l'entrée si non spécifiée (colonne 0)
    if start is None:
        if height > 1 and maze[1][0] == '.':
            start = (0, 1)  # (x, y)
        else:
            for y in range(height):
                if maze[y][0] == '.':
                    start = (0, y)
                    break

    # Détection automatique de la sortie si non spécifiée (dernière colonne)
    if end is None:
        if height > 2 and maze[height - 2][width - 1] == '.':
            end = (width - 1, height - 2)  # (x, y)
        else:
            for y in range(height - 1, -1, -1):
                if maze[y][width - 1] == '.':
                    end = (width - 1, y)
                    break

    if start is None or end is None:
        return maze

    # Heuristique admissible : Distance de Manhattan
    def heuristic(x, y):
        return abs(x - end[0]) + abs(y - end[1])

    # Directions : haut, bas, gauche, droite
    directions = [
        (0, -1),   # haut
        (0, 1),    # bas
        (-1, 0),   # gauche
        (1, 0)     # droite
    ]

    # File de priorité (heapq) : (f_score, h_score, counter, (x, y))
    start_h = heuristic(start[0], start[1])
    open_set = []
    counter = 0
    heapq.heappush(open_set, (start_h, start_h, counter, start))

    came_from = {}
    g_score = {start: 0}
    closed_set = set()

    found = False
    while open_set:
        f, h, _, current = heapq.heappop(open_set)

        if current in closed_set:
            continue
        closed_set.add(current)

        if current == end:
            found = True
            break

        cx, cy = current
        current_g = g_score[current]

        for dx, dy in directions:
            nx = cx + dx
            ny = cy + dy

            # Vérifier les limites de la grille
            if 0 <= nx < width and 0 <= ny < height:
                # Traverser uniquement les passages libres (pas les murs '#')
                if maze[ny][nx] != '#':
                    neighbor = (nx, ny)
                    tentative_g = current_g + 1

                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        g_score[neighbor] = tentative_g
                        h_val = heuristic(nx, ny)
                        f_val = tentative_g + h_val
                        came_from[neighbor] = current
                        counter += 1
                        heapq.heappush(open_set, (f_val, h_val, counter, neighbor))

    if found:
        # 1. Marquer toutes les cases explorées qui ne sont pas des murs par '*'
        for (x, y) in closed_set:
            if maze[y][x] != '#':
                maze[y][x] = '*'

        # 2. Reconstituer le chemin optimal de l'arrivée vers le départ avec 'o'
        curr = end
        while curr in came_from:
            maze[curr[1]][curr[0]] = 'o'
            curr = came_from[curr]
        maze[start[1]][start[0]] = 'o'

    return maze


def load_maze(filename):
    with open(filename, 'r') as file:
        return [list(line.rstrip('\r\n')) for line in file if line.strip()]


def save_maze(maze, filename):
    with open(filename, 'w') as file:
        for row in maze:
            file.write(''.join(row) + '\n')


def visualize_graph(maze, n, filename=None):
    """
    Affiche et sauvegarde une visualisation de la théorie des graphes :
    - À gauche : Le labyrinthe résolu avec A* (grille avec murs '#', chemin optimal 'o', cases explorées '*' et non explorées '.')
    - À droite : Le graphe sous-jacent (arbre couvrant G = (V, E)) avec sommets et arêtes.
    """
    fig, (ax_maze, ax_graph) = plt.subplots(1, 2, figsize=(14, 7))

    # 1. Vue Grille du Labyrinthe
    char_map = {'#': 0, '.': 1, '*': 2, 'o': 3}
    grid = np.array([[char_map.get(c, 0) for c in row] for row in maze])
    cmap = mcolors.ListedColormap(['#2c3e50', '#ecf0f1', '#e74c3c', '#2ecc71'])
    ax_maze.imshow(grid, cmap=cmap)
    ax_maze.set_title('Labyrinthe Résolu avec A* (Grille)', fontsize=13, fontweight='bold', pad=12)
    ax_maze.axis('off')

    # 2. Vue Théorie des Graphes (Arbre couvrant G = (V, E))
    G = nx.Graph()
    for y in range(n):
        for x in range(n):
            node = (x, y)
            G.add_node(node, status=maze[2 * y + 1][2 * x + 1])
            # Voisin horizontal droit
            if x + 1 < n and maze[2 * y + 1][2 * x + 2] != '#':
                is_path = (maze[2 * y + 1][2 * x + 1] == 'o' and 
                           maze[2 * y + 1][2 * x + 2] == 'o' and 
                           maze[2 * y + 1][2 * x + 3] == 'o')
                G.add_edge(node, (x + 1, y), is_path=is_path)
            # Voisin vertical bas
            if y + 1 < n and maze[2 * y + 2][2 * x + 1] != '#':
                is_path = (maze[2 * y + 1][2 * x + 1] == 'o' and 
                           maze[2 * y + 2][2 * x + 1] == 'o' and 
                           maze[2 * y + 3][2 * x + 1] == 'o')
                G.add_edge(node, (x, y + 1), is_path=is_path)

    # Position des sommets (inverser y pour aligner avec la grille)
    pos = {(x, y): (x, -y) for x, y in G.nodes()}

    # Séparation des arêtes de l'arbre et du chemin solution
    tree_edges = [(u, v) for u, v, d in G.edges(data=True) if not d['is_path']]
    path_edges = [(u, v) for u, v, d in G.edges(data=True) if d['is_path']]

    edge_width_tree = max(1.0, 15.0 / n)
    edge_width_path = max(2.5, 30.0 / n)

    nx.draw_networkx_edges(G, pos, edgelist=tree_edges, ax=ax_graph, edge_color='#bdc3c7', width=edge_width_tree)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, ax=ax_graph, edge_color='#2ecc71', width=edge_width_path)

    # Couleurs des sommets selon leur état
    node_colors = []
    for node in G.nodes():
        if node == (0, 0):
            node_colors.append('#3498db')  # Entrée
        elif node == (n - 1, n - 1):
            node_colors.append('#e67e22')  # Sortie
        elif G.nodes[node]['status'] == 'o':
            node_colors.append('#2ecc71')  # Chemin optimal A*
        elif G.nodes[node]['status'] == '*':
            node_colors.append('#e74c3c')  # Exploré par A*
        else:
            node_colors.append('#95a5a6')  # Non exploré par A*

    node_size = max(40, int(3000 / (n * 1.5)))
    nx.draw_networkx_nodes(G, pos, ax=ax_graph, node_color=node_colors, node_size=node_size)

    # Étiquettes de coordonnées si n <= 12
    if n <= 12:
        labels = {node: f'({node[0]},{node[1]})' for node in G.nodes()}
        font_size = max(6, int(12 - n * 0.4))
        nx.draw_networkx_labels(G, pos, labels=labels, ax=ax_graph, font_size=font_size, font_color='#2c3e50')

    nb_nodes = G.number_of_nodes()
    nb_edges = G.number_of_edges()
    ax_graph.set_title(f'Théorie des Graphes : Résolution A* (|V|={nb_nodes}, |E|={nb_edges})', fontsize=12, fontweight='bold', pad=12)
    ax_graph.axis('off')

    # Légende explicative
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Entrée (0,0)', markerfacecolor='#3498db', markersize=9),
        Line2D([0], [0], marker='o', color='w', label='Sortie', markerfacecolor='#e67e22', markersize=9),
        Line2D([0], [0], marker='o', color='w', label="Chemin optimal A* ('o')", markerfacecolor='#2ecc71', markersize=9),
        Line2D([0], [0], marker='o', color='w', label="Cases explorées A* ('*')", markerfacecolor='#e74c3c', markersize=9),
        Line2D([0], [0], marker='o', color='w', label="Non exploré ('.')", markerfacecolor='#95a5a6', markersize=9),
        Line2D([0], [0], color='#2ecc71', lw=3, label='Arête solution A*'),
        Line2D([0], [0], color='#bdc3c7', lw=1.5, label='Arête arbre couvrant')
    ]
    ax_graph.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0., frameon=True)

    plt.tight_layout()

    if filename:
        img_filename = f"{filename}_graph.png"
        plt.savefig(img_filename, dpi=150, bbox_inches='tight')
        print(f"Graphique de théorie des graphes sauvegardé dans {img_filename}")

    try:
        if matplotlib.get_backend().lower() != 'agg':
            plt.show()
    except Exception:
        pass


def main():
    try:
        n = int(input("Taille du labyrinthe : "))
    except ValueError:
        print("Erreur : La taille du labyrinthe doit être un nombre entier.")
        return

    if n < 0:
        print("Erreur : La taille du labyrinthe ne peut pas être négative.")
        return

    if n == 0:
        print("Erreur : La taille du labyrinthe ne peut pas être égale à 0 (minimum 1).")
        return

    if n > MAX_SIZE:
        print(f"Erreur : La taille du labyrinthe est trop importante pour être générée (maximum autorisé : {MAX_SIZE}).")
        return

    filename = input("Nom du fichier : ")

    try:
        start_gen = time.perf_counter()
        maze = create_maze(n)
        end_gen = time.perf_counter()

        start_solve = time.perf_counter()
        solve_maze(maze)
        end_solve = time.perf_counter()

        time_gen = end_gen - start_gen
        time_solve = end_solve - start_solve
        time_total = time_gen + time_solve

        save_maze(maze, filename)
        print(f"Labyrinthe créé et résolu avec A* (A-Star) dans {filename}")
        print("⏱️  Chronomètre (A* / A-Star) :")
        print(f"   - Temps de génération : {time_gen:.6f} secondes")
        print(f"   - Temps de résolution (A*) : {time_solve:.6f} secondes")
        print(f"   - Temps total calcul  : {time_total:.6f} secondes")

        # Statistiques d'exploration A*
        explored_count = sum(row.count('*') + row.count('o') for row in maze)
        path_count = sum(row.count('o') for row in maze)
        total_open = sum(row.count('.') + row.count('*') + row.count('o') for row in maze)
        efficiency = (1 - (explored_count / total_open)) * 100 if total_open > 0 else 0
        print("📊 Statistiques A* :")
        print(f"   - Longueur du chemin optimal : {path_count} cases")
        print(f"   - Cases explorées lors de la recherche : {explored_count} / {total_open} ({explored_count / total_open * 100:.1f}%)")
        print(f"   - Économie d'exploration grâce à l'heuristique : {efficiency:.1f}% des cases évitées")

        # Visualisation de théorie des graphes
        visualize_graph(maze, n, filename)
    except Exception as e:
        print(f"Erreur : {e}")


if __name__ == "__main__":
    main()
