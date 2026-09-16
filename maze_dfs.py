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

    # Cases correspondant aux couloirs
    visited = [[False for _ in range(n)] for _ in range(n)]

    def backtrack(x, y):
        visited[y][x] = True

        # Mélange des 4 directions
        directions = [
            (0, -1),   # haut
            (0, 1),    # bas
            (-1, 0),   # gauche
            (1, 0)     # droite
        ]

        random.shuffle(directions)

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            # Vérifier que le voisin est dans la grille
            if 0 <= nx < n and 0 <= ny < n:

                # Si le voisin n'a pas encore été visité
                if not visited[ny][nx]:

                    # Coordonnées dans la vraie matrice
                    current_x = 2 * x + 1
                    current_y = 2 * y + 1

                    next_x = 2 * nx + 1
                    next_y = 2 * ny + 1

                    # Ouvrir le couloir
                    maze[current_y][current_x] = '.'

                    # Casser le mur entre les deux cases
                    wall_x = (current_x + next_x) // 2
                    wall_y = (current_y + next_y) // 2

                    maze[wall_y][wall_x] = '.'

                    # Ouvrir la prochaine case
                    maze[next_y][next_x] = '.'

                    # Récursion
                    backtrack(nx, ny)

    # Commencer en haut à gauche
    backtrack(0, 0)

    # Entrée
    maze[1][0] = '.'

    # Sortie
    maze[size - 2][size - 1] = '.'

    return maze


def solve_maze(maze, start=None, end=None):
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

    # Directions d'exploration : haut, bas, gauche, droite
    directions = [
        (0, -1),   # haut
        (0, 1),    # bas
        (-1, 0),   # gauche
        (1, 0)     # droite
    ]

    def backtrack_solve(x, y):
        # Arrivée à la sortie
        if (x, y) == end:
            maze[y][x] = 'o'
            return True

        # Marquer la case courante comme explorée
        maze[y][x] = '*'

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            # Vérifier les limites de la grille
            if 0 <= nx < width and 0 <= ny < height:
                # Traverser uniquement les passages libres non encore explorés
                if maze[ny][nx] == '.':
                    if backtrack_solve(nx, ny):
                        # La case participe au chemin final menant à la sortie
                        maze[y][x] = 'o'
                        return True

        # Si aucune direction ne mène à la sortie,
        # la case reste '*' (explorée mais ne participant pas au chemin final)
        return False

    backtrack_solve(start[0], start[1])
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
    - À gauche : Le labyrinthe résolu (grille avec murs, chemin 'o' et impasses '*')
    - À droite : Le graphe sous-jacent (arbre couvrant G = (V, E)) avec sommets et arêtes.
    """
    fig, (ax_maze, ax_graph) = plt.subplots(1, 2, figsize=(14, 7))

    # 1. Vue Grille du Labyrinthe
    char_map = {'#': 0, '.': 1, '*': 2, 'o': 3}
    grid = np.array([[char_map.get(c, 0) for c in row] for row in maze])
    cmap = mcolors.ListedColormap(['#2c3e50', '#ecf0f1', '#e74c3c', '#2ecc71'])
    ax_maze.imshow(grid, cmap=cmap)
    ax_maze.set_title('Labyrinthe Résolu (Grille)', fontsize=13, fontweight='bold', pad=12)
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
            node_colors.append('#2ecc71')  # Chemin solution
        elif G.nodes[node]['status'] == '*':
            node_colors.append('#e74c3c')  # Impasse explorée
        else:
            node_colors.append('#95a5a6')  # Non exploré

    node_size = max(40, int(3000 / (n * 1.5)))
    nx.draw_networkx_nodes(G, pos, ax=ax_graph, node_color=node_colors, node_size=node_size)

    # Étiquettes de coordonnées si n <= 12
    if n <= 12:
        labels = {node: f'({node[0]},{node[1]})' for node in G.nodes()}
        font_size = max(6, int(12 - n * 0.4))
        nx.draw_networkx_labels(G, pos, labels=labels, ax=ax_graph, font_size=font_size, font_color='#2c3e50')

    nb_nodes = G.number_of_nodes()
    nb_edges = G.number_of_edges()
    ax_graph.set_title(f'Théorie des Graphes : Arbre Couvrant (|V|={nb_nodes}, |E|={nb_edges})', fontsize=13, fontweight='bold', pad=12)
    ax_graph.axis('off')

    # Légende explicative
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Entrée (0,0)', markerfacecolor='#3498db', markersize=9),
        Line2D([0], [0], marker='o', color='w', label='Sortie', markerfacecolor='#e67e22', markersize=9),
        Line2D([0], [0], marker='o', color='w', label="Chemin solution ('o')", markerfacecolor='#2ecc71', markersize=9),
        Line2D([0], [0], marker='o', color='w', label="Impasse explorée ('*')", markerfacecolor='#e74c3c', markersize=9),
        Line2D([0], [0], color='#2ecc71', lw=3, label='Arête solution'),
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
        print(f"Labyrinthe créé et résolu dans {filename}")
        print("⏱️  Chronomètre (DFS Backtracking) :")
        print(f"   - Temps de génération : {time_gen:.6f} secondes")
        print(f"   - Temps de résolution : {time_solve:.6f} secondes")
        print(f"   - Temps total calcul  : {time_total:.6f} secondes")

        # Visualisation de théorie des graphes
        visualize_graph(maze, n, filename)
    except Exception as e:
        print(f"Erreur : {e}")


if __name__ == "__main__":
    main()