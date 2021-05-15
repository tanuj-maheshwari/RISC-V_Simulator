from decode_functions.identify_instruction import get_format_of_instruction

def get_rs1(ins):
    f_ins = get_format_of_instruction(ins)
    if f_ins != "U" and f_ins != "UJ":
        return int(ins[12:17],2)
    else:
        return 0

def get_rs2(ins):
    f_ins = get_format_of_instruction(ins)
    if f_ins != "I" and f_ins != "U" and f_ins != "UJ":
        return int(ins[7:12],2)
    else:
        return 0

def get_rd(ins):
    f_ins = get_format_of_instruction(ins)
    if f_ins != "S" and f_ins != "SB":
        return int(ins[20:25],2)
    else:
        return 0

