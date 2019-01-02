
def read_input():
    with open('input.txt', 'r') as fh:
        return fh.read()


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

    def cancel_opposite_directions(dir1, dir2):
        if steps[dir1] >= steps[dir2]:
            steps[dir1] -= steps[dir2]
            steps[dir2] = 0
        else:
            steps[dir2] -= steps[dir1]
            steps[dir1] = 0
    
    def cancel_short_loops(dir1, dir2, dir3):
        loops = min(steps[dir1], steps[dir2], steps[dir3])
        steps[dir1] -= loops
        steps[dir2] -= loops
        steps[dir3] -= loops

    def merge_adjacent_directions(left, center, right):
        # e.g. moving se, then sw is the same as moving s. Call this with ('se', 's', 'sw')
        steps_left = steps[left]
        steps_right = steps[right]
        steps_center = min(steps_left, steps_right)
        steps[left] -= steps_center
        steps[right] -= steps_center
        steps[center] += steps_center

    def reduce_steps():
        cancel_short_loops('n', 'se', 'sw')
        cancel_short_loops('s', 'ne', 'nw')
        cancel_opposite_directions('n', 's')
        cancel_opposite_directions('ne', 'sw')
        cancel_opposite_directions('nw', 'se')
        merge_adjacent_directions('nw', 'n', 'ne')
        merge_adjacent_directions('n', 'ne', 'se')
        merge_adjacent_directions('ne', 'se', 's')
        merge_adjacent_directions('se', 's', 'sw')
        merge_adjacent_directions('s', 'sw', 'nw')
        merge_adjacent_directions('sw', 'nw', 'n')
        return {k: v for k, v in steps.items()}

    def calc_steps(some_steps):
        # Should be reduced first
        return sum(some_steps.values())

    wander_distance = 0
    distance_from_home = 0

    # Chart the overall steps
    for action in actions:
        steps[action] += 1
        steps = reduce_steps()
        distance_from_home = calc_steps(steps)
        if wander_distance < distance_from_home:
            wander_distance = distance_from_home

    print(f'Fewest steps: {distance_from_home}, directions: {steps}')
    print(f'Furthest away: {wander_distance}')


if __name__ == "__main__":
    main()
