import gmpy2


class Tape(object):
    def __init__(self):
        self._tape =  gmpy2.mpz(0)
        self._pos = 0

    def shift(self, rel_pos):
        self._pos += rel_pos
        if self._pos < 0:
            self._tape = self._tape << 1
            self._pos += 1

    def mark_pos(self, val):
        if val == 1:
            self._tape = self._tape.bit_set(self._pos)
        else:
            self._tape = self._tape.bit_clear(self._pos)

    @property
    def mem_value(self):
        """returns the value of this memory cell (1 or 0)"""
        # return self._mem_value()[0]
        return 1 if self._tape.bit_test(self._pos) else 0

    @property
    def total_val(self):
        return self._tape
    
    @property
    def binary(self):
        return f'{self._tape:b}'

    def count_ones(self):
        return sum([1 for i in self.binary if i == '1'])
