import sys
from helper_functions.basic_functions import bin_to_dec, extend_to_32_bits
from helper_functions.ALU_utility_functions import *


class ALU:
    def __init__(self):
        self.Out = '0' * 32
        self.branch_control = 0

    def ALU_compute(self, InA, InB, instruction):
        self.Out = '0' * 32
        add_tuple = (1, 13, 16, 17, 18, 19, 20, 21, 22, 27)

        if instruction in add_tuple:
            self.Out = bin_add(InA, InB)
            self.branch_control = 0
        elif instruction == 2 or instruction == 14:
            self.Out = bin_and(InA, InB)
            self.branch_control = 0
        elif instruction == 3 or instruction == 15:
            self.Out = bin_or(InA, InB)
            self.branch_control = 0
        elif instruction == 4:
            self.Out = bin_shift_left(InA, InB)
            self.branch_control = 0
        elif instruction == 5:
            self.Out = 1 if bin_to_dec(InA) < bin_to_dec(InB) else 0
            self.branch_control = 0
        elif instruction == 6 or instruction == 7:
            arithmetic = 1 if instruction == 6 else 0
            self.Out = bin_shift_right(InA, InB, arithmetic)
            self.branch_control = 0
        elif instruction == 8:
            self.Out = bin_sub(InA, InB)
            self.branch_control = 0
        elif instruction == 9:
            self.Out = bin_xor(InA, InB)
            self.branch_control = 0
        elif instruction == 10:
            self.Out = bin_mul(InA, InB)
            self.branch_control = 0
        elif instruction == 11:
            self.Out = bin_div(InA, InB)
            self.branch_control = 0
        elif instruction == 12:
            self.Out = bin_rem(InA, InB)
            self.branch_control = 0

        elif instruction == 23:
            self.branch_control = 1 if InA == InB else 0
        elif instruction == 24:
            self.branch_control = 1 if InA != InB else 0
        elif instruction == 25:
            self.branch_control = 1 if bin_to_dec(
                InA) >= bin_to_dec(InB) else 0
        elif instruction == 26:
            self.branch_control = 1 if bin_to_dec(InA) < bin_to_dec(InB) else 0

        elif instruction == 28:
            InA_upper_excluded = bin_and(
                InA, '00000000000000000000111111111111')
            self.Out = bin_add(InA_upper_excluded, InB)
            self.branch_control = 0

        elif instruction == 29:
            self.branch_control = 1

        else:
            self.Out = extend_to_32_bits('0')
