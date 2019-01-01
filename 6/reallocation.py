
def parse_input(filepath):
    with open(filepath, 'r') as fh:
        return [int(s) for s in fh.read().split('\t')]


def max_index(l):
    maximum_index = 0
    for idx, item in enumerate(l):
        if item > l[maximum_index]:
            maximum_index = idx

    return maximum_index


def distribute(l, index):
    distributable = l[index]
    l[index] = 0

    for i in range(1, distributable + 1):
        new_index = (index + i) % len(l)
        l[new_index] += 1
    
    return l

blocks = parse_input('input.txt')
configurations = []
count = 0

while blocks not in configurations:
    configurations.append([*blocks])
    # import pdb; pdb.set_trace()
    idx = max_index(blocks)
    blocks = distribute(blocks, idx)
    count += 1

base_config = [*blocks]
base_count = count

blocks = distribute(blocks, max_index(blocks))
count += 1
while blocks != base_config:
    idx = max_index(blocks)
    blocks = distribute(blocks, idx)
    count += 1


# print(f'{base_count} / {base_config} -> {count} ({blocks})')
print(f'Solution part 1: {base_count}')
print(f'Solution part 2: {count - base_count}')
