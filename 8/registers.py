

def load_input():
    lines = []
    with open('input.txt', 'r') as fh:
        for line in fh:
            lines.append(line.strip())
    return lines


def main():
    commands = load_input()
    registers = {}

    def get_reg(name):
        val = registers.get(name)
        if val is None:
            registers[name] = 0
            return 0
        return val
    
    conditions = {
        '>': lambda reg_name, value: get_reg(reg_name) > value,
        '>=': lambda reg_name, value: get_reg(reg_name) >= value,
        '<': lambda reg_name, value: get_reg(reg_name) < value,
        '<=': lambda reg_name, value: get_reg(reg_name) <= value,
        '!=': lambda reg_name, value: get_reg(reg_name) != value,
        '==': lambda reg_name, value: get_reg(reg_name) == value
    }

    reg_actions = {
        'inc': lambda reg_name, value: registers.get(reg_name, 0) + value,
        'dec': lambda reg_name, value: registers.get(reg_name, 0) - value,
    }

    maximum_value_during_run = 0

    for cmd in commands:
        components = cmd.split(' ')
        target_register, action, quantity = components[:3]
        cond_register, comparison, cond_val = components[4:]
        quantity, cond_val = int(quantity), int(cond_val)

        result = conditions[comparison](cond_register, cond_val)
        if result:
            registers[target_register] = reg_actions[action](target_register, quantity)
            if maximum_value_during_run < get_reg(target_register):
                maximum_value_during_run = get_reg(target_register)

    maximum = max(registers.values())
    print(f"Max ending register value is: {maximum}")
    print(f"Max in-process register value is: {maximum_value_during_run}")


if __name__ == "__main__":
    main()
