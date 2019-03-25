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

    step = 0
    # part 1
    sev, stop_layer = calc_severity(scanners, max_layer, step)
    print(f'severity on step: {step} is: {sev}')

        

def calc_severity(scanners, num_layers, step_num, stop_on_nonzero=False):
    severity = 0
    layer_ptr = 0
    
    for layer_sec in range(num_layers+1):
        next_scanner = scanners[layer_ptr]
        if layer_sec == next_scanner.layer:
            layer_ptr += 1
            if next_scanner.pos_at_step(step_num) == 0:
                severity += next_scanner.severity
                        if stop_on_nonzero and severity > 0:
            return severity, layer_sec
                
    return severity, num_layers+1

class Scanner(object):
    def __init__(self, layer, depth):
        self.layer = layer
        self.depth = depth
        self.true_depth = (depth - 1) * 2
        self.position = 0

    @classmethod
    def from_tuple(cls, t):
        return cls(t[0], t[1])

    @property
    def offset(self):
        return self.depth
    
    def advance(self):
        self.position = (self.position + 1) % self.true_depth

    def pos_at_step(self, step_num):
        return (self.layer + step_num) % self.true_depth
        
    @property
    def severity(self):
        return self.depth * self.layer

if __name__ == "__main__":
    main()
