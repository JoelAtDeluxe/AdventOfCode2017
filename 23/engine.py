import math


class ComputeEngine(object):
    NOP = 0  # in case we can simplify the instruction set

    OP_SET_REG = 10
    OP_SET_NUM = 11

    OP_ADD_REG = 20
    OP_ADD_NUM = 21

    OP_SUB_REG = 30
    OP_SUB_NUM = 31

    OP_MUL_REG = 40
    OP_MUL_NUM = 41

    OP_MOD_REG = 50
    OP_MOD_NUM = 51

    OP_IDV_REG = 60
    OP_IDV_NUM = 61
    OP_RT_UP_REG = 62
    OP_RT_UP_NUM = 63
    OP_RT_DN_REG = 63
    OP_RT_DN_NUM = 64

    OP_JGZ_REG = 70
    OP_JGZ_NUM = 71

    OP_JNZ_REG = 80
    OP_JNZ_NUM = 81

    OP_JMP_REG = 90
    OP_JMP_NUM = 91

    def __init__(self):
        self.registers = {}
        self.instructions = []
        self.std_lib = {
            ComputeEngine.NOP: lambda x, y: None,

            ComputeEngine.OP_SET_REG: self._op_set_reg, 
            ComputeEngine.OP_SET_NUM: self._op_set_num,

            ComputeEngine.OP_ADD_REG: self._op_add_reg, 
            ComputeEngine.OP_ADD_NUM: self._op_add_num, 

            ComputeEngine.OP_SUB_REG: self._op_sub_reg, 
            ComputeEngine.OP_SUB_NUM: self._op_sub_num, 

            ComputeEngine.OP_MUL_REG: self._op_mul_reg, 
            ComputeEngine.OP_MUL_NUM: self._op_mul_num, 

            ComputeEngine.OP_MOD_REG: self._op_mod_reg, 
            ComputeEngine.OP_MOD_NUM: self._op_mod_num,

            ComputeEngine.OP_IDV_REG: self._op_idv_reg, 
            ComputeEngine.OP_IDV_NUM: self._op_idv_num,

            ComputeEngine.OP_RT_UP_REG: self._op_rt_up_reg, 
            ComputeEngine.OP_RT_UP_NUM: self._op_rt_up_num,
            ComputeEngine.OP_RT_DN_REG: self._op_rt_dn_reg, 
            ComputeEngine.OP_RT_DN_NUM: self._op_rt_dn_num,

            ComputeEngine.OP_JGZ_REG: self._op_jgz_reg,
            ComputeEngine.OP_JGZ_NUM: self._op_jgz_num,

            ComputeEngine.OP_JNZ_REG: self._op_jnz_reg,
            ComputeEngine.OP_JNZ_NUM: self._op_jnz_num,

            ComputeEngine.OP_JMP_REG: self._op_jmp_reg,
            ComputeEngine.OP_JMP_NUM: self._op_jmp_num,
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
        is_int, val = ComputeEngine._safe_to_int(parts[1])
        return ((op_if_int if is_int else op_if_reg), val, None)
    
    @staticmethod
    def _parse_cmd_two_arity(op_if_int, op_if_reg, parts):
        is_int, val = ComputeEngine._safe_to_int(parts[2])
        return ((op_if_int if is_int else op_if_reg), parts[1], val)
    
    @staticmethod
    def _safe_to_int(val):
        try:
            return True, int(val)
        except:
            return False, val

    @staticmethod
    def _parse_jnz(parts):
        # 4 cases: values can be: (reg, reg), (non-reg, reg), (reg, non-reg), (non-reg, non-reg)
        # One subcase for non-reg/non-reg: it could be "jnz 0 ?" in which case, it's a nop
        is_check_int, check_val = ComputeEngine._safe_to_int(parts[1])
        is_to_int, to_val = ComputeEngine._safe_to_int(parts[2])

        if is_check_int:
            if check_val == 0:
                return (ComputeEngine.NOP, 0, 0)
            elif is_to_int:
                return (ComputeEngine.OP_JMP_NUM, check_val, to_val) 
            else:
                return (ComputeEngine.OP_JNZ_NUM, check_val, to_val)
        elif is_to_int:
            return (ComputeEngine.OP_JNZ_NUM, check_val, to_val)
        return (ComputeEngine.OP_JNZ_REG, check_val, to_val)

    @staticmethod
    def _parse_jgz(parts):
        is_check_int, check_val = ComputeEngine._safe_to_int(parts[1])
        is_to_int, to_val = ComputeEngine._safe_to_int(parts[2])
        if is_check_int:
            if check_val <= 0:
                return (ComputeEngine.NOP, 0, 0)
            if is_to_int:
                return (ComputeEngine.OP_JMP_NUM, check_val, to_val)
            return (ComputeEngine.OP_JMP_REG, check_val, to_val)
        elif is_to_int:
            return (ComputeEngine.OP_JGZ_NUM, check_val, to_val)
        return (ComputeEngine.OP_JGZ_REG, check_val, to_val)

    def preprocess(self, cmds):
        import math
        resolve = {
            'set': lambda cmd: ComputeEngine._parse_cmd_two_arity(ComputeEngine.OP_SET_NUM, ComputeEngine.OP_SET_REG, cmd),
            'sub': lambda cmd: ComputeEngine._parse_cmd_two_arity(ComputeEngine.OP_SUB_NUM, ComputeEngine.OP_SUB_REG, cmd),
            'mul': lambda cmd: ComputeEngine._parse_cmd_two_arity(ComputeEngine.OP_MUL_NUM, ComputeEngine.OP_MUL_REG, cmd),
            'idv': lambda cmd: ComputeEngine._parse_cmd_two_arity(ComputeEngine.OP_IDV_NUM, ComputeEngine.OP_IDV_REG, cmd),
            'mod': lambda cmd: ComputeEngine._parse_cmd_two_arity(ComputeEngine.OP_MOD_NUM, ComputeEngine.OP_MOD_REG, cmd),
            '√up': lambda cmd: ComputeEngine._parse_cmd_two_arity(ComputeEngine.OP_RT_UP_NUM, ComputeEngine.OP_RT_UP_REG, cmd),
            '√dn': lambda cmd: ComputeEngine._parse_cmd_two_arity(ComputeEngine.OP_RT_DN_NUM, ComputeEngine.OP_RT_DN_REG, cmd),

            'jnz': ComputeEngine._parse_jnz,
        }

        self.instructions = [resolve[cmd[:3]](cmd.split()) for cmd in cmds]
        symbols = []
        for inst in self.instructions:
            symbols.extend([sym for sym in inst[1:] if type(sym) == str])
        self.registers = { k: 0 for k in set(symbols) }

    def process_debug(self, on_op_result_func=lambda x: False, action_handler= lambda x, y, z: None):
        pc = 0
        cmd_len = len(self.instructions)
        while 0 <= pc < cmd_len:
            cmd = self.instructions[pc]
            action = self.std_lib.get(cmd[0])
            if action == None:
                print(f"Unknown command: {cmd[0]}. Please check script (instruction on line {pc+1})")
                break
            action_handler(cmd[0], pc, self)
            result = action(*cmd[1:])
            result = 1 if result is None else result
            stop = on_op_result_func(result)
            if stop:
                break
            pc += result

    def process_optimized(self):
        """ Streamlined version of process without bells and whisles (roughly 2x speed)"""
        pc = 0
        cmd_len = len(self.instructions)
        # The below is a slight speed improvement, at the cost of lots of memory. 
        op_list = [None] * (max(self.std_lib) + 1)
        for k, v in self.std_lib.items():
            op_list[k] = v

        while 0 <= pc < cmd_len:
            cmd = self.instructions[pc]
            action = op_list[cmd[0]]
            result = action(cmd[1], cmd[2])
            pc += 1 if result is None else result

    def get_register(self, which):
        return self.registers[which]
    
    def _s_reg(self):
        return sorted(self.registers.items())

    def _op_set_num(self, which, val): 
        self.registers[which] = val

    def _op_set_reg(self, which, reg): 
        self._op_set_num(which, self.registers[reg])

    def _op_add_num(self, which, val): 
        self.registers[which] += val
    
    def _op_add_reg(self, which, reg): 
        self._op_add_num(which, self.registers[reg])

    def _op_sub_num(self, which, val):
        self.registers[which] -= val

    def _op_sub_reg(self, which, reg):
        self._op_sub_num(which, self.registers[reg])

    def _op_mul_num(self, which, val): 
        self.registers[which] *= val

    def _op_mul_reg(self, which, reg): 
        self._op_mul_num(which, self.registers[reg])

    def _op_mod_num(self, which, val): 
        self.registers[which] = self.registers[which] % val

    def _op_mod_reg(self, which, reg): 
        self._op_mod_num(which, self.registers[reg])
    
    def _op_idv_num(self, which, val):
        self.registers[which] = self.registers[which] // val

    
    def _op_rt_up_num(self, which, val):
        self.registers[which] = math.ceil(math.sqrt(val))

    def _op_rt_up_reg(self, which, reg):
        return self._op_rt_up_num(which, self.registers[reg])

    def _op_rt_dn_num(self, which, val):
        self.registers[which] = math.floor(math.sqrt(val))

    def _op_rt_dn_reg(self, which, reg):  #This should actually be a unary operator, really, it's sqrt(x) + set
        return self._op_rt_dn_num(which, self.registers[reg])


    def _op_idv_reg(self, which, reg):
        self._op_idv_num(which, self.registers[reg])

    def _op_jmp_num(self, _, to): 
        return to

    def _op_jmp_reg(self, _, reg): 
        return self._op_jmp_num(_, self.registers[reg])

    def _op_jgz_num(self, reg, to): 
        return to if self.registers[reg] > 0 else 1

    def _op_jgz_reg(self, reg, reg_to): 
        return self._op_jgz_num(reg, self.registers[reg_to])

    def _op_jnz_num(self, reg, to):
        return to if self.registers[reg] != 0 else 1
    
    def _op_jnz_reg(self, reg, reg_to):
        return self._op_jnz_num(reg, self.registers[reg_to])
