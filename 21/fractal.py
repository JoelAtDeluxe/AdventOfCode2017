import re
from grid_funcs import (rotate_90_clockwise, grid_list_to_str, 
    grid_str_to_list, print_grid, flip_h, flip_v, partition_grid,
    merge_chunks, flatten)


def parse_input(path):
    two_patterns = []
    three_patterns = []
    with open(path, 'r') as fh:
        for line in fh:
            matchobj = re.match(r'(.+)=>(.+)', line)
            in_pattern = matchobj.group(1).strip()
            out_pattern = matchobj.group(2).strip()
            if len(in_pattern.split('/')) == 2:
                two_patterns.append((in_pattern, out_pattern))
            else:
                three_patterns.append((in_pattern, out_pattern))

    return two_patterns, three_patterns


def count_on(pattern):
    return len([ch for ch in pattern if ch == '#'])


def process_input(patterns):
    sorted_patterns = {}

    for p in patterns:
        num_on = count_on(p[0])
        group = sorted_patterns.get(num_on, [])
        group.append(p)
        sorted_patterns[num_on] = group

    return sorted_patterns


def get_subgrid_rotations(subgrid):
    possibilities = set([subgrid])

    for _ in range(3):
        subgrid = grid_list_to_str(
            rotate_90_clockwise(
                grid_str_to_list(subgrid)))
        possibilities.add(subgrid)
    return list(possibilities)


def get_subgrid_flips(subgrid):
    possibilities = set([subgrid])

    subgrid_list = grid_str_to_list(subgrid)
    
    possibilities.add(grid_list_to_str(flip_v(subgrid_list)))
    possibilities.add(grid_list_to_str(flip_h(subgrid_list)))

    return list(possibilities)


def enhance(subgrid, shapes):
    flips = get_subgrid_flips(subgrid)
    all_options = set(flatten([get_subgrid_rotations(v) for v in flips]))

    for shape in shapes:
        if shape[0] in all_options:
            return shape[1]

    print("Couldn't find the shape!")


def partition_enhance(grid, two_patterns, three_patterns, steps):
    
    for i in range(steps):
        size = len(grid)
        
        if size % 2 == 0:
            chunks = partition_grid(grid, 2)
            check_patterns = two_patterns

        elif size % 3  == 0:
            chunks = partition_grid(grid, 3)
            check_patterns = three_patterns
    
        for i, chunk_row in enumerate(chunks):
            for j, chunk in enumerate(chunk_row):
                pattern_index = count_on(grid_list_to_str(chunk))
                new_shape = enhance(grid_list_to_str(chunk), check_patterns[pattern_index])
                # breakpoint()
                chunks[i][j] = grid_str_to_list(new_shape)
        
        grid = merge_chunks(chunks)
    return grid


def main():
    starting_grid = grid_str_to_list(".#./..#/###")
    two_patterns, three_patterns=parse_input('input.txt')

    two_patterns = process_input(two_patterns)
    three_patterns = process_input(three_patterns)

    # Part 1
    # new_grid = partition_enhance(starting_grid, two_patterns, three_patterns, 5)

    # Part 2
    new_grid = partition_enhance(starting_grid, two_patterns, three_patterns, 18)

    print(f'Number of "On" cells: {count_on(grid_list_to_str(new_grid))}')

    # rots=get_subgrid_rotations(starting_grid)
    # for r in rots:
    #     print_grid(grid_str_to_list(r))
    #     print()

    # part 1
    # print(result)

if __name__ == "__main__":
    main()
