class Virus(object):
    NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3

    def __init__(self, row_count, col_count):
        self.position = (row_count//2, col_count//2)
        self.direction = Virus.NORTH
    
    def turn(self, right=True):
        twist = 1 if right else -1

        self.direction = (self.direction + twist) % 4
        if self.direction < Virus.NORTH:
            self.direction = Virus.WEST

    @staticmethod
    def add_tuple(a, b):
        return (a[0] + b[0]), (a[1] + b[1])

    def move(self):
        directions = {
            Virus.NORTH: (-1, 0),
            Virus.SOUTH: (1, 0),
            Virus.WEST: (0, -1),
            Virus.EAST: (0, 1)
        }
        self.position = Virus.add_tuple(self.position, directions[self.direction])

    def adjust_position(self, row_off, col_off):
        self.position = Virus.add_tuple(self.position, (row_off, col_off) )

    def on_cell_encountered(self, cell_value):
        infected = (cell_value == '#')
        self.turn(infected)
        self.move()
        return '.' if infected else '#'
        