import sys
from helper_functions.MC_to_dict import *
from logic_units.basic_logical_devices import *
from helper_functions.basic_functions import *
from decode_functions.immediate_genration import *
from logic_units.RegisterFile import *
from logic_units.ALU import *
from logic_units.IAG import *
from logic_units.MemoryWithoutCache import *
from logic_units.MemoryWithCache import *
from logic_units.ControlUnit import *


clock = 0
instruction = ''
instruction_code = 0
reg_file = RegisterFile()
rs1 = rs2 = rd = 0
alu = ALU()
iag = IAG()
memory = MemoryWithoutCache()
control = ControlUnit()
control_signals = {}
MuxRs1 = MUX(2)
RA = Register()
RB = Register()
MuxA = MUX(2)
MuxB = MUX(2)
MuxY = MUX(3)
RY = Register()
RZ = Register()
IR = Register()
immediate = Register()
step = 1
next_clock = -1

log_file = open("output_dump/logs.txt", 'w')


def fetch():
    global instruction, instruction_code, IR, control_signals, immediate, memory, control, iag, clock

    instruction = memory.Ins_Load(iag.getPC())
    instruction_code = instruction_sr_no(instruction)

    if instruction_code == 0:
        print("\n\nEnd of execution")
        clock += 1
        return True
    elif instruction_code == 99:
        print("\n\nWrong instruction")
        return True

    IR.write(instruction)

    log_file.write("Fetch:\n")
    log_file.write("PC : " + '0x' + hex(int(iag.getPC(), 2))
                   [2:].zfill(8) + "\n")
    log_file.write("IR : " + '0x' + hex(int(IR.read(), 2))[2:].zfill(8) + "\n")

    return False


def decode():
    global MuxRs1, instruction, control_signals, RA, RB, reg_file, MuxA, MuxB, iag, immediate, rs1, rs2, rd

    control_signals = control.get_control_signals(instruction)

    immediate.write(ext_imm(instruction))

    MuxRs1.setInputs([instruction[12:17], instruction[20:25]])

    rs1 = int(MuxRs1.getOutput(control_signals['MuxRs1']), 2)
    rs2 = int(instruction[7:12], 2)
    rd = int(instruction[20:25], 2)

    RA.write(reg_file.read(rs1))
    RB.write(reg_file.read(rs2))

    MuxA_inputs = [RA.read(), iag.getPC()]
    MuxB_inputs = [RB.read(), immediate.read()]
    MuxA.setInputs(MuxA_inputs)
    MuxB.setInputs(MuxB_inputs)

    log_file.write("Decode:\n")
    log_file.write("RA : " + '0x' + hex(int(RA.read(), 2))[2:].zfill(8) + "\n")
    log_file.write("RB : " + '0x' + hex(int(RB.read(), 2))[2:].zfill(8) + "\n")


def execute():
    global alu, MuxA, MuxB, control_signals, instruction_code, RZ, iag, immediate

    alu.ALU_compute(MuxA.getOutput(control_signals['MuxA']), MuxB.getOutput(
        control_signals['MuxB']), instruction_code)

    RZ.write(alu.Out)

    iag.run(immediate.read(),
            control_signals['MuxPC'], alu.branch_control, alu.Out)

    log_file.write("Execute:\n")
    log_file.write("RZ : " + '0x' + hex(int(RZ.read(), 2))[2:].zfill(8) + "\n")
    log_file.write("PC : " + '0x' + hex(int(iag.getPC(), 2))
                   [2:].zfill(8) + " (for next instruction)\n")


def memory_access():
    global memory, RB, RZ, instruction_code, MuxY, RY, control_signals, iag

    memory.MDR.write(RB.read())
    memory.MAR.write(RZ.read())

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

    MuxY_inputs = [RZ.read(), memory.MDR.read(), iag.PC_temp.read()]
    MuxY.setInputs(MuxY_inputs)

    log_file.write("MDR : " + '0x' + hex(int(memory.MDR.read(), 2))
                   [2:].zfill(8) + " (after memory access)\n")


def write_back():
    global instruction_code, reg_file, rd, RY, clock

    RY.write(MuxY.getOutput(control_signals['MuxY']))

    if instruction_code < 20 or instruction_code > 26:
        reg_file.write(rd, RY.read())

    clock += 1

    log_file.write("Write Back:\n")
    log_file.write("RY : " + '0x' + hex(int(RY.read(), 2))
                   [2:].zfill(8) + "\n\n")


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

while True:
    log_file.write("Clock cycle " + str(clock+1) + " :-\n")

    end = fetch()

    if step != 0 and clock >= next_clock:
        print("\nCurrent instruction :- " + '0x' +
              hex(int(instruction, 2))[2:].zfill(8), "(at PC : " + hex(int(iag.PC.read(), 2)) + ")", sep="")

        step = -1
        while step == -1:
            print("\nEnter an integer according to your choice below :-")
            print("a) Enter 0 to run the code and skip to end")
            print("b) Enter 1 to step to next instruction")
            print("c) Enter -1 to inspect memory")
            print("d) Enter any other integer to skip that many clock cycles\n")
            step = int(input("Enter the number :- "))
            while step < -1:
                step = input("Entered choice was wrong, enter again :- ")
            if step == -1:
                memory.display_status()
        if step not in (-1, 0, 1):
            next_clock = clock + step

    if end is True:
        log_file.write("End of instruction")
        print("\nFinal Register File status (total", clock,
              "clock cycles, including terminating instruction):- \n")
        reg_file.display_status()
        flag = 'y'
        while flag == 'y' or flag == 'Y':
            flag = input("\n\nWant to inspect memory (y/n)? ")
            if flag == 'y' or flag == 'Y':
                memory.display_status()

        if knob6 != 0:
            print("\nI cache access :-", memory.I_access, "( all read )")
            print("I cache misses :-", memory.I_miss, "( all read )")
            print("D cache access :-", memory.D_read_access + memory.D_write_access,
                  "(", memory.D_read_access, "read,", memory.D_write_access, "write )")
            print("D cache misses :-", memory.D_read_miss + memory.D_write_miss,
                  "(", memory.D_read_miss, "read,", memory.D_write_miss, "write )")

        sys.exit()

    decode()

    execute()

    memory_access()

    write_back()

    if step != 0 and clock >= next_clock:
        print("\nRegister File status after clock cycle ", clock, " :-\n")
        reg_file.display_status()
