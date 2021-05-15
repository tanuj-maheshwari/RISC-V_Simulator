from logic_units.basic_logical_devices import Register


class InterStageBuffer:
    def __init__(self, type):
        self.active_state = False
        if type == 1:
            self.instruction = Register()
            self.PC_val = Register()
        if type in (2, 3):
            self.control_signals = {'MuxRs1': 0,
                                    'MuxA': 0, 'MuxB': 0, 'MuxY': 0, 'MuxPC': 1}
            self.PC_val = Register()
            self.rs2_val = Register()
        if type == 2:
            self.rs1_val = Register()
            self.immediate_val = Register()
        if type in (2, 3, 4):
            self.rd = 0
            self.instruction_type = 1
        if type == 3:
            self.ALU_result = Register()
            self.RM_val = Register()
        if type == 4:
            self.final_val = Register()

    def flush(self, type):
        if type == 1:
            self.instruction.write('00110011')
            self.PC_val.write('1')
        if type in (2, 3):
            self.control_signals = {'MuxRs1': 0,
                                    'MuxA': 0, 'MuxB': 0, 'MuxY': 0, 'MuxPC': 1}.copy()
            self.PC_val.write('1')
            self.rs2_val.write('0')
        if type == 2:
            self.rs1_val.write('0')
            self.immediate_val.write('0')
        if type in (2, 3, 4):
            self.rd = 0
            self.instruction_type = 1
        if type == 3:
            self.ALU_result.write('0')
            self.RM_val.write('0')
        if type == 4:
            self.final_val.write('0')

    def read(self):
        keys = self.__dict__.keys()
        vals = []
        for key in keys:
            if type(self.__dict__[key]) != Register:
                vals.append(self.__dict__[key])
            else:
                vals.append(self.__dict__[key].read())

        return dict(zip(keys, vals))

    def update_FD(self, active_state, instruction, PC_val):
        self.instruction.write(instruction)
        self.active_state = active_state
        self.PC_val.write(PC_val)

    def update_DE(self, active_state, control_signals, rs1_val, rs2_val, rd, PC_val, instruction_type, immediate_val):
        self.active_state = active_state
        self.control_signals = control_signals.copy()
        self.rs1_val.write(rs1_val)
        self.rs2_val.write(rs2_val)
        self.rd = rd
        self.PC_val.write(PC_val)
        self.instruction_type = instruction_type
        self.immediate_val.write(immediate_val)

    def update_EM(self, active_state, control_signals, ALU_result, RM_val, rs2_val, rd, PC_val, instruction_type):
        self.active_state = active_state
        self.control_signals = control_signals.copy()
        self.ALU_result.write(ALU_result)
        self.RM_val.write(RM_val)
        self.rs2_val.write(rs2_val)
        self.rd = rd
        self.PC_val.write(PC_val)
        self.instruction_type = instruction_type

    def update_MW(self, active_state, final_val, rd, instruction_type):
        self.active_state = active_state
        self.final_val.write(final_val)
        self.rd = rd
        self.instruction_type = instruction_type
