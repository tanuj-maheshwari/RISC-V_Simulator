# RISC-V ISA Simulator

> ## CS204 Course Project (Phase 2)

A RISC-V ISA Simulator written in python. Phase 2 implements a pipelined datapath with data forwarding paths.


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
$python phase2.py instructions.mc
```


## Changing the machine code

To change the machine code, copy the machine code into the instructions.mc file, or write them in a new file and run (change `instructions.mc` to your file name in the command)

To choose from one of the examples in `tests` folder, say `InplaceSelectionSort.mc`, run

```
$python phase2.py tests/InplaceSelectionSort.mc
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

First you can choose from 5 options (knobs) :-

1. Pipelined or Non-Pipelined
2. Data Forwrding or only stalls
3. Display Reg file or not
4. Display InterStageBuffers or not
5. Display ISB for specific instruction

During execution, there are four options for each clock cycle :-

1. Run the complete code and skip to the end
2. To step to the next clock cycle
3. Inspect the memory
4. Skip a certain number of clock cycles

After each cycle, the status of register file and ISB will be shown (if knobs are set)

### Register values after each stage

The register values after each of the five stage for all cycles will be dumped in `logs.txt` in `output_dump` folder after end of execution. Note that details for only those stages are written which run during that cycle.


## Implementation Details and I/O format

In depth implementation details and I/O examples can be found in `Design_Phase_2.pdf` in the `documentation` folder


## Individual Contribution

Tanuj Maheshwari - datapath (forwarding and non-forwarding), hazard detection, debugging

Aman Battan - documentation

Solanki Dhruv - BranchTargetBuffer, documentation

Dhiresh Kumar Singh - hazard detection (forwarding), debugging

Sudhanshu Kumar - debugging