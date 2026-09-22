import random
import time
import sys

while True:
    user_choice = input(
        "To generate a maze, choose an algorithm:\n"
        " - Type 1 for iterative backtracking\n"
        " - Type 2 for recursive backtracking\n"
        " - Type 3 for Kruskal's algorithm\n"
        " - Type q to quit\n"
        "Enter your choice: "
    )

# Iterative backtracking:
    if user_choice == "1":
        n = int(input("Please enter a number: "))

        def maze(n):
            width = 2 * n + 1
            height = 2 * n + 1

            grid = []
            for x in range(height):
                row = ['#' for _ in range(width)]
                grid.append(row)
            return grid

        def display(grid):
            for row in grid:
                print(''.join(row))

        def display_to_file(grid):
            text = ""
            for row in grid:
                text += ''.join(row) + "\n"
            return text

        generated_grid = maze(n)

        def unvisited_neighbors(grid, y, x, n):
            # Create a list of direction tuples
            direction = [(-2, 0), (2, 0), (0, -2), (0, 2)]

            potential_cells = []
            for dy, dx in direction:
                ny, nx = (y + dy), (x + dx)
                if 1 <= ny <= 2 * n - 1 and 1 <= nx <= 2 * n - 1 and grid[ny][nx] == "#":
                    potential_cells.append((ny, nx))
            return potential_cells

        def backtracking(grid, n):
            stack = [(1, 1)]
            grid[1][1] = "."
            while stack:
                # Here, stack[-1] looks at the last element of the stack
                y, x = stack[-1]
                neighbors = unvisited_neighbors(grid, y, x, n)
                # If the list contains something:
                if neighbors:
                    # Choose an element from the list
                    ny, nx = random.choice(neighbors)
                    # The wall changes from "#" to "."
                    grid[(y + ny) // 2][(x + nx) // 2] = "."
                    # The visited element changes from "#" to "."
                    grid[(ny)][(nx)] = "."
                    stack.append((ny, nx))
                else:
                    stack.pop()
            return grid

        start_time = time.time()
        final_grid = backtracking(generated_grid, n)
        final_grid[0][1] = "."
        final_grid[2 * n - 1][2 * n] = "."
        display(final_grid)
        elapsed = time.time() - start_time
        print(f"The total time to create the maze with iterative backtracking is {elapsed} seconds.")

        ###### Display and file creation:
        def display_to_file(grid):
            text = ""
            for row in grid:
                text += ''.join(row) + "\n"
            return text

        while True:
            file_name = input("Please enter a file name: ")
            try:
                # "a" creates the file if it doesn't exist yet
                with open(f"{file_name}.txt", "a") as f:
                    f.write(f"{display_to_file(final_grid)}")
                    print("File generated!")
                    pass                             # we do nothing: we just wanted to create the file
                break                                # no error -> exit the loop
            except FileExistsError:
                print("Name already in use, please give another name.")
        break


    # Recursive backtracking
    elif user_choice == "2":
        n = int(input("Please enter a number: "))

        sys.setrecursionlimit((2 * n + 1) ** 2)

            # if n<=45 :
            #     break
            # else :
            #     print("The number of recursive calls will be too high if n>45, and the program will crash.")


        def maze(n):
            width = 2 * n + 1
            height = 2 * n + 1

            grid = []
            for x in range(height):
                row = ['#' for _ in range(width)]
                grid.append(row)
            return grid

        def display(grid):
            for row in grid:
                print(''.join(row))

        def display_to_file(grid):
            text = ""
            for row in grid:
                text += ''.join(row) + "\n"
            return text

        generated_grid = maze(n)

        def unvisited_neighbors(grid, y, x, n):
            # Create a list of direction tuples
            direction = [(-2, 0), (2, 0), (0, -2), (0, 2)]

            potential_cells = []
            for dy, dx in direction:
                ny, nx = (y + dy), (x + dx)
                if 1 <= ny <= 2 * n - 1 and 1 <= nx <= 2 * n - 1 and grid[ny][nx] == "#":
                    potential_cells.append((ny, nx))
            return potential_cells

        def backtracking(grid, y, x, n):
            # Mark the current cell as visited
            grid[y][x] = "."

            neighbors = unvisited_neighbors(grid, y, x, n)

            # As long as the current cell still has neighbors to explore
            while neighbors:
                # Choose a direction at random
                ny, nx = random.choice(neighbors)
                # Open the wall between the current cell and the neighbor
                grid[(y + ny) // 2][(x + nx) // 2] = "."
                # Descend into the neighbor: this is where the call stack grows
                backtracking(grid, ny, nx, n)
                # Upon returning from the call, the explored branch has visited other cells:
                # the list must be recalculated, some neighbors are no longer "#"
                neighbors = unvisited_neighbors(grid, y, x, n)
            # No more neighbors: the function ends, we automatically go back up
            # one level in the call stack (equivalent to pop())

        start_time = time.time()
        backtracking(generated_grid, 1, 1, n)
        generated_grid[1][0] = "."
        generated_grid[2 * n - 1][2 * n] = "."
        display(generated_grid)
        elapsed = time.time() - start_time
        print(f"The total time to create the maze with recursive backtracking is {elapsed} seconds.")

        ###### Display and file creation:
        while True:
            file_name = input("Please enter a file name: ")
            try:
                # "x" creates the file, and raises FileExistsError if it already exists
                with open(f"{file_name}_btrg.txt", "x"):
                    pass                             # we do nothing: we just wanted to create the file
                break                                # no error -> exit the loop
            except FileExistsError:
                print("Name already in use, please give another name.")


        with open(f"{file_name}_btrg.txt", "a") as f:
            f.write(f"{display_to_file(generated_grid)}")
            print("File generated!")
        break

# Kruskal:
    elif user_choice == "3":
        n = int(input("Please enter a number: "))

        def neighboring_cells(wall):
            y, x = wall
            if y % 2 == 1:   # horizontal wall -> left/right
                return (y, x - 1), (y, x + 1)
            else:            # vertical wall -> up/down
                return (y - 1, x), (y + 1, x)

        # Grid generation:
        def maze(n):
            grid = []
            for x in range(2 * n + 1):
                row = ['#' for _ in range(2 * n + 1)]
                grid.append(row)
            return grid

        def find(group, c):
            # Climb up to the root, compressing the path along the way
            while group[c] != c:
                group[c] = group[group[c]]  # skip one level (partial compression)
                c = group[c]
            return c

        def generate_maze():
            grid = maze(n)

            h_conn_walls = [(y, x) for y in range(1, 2 * n, 2) for x in range(2, 2 * n - 1, 2)]   # odd y, even x → horizontal wall
            v_conn_walls = [(y, x) for y in range(2, 2 * n - 1, 2) for x in range(1, 2 * n, 2)]    # even y, odd x → vertical wall

            cells = [(y, x) for y in range(1, 2 * n, 2) for x in range(1, 2 * n, 2)]
            group = {c: c for c in cells}

            for (y, x) in cells:
                grid[y][x] = "."

            walls = h_conn_walls + v_conn_walls
            random.shuffle(walls)

            # Kruskal
            for wall in walls:
                # Get the cells separated by a wall
                c1, c2 = neighboring_cells(wall)
                r1, r2 = find(group, c1), find(group, c2)
                if r1 != r2:
                    (y, x) = wall
                    grid[y][x] = "."
                    group[r2] = r1   # a single assignment, no loop over the whole dict
                # (old naive block removed: it redid the same work in O(n²))

            return grid

        def display(grid):
            for row in grid:
                print(''.join(row))

        start_time = time.time()
        final_grid = generate_maze()
        final_grid[0][1] = "."
        final_grid[2 * n - 1][2 * n] = "."
        elapsed = time.time() - start_time
        display(final_grid)
        print(f"The total time to create the maze with Kruskal is {elapsed} seconds.")

        ###### Display and file creation:
        def display_to_file(grid):
            text = ""
            for row in grid:
                text += ''.join(row) + "\n"
            return text

        while True:
            file_name = input("Please enter a file name: ")
            try:
                # "x" creates the file, and raises FileExistsError if it already exists
                with open(f"{file_name}.txt", "x"):
                    pass                             # we do nothing: we just wanted to create the file
                break                                # no error -> exit the loop
            except FileExistsError:
                print("Name already in use, please give another name.")


        with open(f"{file_name}_kg.txt", "a") as f:
            f.write(f"{display_to_file(final_grid)}")
            print("File generated!")
        break

    elif user_choice == "q":
            print("End of program.")
            break