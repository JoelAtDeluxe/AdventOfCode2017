from typing import List


def main(use_real=True, part_one=False):
    spase_hash, ops, rounds = load_data(use_real, part_one)

    cur_pos = 0
    skip_size = 0

    for _ in range(rounds):
        cur_pos, skip_size = knot_hash(spase_hash, ops, cur_pos, skip_size)

    check_product = spase_hash[0] * spase_hash[1]
    print(f"After {rounds} round(s), CheckProduct for sparse hash is: {check_product}")

    if use_real and not(part_one):
        dense_hash = to_dense_hash(spase_hash)
        print(f'Dense Hash is: {to_hex(dense_hash)}')


def knot_hash(l, ops, current_position, skip_size):
    l_len = len(l)

    for action in ops:
        # import pdb; pdb.set_trace()
        if action > 0:
            start_idx = current_position
            end_idx = (current_position + action - 1) % l_len
            reverse_circular(l, start_idx, end_idx)

        current_position = (current_position + action + skip_size) % l_len
        skip_size += 1

    return current_position, skip_size


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


def to_dense_hash(sparse_hash: List[int]):
    dense_hash = [0 for _ in range(16)]

    for block_idx in range(16):
        xord = sparse_hash[block_idx * 16]
        for x_index in range(15):
            xord = xord ^ sparse_hash[block_idx * 16 + 1 + x_index]
        dense_hash[block_idx] = xord

    return dense_hash


def to_hex(dense_hash: List[int]):
    result = ['' for _ in range(len(dense_hash)*2)]
    symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

    for i, v in enumerate(dense_hash):
        high = v // 16
        low = v % 16
        result[2*i], result[(2*i)+1] = symbols[high], symbols[low]

    return ''.join(result)


def print_list(l, current_position):
    str_l = [str(i) for i in l]
    print(' '.join(str_l[:current_position]), end='')
    print(f' [{str_l[current_position]}] ', end='')
    print(' '.join(str_l[current_position + 1:]))


def read_input():
    with open('input.txt', 'r') as fh:
        return fh.read()


def reverse_circular(l, start, end):
    # copy = [*l]
    some_list = l  # ptr to list (in case we want to make this pure)

    list_len = len(some_list)
    if start > end:
        true_length = (list_len - start) + end + 1
    else:
        true_length = (end - start) + 1

    for i in range(true_length // 2):
        start_idx = (start + i) % list_len
        end_idx = end - i
        end_idx = end_idx if end_idx >= 0 else list_len + end_idx

        some_list[start_idx], some_list[end_idx] = some_list[
            end_idx], some_list[start_idx]

    return some_list


if __name__ == "__main__":
    main()
