import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np


def display_maze(file_path, output_image_path=None):
    # Read the text file (grid of characters #, ., o, *)
    file_path = file_path + ".txt"
    with open(file_path) as f:
        lines = [line.rstrip("\n") for line in f if line.strip() != ""]

    height = len(lines)
    width = len(lines[0])

    # Check that the maze is well-formed:
    for i, line in enumerate(lines):
        if len(line) != width:
            raise ValueError(
                f"Line {i} has length {len(line)}, expected {width}"
            )

    # Character -> numeric value mapping
    # 0 = wall, 1 = free cell, 2 = explored cell, 3 = final path
    mapping = {"#": 0, ".": 1, "*": 2, "o": 3}

    # Empty numeric grid, filled in cell by cell afterward
    num_grid = np.zeros((height, width), dtype=int)
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            if character not in mapping:
                raise ValueError(
                    f"Unexpected character '{character}' at position ({y}, {x})"
                )
            num_grid[y, x] = mapping[character]

    # One color per value, in order 0, 1, 2, 3
    colors = ["black", "white", "orange", "red"]
    cmap = ListedColormap(colors)  # import at the top of the file: from matplotlib.colors import ListedColormap

    plt.figure(figsize=(width / 10, height / 10))
    plt.imshow(num_grid, cmap=cmap, vmin=0, vmax=3)
    plt.axis("off")

    plt.savefig(output_image_path, dpi=150, bbox_inches="tight", pad_inches=0)
    print(f"Image saved to {output_image_path}")
    plt.close()  # frees the figure, essential if the function is called in a loop

file_path = str(input("Please enter a file name: "))
output_image_path = input("Output image file name (e.g. maze.png): ")
display_maze(file_path, output_image_path)