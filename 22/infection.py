from virus import Virus


def parse_input(path):
    lines = []
    with open(path, 'r') as fh:
        for line in fh:
            lines.append(line.strip())
    return lines

def print_grid(grid):
    for row in grid:
        print(row)


def grow_grid(old_grid):
    """ Returns back a new grid, with _half_ the amount grown in each direction
        (i.e. the offset if you were tracking something inside of it).
        Assumes grid size >= 3
    """
    grid_rows, grid_cols = get_dimensions(old_grid)
    half_row, half_col = (grid_rows//2), (grid_cols//2)
    new_rows = 2 * half_row + grid_rows
    new_cols = 2 * half_col + grid_cols

    # this should ensure that we always have an odd number of rows/columns
    # e.g. 25x25 grid => new is (25//2)*2 + 25 (one side) => 24+25 => 49x49

    # Construct fillables
    clean_row = '.' * new_cols
    row_header_footer = [clean_row for _ in range(half_row)]
    col_header_footer = '.' * half_col

    # Construct the new grid
    new_grid = [*row_header_footer]

    for row in old_grid:
        new_grid.append( col_header_footer + row + col_header_footer )
    
    new_grid = new_grid + row_header_footer
    
    return new_grid, half_row, half_col


def make_needs_growth(grid):
    size = get_dimensions(grid)
    
    def needs_growth(pos):
        if pos[0] < 0 or pos[1] < 0:
            return True
        if pos[0] >= size[0] or pos[1] >= size[1]:
            return True
        return False

    return needs_growth


def val_at(grid, pos):
    return grid[pos[0]][pos[1]]


def get_dimensions(grid):
    return len(grid), len(grid[0])


def simulate_phase_one(grid, virus, iterations):
    infection_count = 0

    needs_growth = make_needs_growth(grid)
    for _ in range(iterations):
        site_row, site_col = virus.position
        cell_status = virus.on_cell_encountered( val_at(grid, virus.position) )
        if cell_status == '#':
            infection_count += 1
        grid[site_row] = grid[site_row][:site_col] + cell_status + grid[site_row][site_col + 1:]

        if needs_growth(virus.position):
            grid, off_row, off_col = grow_grid(grid)
            needs_growth = make_needs_growth(grid)
            virus.adjust_position(off_row, off_col)
    
    return grid, infection_count


def main():
    starting_grid = parse_input('input.txt')
    # starting_grid = parse_input('alt-input.txt')

    virus = Virus(*get_dimensions(starting_grid))

    # Part 1
    new_grid, infec_count = simulate_phase_one(starting_grid, virus, 10000)
    # print_grid(new_grid)
    print(f'Tracked {infec_count} new infections')


if __name__ == "__main__":
    main()
