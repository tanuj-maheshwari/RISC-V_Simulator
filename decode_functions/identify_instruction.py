import math


# convert a string from hex to binary [Note:input string without 0x at start]
def hex_to_binary(hex_string):
    bin_string = "{0:032b}".format(int(hex_string, 16))
    return str(bin_string)


def get_opcode(bin_string):
    return bin_string[25:32]


def get_funct3(bin_string):
    return bin_string[17:20]


def get_funct7(bin_string):
    return bin_string[0:7]


# identify whether a instruction is R / I / S / SB / U / UJ.
def get_format_of_instruction(bin_string):
    opcode = get_opcode(bin_string)
    format_of_instruction = ""
    if opcode == "0110011":
        format_of_instruction = "R"
    elif opcode == "0010011" or opcode == "0000011" or opcode == "1100111":
        format_of_instruction = "I"
    elif opcode == "0100011":
        format_of_instruction = "S"
    elif opcode == "1100011":
        format_of_instruction = "SB"
    elif opcode == "0010111" or opcode == "0110111":
        format_of_instruction = "U"
    elif opcode == "1101111":
        format_of_instruction = "UJ"
    else:
        format_of_instruction = "ERROR"
    return format_of_instruction


# returns 1->add, 2->and, 3->or, ... 29->jal [Note:input string without 0x at start]
def instruction_sr_no(bin_string):
    end_inst = '1' * 32
    if bin_string == end_inst:
        return 0
    #bin_string = hex_to_binary(hex_string)
    format_of_instruction = get_format_of_instruction(bin_string)
    opcode = get_opcode(bin_string)
    funct3 = get_funct3(bin_string)
    funct7 = get_funct7(bin_string)
    instruction = 0
    if format_of_instruction == "R":
        if funct7 == "0000000":
            if funct3 == "000":
                instruction = 1  # add
            elif funct3 == "111":
                instruction = 2  # and
            elif funct3 == "110":
                instruction = 3  # or
            elif funct3 == "001":
                instruction = 4  # sll
            elif funct3 == "010":
                instruction = 5  # slt
            elif funct3 == "101":
                instruction = 7  # srl
            elif funct3 == "100":
                instruction = 9  # xor
            else:
                instruction = 99  # error
        elif funct7 == "0100000":
            if funct3 == "101":
                instruction = 6  # sra
            elif funct3 == "000":
                instruction = 8  # sub
            else:
                instruction = 99  # error
        elif funct7 == "0000001":
            if funct3 == "000":
                instruction = 10  # mul
            elif funct3 == "100":
                instruction = 11  # div
            elif funct3 == "110":
                instruction = 12  # rem
            else:
                instruction = 99  # error
        else:
            instruction = 99  # error
    elif format_of_instruction == "I":
        if opcode == "0010011":
            if funct3 == "000":
                instruction = 13  # addi
            elif funct3 == "111":
                instruction = 14  # andi
            elif funct3 == "110":
                instruction = 15  # ori
            else:
                instruction = 99  # error
        elif opcode == "0000011":
            if funct3 == "000":
                instruction = 16  # lb
            elif funct3 == "001":
                instruction = 17  # lh
            elif funct3 == "010":
                instruction = 18  # lw
            else:
                instruction = 99  # error
        elif opcode == "1100111":
            instruction = 19  # jalr
        else:
            instruction = 99  # error
    elif format_of_instruction == "S":
        if funct3 == "000":
            instruction = 20  # sb
        elif funct3 == "010":
            instruction = 21  # sw
        elif funct3 == "001":
            instruction = 22  # sh
        else:
            instruction = 99  # error
    elif format_of_instruction == "SB":
        if funct3 == "000":
            instruction = 23  # beq
        elif funct3 == "001":
            instruction = 24  # bne
        elif funct3 == "101":
            instruction = 25  # bge
        elif funct3 == "100":
            instruction = 26  # blt
        else:
            instruction = 99  # error
    elif format_of_instruction == "U":
        if opcode == "0010111":
            instruction = 27  # auipc
        elif opcode == "0110111":
            instruction = 28  # lui
        else:
            instruction = 99  # error
    elif format_of_instruction == "UJ":
        instruction = 29  # jal
    elif format_of_instruction == "ERROR":
        instruction = 99  # error
    # print(instruction)
    return instruction


"""
add -> 1
and -> 2
or  -> 3
sll -> 4
slt -> 5
sra -> 6
srl -> 7
sub -> 8
xor -> 9
mul -> 10
div -> 11
rem -> 12
addi-> 13
andi-> 14
ori -> 15
lb  -> 16
lh  -> 17
lw  -> 18
jalr-> 19
sb  -> 20
sw  -> 21
sh  -> 22
beq -> 23
bne -> 24
bge -> 25
blt -> 26
auipc->27
lui -> 28
jal -> 29
"""
