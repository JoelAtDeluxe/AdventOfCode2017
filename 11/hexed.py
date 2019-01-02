
def read_input():
    with open('input.txt', 'r') as fh:
        return fh.read()


def cancel_opposite_directions(steps, dir1, dir2):
    copy = {**steps}
    if copy[dir1] >= copy[dir2]:
        copy[dir1] -= copy[dir2]
        copy[dir2] = 0
    else:
        copy[dir2] -= copy[dir1]
        copy[dir1] = 0
    return copy


def cancel_short_loops(steps, dir1, dir2, dir3):
    copy = {**steps}
    loops = min(copy[dir1], copy[dir2], copy[dir3])
    copy[dir1] -= loops
    copy[dir2] -= loops
    copy[dir3] -= loops
    return copy


def merge_adjacent_directions(steps, left, center, right):
    # e.g. moving se, then sw is the same as moving s. Call this with ('se', 's', 'sw')
    copy = {**steps}
    steps_center = min(steps[left], steps[right])
    copy[left] -= steps_center
    copy[right] -= steps_center
    copy[center] += steps_center
    return copy


def calc_steps(some_steps):
        # Should be reduced first
        return sum(some_steps.values())


def reduce_steps(steps):
    # a couple of optimizations
    # 1: embed the below 3 functions in here, to avoid copies being generated at each step
    # 2: somehow communicate back the changes to be made, rather than returning the result set
    # 2: if/else around each operation/set, if you know the last step made
    copy = {**steps}
    copy = cancel_short_loops(copy, 'n', 'se', 'sw')
    copy = cancel_short_loops(copy, 's', 'ne', 'nw')
    copy = cancel_opposite_directions(copy, 'n', 's')
    copy = cancel_opposite_directions(copy, 'ne', 'sw')
    copy = cancel_opposite_directions(copy, 'nw', 'se')
    copy = merge_adjacent_directions(copy, 'nw', 'n', 'ne')
    copy = merge_adjacent_directions(copy, 'n', 'ne', 'se')
    copy = merge_adjacent_directions(copy, 'ne', 'se', 's')
    copy = merge_adjacent_directions(copy, 'se', 's', 'sw')
    copy = merge_adjacent_directions(copy, 's', 'sw', 'nw')
    copy = merge_adjacent_directions(copy, 'sw', 'nw', 'n')
    return {k: v for k, v in copy.items()}


def main():
    actions = read_input().split(',')
    # actions = "se,sw,se,sw,sw".split(',')
    # actions = "ne,ne,s,s".split(',')
    # actions = "ne,ne,sw,sw".split(',')
    # actions = "ne,ne,ne".split(',')

    steps = {
        'nw': 0,
        'n': 0,
        'ne': 0,

        'se': 0,
        's': 0,
        'sw': 0,
    }
    
    wander_distance = 0
    distance_from_home = 0

    # Chart the overall steps
    for action in actions:
        steps[action] += 1
        steps = reduce_steps(steps)
        distance_from_home = calc_steps(steps)
        if wander_distance < distance_from_home:
            wander_distance = distance_from_home

    print(f'Fewest steps: {distance_from_home}, directions: {steps}')
    print(f'Furthest away: {wander_distance}')


if __name__ == "__main__":
    main()
