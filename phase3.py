import os
import sys

print("\n\n\t\t\tRISC-V SIMULATOR\n")
input("Press enter key to start execution...")
print("\n")
knob1 = int(input("KNOB 1 :- Pipelining? (1 for yes, 0 for no) : "))
if knob1 == 0:
    os.system("python non_pipelined.py " + sys.argv[1])
    sys.exit()

knob2 = int(input("KNOB 2 :- Data Forwarding? (1 for yes, 0 for no) : "))
if knob2 == 0:
    os.system("python pipelined_without_forwarding.py " + sys.argv[1])
else:
    os.system("python pipelined_with_forwarding.py " + sys.argv[1])
