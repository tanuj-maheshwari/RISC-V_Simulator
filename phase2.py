import os
import sys

print("\n\n\t\t\tRISC-V SIMULATOR\n")
input("Press enter key to start execution...")
print("\n")
knob1 = int(input("KNOB 1 :- Pipelining? (1 for yes, 0 for no) : "))
if knob1 == 0:
    os.system("python phase1.py " + sys.argv[1])

knob2 = int(input("KNOB 2 :- Data Forwarding? (1 for yes, 0 for no) : "))
if knob2 == 0:
    os.system("python phase2_nf.py " + sys.argv[1])
else:
    os.system("python phase2_f.py " + sys.argv[1])
