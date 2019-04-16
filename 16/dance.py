from collections import namedtuple

DanceMove = namedtuple("DanceMove", ["action", "a", "b"])

SPIN = 0
EXCHANGE = 1
PARTNER = 2


def load_data(path):
    with open(path, 'r') as fh:
        return fh.read().split(",")


def preprocess(moves):
    def simplify(move):
        if move[0] == 's':
            return DanceMove(SPIN, int(move[1:]), 0)

        parts = move[1:].split('/')
        return DanceMove(PARTNER, parts[0], parts[1]) if move[0] == 'p' else \
            DanceMove(EXCHANGE, int(parts[0]), int(parts[1]))

    return [simplify(m) for m in moves]


def main():
    # lineup = ['a', 'b', 'c', 'd', 'e']
    # moves = preprocess(['s1', 'x3/4', 'pe/b'])
    moves = preprocess(load_data('input.txt'))
    lineup = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
        'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'
    ]
    initial_state = [*lineup]

    part_one = False

    if part_one:
        print(''.join(do_dance_round(lineup, moves)))
        return

    reps = 1_000_000_000  # part 2

    # run until it repeats
    repeats = False
    counter = 0
    keep_dancing_limit = reps/2
    while not repeats:
        lineup = do_dance_round(lineup, moves)
        counter += 1
        if lineup == initial_state:
            repeats = True
        elif counter == keep_dancing_limit:
            break

    # If it repeated, reduce the number of runs we will actually do
    # Otherwise, just finish out the dance
    if repeats:
        reps = reps % counter
        start = 0
        lineup = initial_state
    else:
        start = counter

    for _ in range(start, reps):
        lineup = do_dance_round(lineup, moves)

    print(''.join(lineup))


def do_dance_round(l, moves):
    for move in moves:
        if move[0] == SPIN:
            l = rotate(l, move[1])
        else:
            if move[0] == PARTNER:
                a, b = [l.index(d) for d in move[1:]]
            else:
                a, b = move[1:]
            l[a], l[b] = l[b], l[a]
    return l


def rotate(l, times):
    l_len = len(l)

    # Not needed for this puzzle -- but would help otherwise
    # times = times % l_len
    # if times == 0:
    #   return

    copy = [''] * l_len
    for i in range(l_len):
        copy_pos = (i + times) % l_len
        copy[copy_pos] = l[i]

    return copy


if __name__ == "__main__":
    main()
