
def load_file(path):
    lines = []
    with open(path, 'r') as fh:
        for line in fh:
            lines.append(int(line.strip()))
    return lines


def navigate_maze(maze):
    position = 0
    next_position = 0
    jump_count = 0

    while 0 <= position < len(maze):
        jump_count += 1
        next_position = position + maze[position]
        maze[position] += 1
        position = next_position

    print(f'Escaped after {jump_count} steps!')

_maze = load_file('input.txt')
navigate_maze(_maze)