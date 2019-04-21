from engine import DuetSound, DuetBase


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


def main():
    script = load_data('input.txt', real=True)
    
    base_runtime = DuetBase.from_script(script)
    system = DuetSound(base_runtime)

    system.process()
    print(system.runtime.registers)


if __name__ == "__main__":
    main()
