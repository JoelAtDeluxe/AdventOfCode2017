import math
import pprint


def print_grid(grid):
    for line in grid:
        print(', '.join([str(v) for v in line]))


def build_grid(width):
    center = int(width // 2)
    zeros = [[0 for _inner in range(width)] for _outer in range(width)]
    return zeros


def grow_grid(starting_grid):
    width = len(starting_grid) + 2

    grid = []
    grid.append([0 for _ in range(width)])
    for i in range(0, len(starting_grid)):
        grid.append([0, *starting_grid[i], 0])
    grid.append([0 for _ in range(width)])

    return grid


def is_odd(num):
    if int(num) != num:
        return False
    return (num % 2) == 1
    

def gen_directions():
    # These are actually in (y, x), since the first index represents which row, while the 2nd index represents the column
    # Also note that the pattern is what's importnat. Swapping which is 1 and -1 changes the spiral direction, but
    # not it's value

    east = (0, 1)
    north = (-1, 0)
    west = (0, -1)
    south = (1, 0)

    directions = (east, north, west, south)
    dir_idx = 0
    while True:
        yield directions[dir_idx]
        dir_idx = (dir_idx + 1) % len(directions)


def spiral_traverse(grid):
    center = int(len(grid) // 2)
       
    offsets = [0, 0]
    direction = gen_directions()
    heading = next(direction)
    grid[center][center] = 1

    steps = 1
    while True:
        for turn_idx in range(2):
            for step_idx in range(steps):
                offsets[0], offsets[1] = offsets[0] + heading[0], offsets[1] + heading[1]  # step
                x = center + offsets[0]
                y = center + offsets[1]
                grid = yield grid, x, y
                center = int(len(grid) // 2)
                
            heading = next(direction)
        steps += 1


def sum_neighbors(grid, x, y):
    def get(a, b):
        if a < 0 or b < 0 or a >= len(grid) or b >= len(grid):
            return 0
        return grid[a][b]

    adjacent_cell_values = [
        get(x + 0, y + 1),
        get(x - 1, y + 1),
        get(x - 1, y + 0),
        get(x - 1, y - 1),
        get(x + 0, y - 1),
        get(x + 1, y - 1),
        get(x + 1, y + 0),
        get(x + 1, y + 1),
    ]

    return sum(adjacent_cell_values)
    

def main():
    grid = build_grid(3)
    cell = spiral_traverse(grid)

    grid, x, y = cell.send(None)
    target = 265149
    cells_encountered = 1
    last_val = 1
    while last_val < target:
        cells_encountered += 1
        root = math.sqrt(cells_encountered)
        if is_odd(root) and len(grid) == root:
            grid = grow_grid(grid)
            x, y = x + 1, y + 1
        last_val = sum_neighbors(grid, x, y)
        grid[x][y] = last_val
        grid, x, y = cell.send(grid)
    
    print(f'The answer is: {last_val}')
    print_grid(grid)


if __name__ == "__main__":
    main()
