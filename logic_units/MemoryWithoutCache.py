import sys
from helper_functions.basic_functions import *
from logic_units.basic_logical_devices import Register


class MemoryWithoutCache:
    MAX_ADDRESS = 0x7fffffff
    MIN_ADDRESS = 0x10000000
    MIN_PC = 0x00000000
    MAX_PC = 0x0ffffffc

    def __init__(self):
        self.InsMem = {}
        self.DataMem = {}
        self.MAR = Register()
        self.MDR = Register()
        self.final_ins = 0

    def Prog_Load(self, PC_in):
        for i in PC_in:
            for every_byte in range(4):
                byte = PC_in[i] & 255
                if i <= self.MAX_PC:
                    self.InsMem[i+every_byte] = byte
                else:
                    self.DataMem[i+every_byte] = byte
                PC_in[i] = PC_in[i] >> 8

    def Ins_Load(self, PC_bin):
        PC = int(PC_bin, 2)
        if PC % 4 != 0:
            print("\nInstrucion Not Aligned")
            sys.exit()
        else:
            if PC < self.MIN_PC or PC > self.MAX_PC:
                print("\nPC, range exceeded!")
                sys.exit()
            else:
                temp_inst = temp_inst_sum = 0
                for every_byte in range(4):
                    temp_inst = self.InsMem.get(
                        PC+every_byte, 0)*(256**every_byte)
                    temp_inst_sum += temp_inst
                self.final_ins = temp_inst_sum
                inst = bin(self.final_ins).replace('0b', '')
                self.MDR.write(inst, False)
                return self.MDR.read()

    def Mem_write(self, no_of_bytes):
        base_address = int(self.MAR.read(), 2)
        data = int(self.MDR.read(), 2)
        for every_byte in range(no_of_bytes):
            byte = data & 255
            if base_address+every_byte < self.MIN_ADDRESS or base_address+every_byte > self.MAX_ADDRESS:
                print("\nAddress out of range")
                sys.exit()
            self.DataMem[base_address+every_byte] = byte
            data = data >> 8

    def Mem_read(self, no_of_bytes):
        base_address = int(self.MAR.read(), 2)
        mdr = 0
        for every_byte in range(no_of_bytes):
            if base_address+every_byte < self.MIN_ADDRESS or base_address+every_byte > self.MAX_ADDRESS:
                print("\nAddress out of range")
                sys.exit()
            data = self.DataMem.get(base_address+every_byte, 0)
            for i in range(every_byte):
                data = data << 8
            mdr += data
        self.MDR.write(bin(mdr).replace('0b', ''), False)

    def display_status(self):
        address = int(input("\nJump to address (hex) :- 0x"), 16)
        if address < self.MIN_ADDRESS or address > self.MAX_ADDRESS:
            print("\nAddress out of range")
            return
        address = (address // 4) * 4

        print("\n\n Address      +0  +1  +2  +3\n")
        for base in range(20, -21, -4):
            if base+address >= self.MIN_ADDRESS and base+address <= self.MAX_ADDRESS:
                segmented_value = [0, 0, 0, 0]
                for every_byte in range(4):
                    segmented_value[every_byte] = hex(self.DataMem.get(
                        address+base+every_byte, 0)).replace('0x', '').zfill(2)
                print('0x'+hex(address+base)[2:].zfill(8), '', segmented_value[0],
                      segmented_value[1], segmented_value[2], segmented_value[3], sep='  ')
