from typing import Any
from assembler import *

def Parse(x):
    #check if valid:
    if (x[0] == "#" or x[0] == "\n" or x[0] == "" or x[0] == "."):
        return ''
    #handle inline comments, replace , with space
    if "#" in x:
        pos = x.index("#")
        if pos != 0 and pos != len(x)-1:
            x = x[0:pos].replace(',', ' ')
    else:
        x = x.replace(',', ' ')
    
    tokens = x.split(' ')
    return tokens



#read and store input from file
with open("input.txt") as f:
    inp_lines = [i.strip('\n') for i in f]

with open("output.txt", "w") as f:
    for line in inp_lines:
        out_line = Parse(line)
        print(out_line)
        # f.writeline(out_line)