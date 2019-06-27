class Virus(object):
    NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3

    def __init__(self, row_count, col_count):
        self.position = (row_count//2, col_count//2)
        self.direction = Virus.NORTH
    
    def turn(self, right=True):
        twist = 1 if right else 3  # left = right, right, right -- we can avoid a check this way
        self.direction = (self.direction + twist) % 4

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


class SmartVirus(Virus):
    def __init__(self, row_count, col_count):
        super().__init__(row_count, col_count)

    def about_face(self):
        self.direction = (self.direction + 2) % 4
        
    def on_cell_encountered(self, cell_value):
        effect_action = {
            '.': ('W', lambda : self.turn(False)),
            'W': ('#', lambda : None),  # no-op
            '#': ('F', lambda : self.turn(True)),
            'F': ('.', lambda : self.about_face())
        }
        effect, action = effect_action[cell_value]
        action()
        self.move()
        return effect
        