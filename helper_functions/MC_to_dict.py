def MC_to_dict(filename):
    PC_in = {}
    instructions = open(filename, 'r')

    for each_inst in instructions:
        each_inst = each_inst.strip()
        if each_inst == '':
            continue
        each_inst = each_inst.strip().split()
        l = len(each_inst)
        if l < 2:
            print("Invalid Syntax")
            return

        each_inst[0] = int(each_inst[0], 16)
        each_inst[1] = int(each_inst[1], 16)

        if each_inst[0] > 0xffffffff:
            print("PC out of range")
            return
        if each_inst[1] > 0xffffffff:
            print("Instruction out of range")
            return
        PC_in[each_inst[0]] = each_inst[1]

    return PC_in
