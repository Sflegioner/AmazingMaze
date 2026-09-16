import string
import random


links = {}
already_visited = set()

def check_move_and_create_link(list_m:list,current_point:tuple,random_step:tuple,iteration:int):

    current_letter = list_m[current_point[0]][current_point[1]]
    next_letter  =list_m[current_point[0]+random_step[0]][current_point[1]+random_step[1]]

    current_point = current_point[0],current_point[1]
    next_point = random_step[0]+current_point[0],random_step[1]+current_point[1]

    print(f'letters = {current_letter,next_letter}')
    print(f'{current_point}<->{next_point}')

    list_pos = []
    list_pos.append((current_letter,next_letter))
    list_pos.append((current_point[0],current_point[1]))
    list_pos.append((next_point[0], next_point[1]))

    if (current_letter,next_letter) not in already_visited:
        already_visited.add((current_letter,next_letter))
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
        
        list_for_maze.insert(y,[])
        for x in range(n):
            list_for_maze[y].insert(x,lettre[i])
            i += 1

    for row in list_for_maze:
            print(row)

    print(list_for_maze)
    return list_for_maze

def build_walls(list_m:list):
    
    col,row = random.randint(0,len(list_m)-1),random.randint(0,len(list_m)-1)
    current_LETTRE = list_m[col][row]
    current_point = col,row 
    print(f'random point = {current_LETTRE} - y:{col}-x:{row}')
    itr = 0

    for y in range(len(list_m)):
        for x in range(len(list_m[y])):
            random_step=random.choice([[-1,0],[1,0],[0,1],[0,-1]])
            print(random_step)
            
            if current_point[0]+random_step[0] != -1 and current_point[1]+random_step[1] != -1: 
                print("ok dont go from another side")
                if current_point[0]+random_step[0]<=len(list_m[y])-1 and current_point[1]+random_step[1]<=len(list_m[y])-1:   
                    print("ok dont go outside of list")
                    
                    current_point = check_move_and_create_link(list_m,current_point,random_step,iteration=itr+1)
            
   
list_m = generate_maze()
build_walls(list_m)
print(already_visited)