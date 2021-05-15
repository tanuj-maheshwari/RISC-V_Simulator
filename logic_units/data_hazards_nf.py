from decode_functions.identify_instruction import *
from decode_functions.get_rs1_rs2_rd import *


class DataHazards:
    def __init__(self):
        self.rd_vals = [0, 0, 0]
        self.stalls = 0

    def getStalls(self, instruction):
        ins_for = get_format_of_instruction(instruction)
        ins_code = instruction_sr_no(instruction)
        ins_rs1 = get_rs1(instruction)
        ins_rs2 = get_rs2(instruction)
        ins_rd = get_rd(instruction)

        self.rd_vals[2] = self.rd_vals[1]
        self.rd_vals[1] = self.rd_vals[0]
        self.rd_vals[0] = ins_rd

        stall_rs1 = stall_rs2 = 0

        if ins_for in ('R', 'S', 'SB'):
            if (ins_rs1 != 0) and (ins_rs1 in [self.rd_vals[1], self.rd_vals[2]]):
                if ins_rs1 == self.rd_vals[1]:
                    stall_rs1 = 2
                else:
                    stall_rs1 = 1

            if (ins_rs2 != 0) and (ins_rs2 in [self.rd_vals[1], self.rd_vals[2]]):
                if ins_rs2 == self.rd_vals[1]:
                    stall_rs2 = 2
                else:
                    stall_rs2 = 1

        elif ins_for == 'I' or ins_code == 28:
            if (ins_rs1 != 0) and (ins_rs1 in [self.rd_vals[1], self.rd_vals[2]]):
                if ins_rs1 == self.rd_vals[1]:
                    stall_rs1 = 2
                else:
                    stall_rs1 = 1

        self.stalls = max(stall_rs1, stall_rs2)
        if self.stalls == 1:
            self.rd_vals[0] = 0
        elif self.stalls == 2:
            self.rd_vals[2] = self.rd_vals[1]
            self.rd_vals[1] = self.rd_vals[0] = 0

        return self.stalls
