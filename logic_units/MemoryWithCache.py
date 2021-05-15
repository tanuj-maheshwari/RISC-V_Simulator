import sys
import math
from helper_functions.basic_functions import *
from helper_functions.ALU_utility_functions import *
from logic_units.basic_logical_devices import Register


class MemoryWithCache:
    MAX_ADDRESS = 0x7fffffff
    MIN_ADDRESS = 0x10000000
    MIN_PC = 0x00000000
    MAX_PC = 0x0ffffffc

    def __init__(self):
        self.InsMem = {}
        self.I_Cache = {}
        self.I_access = 0
        self.I_miss = 0
        self.I_numblocks = 0
        self.I_numsets = 0
        self.I_offsetwidth = 0
        self.I_indexwidth = 0
        self.DataMem = {}
        self.D_Cache = {}
        self.D_read_access = 0
        self.D_write_access = 0
        self.D_read_miss = 0
        self.D_write_miss = 0
        self.D_numblocks = 0
        self.D_numsets = 0
        self.D_offsetwidth = 0
        self.D_indexwidth = 0
        self.MAR = Register()
        self.MDR = Register()
        self.final_ins = 0

    def inst_cache(self, i_csize, i_bsize, i_ways, d_csize, d_bsize, d_ways):
        empty_block = ["", 0, [], 0]

        self.I_numblocks = int(i_csize/i_bsize)
        self.I_numsets = int(self.I_numblocks/i_ways)
        self.I_offsetwidth = int(math.log2(i_bsize))
        self.I_indexwidth = int(math.log2(self.I_numsets))
        for i in range(self.I_numblocks):
            self.I_Cache[i] = empty_block.copy()

        self.D_numblocks = int(d_csize/d_bsize)
        self.D_numsets = int(self.D_numblocks/d_ways)
        self.D_offsetwidth = int(math.log2(d_bsize))
        self.D_indexwidth = int(math.log2(self.D_numsets))
        for i in range(self.D_numblocks):
            self.D_Cache[i] = empty_block.copy()

    def read_byte_from_Icache(self, address):
        data = 0
        hit = 0
        tag = address[:-(self.I_offsetwidth+self.I_indexwidth)]
        index = int(
            address[(32-(self.I_offsetwidth+self.I_indexwidth)):(32-self.I_offsetwidth)], 2)
        offset = int(address[-self.I_offsetwidth:], 2)
        num_blocksinset = int(self.I_numblocks/self.I_numsets)

        for i in range(num_blocksinset*index, num_blocksinset*index+num_blocksinset):
            if (self.I_Cache[i][0] == tag) and (self.I_Cache[i][1] == 1):
                hit = 1
                data = self.I_Cache[i][2][offset]
                self.I_Cache[i][3] = num_blocksinset - 1
                break

        if hit == 0:
            address_int = int(address, 2)
            block_size = int(pow(2, self.I_offsetwidth))
            block_data = []
            address_lowerbound = address_int - (address_int % block_size)
            for i in range(block_size):
                block_data.append(self.InsMem.get(address_lowerbound+i, 0))

            space_in_cache = False
            for i in range(num_blocksinset*index, num_blocksinset*index+num_blocksinset):
                if self.I_Cache[i][1] == 0:
                    self.I_Cache[i] = [
                        tag, 1, block_data.copy(), num_blocksinset-1].copy()
                    space_in_cache = True
                    data = self.I_Cache[i][2][offset]
                    break

            if space_in_cache is False:
                for i in range(num_blocksinset*index, num_blocksinset*index+num_blocksinset):
                    if self.I_Cache[i][3] == 0:
                        self.I_Cache[i] = [
                            tag, 1, block_data.copy(), num_blocksinset-1].copy()
                        data = self.I_Cache[i][2][offset]
                        break

        for i in range(num_blocksinset*index, num_blocksinset*index+num_blocksinset):
            if self.I_Cache[i][0] != tag:
                self.I_Cache[i][3] -= (1 if self.I_Cache[i][3] != 0 else 0)

        return data, hit

    def read_byte_from_Dcache(self, address):
        data = 0
        hit = 0
        tag = address[:-(self.D_offsetwidth+self.D_indexwidth)]
        index = int(
            address[(32-(self.D_offsetwidth+self.D_indexwidth)):(32-self.D_offsetwidth)], 2)
        offset = int(address[-self.D_offsetwidth:], 2)
        num_blocksinset = int(self.D_numblocks/self.D_numsets)

        for i in range(num_blocksinset*index, num_blocksinset*index+num_blocksinset):
            if (self.D_Cache[i][0] == tag) and (self.D_Cache[i][1] == 1):
                hit = 1
                data = self.D_Cache[i][2][offset]
                self.D_Cache[i][3] = num_blocksinset - 1
                break

        if hit == 0:
            address_int = int(address, 2)
            block_size = int(pow(2, self.D_offsetwidth))
            block_data = []
            address_lowerbound = address_int - (address_int % block_size)
            for i in range(block_size):
                block_data.append(self.DataMem.get(address_lowerbound+i, 0))

            space_in_cache = False
            for i in range(num_blocksinset*index, num_blocksinset*index+num_blocksinset):
                if self.D_Cache[i][1] == 0:
                    self.D_Cache[i] = [
                        tag, 1, block_data.copy(), num_blocksinset-1].copy()
                    space_in_cache = True
                    data = self.D_Cache[i][2][offset]
                    break

            if space_in_cache is False:
                for i in range(num_blocksinset*index, num_blocksinset*index+num_blocksinset):
                    if self.D_Cache[i][3] == 0:
                        self.D_Cache[i] = [
                            tag, 1, block_data.copy(), num_blocksinset-1].copy()
                        data = self.D_Cache[i][2][offset]
                        break

        for i in range(num_blocksinset*index, num_blocksinset*index+num_blocksinset):
            if self.D_Cache[i][0] != tag:
                self.D_Cache[i][3] -= (1 if self.D_Cache[i][3] != 0 else 0)

        return data, hit

    def write_byte_to_DCache(self, data, address):
        hit = 0
        tag = address[:-(self.D_offsetwidth+self.D_indexwidth)]
        index = int(
            address[(32-(self.D_offsetwidth+self.D_indexwidth)):(32-self.D_offsetwidth)], 2)
        offset = int(address[-self.D_offsetwidth:], 2)
        num_blocksinset = int(self.D_numblocks/self.D_numsets)

        for i in range(num_blocksinset*index, num_blocksinset*index+num_blocksinset):
            if (self.D_Cache[i][0] == tag) and (self.D_Cache[i][1] == 1):
                hit = 1
                self.D_Cache[i][2][offset] = data
                break

        if hit == 1:
            for i in range(num_blocksinset*index, num_blocksinset*index+num_blocksinset):
                if self.D_Cache[i][0] != tag:
                    self.D_Cache[i][3] -= (1 if self.D_Cache[i][3] != 0 else 0)

        return hit

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
                self.I_access += 1
                miss = False
                temp_inst = temp_inst_sum = 0
                for every_byte in range(4):
                    PC_val = bin_add(PC_bin, bin(every_byte)[2:], False)
                    temp_inst, hit = self.read_byte_from_Icache(PC_val)
                    if hit == 0 and miss is False:
                        self.I_miss += 1
                        miss = True
                    temp_inst = temp_inst*(256**every_byte)
                    temp_inst_sum += temp_inst
                self.final_ins = temp_inst_sum
                inst = bin(self.final_ins).replace('0b', '')
                self.MDR.write(inst, False)
                return self.MDR.read()

    def Mem_write(self, no_of_bytes):
        base_address = int(self.MAR.read(), 2)
        data = int(self.MDR.read(), 2)
        self.D_write_access += 1
        miss = False
        for every_byte in range(no_of_bytes):
            byte = data & 255
            if base_address+every_byte < self.MIN_ADDRESS or base_address+every_byte > self.MAX_ADDRESS:
                print("\nAddress out of range")
                sys.exit()
            address = bin_add(self.MAR.read(), bin(every_byte)[2:], False)
            hit = self.write_byte_to_DCache(byte, address)
            if hit == 0 and miss is False:
                self.D_write_miss += 1
                miss = True
            self.DataMem[base_address+every_byte] = byte
            data = data >> 8

    def Mem_read(self, no_of_bytes):
        base_address = int(self.MAR.read(), 2)
        mdr = 0
        self.D_read_access += 1
        miss = False
        for every_byte in range(no_of_bytes):
            if base_address+every_byte < self.MIN_ADDRESS or base_address+every_byte > self.MAX_ADDRESS:
                print("\nAddress out of range")
                sys.exit()
            address = bin_add(self.MAR.read(), bin(every_byte)[2:], False)
            data, hit = self.read_byte_from_Dcache(address)
            if hit == 0 and miss is False:
                self.D_read_miss += 1
                miss = True
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
