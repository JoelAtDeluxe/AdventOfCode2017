

class Piece(object):
    def __init__(self, north, south):
        self.north = north
        self.south = south
        self.used = False
        self._north_used = False
        self._south_used = False

    def reset(self):
        self.used = False
        self._north_used = False
        self._south_used = False
    
    def clone(self):
        p = Piece(self.north, self.south)
        p._north_used = self._north_used
        p._south_used = self._south_used
        return p

    def _can_fit_north_side(self, side):
        return not(self._north_used ) and self.north == side

    def _can_fit_south_side(self, side):
        return not(self._south_used ) and self.south == side

    def can_fit_side(self, side):
        return not self.used and side in (self.north, self.south)

    def fit_with(self, side):
        if self._can_fit_north_side(side):
            self._north_used = True
            self.used = True
            return True
        elif self._can_fit_south_side(side):
            self._south_used = True
            self.used = True
            return True
        
        return False

    def get_other_side(self, side_a):
        if side_a == self.north:
            return self.south
        return self.north

    def __repr__(self):
        return f'{self.north}/{self.south}'

    @property
    def size(self):
        return self.north + self.south