
def load_file(path):
    lines = []
    with open(path, 'r') as fh:
        for line in fh:
            lines.append(int(line.strip()))
    return lines


def navigate_maze(maze, update_cell_func):
    position = 0
    next_position = 0
    jump_count = 0

    while 0 <= position < len(maze):
        jump_count += 1
        next_position = position + maze[position]
        maze[position] = update_cell_func(maze[position])
        position = next_position

    # print( maze )
    print(f'Escaped after {jump_count} steps!')


def plus_one(value):
    return value + 1

def part_two_logic(value):
    return value + 1 if value <= 2 else value - 1

# _maze = [0, 3, 0, 1, -3]
_maze = load_file('input.txt')

# navigate_maze(_maze, plus_one)  # p1 solution
navigate_maze(_maze, part_two_logic)  # p2 solution