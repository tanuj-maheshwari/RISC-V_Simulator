import sys
from decode_functions.identify_instruction import *
from decode_functions.get_rs1_rs2_rd import *


class DataHazards:
    def __init__(self):
        self.rd_int = [[0, -2], [0, -2], [0, -2]]
        self.rs1 = [-1, 3]
        self.rs2 = [-1, 3]
        self.num_stall = 0
        self.flag = 0

    def get_stalls_forwarding_path(self, ins, control_signals):
        f_ins = get_format_of_instruction(ins)

        ins_no = instruction_sr_no(ins)

        ins_rs1 = get_rs1(ins)
        ins_rs2 = get_rs2(ins)
        ins_rd = get_rd(ins)

        self.rs1[0] = ins_rs1
        self.rs2[0] = ins_rs2

        if f_ins == "R":
            self.rs1[1] = 0
            self.rs2[1] = 0

        elif ins_no == 19:
            self.rs1[1] = -1
            self.rs2[1] = 3

        elif f_ins == "I":
            self.rs1[1] = 0
            self.rs2[1] = 3

        elif f_ins == "S":
            self.rs1[1] = 0
            self.rs2[1] = 1

        elif f_ins == "SB":
            self.rs1[1] = -1
            self.rs2[1] = -1

        elif ins_no == 28:
            self.rs1[1] = 0
            self.rs2[1] = 3

        if self.flag == 0:
            self.rd_int[0][0] = ins_rd

            if ins_no <= 15 or ins_no == 27 or ins_no == 28:
                self.rd_int[0][1] = 1
            elif (ins_no > 15 and ins_no <= 19) or ins_no == 29:
                self.rd_int[0][1] = 2
            else:
                self.rd_int[0][1] = -2

            self.flag += 1
            self.num_stall = 0

        else:  # else part of flag
            self.rd_int[2] = self.rd_int[1].copy()
            self.rd_int[1] = self.rd_int[0].copy()

            self.rd_int[0][0] = ins_rd
            if ins_no <= 15 or ins_no == 27 or ins_no == 28:
                self.rd_int[0][1] = 1
            elif (ins_no > 15 and ins_no <= 19) or ins_no == 29:
                self.rd_int[0][1] = 2
            else:
                self.rd_int[0][1] = -2

            # (RD1 = 0 and RD2 = 0)
            if self.rd_int[1][0] == 0 and self.rd_int[2][0] == 0:
                self.num_stall = 0

            else:
                stall_rs1 = stall_rs2 = 0

                if (ins_rs1 != 0) and (ins_rs1 in [self.rd_int[1][0], self.rd_int[2][0]]):

                    if ins_rs1 == self.rd_int[1][0]:
                        if self.rd_int[1][1] == 1:
                            if self.rs1[1] == -1:
                                stall_rs1 = 1
                            elif self.rs1[1] == 0:
                                control_signals['MuxA'] = 2
                            elif self.rs1[1] == 1:
                                control_signals['MuxM'] = 1

                        elif self.rd_int[1][1] == 2:
                            if self.rs1[1] == -1:
                                stall_rs1 = 2
                            elif self.rs1[1] == 0:
                                stall_rs1 = 1
                            elif self.rs1[1] == 1:
                                control_signals['MuxM'] = 1

                    else:
                        if self.rd_int[2][1] == 1:
                            if self.rs1[1] == -1:
                                control_signals['MuxDrs1'] = 1
                            elif self.rs1[1] == 0:
                                control_signals['MuxA'] = 3
                            elif self.rs1[1] == 1:
                                control_signals['MuxDrs1'] = 1

                        elif self.rd_int[2][1] == 2:
                            if self.rs1[1] == -1:
                                stall_rs1 = 1
                            elif self.rs1[1] == 0:
                                control_signals['MuxA'] = 3
                            elif self.rs1[1] == 1:
                                control_signals['MuxM'] = 2

                if (ins_rs2 != 0) and (ins_rs2 in [self.rd_int[1][0], self.rd_int[2][0]]):

                    if ins_rs2 == self.rd_int[1][0]:
                        if self.rd_int[1][1] == 1:
                            if self.rs2[1] == -1:
                                stall_rs2 = 1
                            elif self.rs2[1] == 0:
                                control_signals['MuxB'] = 2
                            elif self.rs2[1] == 1:
                                control_signals['MuxM'] = 1

                        elif self.rd_int[1][1] == 2:
                            if self.rs2[1] == -1:
                                stall_rs2 = 2
                            elif self.rs2[1] == 0:
                                stall_rs2 = 1
                            elif self.rs2[1] == 1:
                                control_signals['MuxM'] = 1

                    else:
                        if self.rd_int[2][1] == 1:
                            if self.rs2[1] == -1:
                                control_signals['MuxDrs2'] = 1
                            elif self.rs2[1] == 0:
                                control_signals['MuxB'] = 3
                            elif self.rs2[1] == 1:
                                control_signals['MuxDrs2'] = 1

                        elif self.rd_int[2][1] == 2:
                            if self.rs2[1] == -1:
                                stall_rs2 = 1
                            elif self.rs2[1] == 0:
                                control_signals['MuxB'] = 3
                            elif self.rs2[1] == 1:
                                control_signals['MuxM'] = 2

                self.num_stall = max(stall_rs1, stall_rs2)

                if self.num_stall == 1:
                    self.rd_int[0] = [0, -2]
                elif self.num_stall == 2:
                    self.rd_int[2] = [self.rd_int[1][0], self.rd_int[1][1]]
                    self.rd_int[1] = self.rd_int[0] = [0, -2]

        return self.num_stall, control_signals
