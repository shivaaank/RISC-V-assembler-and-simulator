from instr_dicts import *
from converters import *

def convert(x : list, instr : str)-> str:
    if instr in R_:
        return convert_R(x, instr)
    elif instr in I_:
        return convert_I(x, instr)
    elif instr in S_:
        return convert_S(x, instr)
    elif instr in J_:
        return convert_J(x, instr)
    else:
        raise Exception ('{} is an invalid instruction'.format(instr))
        

def Parse(x : str)-> str:
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
    
    tokens = x.split(' ')   #[instruction, rd, rs1, ..]
    instr = tokens[0]       #instruction
    
    output_line = convert(tokens[1:], instr)
    
    return output_line



#read and store input from file
with open("src\input.txt") as f:
    inp_lines = [i.strip('\n') for i in f]

with open("src\output.txt", "w") as f:
    for line in inp_lines:
        out_line = Parse(line)
        print(out_line)
        f.write(out_line)
        f.write("\n")