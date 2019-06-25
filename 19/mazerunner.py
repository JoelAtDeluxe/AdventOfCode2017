
def load_data(path, real):
    if not real:
        grid = \
            "     |          \n" \
            "     |  +--+    \n" \
            "     A  |  C    \n" \
            " F---|----E|--+ \n" \
            "     |  |  |  D \n" \
            "     +B-+  +--+ "
    else:
        with open(path, 'r') as fh:
            grid = fh.read()

    return grid.split("\n")


def print_grid(grid, position):
    target_row, target_col = position[1], position[0]
    for i, row in enumerate(grid):
        if i == target_row:
            print("".join([ 
                row[:target_col],
                "*",
                row[target_col+1] 
            ]))
        else:
            print(row)


def find_starting_position(grid):
    return (0, grid[0].index("|"))  # coordinates are in (y, x) (row, column) order


def grid_at(grid, pos):
    if 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0]):
        return grid[pos[0]][pos[1]]
    return ' '


def traverse_grid(grid, start):
    UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
    
    def add_tuple(a, b):
        return (a[0] + b[0]), (a[1] + b[1])

    def find_next_path_step(cur_pos, cross_pos):
        up_pos = add_tuple(cross_pos, UP), UP
        down_pos = add_tuple(cross_pos, DOWN), DOWN
        left_pos = add_tuple(cross_pos, LEFT), LEFT
        right_pos = add_tuple(cross_pos, RIGHT), RIGHT

        possible_dirs = [d for d in (up_pos, down_pos, left_pos, right_pos) if cur_pos != d[0]]
        valid_future_pos = [d for d in possible_dirs if grid_at(grid, d[0]) != ' ']
        
        return valid_future_pos[0]

    current_pos = start
    direction = DOWN
    reached_end = False
    steps_taken = 1  # we count the starting space as a step

    items_passed = []
    
    while not reached_end:
        next_pos = add_tuple(current_pos, direction)
        next_char = grid_at(grid, next_pos)

        if next_char == "+":
            next_pos, direction = find_next_path_step(current_pos, next_pos)
            steps_taken += 1  # we skip over the cross here, but we really step on it
            next_char = grid_at(grid, next_pos)
        elif next_char == ' ':
            reached_end = True
            steps_taken -= 1  # we don't count this step -- we already reached our destination
        
        if next_char not in ('-', '|', ' ', '+'):
            items_passed.append(next_char)
        
        steps_taken += 1  # we made a step here
        current_pos = next_pos
        # print(f"{current_pos} => {grid_at(grid, current_pos)}")
    
    return items_passed, steps_taken

def main():
    grid = load_data('input.txt', real=True)
    start = find_starting_position(grid)
    breakpoint()

    # part 1 & 2
    result = traverse_grid(grid, start)

    print(f"Routing directions: {''.join(result[0])}")
    print(f'Steps taken: {result[1]}')


if __name__ == "__main__":
    main()
