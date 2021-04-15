from decode_functions.identify_instruction import instruction_sr_no


def ext_imm(ins):
    ins_type = instruction_sr_no(ins)
    imm = ""
    if ins_type >= 1 and ins_type <= 12:
        return '0'*32
    elif ins_type >= 13 and ins_type <= 19:
        imm = ins[:12]
        return imm
    elif ins_type >= 20 and ins_type <= 22:
        imm1 = ins[:7]
        imm2 = ins[20:25]
        imm = imm1 + imm2
        return imm
    elif ins_type >= 23 and ins_type <= 26:
        imm += ins[1:7]
        imm += ins[20:24]
        imm = ins[24] + imm
        imm += '0'
        return imm
    elif ins_type == 27 or ins_type == 28:
        imm1 = ins[:20]
        imm2 = '0'*12
        imm = imm1 + imm2
        return imm
    elif ins_type == 29:
        imm += ins[12:20]
        imm += ins[11]
        imm += ins[1:11]
        imm += '0'
        return imm
