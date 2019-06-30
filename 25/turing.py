from tape import Tape
from state import State
import re


preamble = re.compile(
    r'Begin in state ([A-Z])\.\n'
    r'Perform a diagnostic checksum after (\d+) steps\.', 
    re.MULTILINE)

_write_val_re  = r'    - Write the value ([01]).\n'
_move_re       = r'    - Move one slot to the ((?:right)|(?:left)).\n'
_next_state_re = r'    - Continue with state ([A-Z]).'

state_block = re.compile(
    r'In state ([A-Z]):\n'
    r'  If the current value is 0:\n' + 
    _write_val_re + 
    _move_re +
    _next_state_re + '\n' +
    r'  If the current value is 1:\n' +
    _write_val_re + 
    _move_re +
    _next_state_re,
    re.MULTILINE)


def parse_script(path):
    with open(path, 'r') as fh:
        contents = fh.read()
    
    blocks = contents.split('\n\n')
    
    start_state, step_count = preamble.match(blocks[0]).groups()
    step_count = int(step_count)

    states = {}
    for block in blocks[1:]:
        vals = state_block.match(block).groups()

        false_vals = ( int(vals[1]), 1 if vals[2] == 'left' else -1, vals[3])
        true_vals  = ( int(vals[4]), 1 if vals[5] == 'left' else -1, vals[6])

        states[vals[0]] = State(false_vals, true_vals)

    return states, start_state, step_count


def run_diagnostic(states, start_state, iterations):
    tape = Tape()

    next_state = start_state

    for i in range(iterations):
        next_steps = states[next_state].eval(tape.mem_value)
        tape.mark_pos(next_steps[0])
        tape.shift(next_steps[1])
        next_state = next_steps[2]

    return tape

def main():
    states, start_state, steps_to_execute = parse_script('input.txt')

    result = run_diagnostic(states, start_state, steps_to_execute)
    # print(f'Diagnostic produced a count of {result.count_ones()} 1\'s (number: {result.binary}')
    print(f'Diagnostic produced a count of {result.count_ones()}')


if __name__ == "__main__":
    main()

