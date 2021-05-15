from logic_units.basic_logical_devices import *
from helper_functions.ALU_utility_functions import bin_add


class IAG:
    def __init__(self):
        self.PC = Register()
        self.PC_temp = Register()
        self.MuxPC = MUX(2)
        self.MuxINC = MUX(2)

    def getPC(self):
        return self.PC.read()

    def run(self, immediate, MuxPC_select, MuxINC_select, RA):
        self.PC_temp.write(bin_add(self.PC.read(), '0100'))
        Mux_INC_inputs = [extend_to_32_bits('0100'), immediate]
        self.MuxINC.setInputs(Mux_INC_inputs)
        MuxINC_Out = self.MuxINC.getOutput(MuxINC_select)
        next_PC = bin_add(self.PC.read(), MuxINC_Out)
        MuxPC_inputs = [RA, next_PC]
        self.MuxPC.setInputs(MuxPC_inputs)
        MuxPC_Out = self.MuxPC.getOutput(MuxPC_select)
        self.PC.write(MuxPC_Out)
