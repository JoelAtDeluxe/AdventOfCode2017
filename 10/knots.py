from knot_lib import KnotHash


def main(use_real=True, part_one=False):
    sparse_hash, ops, rounds = load_data(use_real, part_one)

    kh = KnotHash(ops, sparse_hash, use_ops_suffix=not(use_real))
    kh.knot_hash(rounds)
    
    print(f"After {rounds} round(s), CheckProduct for sparse hash is: {kh.check_product}")

    if use_real and not(part_one):
        print(f'Dense Hash is {kh.dense_hash()}')


def load_data(use_real: bool, part_one: bool):
    l = [i for i in range(256)] if use_real else [i for i in range(5)]

    ops_str = read_input() if use_real else '3,4,1,5'
    if part_one:
        ops = [int(i) for i in ops_str.split(',')]
    else:
        suffix = [17, 31, 73, 47, 23]
        ops = [ord(i) for i in ops_str]
        ops = [*ops, *suffix]

    rounds = 1 if part_one else 64

    return l, ops, rounds


def read_input():
    with open('input.txt', 'r') as fh:
        return fh.read()


if __name__ == "__main__":
    main(part_one=False)
