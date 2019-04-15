from typing import List

class KnotHash(object):
    def __init__(self, ops, sparse_hash=None, use_ops_suffix=True):
        self.sparse_hash = [i for i in range(256)] if sparse_hash is None else sparse_hash
        self.ops = KnotHash._encode_ops(ops, use_ops_suffix)

    @classmethod
    def simple_hash(cls, value):
        kn = cls(value)
        kn.knot_hash()
        return kn.dense_hash()

    @staticmethod
    def _encode_ops(base, use_suffix):
        suffix = [17, 31, 73, 47, 23] if use_suffix else []
        ops = base if type(base) == list else [ord(i) for i in base]
        return [*ops, *suffix]
        

    def knot_hash(self, num_rounds=64):
        cur_pos = 0
        skip_size = 0

        for _ in range(num_rounds):
            cur_pos, skip_size = self._do_round(cur_pos, skip_size)

    def _do_round(self, current_position, skip_size):
        l_len = len(self.sparse_hash)

        for action in self.ops:
            if action > 0:
                start_idx = current_position
                end_idx = (current_position + action - 1) % l_len
                self._reverse_circular(start_idx, end_idx)

            current_position = (current_position + action + skip_size) % l_len
            skip_size += 1

        return current_position, skip_size

    def _reverse_circular(self, start, end):
        some_list = self.sparse_hash  # ptr to list (in case we want to make this pure)

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

    @property
    def check_product(self):
        return self.sparse_hash[0] * self.sparse_hash[1]

    def dense_hash(self):
        dh = [0 for _ in range(16)]

        for block_idx in range(16):
            xord = self.sparse_hash[block_idx * 16]
            for x_index in range(15):
                xord = xord ^ self.sparse_hash[block_idx * 16 + 1 + x_index]
            dh[block_idx] = xord

        return KnotHash.to_hex(dh)

    @staticmethod
    def to_hex(int_list: List[int]):
        result = ['' for _ in range(len(int_list)*2)]
        symbols = ['0', '1', '2', '3', '4', '5', '6', '7', 
                   '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

        for i, v in enumerate(int_list):
            high = v // 16
            low = v % 16
            result[2*i], result[(2*i)+1] = symbols[high], symbols[low]

        return ''.join(result)
