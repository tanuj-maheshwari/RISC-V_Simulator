import sys
from helper_functions.MC_to_dict import *
from logic_units.basic_logical_devices import *
from helper_functions.basic_functions import *
from decode_functions.immediate_genration import *
from decode_functions.identify_instruction import *
from logic_units.RegisterFile import *
from logic_units.ALU import *
from logic_units.IAG import *
from logic_units.MemoryWithoutCache import *
from logic_units.MemoryWithCache import *
from logic_units.ControlUnit import *
from logic_units.InterStageBuffers import *
from logic_units.BranchTargetBuffer import *
from logic_units.data_hazards_f import *


clock = 0
next_clock = 1
instruction = ''
instruction_code = 0
reg_file = RegisterFile()
rs1 = rs2 = rd = 0
alu = ALU()
iag = IAG()
memory = MemoryWithoutCache()
control = ControlUnit()
MuxRs1 = MUX(2)
RA = Register()
RB = Register()
MuxA = MUX(4)
MuxB = MUX(4)
MuxY = MUX(3)
MuxM = MUX(3)
MuxDrs1 = MUX(3)
MuxDrs2 = MUX(3)
RY = Register()
RZ = Register()
IR = Register()
immediate = Register()
step = 1
next_clock = -1
end_inst = end_exec = False

ISB_FD = InterStageBuffer(1)
ISB_DE = InterStageBuffer(2)
ISB_EM = InterStageBuffer(3)
ISB_MW = InterStageBuffer(4)
stall = 0
flush = False
btb = BTB()
hazard_unit = DataHazards()
RM = Register()

tot_inst = 0
CPI = 0
data_inst = 0
alu_inst = 0
control_inst = 0
tot_stalls = 0
tot_data_hazards = 0
tot_control_hazards = 0
tot_miss = 0
tot_hit = 0
data_stall = 0
control_stall = 0

knob3 = 0
knob4 = 0
knob5 = 0
knob6 = 0
knob5_PC = '1' * 32

log_file = open("output_dump/logs.txt", 'w')


def fetch():
    global IR, immediate, memory, iag, ISB_FD

    instruction = memory.Ins_Load(iag.getPC())

    IR.write(instruction)

    log_file.write("Fetch:\n")
    log_file.write("PC : " + '0x' + hex(int(iag.getPC(), 2))
                   [2:].zfill(8) + "\n")
    log_file.write("IR : " + '0x' + hex(int(IR.read(), 2))[2:].zfill(8) + "\n")

    return True, instruction, iag.getPC()


def decode():
    global MuxRs1, RA, RB, reg_file, MuxDrs1, MuxDrs2, ISB_FD, ISB_DE, control, end_inst, stall, flush, btb, hazard_unit, data_inst, control_inst, alu_inst, tot_stalls, tot_hit, tot_miss, tot_data_hazards, tot_control_hazards, data_stall, control_stall

    ISB_vals = ISB_FD.read()

    instruction = ISB_vals['instruction']
    PC_val = ISB_vals['PC_val']

    instruction_code = instruction_sr_no(instruction)
    control_signals = control.get_control_signals(instruction)

    if instruction_code == 0:
        end_inst = True
    elif instruction_code == 99:
        end_inst = True

    if end_inst is False:
        stall, temp_control = hazard_unit.get_stalls_forwarding_path(
            instruction, control_signals)
        control_signals = temp_control.copy()
    else:
        stall = 0

    if stall != 0:
        tot_stalls += stall
        data_stall += stall
        tot_data_hazards += 1
        return

    if instruction_code in (16, 17, 18, 20, 21, 22):
        data_inst += 1
    elif (instruction_code >= 1 and instruction_code <= 15) or instruction_code in (27, 28):
        alu_inst += 1
    elif instruction_code not in (0, 99):
        control_inst += 1

    immediate_val = ext_imm(instruction)

    MuxRs1.setInputs([instruction[12:17], instruction[20:25]])

    rs1 = int(MuxRs1.getOutput(control_signals['MuxRs1']), 2)
    rs2 = int(instruction[7:12], 2)
    rd = int(instruction[20:25], 2)

    MuxDrs1_inputs = [reg_file.read(
        rs1), ISB_EM.ALU_result.read(), ISB_MW.final_val.read()]
    MuxDrs2_inputs = [reg_file.read(
        rs2), ISB_EM.ALU_result.read(), ISB_MW.final_val.read()]
    MuxDrs1.setInputs(MuxDrs1_inputs)
    MuxDrs2.setInputs(MuxDrs2_inputs)

    RA.write(MuxDrs1.getOutput(control_signals['MuxDrs1']))
    RB.write(MuxDrs2.getOutput(control_signals['MuxDrs2']))

    log_file.write("Decode:\n")
    log_file.write("RA : " + '0x' + hex(int(RA.read(), 2))[2:].zfill(8) + "\n")
    log_file.write("RB : " + '0x' + hex(int(RB.read(), 2))[2:].zfill(8) + "\n")

    res = ''
    pred = ''
    if instruction_code in (19, 23, 24, 25, 26, 29):
        if instruction_code == 29:
            res = bin_add(PC_val, immediate_val)
        elif instruction_code == 19:
            res = bin_add(RA.read(), immediate_val)
        else:
            alu.ALU_compute(RA.read(), RB.read(), instruction_code)
            if alu.branch_control == 1:
                res = bin_add(PC_val, immediate_val)
            else:
                res = bin_add(PC_val, '0100')

        if btb.isjump_btb(FD_tuple[2]) or (btb.ispresent_btb(FD_tuple[2]) and FD_tuple[1][0] == '1'):
            pred = btb.target_from_btb(PC_val)
        else:
            pred = bin_add(PC_val, '0100')

        if res == pred:
            flush = False
            tot_hit += 1
        else:
            flush = True
            tot_miss += 1
            tot_stalls += 1
            control_stall += 1
            tot_control_hazards += 1

        if btb.ispresent_btb(PC_val) == False:
            if instruction_code == 29:
                btb.add_to_btb(PC_val, bin_add(PC_val, immediate_val), True)
            elif instruction_code == 19:
                btb.add_to_btb(PC_val, bin_add(RA.read(), immediate_val), True)
            else:
                btb.add_to_btb(PC_val, bin_add(PC_val, immediate_val))

    else:
        flush = False

    return True, control_signals, RA.read(), RB.read(), rd, ISB_vals['PC_val'], instruction_code, immediate_val, res


def execute():
    global alu, RZ, ISB_DE, ISB_EM, MuxA, MuxB, RM, ISB_MW

    ISB_vals = ISB_DE.read()
    instruction_code = ISB_vals['instruction_type']
    control_signals = ISB_vals['control_signals']
    rs1_val = ISB_vals['rs1_val']
    rs2_val = ISB_vals['rs2_val']

    MuxA_inputs = [rs1_val, ISB_vals['PC_val'],
                   ISB_EM.ALU_result.read(), ISB_MW.final_val.read()]
    MuxB_inputs = [rs2_val, ISB_vals['immediate_val'],
                   ISB_EM.ALU_result.read(), ISB_MW.final_val.read()]
    MuxA.setInputs(MuxA_inputs)
    MuxB.setInputs(MuxB_inputs)
    ALU_inp1 = MuxA.getOutput(control_signals['MuxA'])
    ALU_inp2 = MuxB.getOutput(control_signals['MuxB'])

    alu.ALU_compute(ALU_inp1, ALU_inp2, instruction_code)

    RZ.write(alu.Out)
    RM.write(ISB_MW.final_val.read())

    log_file.write("Execute:\n")
    log_file.write("RZ : " + '0x' + hex(int(RZ.read(), 2))[2:].zfill(8) + "\n")
    log_file.write("RM : " + '0x' + hex(int(RM.read(), 2))[2:].zfill(8) + "\n")

    return True, control_signals, RZ.read(), RM.read(), ISB_vals['rs2_val'], ISB_vals['rd'], ISB_vals['PC_val'], instruction_code


def memory_access():
    global memory, MuxY, RY, ISB_EM, ISB_MW, end_exec, MuxM

    ISB_vals = ISB_EM.read()
    instruction_code = ISB_vals['instruction_type']
    control_signals = ISB_vals['control_signals']
    ALU_result = ISB_vals['ALU_result']
    rs2_val = ISB_vals['rs2_val']
    RM_val = ISB_vals['RM_val']

    if instruction_code == 0:
        print("\n\nEnd of execution")
        end_exec = True
        return True, RY.read(), ISB_vals['rd'], instruction_code
    elif instruction_code == 99:
        print("\n\nWrong instruction")
        end_exec = True
        return True, RY.read(), ISB_vals['rd'], instruction_code

    MuxM_inputs = [rs2_val, ISB_MW.final_val.read(), RM_val]
    MuxM.setInputs(MuxM_inputs)

    memory.MDR.write(MuxM.getOutput(control_signals['MuxM']))
    memory.MAR.write(ALU_result)

    log_file.write("Memory Access:\n")
    log_file.write("MAR : " + '0x' +
                   hex(int(memory.MAR.read(), 2))[2:].zfill(8) + "\n")
    log_file.write("MDR : " + '0x' + hex(int(memory.MDR.read(), 2))
                   [2:].zfill(8) + " (before memory access)\n")

    if instruction_code in (16, 17, 18, 20, 21, 22):
        if instruction_code in (16, 17, 18):
            if instruction_code == 16:
                memory.Mem_read(1)
            elif instruction_code == 17:
                memory.Mem_read(2)
            else:
                memory.Mem_read(4)
        else:
            if instruction_code == 20:
                memory.Mem_write(1)
            elif instruction_code == 21:
                memory.Mem_write(4)
            else:
                memory.Mem_write(2)

    MuxY_inputs = [ALU_result, memory.MDR.read(), bin_add(
        ISB_vals['PC_val'], '0100')]
    MuxY.setInputs(MuxY_inputs)

    log_file.write("MDR : " + '0x' + hex(int(memory.MDR.read(), 2))
                   [2:].zfill(8) + " (after memory access)\n")

    RY.write(MuxY.getOutput(control_signals['MuxY']))

    return True, RY.read(), ISB_vals['rd'], instruction_code


def write_back():
    global reg_file, ISB_MW, tot_inst

    ISB_vals = ISB_MW.read()
    instruction_code = ISB_vals['instruction_type']
    rd = ISB_vals['rd']
    final_val = ISB_vals['final_val']

    if instruction_code < 20 or instruction_code > 26:
        reg_file.write(rd, final_val)

    tot_inst += 1


WR_first = True
FD_tuple = DE_tuple = EM_tuple = MW_tuple = ()
f_run = d_run = e_run = m_run = w_run = False
f_pause = False
step = 1

knob3 = int(input("KNOB 3 :- Show Reg file? (1 for yes, 0 for no) : "))
knob4 = int(input("KNOB 4 :- Show Pipeline Buffers? (1 for yes, 0 for no) : "))
knob5 = int(input(
    "KNOB 5 :- Show Pipeline Buffers for specific inst.? (inst no. for yes, 0 for no) : "))
knob6 = int(input("KNOB 6 :- Use Caches? (1 for yes, 0 for no) : "))

if knob6 != 0:
    memory = MemoryWithCache()
    i_csize = int(input("\nInstruction Cache Size (in Bytes):- "))
    i_bsize = int(input("Instruction Cache Block Size (in Bytes):- "))
    i_ways = int(input("Number of ways for I$:- "))

    d_csize = int(input("\nData Cache Size (in Bytes):- "))
    d_bsize = int(input("Data Cache Block Size (in Bytes):- "))
    d_ways = int(input("Number of ways for D$:- "))

    memory.inst_cache(i_csize, i_bsize, i_ways, d_csize, d_bsize, d_ways)

memory.Prog_Load(MC_to_dict(sys.argv[1]))

knob5_temp = False
knob5_temp2 = 0
if knob5 != 0:
    knob5_PC = extend_to_32_bits(bin((knob5 - 1) * 4)[2:], False)
    knob5_temp = False
    knob5_temp2 = 0

while True:
    log_file.write("\nClock cycle " + str(clock+1) + " :-\n")

    if ISB_MW.active_state:
        write_back()
        w_run = True
    else:
        w_run = False

    if end_inst is False and f_pause is False:
        FD_tuple = fetch()
        f_run = True
    else:
        f_run = False
        f_pause = False

    if ISB_FD.active_state:
        DE_tuple = decode()
        d_run = True
    else:
        d_run = False

    if ISB_DE.active_state:
        EM_tuple = execute()
        e_run = True
    else:
        e_run = False

    if ISB_EM.active_state:
        MW_tuple = memory_access()
        m_run = True
    else:
        m_run = False

    if w_run:
        log_file.write("Write Back:\n")
        log_file.write("RY : " + '0x' + hex(int(ISB_MW.final_val.read(), 2))
                       [2:].zfill(8) + "\n")
        log_file.write("Rd : " + str(ISB_MW.rd) + "\n")

    if step != 0 and clock >= next_clock and end_exec is False:
        step = -1
        while step == -1:
            print("\nEnter an integer according to your choice below :-")
            print("a) Enter 0 to run the code and skip to end")
            print("b) Enter 1 to step to next cycle")
            print("c) Enter -1 to inspect memory")
            print("d) Enter any other integer to skip that many clock cycles\n")
            step = int(input("Enter the number :- "))
            while step < -1:
                step = input("Entered choice was wrong, enter again :- ")
            if step == -1:
                memory.display_status()
        if step not in (-1, 0, 1):
            next_clock = clock + step

    clock += 1

    if stall != 0:
        stall -= 1
        ISB_DE.active_state = False
        if stall != 0:
            f_pause = True
            ISB_FD.active_state = False
            stall -= 1
    else:
        if flush:
            ISB_FD.flush(1)
            iag.run(extend_to_32_bits('0100'), 0, 0, DE_tuple[8])
            flush = False

        elif f_run:
            ISB_FD.update_FD(FD_tuple[0], FD_tuple[1], FD_tuple[2])

            if btb.isjump_btb(FD_tuple[2]) or (btb.ispresent_btb(FD_tuple[2]) and FD_tuple[1][0] == '1'):
                iag.run(extend_to_32_bits('0100'), 0, 0,
                        btb.target_from_btb(FD_tuple[2]))
            else:
                iag.run(extend_to_32_bits('0100'),
                        1, 0, extend_to_32_bits('0'))

        if d_run:
            ISB_DE.update_DE(DE_tuple[0], DE_tuple[1], DE_tuple[2], DE_tuple[3],
                             DE_tuple[4], DE_tuple[5], DE_tuple[6], DE_tuple[7])
        else:
            ISB_FD.active_state = True
            ISB_DE.active_state = False

    if e_run:
        ISB_EM.update_EM(EM_tuple[0], EM_tuple[1], EM_tuple[2], EM_tuple[3],
                         EM_tuple[4], EM_tuple[5], EM_tuple[6], EM_tuple[7])
    else:
        ISB_EM.active_state = False

    if m_run:
        ISB_MW.update_MW(MW_tuple[0], MW_tuple[1], MW_tuple[2], MW_tuple[3])
    else:
        ISB_MW.active_state = False

    if step != 0 and clock >= next_clock and knob3 == 1:
        print("\nRegister File status after clock cycle ", clock, " :-\n")
        reg_file.display_status()

    if step != 0 and clock >= next_clock and knob4 == 1:
        print("\nInter Stage Buffer values are as follows :-\n")
        print("F-D buffer :-" + str(ISB_FD.read()))
        print("D-E buffer :-" + str(ISB_DE.read()))
        print("E-M buffer :-" + str(ISB_EM.read()))
        print("M-W buffer :-" + str(ISB_MW.read()))

    if iag.getPC() == knob5_PC and knob4 == 0:
        knob5_temp = True

    if knob5_temp:
        knob5_temp = True
        print("\nInter Stage Buffer values are as follows :-\n")
        print("F-D buffer :-" + str(ISB_FD.read()))
        print("D-E buffer :-" + str(ISB_DE.read()))
        print("E-M buffer :-" + str(ISB_EM.read()))
        print("M-W buffer :-" + str(ISB_MW.read()))
        if ISB_EM.PC_val.read() == knob5_PC:
            knob5_temp2 = 2
            knob5_temp = False

    if knob5_temp2 != 0:
        if knob5_temp2 != 2:
            print("\nInter Stage Buffer values are as follows :-\n")
            print("F-D buffer :-" + str(ISB_FD.read()))
            print("D-E buffer :-" + str(ISB_DE.read()))
            print("E-M buffer :-" + str(ISB_EM.read()))
            print("M-W buffer :-" + str(ISB_MW.read()))
        knob5_temp2 -= 1

    if end_exec:
        break


print("\nFinal Register File status (total", clock,
      "clock cycles, NOT including terminating instruction writeback):- \n")
reg_file.display_status()
flag = 'y'
while flag == 'y' or flag == 'Y':
    flag = input("\n\nWant to inspect memory (y/n)? ")
    if flag == 'y' or flag == 'Y':
        memory.display_status()

tot_inst -= control_stall
alu_inst -= control_stall
CPI = clock/tot_inst


print("\n\nStats :\n")
print("Total cycles :-", clock)
print("Total instructions executed :-", tot_inst)
print("CPI :-", CPI)
print("Data Transfer instructions executed :-", data_inst)
print("ALU instructions executed :-", alu_inst)
print("Control instructions executed :-", control_inst)
print("Total Stalls (Stalls + Flushes) :-", tot_stalls)
print("Number of Data Hazards :-", tot_data_hazards)
print("Number of Control Hazards :-", tot_control_hazards)
print("Branch Mispredictions :-", tot_miss)
print("Stalls due to data hazards :-", data_stall)
print("Stalls due to control hazards :-", control_stall)
if knob6 != 0:
    print("\nI cache access :-", memory.I_access, "( all read )")
    print("I cache misses :-", memory.I_miss, "( all read )")
    print("D cache access :-", memory.D_read_access + memory.D_write_access,
          "(", memory.D_read_access, "read,", memory.D_write_access, "write )")
    print("D cache misses :-", memory.D_read_miss + memory.D_write_miss,
          "(", memory.D_read_miss, "read,", memory.D_write_miss, "write )")
