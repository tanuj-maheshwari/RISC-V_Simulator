from helper_functions.basic_functions import extend_to_32_bits


class Register:
    def __init__(self):
        self.val = '0' * 32

    def write(self, value, signed=True):
        self.val = extend_to_32_bits(value, signed)

    def read(self):
        return self.val


class MUX:
    def __init__(self, num_inputs):
        self.num_inputs = num_inputs
        self.inputs = [''] * num_inputs
        self.Out = ''

    def setInputs(self, inputs):
        if len(inputs) != self.num_inputs:
            print("Wrong number of inputs to MUX")
        else:
            self.inputs = inputs

    def getOutput(self, select):
        if select >= self.num_inputs or select < 0:
            print("Wrong select line to MUX")
        else:
            return self.inputs[select]
