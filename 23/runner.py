from engine import ComputeEngine


def load_data(path):
    with open(path, 'r') as fh:
        return fh.read()


def benchmark(script, optimized, iterations):

    import time
    cumulative_time = 0
    for i in range(iterations):
        # reset the engine
        engine = ComputeEngine.from_script(script)
        func = engine.process_optimized if optimized else engine.process

        start = time.time()
        func()
        end = time.time()
        cumulative_time += end - start
    
    return cumulative_time


def run_benchmarks(script):
    print(f'Normal: {benchmark(script, False, 10)}')
    print(f'Optimized: {benchmark(script, True, 10)}')


def run_challenge1(script):
    engine = ComputeEngine.from_script(script)

    mult_count = [0]
    def count_mults(op, pc):
        if op in (ComputeEngine.OP_MUL_REG, ComputeEngine.OP_MUL_NUM):
            mult_count[0] += 1
    engine.process_debug(action_handler=count_mults)
    print(f'Multiply called {mult_count[0]} times')


def run_challenge2(script):
    engine = ComputeEngine.from_script(script)
    engine._op_add_num('a', 1)
    engine.process_optimized()

    print(f'Value of register "h": {engine.get_register("h")}')


def debug_challenge(script):
    engine = ComputeEngine.from_script(script)
    nop = lambda : None

    def wait_for_h(op, pc, eng):
        def status(eng):
            print('----> @ {} // Op: {}'.format(pc, eng.instructions[pc]))
            print(eng._s_reg())
            breakpoint()
            nop()

        if pc == 8:                        # Sets up the starting condition
            status(eng)                    #
        # if pc == 14:                       #  With 19, causes a move g values to e loop
        #     status(eng)                    #
        # if pc == 19:                       #  With 14, causes a move g values to e loop
        #     status(eng)                    #

        # if pc == 10:                        # 
        #     status(eng)                    #

        # if pc == 13:                        # 
        #     status(eng)                    #

        # if pc == 15:                        # 
        #     status(eng)                    #

        # if pc == 20:                       # 
        #     status(eng)                    #

        # if pc == 23:                       # 
        #     status(eng)                    #
        # if pc == 24:                       # 
        #     status(eng)                    #
        # if pc == 28:                       # 
        #     status(eng)                    #
        # if pc == 29:                       # 
        #     status(eng)                    #
        # if pc == 31:                       # 
        #     status(eng)                    #

    engine._op_set_num('a', 1)
    engine.process_debug(action_handler=wait_for_h)


def main():
    # run_benchmarks(load_data('input.txt'))
    # debug_challenge(load_data('input-optimized.txt'))
    
    # run_challenge1(load_data('input.txt'))
    run_challenge2(load_data('input-optimized.txt'))

if __name__ == "__main__":
    main()
