
class DuetBase(object):
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

    def __init__(self):
        self.registers = {}
        self.instructions = []
        self.std_lib = {
            DuetBase.OP_SET_REG: self._op_set_reg, 
            DuetBase.OP_SET_NUM: self._op_set_num,
            DuetBase.OP_ADD_NUM: self._op_add_num, 
            DuetBase.OP_ADD_REG: self._op_add_reg, 
            DuetBase.OP_MUL_REG: self._op_mul_reg, 
            DuetBase.OP_MUL_NUM: self._op_mul_num, 
            DuetBase.OP_MOD_REG: self._op_mod_reg, 
            DuetBase.OP_MOD_NUM: self._op_mod_num,
            DuetBase.OP_JGZ_REG: self._op_jgz_reg,
            DuetBase.OP_JGZ_NUM: self._op_jgz_num,
            DuetBase.OP_JMP_REG: self._op_jmp_reg,
            DuetBase.OP_JMP_NUM: self._op_jmp_num,
        }
    
    @classmethod
    def from_script(cls, script):
        rtn = cls()

        if type(script) == str:
            script = script.strip().split('\n')
        script = [cmd.strip().lower() for cmd in script]

        rtn.preprocess(script)

        return rtn

    @staticmethod
    def _parse_cmd_one_arity(op_if_int, op_if_reg, parts):
        is_int, val = DuetBase._safe_to_int(parts[1])
        return ((op_if_int if is_int else op_if_reg), val, None)
    
    @staticmethod
    def _parse_cmd_two_arity(op_if_int, op_if_reg, parts):
        is_int, val = DuetBase._safe_to_int(parts[2])
        return ((op_if_int if is_int else op_if_reg), parts[1], val)
    
    @staticmethod
    def _safe_to_int(val):
        try:
            return True, int(val)
        except:
            return False, val

    def preprocess(self, cmds):
        def _parse_jump(parts):
            is_check_int, check_val = DuetBase._safe_to_int(parts[1])
            is_to_int, to_val = DuetBase._safe_to_int(parts[2])
            if is_check_int:
                if is_to_int:
                    return (DuetBase.OP_JMP_NUM, check_val, to_val)
                return (DuetBase.OP_JMP_REG, check_val, to_val)
            elif is_to_int:
                return (DuetBase.OP_JGZ_NUM, check_val, to_val)
            return (DuetBase.OP_JGZ_REG, check_val, to_val)

        resolve = {
            'snd': lambda cmd: DuetBase._parse_cmd_one_arity(DuetBase.OP_SND_NUM, DuetBase.OP_SND_REG, cmd),
            'rcv': lambda cmd: DuetBase._parse_cmd_one_arity(DuetBase.OP_RCV_NUM, DuetBase.OP_RCV_REG, cmd),

            'set': lambda cmd: DuetBase._parse_cmd_two_arity(DuetBase.OP_SET_NUM, DuetBase.OP_SET_REG, cmd),
            'add': lambda cmd: DuetBase._parse_cmd_two_arity(DuetBase.OP_ADD_NUM, DuetBase.OP_ADD_REG, cmd),
            'mul': lambda cmd: DuetBase._parse_cmd_two_arity(DuetBase.OP_MUL_NUM, DuetBase.OP_MUL_REG, cmd),
            'mod': lambda cmd: DuetBase._parse_cmd_two_arity(DuetBase.OP_MOD_NUM, DuetBase.OP_MOD_REG, cmd),

            'jgz': _parse_jump
        }

        self.instructions = [resolve[cmd[:3]](cmd.split()) for cmd in cmds]
        symbols = []
        for inst in self.instructions:
            symbols.extend([sym for sym in inst[1:] if type(sym) == str])
        self.registers = { k: 0 for k in set(symbols) }

    
    def process(self, on_op_result_func=lambda x: False):
        pc = 0
        cmd_len = len(self.instructions)
        while 0 <= pc < cmd_len:
            cmd = self.instructions[pc]
            action = self.std_lib.get(cmd[0])
            if action == None:
                print(f"Unknown command: {cmd[0]}. Please check script (instruction on line {pc+1})")
                break
            result = action(*cmd[1:])
            result = 1 if result is None else result
            stop = on_op_result_func(result)
            if stop:
                break
            pc += result

    def eval_op_result(self, item):
        return False

    def _op_set_num(self, which, val): 
        self.registers[which] = val

    def _op_set_reg(self, which, reg): 
        self._op_set_num(which, self.registers[reg])

    def _op_add_num(self, which, val): 
        self.registers[which] += val
    
    def _op_add_reg(self, which, reg): 
        self._op_add_num(which, self.registers[reg])

    def _op_mul_num(self, which, val): 
        self.registers[which] *= val

    def _op_mul_reg(self, which, reg): 
        self._op_mul_num(which, self.registers[reg])

    def _op_mod_num(self, which, val): 
        self.registers[which] = self.registers[which] % val

    def _op_mod_reg(self, which, reg): 
        self._op_mod_num(which, self.registers[reg])

    def _op_jmp_num(self, _, to): 
        return to

    def _op_jmp_reg(self, _, reg): 
        return self._op_jmp_num(_, self.registers[reg])

    def _op_jgz_num(self, reg, to): 
        return to if self.registers[reg] > 0 else 1

    def _op_jgz_reg(self, reg_check, reg_to): 
        return self._op_jgz_num(reg_check, self.registers[reg_to])

    
class DuetSingle(DuetBase):
    pass


# We could also use inheritance here, but I'm going to opt for a module-like solution
class DuetSound(object):
    def __init__(self, runtime):
        self.runtime = runtime
        self.runtime.std_lib.update({
            DuetBase.OP_SND_REG: self._op_snd_reg,
            DuetBase.OP_SND_NUM: self._op_snd_num,
            DuetBase.OP_RCV_REG: self._op_rcv_reg,
            DuetBase.OP_RCV_NUM: self._op_rcv_num,
        })
        self.runtime.registers['last'] = None
        
    def _op_rcv_num(self, _a, _b):
        print(self.runtime.registers.get('last'))
        return 0

    def _op_rcv_reg(self, which, _):
        temp = self.runtime.registers[which]
        return self._op_rcv_num(which, _) if temp > 0 else 1    
    
    def _op_snd_num(self, val, _): 
        pass  # effective no op since we're not using this note for anything

    def _op_snd_reg(self, reg, _): 
        self.runtime.registers['last'] = self.runtime.registers[reg]

    def process(self):
        self.runtime.process(lambda nxt: nxt == 0)