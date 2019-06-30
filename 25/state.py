class State(object):
    def __init__(self, false_vals, true_vals):
        self.true_vals = true_vals
        self.false_vals = false_vals
    
    def eval(self, test_val):
        return self.true_vals if test_val == 1 else self.false_vals

    def __repr__(self):
        return 'cur_val == 1 ?' \
            f' {{ Write {self.true_vals[0]}; Move {self.true_vals[1]}; NextState: {self.true_vals[2]} }}' \
            f': {{ Write {self.false_vals[0]}; Move {self.false_vals[1]}; NextState: {self.false_vals[2]} }}'

