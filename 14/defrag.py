from typing import List
from knot_lib import KnotHash

def make_to_binary():
    junk = {}
    for i in range(10):
        junk[f'{i}'] = '{0:04b}'.format(i)

    for i in range(6):
        junk[ chr(ord('a')+i) ] = '{0:04b}'.format(10 + i)
    
    def to_binary_str(hex_str: str) -> str:
        hex_str = hex_str.lower()
        in_binary = [ junk.get(ch) for ch in hex_str ]
        return "".join(in_binary)

    def to_binary_int_array(hex_str: str) -> List[int]:
        s = to_binary_str(hex_str)
        return [int(ch) for ch in s]

    return to_binary_str, to_binary_int_array


def render_portion(lines, num_rows, num_cols):
    to_binary_str, _ = make_to_binary()
    iterations = min(len(lines), num_rows)
    for i in range(iterations):
        b = to_binary_str(lines[i])
        chunk = b[:num_cols]
        block = ["#" if ch == '1' else "." for ch in chunk]
        print(''.join(block))


def main():
    puzzle_data = "ljoxqyyw"
    # puzzle_data = 'flqrgnkx'

    rows = [ KnotHash.simple_hash(f'{puzzle_data}-{i}') for i in range(128) ]
    
    # part 1
    # used_count = get_num_square_of_type(rows)
    # print(f"There are {used_count} used squares")

    # Part 2
    region_count = count_regions(rows)
    print(f"There are {region_count} regions")


def traverse_grid(grid, positions, spread, diagonals=False):
    victims = set(positions if type(positions) == list else [positions])
    max_row, max_col = len(grid), len(grid[0])  # assumed to be nxm
    innoculations = [[False] * max_col for _ in range(max_row)]

    def innocuated(coordinate):
        r, c = coordinate
        # check ranges
        if not(0 <= r < max_row) or not(0 <= c < max_col):
            return True
        return innoculations[r][c]

    def vacinate(coordinate):
        r, c = coordinate
        if 0 <= r < max_row and 0 <= c < max_col:
            innoculations[r][c] = True

    while len(victims) != 0:
        quarantine = set()

        # infect the cells
        for cell in victims:
            vacinate(cell)
            if spread(grid, cell[0], cell[1]):
                quarantine.add(cell)

        # spread to next victims
        victims = set() # really future victims at this point
        for r, c in quarantine:
            north, south = (r - 1), (r + 1)
            east, west = (c + 1), (c - 1)
            victims.update( [(north, c), (south, c), (r, east), (r, west)] )
            if diagonals:
                victims.update([(north, east), (north, west), (south, east), (south, west)]) 

        # Restrict infection to only those who have not yet been affected
        victims = set([vic for vic in victims if not innocuated(vic)])


def count_regions(memory):
    _, to_binary_int_array = make_to_binary()
    region_count = 0
    expanded = [to_binary_int_array(r) for r in memory]
    max_rows = len(expanded)
    max_cols = len(expanded[0])

    def make_mark_region(symbol):
        def on_spread(grid, r, c):
            if grid[r][c] == 1:
                grid[r][c] = symbol
                return True
            return False
        return on_spread
    
    for r in range(max_rows):
        for c in range(max_cols):
            if expanded[r][c] == 1:
                region_count += 1
                mark = make_mark_region(region_count + 2)
                traverse_grid(expanded, (r, c), mark)

    return region_count


def get_num_square_of_type(memory, used=True):
    char_type = 1 if used else 0
    _, to_binary_int_array = make_to_binary()
    binary_memory = [to_binary_int_array(r) for r in memory]
    used_counts = [sum(r) for r in binary_memory]
    max_value = len(binary_memory[0]) * len(memory)
    sum_used = sum(used_counts)
    return sum_used if used else max_value - sum_used


def traverse_grid_test():
    size = 5
    grid = [[] for _ in range(size)]
    copy = [[-1]*size for _ in range(size)]

    # breakpoint()
    for r in range(1, size+1):
        for c in range(1, size+1):
            grid[r-1].append(r * c)


    def spread_func(g, r, c):
        copy[r][c] = g[r][c]
        g[r][c] = 100 + g[r][c]
        return  copy[r][c] % 2 == 1

    traverse_grid(grid, (2,2), spread_func)
    print(copy)
    print(grid)

if __name__ == "__main__":
    main()

