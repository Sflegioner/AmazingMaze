import math
import random
import time 


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
            return
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
        maze_to_solve[current_cell[0]][current_cell[1]] = "~"
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

A_Star(name_of_file="20.txt")