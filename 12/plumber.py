
class SimpleOrderedSet(object):
    def __init__(self, items=[]):
        self._items = items
    
    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return repr(self._items)
    
    def __getitem__(self, pos):
        return self._items[pos]

    def append(self, item):
        if item not in self._items:
            self._items.append(item)
    
    def append_list(self, sublist):
        for item in sublist:
            self.append(item)


def parse_input():
    routes = []
    with open('input.txt', 'r') as fh:
        for line in fh:
            _, channels = line.split(' <-> ')
            channels = [int(x.strip()) for x in channels.split(',')]
            routes.append(channels)
    return routes


def approach_one(routes, connected_to=0):
    # Because these are just in order, we can take advantage of that ordering to simplify the process
    connected_pipes = []
    to_be_connected = SimpleOrderedSet([connected_to])

    # Read in everything, then jump around until you fulfill the whole list
    for pipe in to_be_connected:
        to_be_connected.append_list(routes[pipe])
        connected_pipes.append(pipe)

    return len(connected_pipes)


def main():
    routes = parse_input()
    target = 0
    result = approach_one(routes, connected_to=target)

    print(f'There are {result} pipes connected to {target}')


if __name__ == "__main__":
    main()
