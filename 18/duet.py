from engine import DuetSound, DuetBase, DuetProcess


def load_data(path, real):
    if not real:
        return [line.strip() for line in """set a 1
            add a 2
            mul a a
            mod a 5
            snd a
            set a 0
            rcv a
            jgz a -1
            set a 1
            jgz a -2
        """.strip().split('\n')]

    with open(path, 'r') as fh:
        return [line.strip() for line in fh]


def sequence_runner(script):

    # Unfortunately, we need to parse the script twice, otherwise funtion pointers aren't updated properly
    p0 = DuetProcess(0, DuetBase.from_script(script))
    p1 = DuetProcess(1, DuetBase.from_script(script))
    p0.companion = p1
    p1.companion = p0

    def stopped():
        if p0.exited and p1.exited:
            return True
        elif (p0.exited and p1.is_stalled()) or (p0.is_stalled() and p1.exited):
            return True
        elif p0.is_stalled() and p1.is_stalled():
            return True
        return False 

    while not stopped():
        if not p0.exited:
            p0.process()
        if not p1.exited:
            p1.process()
    
    print(f"P1 set {len(p0.msg_queue)} messages")


def main():
    script = load_data('input.txt', real=True)

    # Part 1
    # system = DuetSound(base_runtime)

    # Part 2
    sequence_runner(script)


if __name__ == "__main__":
    main()
