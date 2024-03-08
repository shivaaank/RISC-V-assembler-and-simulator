from assembler import *

#read and store input from file
with open("input.txt") as f:
    inp_lines = [i.strip('\n') for i in f]

with open("output.txt", "w") as f:
    for line in inp_lines:
        out_line = Parse(line)
        f.writeline(out_line)