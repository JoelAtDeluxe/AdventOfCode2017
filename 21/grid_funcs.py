def rotate_sq_edge_clockwise(grid):
    new = [
        f'{grid[1][0]}{grid[0][:-1]}'  # row one
    ]

    for i in range(1, len(grid)-1):
        new.append(f'{grid[i+1][0]}{grid[i][1:-1]}{grid[i-1][-1]}')

    new.append(f'{grid[-1][1:]}{grid[-2][-1]}')  # last row

    return new


def rotate_90_clockwise(grid):
    new = []
    for i in range(len(grid[0])):
        new.append(''.join([r[i] for r in reversed(grid)]))
    return new


def flip_h(grid):
    return [reverse(r) for r in grid]


def flip_v(grid):
    return reverse(grid)

def rotate_edge_90_clockwise(grid):
    top_edge = grid[0]
    bottom_edge = grid[-1]
    left_edge = ''.join([r[0] for r in grid])
    right_edge = ''.join([r[-1] for r in grid])

    # clockwise, so left becomes top, top becomes right, and so on
    new = [reverse(left_edge)]  # top

    for i in range(1, len(grid)-1):  # middle rows
        r = grid[i]
        new.append(f'{bottom_edge[(-1 * i) -1]}{r[1:-1]}{top_edge[i]}')

    new.append(reverse(right_edge))  # bottom

    return new


def reverse(it):
    return it[::-1]


def print_grid(grid):
    for row in grid:
        print(row)


def grid_list_to_str(grid_l):
    return '/'.join(grid_l)


def grid_str_to_list(grid_s):
    return grid_s.split('/')


def partition_grid(grid, chunk_size):
    if len(grid) % chunk_size != 0 or len(grid[0]) % chunk_size != 0:
        print("Can't partition this")
        return []
    
    chunks = []
    
    for start_r in range(0, len(grid), chunk_size):
        chunk_row = []
        for start_c in range(0, len(grid[0]), chunk_size):
            chunk = []
            for r_index in range(start_r, start_r + chunk_size):
                chunk.append(grid[r_index][start_c: start_c + chunk_size])
            chunk_row.append(chunk)
        chunks.append(chunk_row)

    return chunks   

def flatten(lst):
    return [row for section in lst for row in section]

def merge_chunks(chunks):
    # We need to figure out how many rows are in each chunk -- chunks are typically square, but
    # trying to account for rectangular grids
    # Chunks look like this:
    # chunks = [rows[ chunk ]] in drawing:
    # 
    # Whole thing is a "grid" or "chunks"
    # +-----+-----+-----+   \
    # |     |     |     |    \
    # |     |     |     |    / Chunk row
    # +-----+-----+-----+   /
    # |     |     |     |
    # |     |     |     |
    # +-----+-----+-----+
    #        \   /
    #         \ /
    #         A chunk

    rows_per_chunk = len(grid_list_to_str(chunks[0][0]).split('/'))
    merged_rows = []

    for chunk_row in chunks:
        section = [''] * rows_per_chunk
        for chunk in chunk_row:
            for i, line in enumerate(chunk):
                section[i] = section[i] + line
        merged_rows.append(section)

    return flatten(merged_rows)

# Tests below

def do_rotation_3():
    grid = [
        '#.?',
        '.X.',
        '?.#'
    ]
    import time
    for _ in range(8):
        print_grid(grid)
        grid = rotate_sq_edge_clockwise(grid)
        print('\n')
        time.sleep(.5)


def do_rotation_rect():
    grid = [
        '#..',
        '.X.',
        '.X.',
        '...'
    ]
    import time
    for _ in range(10):
        print_grid(grid)
        grid = rotate_sq_edge_clockwise(grid)
        print('\n')
        time.sleep(.5)


def do_rotation_2():
    grid = [
        '#.',
        '..'
    ]
    import time
    for _ in range(4):
        print_grid(grid)
        grid = rotate_sq_edge_clockwise(grid)
        print('\n')
        time.sleep(.5)


def do_90_rotate_2():
    grid = [
        '#.',
        '..'
    ]
    import time
    for _ in range(4):
        print_grid(grid)
        grid = rotate_edge_90_clockwise(grid)
        print('\n')
        time.sleep(.5)


def do_90_rotate_3():
    grid = [
        '123',
        '456',
        '789'
    ]
    import time
    for _ in range(4):
        print_grid(grid)
        grid = rotate_edge_90_clockwise(grid)
        print('\n')
        time.sleep(.5)


def do_full_90_rotate_2():
    grid = [
        '12',
        '34'
    ]
    import time
    for _ in range(4):
        print_grid(grid)
        grid = rotate_90_clockwise(grid)
        print('\n')
        time.sleep(.5)


def do_full_90_rotate_3():
    grid = [
        '123',
        '456',
        '789'
    ]
    import time
    for _ in range(4):
        print_grid(grid)
        grid = rotate_90_clockwise(grid)
        print('\n')
        time.sleep(.5)


def do_full_90_rotate_4():
    grid = [
        '1234',
        '5678',
        '9ABC',
        'DEF0'
    ]
    import time
    for _ in range(4):
        print_grid(grid)
        grid = rotate_90_clockwise(grid)
        print('\n')
        time.sleep(.5)


def do_full_90_rotate_5():
    grid = [
        '12345',
        '6789A',
        'BCDEF',
        'GHIJK',
        'LMNOP'
    ]
    import time
    for _ in range(5):
        print_grid(grid)
        grid = rotate_90_clockwise(grid)
        print('\n')
        time.sleep(.5)


def do_h_flip():
    grid = [
        'ABC',
        'DEF',
        'GHI'
    ]
    import time
    for _ in range(3):
        print_grid(grid)
        grid = flip_h(grid)
        print('\n')
        time.sleep(.5)


def do_v_flip():
    grid = [
        'ABC',
        'DEF',
        'GHI'
    ]
    import time
    for _ in range(3):
        print_grid(grid)
        grid = flip_v(grid)
        print('\n')
        time.sleep(.5)


def do_partition():
    grid = [
        '123456',
        'abcdef',
        "[];'./",
        '!@#$%^',
        'ABCDEF',
        '{}:">?',
    ]
    result = partition_grid(grid, 2)

    for row in result:
        for chunk in row:
            print_grid(chunk)
            print()


def do_merge():
    # grid = [
    #     'ABCD',
    #     'EFGH',
    #     'IJKL',
    #     'MNOP'
    # ]
    # start = partition_grid(grid, 2)

    # start = [
    #     [
    #         ['AB', 'EF'],
    #         ['CD', 'GH']
    #     ],
    #     [
    #         ['IJ', 'MN'],
    #         ['KL', 'OP']
    #     ]
    # ]

    # start = [
    #     [
    #         ['ABC'],
    #         ['DEF'],
    #         ['GHI']
    #     ]
    # ]
    grid = [
        'ABC',
        'DEF',
        'GHI'
    ]
    start = partition_grid(grid, 3)
    for row in start:
        for chunk in row:
            print_grid(chunk)
            print()
    print( "---- Becomes ----" )
    merged = merge_chunks(start)
    print_grid(merged)


if __name__ == "__main__":
    do_merge()
