from engine import ComputeEngine


def load_data(path):
    with open(path, 'r') as fh:
        return fh.read()


def main():
    script = load_data('input.txt')

    engine = ComputeEngine.from_script(script)

    # Part 1
    mult_count = [0]
    def count_mults(op):
        if op in (ComputeEngine.OP_MUL_REG, ComputeEngine.OP_MUL_NUM):
            mult_count[0] += 1
    engine.process(action_handler=count_mults)
    print(f'Multiply called {mult_count[0]} times')

    # Part 2
    


if __name__ == "__main__":
    main()
