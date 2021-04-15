from logic_units.basic_logical_devices import Register
from helper_functions.basic_functions import hex_to_bin


class RegisterFile:
    def __init__(self):
        self.x = [Register() for i in range(32)]
        self.x[2].write(hex_to_bin('7FFFFFF0', signed=False))
        self.x[3].write(hex_to_bin('10000000', signed=False))

    def write(self, reg_no, bin_val, signed=True):
        if reg_no > 0 and reg_no < 32:
            self.x[reg_no].write(bin_val, signed)

    def read(self, reg_no):
        if reg_no >= 0 and reg_no < 32:
            return self.x[reg_no].read()

    def display_status(self):
        for reg_no in range(32):
            print('x', reg_no, ' :- ',
                  hex(int(self.x[reg_no].read(), 2)), end='\n')
