import time
import sys


while True:
    user_choice = input(
        "Choose a maze solving method:\n"
        " - Type 1 for recursive backtracking\n"
        " - Type 2 for the A* algorithm\n"
        " - Type q to quit\n"
        "Enter your choice: "
    )

# Recursive backtracking:
    if user_choice == "1":
        def read_maze(file_name):
            with open(f"{file_name}.txt", "r") as f:
                lines = f.read().splitlines()
            return [list(line) for line in lines]

        def deduce_n(grid):
            # The grid is always (2n+1) x (2n+1): n is derived directly from it
            height = len(grid)
            width = len(grid[0])
            assert height == width, "the grid is not square"
            return (height - 1) // 2

        def display(grid):
            for row in grid:
                print(''.join(row))

        def display_to_file(grid):
            text = ""
            for row in grid:
                text += ''.join(row) + "\n"
            return text

        def find_opening(grid, edge):
            """Looks for the '.' cell opened on a given edge of the grid.
            Returns (y, x) of the first open cell found on that edge, or None."""
            height, width = len(grid), len(grid[0])
            if edge == "top":
                return next(((0, x) for x in range(width) if grid[0][x] == "."), None)
            if edge == "bottom":
                return next(((height - 1, x) for x in range(width) if grid[height - 1][x] == "."), None)
            if edge == "left":
                return next(((y, 0) for y in range(height) if grid[y][0] == "."), None)
            if edge == "right":
                return next(((y, width - 1) for y in range(height) if grid[y][width - 1] == "."), None)

        def find_entry_exit(grid):
            """The entry is opened either on the top edge or the left edge.
            The exit is opened either on the bottom edge or the right edge.
            We no longer assume they are necessarily the corners (0,0) / (2n,2n)."""
            entry = find_opening(grid, "top") or find_opening(grid, "left")
            exit_ = find_opening(grid, "bottom") or find_opening(grid, "right")
            return entry, exit_

        def solve(grid, y, x, y_exit, x_exit, visited):
            global counter
            if (y, x) == (y_exit, x_exit):
                grid[y][x] = "o"
                return True

            visited.add((y, x))

            direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dy, dx in direction:
                counter += 1
                ny, nx = y + dy, x + dx
                valid_move = (
                    0 <= ny < len(grid)
                    and 0 <= nx < len(grid[0])
                    and grid[ny][nx] != "#"
                    and (ny, nx) not in visited
                )
                if valid_move:
                    if solve(grid, ny, nx, y_exit, x_exit, visited):
                        grid[y][x] = "o"
                        return True

            grid[y][x] = "*"
            return False

        counter = 0
        file_name = input("Name of the maze file to solve: ")
        grid = read_maze(file_name)
        n = deduce_n(grid)
        sys.setrecursionlimit((2 * n + 1) ** 2)

        entry, exit_ = find_entry_exit(grid)
        if entry is None or exit_ is None:
            print("Could not find the entry or exit on the edges of the grid.")
            sys.exit()

        y_entry, x_entry = entry
        y_exit, x_exit = exit_

        start_time = time.time()
        try:
            found = solve(grid, y_entry, x_entry, y_exit, x_exit, set())
        except RecursionError:
            print("Maze too large for recursive backtracking (Python recursion limit reached).")
            sys.exit()

        if not found:
            print("No path found between the entry and the exit.")

        display(grid)
        elapsed = time.time() - start_time
        output_name = input(f"The solution was generated in {elapsed:.6f} seconds for a cost of {counter} operations (neighbor checks). Output file name (maze + solution): ")
        with open(f"{output_name}_btr.txt", "w") as f:
            f.write(display_to_file(grid))
        break


# A*:
    if user_choice == "2":

        # f(n) = g(n) + h(n)
        def a_star(name_of_file: str):
            #               y,x
            maze = load_maze(name_of_file)

            current_cell = [0, 1]
            finish_point = [len(maze) - 2, len(maze[0]) - 1]
            maze[finish_point[0]][finish_point[1]] = "."

            g = 0

            while True:
                g = g + 1
                if current_cell == finish_point:
                    # print("FINISH")
                    maze[finish_point[0]][finish_point[1]] = "o"
                    print_maze(maze)
                    return maze
                current_cell = check_next_cell(maze_to_solve=maze, current_cell=current_cell, finish_point=finish_point, g=g)

        def check_next_cell(maze_to_solve: list, current_cell: list, finish_point: tuple, g: int) -> tuple:
            """return best cell to choose"""

            possible_ways = []
            directions = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

            tried_steps = 0  # for checking dead end only 4 tries if not go and block by ~
            for d in directions:
                # try to go until branching
                new_y = current_cell[0] + directions[d][0]
                new_x = current_cell[1] + directions[d][1]
                # add possible cells to go
                if maze_to_solve[new_y][new_x] == "." and maze_to_solve[new_y][new_x] != "o":
                    possible_ways.append((new_y, new_x))
                    maze_to_solve[current_cell[0]][current_cell[1]] = "o"

            # go if there's only 1 way to go
            if len(possible_ways) == 1:
                current_cell = list(possible_ways[0])
                # print("new point set")

            # find where is V and bound (assign)
            elif len(possible_ways) == 0:
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
                # choose best way
                # manhattan distance to implement
                list_to_find = []
                for way in possible_ways:
                    h = heuristic(way[1], finish_point[1], way[0], finish_point[0])
                    f = h + g
                    list_to_find.append([f, way])
                    # print(list_to_find)

                best_y, best_x = take_lowest_cell(list_to_find)
                current_cell = [best_y, best_x]
                # print("new point set")
                pass

            # print_maze(maze_to_solve)
            return current_cell

        # ____________________________________________________________________

        def take_lowest_cell(arr: list) -> tuple:
            if not arr:
                return None
            best_way = arr[0]

            for way in arr:
                if way[0] < best_way[0]:
                    best_way = way
            # print(f'Best way - {best_way[1]} - lowest f - {way}')
            return best_way[1]

        def heuristic(x2, x1, y2, y1):
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

        def display_to_file(grid):
            text = ""
            for row in grid:
                text += ''.join(row) + "\n"
            return text

        def read_maze(file_name):
            with open(f"{file_name}.txt", "r") as f:
                lines = f.read().splitlines()
            return [list(line) for line in lines]

        name_of_file = input("Name of the maze file to solve (without extension): ")
        start_time = time.time()
        solution = a_star(f"{name_of_file}.txt")   # solution = the solved grid (list of lists)
        elapsed = time.time() - start_time
        output_name = input(f"The maze was solved in {elapsed:.5f} second(s). Give a name to the generated file: ")
        with open(f"{output_name}_ar.txt", "w") as f:
            f.write(display_to_file(solution))
        break