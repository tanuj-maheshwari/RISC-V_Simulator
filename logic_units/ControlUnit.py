from decode_functions.identify_instruction import *


class ControlUnit:
    def __init__(self):
        self.control_signals = {
            'MuxRs1': 0,
            'MuxA': 0,
            'MuxB': 0,
            'MuxY': 0,
            'MuxPC': 1
        }

    def get_control_signals(self, bin_inst):
        instruction = instruction_sr_no(bin_inst)

        # R-type
        if instruction >= 1 and instruction <= 12:
            self.control_signals['MuxRs1'] = 0
            self.control_signals['MuxA'] = 0
            self.control_signals['MuxB'] = 0
            self.control_signals['MuxY'] = 0
            self.control_signals['MuxPC'] = 1

        # I-type
        elif instruction >= 13 and instruction <= 15:
            self.control_signals['MuxRs1'] = 0
            self.control_signals['MuxA'] = 0
            self.control_signals['MuxB'] = 1
            self.control_signals['MuxY'] = 0
            self.control_signals['MuxPC'] = 1

        # load instructions
        elif instruction >= 16 and instruction <= 18:
            self.control_signals['MuxRs1'] = 0
            self.control_signals['MuxA'] = 0
            self.control_signals['MuxB'] = 1
            self.control_signals['MuxY'] = 1
            self.control_signals['MuxPC'] = 1

        # jalr
        elif instruction == 19:
            self.control_signals['MuxRs1'] = 0
            self.control_signals['MuxA'] = 0
            self.control_signals['MuxB'] = 1
            self.control_signals['MuxY'] = 2
            self.control_signals['MuxPC'] = 0

        # S-type
        elif instruction >= 20 and instruction <= 22:
            self.control_signals['MuxRs1'] = 0
            self.control_signals['MuxA'] = 0
            self.control_signals['MuxB'] = 1
            self.control_signals['MuxY'] = 0
            self.control_signals['MuxPC'] = 1

        # SB-type
        elif instruction >= 23 and instruction <= 26:
            self.control_signals['MuxRs1'] = 0
            self.control_signals['MuxA'] = 0
            self.control_signals['MuxB'] = 0
            self.control_signals['MuxY'] = 1
            self.control_signals['MuxPC'] = 1

        # auipc
        elif instruction == 27:
            self.control_signals['MuxRs1'] = 0
            self.control_signals['MuxA'] = 1
            self.control_signals['MuxB'] = 1
            self.control_signals['MuxY'] = 0
            self.control_signals['MuxPC'] = 1

        # lui
        elif instruction == 28:
            self.control_signals['MuxRs1'] = 1
            self.control_signals['MuxA'] = 0
            self.control_signals['MuxB'] = 1
            self.control_signals['MuxY'] = 0
            self.control_signals['MuxPC'] = 1

        # UJ-type
        else:
            self.control_signals['MuxRs1'] = 0
            self.control_signals['MuxA'] = 0
            self.control_signals['MuxB'] = 0
            self.control_signals['MuxY'] = 2
            self.control_signals['MuxPC'] = 1

        return self.control_signals
