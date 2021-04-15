# RISC-V ISA Simulator

> ## CS204 Course Project (Phase 1)

A RISC-V ISA Simulator written in python. Phase 1 implements a simple non-pipelined design with no memory-hierarchy.


## Team Members

|Name|Entry No.|
|----|---------|
|Tanuj Maheshwari|2019CSB1125|
|Aman Battan|2019EEB1139|
|Solanki Dhruv|2019CSB1122|
|Dhiresh Kumar Singh|2019CSB1255|
|Sudhanshu Kumar|2019CSB1123|


## Instructions to run

Open the terminal/command prompt at the location where the project files are stored, and run

```
    $python phase1.py instructions.mc
```


## Changing the machine code

To change the machine code, copy the machine code into the instructions.mc file, or write them in a new file and run (change `instructions.mc` to your file name in the command)

To choose from one of the examples in `tests` folder, say `InplaceSelectionSort.mc`, run

```
    $python phase1.py tests/InplaceSelectionSort.mc
```


## Input and Output format

### Input Format

A single .mc file, with the given format :-

    <PC> <space> <machine_code_of_instruction> [<space> <comments>]
    …
    <PC> <space> 0xFFFFFFFF [<space> <comment>]
    <blank_line>
    <Address> <space> <data_to_be_stored> [<space> <comments>]
    …

Comments can be included after each line

### Output Format

Specific instructions for output will be displayed on the terminal itself. There are four options for each instruction :-

1. Run the complete code and skip to the end
2. To step to the next instruction
3. Inspect the memory
4. Skip a certain number of clock cycles.

After each instruction, the status of register file will be shown.

### Register values after each stage

The register values after each of the five stage for all instructions will be dumped in `logs.txt` in `output_dump` folder after end of execution


## Implementation Details and I/O format

In depth implementation details and I/O examples can be found in `Design_Phase_1.pdf` in the `documentation` folder


## Individual Contribution

Tanuj Maheshwari - ALU, IAG, RegisterFile, datapath, ALU_utility_functions, debugging, test files

Aman Battan - Memory Unit, Control Unit, MC_to_dict, test files

Solanki Dhruv - datapath, identify_instruction, debugging, documentation

Dhiresh Kumar Singh - immediate_generation, debugging, documentation, test files

Sudhanshu Kumar - basic_functions, basic_logical_devices, datapath, documentation