

NOP = 0  # in case we can simplify the instruction set
OP_SND_REG = 10
OP_SND_NUM = 11
OP_SET_REG = 20
OP_SET_NUM = 21
OP_ADD_REG = 30
OP_ADD_NUM = 31
OP_MUL_REG = 40
OP_MUL_NUM = 41
OP_MOD_REG = 50
OP_MOD_NUM = 51
OP_RCV_REG = 60
OP_RCV_NUM = 61
OP_JGZ_REG = 70
OP_JGZ_NUM = 71
OP_JMP_REG = 80
OP_JMP_NUM = 81

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


def preprocess(cmds):
    def safe_to_int(val):
        try:
            return True, int(val)
        except:
            return False, val

    def parse_normal_two(opt_int, op_reg, parts):
        is_int, val = safe_to_int(parts[1])
        return ((opt_int if is_int else op_reg), val, None)

    def parse_normal_three(op_int, op_reg, parts):
        is_int, val = safe_to_int(parts[2])
        return ((op_int if is_int else op_reg), parts[1], val)

    def interpret(cmd):
        parts = cmd.split()

        if parts[0] == 'snd':
            return parse_normal_two(OP_SND_NUM, OP_SND_REG, parts)

        elif parts[0] == 'set':
            return parse_normal_three(OP_SET_NUM, OP_SET_REG, parts)

        elif parts[0] == 'add':
            return parse_normal_three(OP_ADD_NUM, OP_ADD_REG, parts)

        elif parts[0] == 'mul':
            return parse_normal_three(OP_MUL_NUM, OP_MUL_REG, parts)

        elif parts[0] == 'mod':
            return parse_normal_three(OP_MOD_NUM, OP_MOD_REG, parts)

        elif parts[0] == 'rcv':
            return parse_normal_two(OP_RCV_NUM, OP_RCV_REG, parts)

        elif parts[0] == 'jgz':
            is_check_int, check_val = safe_to_int(parts[1])
            is_to_int, to_val = safe_to_int(parts[2])
            # breakpoint()
            if is_check_int:
                if is_to_int:
                    return (OP_JMP_NUM, check_val, to_val)
                return (OP_JMP_REG, check_val, to_val)
            elif is_to_int:
                return (OP_JGZ_NUM, check_val, to_val)
            return (OP_JGZ_REG, check_val, to_val)

    return [interpret(cmd) for cmd in cmds]


def process_p1(cmds, registers):
    def nop(): pass

    def _get_reg(which):
        rtn = registers.get(which)
        if rtn is None:
            registers[which] = 0
        return registers[which]
    
    # normally these would be lambdas, but I need to do some non-lambda work
    def op_set_num(which, val): registers[which] = val
    def op_set_reg(which, reg): op_set_num(which, _get_reg(reg))

    def op_add_num(which, val): registers[which] = _get_reg(which) + val
    def op_add_reg(which, reg): op_add_num(which, _get_reg(reg))

    def op_mul_num(which, val): registers[which] = _get_reg(which) * val
    def op_mul_reg(which, reg): op_mul_num(which, _get_reg(reg))

    def op_mod_num(which, val): registers[which] = _get_reg(which) % val 
    def op_mod_reg(which, reg): op_mod_num(which, _get_reg(reg))

    def op_rcv_num(_a, _b):
        print(registers.get('last'))
        return 0

    def op_rcv_reg(which, _):
        temp = _get_reg(which)
        if temp > 0:
            return op_rcv_num(which, _)
        return 1
    
    def op_jmp_num(_, to): return to
    def op_jmp_reg(_, reg): op_jmp_num(_, _get_reg(reg))

    def op_jgz_num(reg, to): return to if _get_reg(reg) > 0 else 1
    def op_jgz_reg(reg_check, reg_to): op_jgz_num(reg_check, _get_reg(reg_to))
    
    def op_snd_num(val, _): pass  # effective no op since we're not using this note for anything
    def op_snd_reg(reg, _): registers['last'] = _get_reg(reg)

    actions = {
        OP_SND_REG: op_snd_reg,
        OP_SND_NUM: op_snd_num, 
        OP_SET_REG: op_set_reg, 
        OP_SET_NUM: op_set_num, 
        OP_ADD_REG: op_add_reg, 
        OP_ADD_NUM: op_add_num, 
        OP_MUL_REG: op_mul_reg, 
        OP_MUL_NUM: op_mul_num, 
        OP_MOD_REG: op_mod_reg, 
        OP_MOD_NUM: op_mod_num,
        OP_RCV_REG: op_rcv_reg,
        OP_RCV_NUM: op_rcv_num,
        OP_JGZ_REG: op_jgz_reg,
        OP_JGZ_NUM: op_jgz_num,
        OP_JMP_REG: op_jmp_reg,
        OP_JMP_NUM: op_jmp_num,
    }
    
    pc = 0
    cmd_len = len(cmds)
    import time
    while 0 <= pc < cmd_len:
        cmd = cmds[pc]
        act = actions.get(cmd[0], nop)
        nxt = act(*cmd[1:])
        nxt = 1 if nxt is None else nxt
        if nxt == 0:
            break
        pc += nxt


def main():
    script = load_data('input.txt', real=True)
    actions = preprocess(script)
    registers = {
        'last': None
    }
    process_p1(actions, registers)
    print(registers)


if __name__ == "__main__":
    main()
