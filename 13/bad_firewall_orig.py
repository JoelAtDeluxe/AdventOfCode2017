from collections import namedtuple
from typing import List

Scanner = namedtuple('Scanner', ['size', 'position'])


def parse_input():
    scanners = []
    with open('input.txt', 'r') as fh:
        for line in fh:
            scanner_index, scanner_size = line.split(': ')
            scanners.append((int(scanner_index), int(scanner_size)))
    return scanners


def advance_scanner(prev_state: List[Scanner]) -> List[Scanner]:
    def advance(item: Scanner):
        next_pos = (item.position + 1) % item.size
        return Scanner(item.size, next_pos)

    next_state = [advance(scanner) for scanner in prev_state]
    return next_state


def is_walkable(current_state: List[Scanner]):
    for scanner in current_state:
        if scanner.position == 0:
            return False
    return True


def build_scanner_state(parsed_scanner_input) -> List[Scanner]:
    scanners = []

    for item in parsed_scanner_input:
        # two notes:
        # 1. We don't care about the actual indexing of each position of the scanner -- only whether it's a 0 or not
        # Because of this, we can take a shortcut and simply reflect the scanner as a series of states when it's _not_ 0, and
        # one state where it _is_ 0. In other words, a mod. But, we need to figure out the true "size" of the scanner
        # short version: it takes n-1 steps to reach the end, and n-1 steps to reach 0 from the end, therefore: 2(n-1)
        #
        # 2. Each scanner "starts" at 0, but we need to walk through this, and each step advances all scanners.
        # We can solve this by treating each scanner as starting at a different position based on how far away
        # the step is.
        # import pdb; pdb.set_trace()
        true_size = (item[1] - 1) * 2
        starting_step = item[0] % true_size
        scanners.append(Scanner(true_size, starting_step))

    return scanners


def main():
    # parsed_scanners = parse_input()
    parsed_scanners = [(0, 3), (1, 2), (4, 4), (6, 4)]
    scanner_state = build_scanner_state(parsed_scanners)

    # Part 1
    import pdb; pdb.set_trace()
    severity = 0
    for second in range(parsed_scanners):
        if scanner_state[second].position == 0:
            print(f"Caught on step: {second}")
            severity += scanner_state[second].size * second
        scanner_state = advance_scanner(scanner_state)        

    # wait_count = 0
    # while (not is_walkable(scanner_state)):
    #     wait_count += 1
    #     scanner_state = advance_scanner(scanner_state)
    # 
    # print(f'Needed to wait {wait_count} picoseconds before starting my walk')


if __name__ == "__main__":
    main()
