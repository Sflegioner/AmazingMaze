import string
import random

links = {}
already_visited = set()

def check_move_and_create_link(list_m:list, current_point:tuple, random_step:tuple, iteration:int):
    current_letter = list_m[current_point[0]][current_point[1]]
    next_letter  = list_m[current_point[0]+random_step[0]][current_point[1]+random_step[1]]
    current_point = current_point[0], current_point[1]
    next_point = random_step[0]+current_point[0], random_step[1]+current_point[1]
    print(f'letters = {current_letter, next_letter}')
    print(f'{current_point}<->{next_point}')
    list_pos = []
    list_pos.append((current_letter, next_letter))
    list_pos.append((current_point[0], current_point[1]))
    list_pos.append((next_point[0], next_point[1]))
    if (current_letter, next_letter) not in already_visited:
        already_visited.add((current_letter, next_letter))
        list_pos.append(True)
        links[f'path{iteration}'] = list_pos
    else:
        list_pos.append(False)
        links[f'path{iteration}'] = list_pos
    return next_point

def generate_maze():
    n = 3 
    list_for_maze = []
    lettre = [i for i in string.ascii_uppercase]
    i = 0
    for y in range(n):
        list_for_maze.insert(y, [])
        for x in range(n):
            list_for_maze[y].insert(x, lettre[i])
            i += 1
    for row in list_for_maze:
        print(row)
    print(list_for_maze)
    return list_for_maze

def build_walls(list_m:list):
    n = len(list_m)
    col, row = random.randint(0, n-1), random.randint(0, n-1)
    current_point = (col, row)
    current_LETTRE = list_m[col][row]
    print(f'random point = {current_LETTRE} - y:{col}-x:{row}')

    visited_cells = set()
    visited_cells.add(current_point)
    stack = [current_point]
    itr = 0

    directions = [[-1,0], [1,0], [0,1], [0,-1]]

    while stack:
        current_point = stack[-1]
        neighbors = []
        for step in directions:
            nx = current_point[0] + step[0]
            ny = current_point[1] + step[1]
            if 0 <= nx < n and 0 <= ny < n:
                if (nx, ny) not in visited_cells:
                    neighbors.append(step)

        if neighbors:
            random_step = random.choice(neighbors)
            print(random_step)
            next_point = check_move_and_create_link(list_m, current_point, random_step, iteration=itr+1)
            itr += 1
            visited_cells.add(next_point)
            stack.append(next_point)
        else:
            stack.pop()

    print("\nMaze finished – all cells visited")
    print("Visited cells:", len(visited_cells))


def print_maze_ascii(list_m, links):
    """Print the maze with # = wall and . = open path"""
    n = len(list_m)
    
    connections = set()
    for path in links.values():
        if path[-1] is True:
            a = path[1]         
            b = path[2]         
            connections.add(frozenset([a, b]))
    

    height = 2 * n + 1
    width  = 2 * n + 1
    grid = [['#' for _ in range(width)] for _ in range(height)]
    

    for y in range(n):
        for x in range(n):
            grid[2*y + 1][2*x + 1] = '.'
   
    for a, b in connections:
        y1, x1 = a
        y2, x2 = b
        if y1 == y2:
            wall_y = 2*y1 + 1
            wall_x = 2*min(x1, x2) + 2
            grid[wall_y][wall_x] = '.'
        # vertical connection
        elif x1 == x2:
            wall_y = 2*min(y1, y2) + 2
            wall_x = 2*x1 + 1
            grid[wall_y][wall_x] = '.'
    
    print("\n===== MAZE (# = wall, . = path) =====")
    for row in grid:
        print(''.join(row))



list_m = generate_maze()
build_walls(list_m)

print("\nalready_visited (letter pairs):")
print(already_visited)
print("\nlinks:")
print(links)


print_maze_ascii(list_m, links)