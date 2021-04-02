from basic_logical_devices import Register
from basic_functions import hex_to_bin


class RegisterFile:
    def __init__(self):
        self.x = [Register() for i in range(32)]
        self.x[2].write(hex_to_bin('7FFFFFF0', signed=False))
        self.x[3].write(hex_to_bin('10000000', signed=False))

    def write(self, reg_no, bin_val, signed=True):
        if reg_no > 0 and reg_no < 32:
            self.x[reg_no].write(bin_val, signed)
        elif reg_no >= 32:
            print("Out of bound register number to RegisterFile write")

    def read(self, reg_no):
        if reg_no >= 0 and reg_no < 32:
            return self.x[reg_no].read()
        else:
            print("Out of bound register number to RegisterFile read")
