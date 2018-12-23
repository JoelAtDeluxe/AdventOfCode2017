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
                new_center = int(len(grid) // 2)
                if new_center != center:
                    offsets[0], offsets[1] = offsets[0] + 1, offsets[1] + 1
                    center = new_center

            heading = next(direction)
        steps += 1


def main():
    grid = build_grid(3)
    cell = spiral_traverse(grid)

    grid, x, y = cell.send(None)
    for i in range(1, 17):
        if is_odd(math.sqrt(i)) and len(grid) == math.sqrt(i):
            grid = grow_grid(grid)
        grid[x][y] = i + 1
        grid, x, y = cell.send(grid)
    
    print_grid(grid)

if __name__ == "__main__":
    main()
