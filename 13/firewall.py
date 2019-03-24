from collections import namedtuple

Scanner = namedtuple('Scanner', ['size', 'position'])


def parse_input():
    scanners = []
    with open('input.txt', 'r') as fh:
        for line in fh:
            scanner_index, scanner_size = line.split(': ')
            scanners.append((int(scanner_index), int(scanner_size)))
    return scanners


def main():
    # parsed_scanners = parse_input()
    parsed_scanners = [(0, 3), (1, 2), (4, 4), (6, 4)]
    scanners = [Scanner(t) for t in parsed_scanners]
    max_layer = scanners[-1].layer

    severity = 0
    for packet_pos in range(max_layer+1):
        # step on
        if scanners[packet_pos].position == 0:
            severity += scanners[packet_pos].get_severity()


class Scanner(object):
    def __init__(self, layer, depth):
        self.layer = layer
        self.depth = depth
        self.true_depth = (depth - 1) * 2
        self.position = 0

    @classmethod
    def from_tuple(cls, t):
        return cls(t[0], t[1])

    def advance(self):
        self.position = (self.position + 1) % self.true_depth

    def get_severity(self):
        return self.depth * self.layer

if __name__ == "__main__":
    main()
