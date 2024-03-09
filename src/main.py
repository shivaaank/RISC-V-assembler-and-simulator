from instr_dicts import *
from converters import *

def convert(x : list, instr : str, pc: int)-> str:
    if instr in R_:
        return convert_R(x, instr)
    elif instr in I_:
        return convert_I(x, instr)
    elif instr in S_:
        return convert_S(x, instr)
    elif instr in J_:
        return convert_J(x, instr, pc)
    else:
        raise Exception ('{} is an invalid instruction'.format(instr))
        

def Parse(x : str, pc : int)-> str:
    #check if valid:
    if (x[0] == "#" or x[0] == "\n" or x[0] == "" or x[0] == "."):
        return ''

    if x=="beq zero,zero,0x00000000" or x == "beq zero,zero,0":
        #check if last line
        if pc==length:
            return '00000000000000000000000001100011'
        else:
            raise Exception ('Virtual halt not last instruction')

    if pc==length and x!="beq zero,zero,0x00000000":
        raise Exception ("missing virtual halt")

    #handle inline comments, replace , with space
    if "#" in x:
        pos = x.index("#")
        if pos != 0 and pos != len(x)-1:
            x = x[0:pos].replace(',', ' ')
    else:
        x = x.replace(',', ' ')
    

    tokens = x.split(' ')   #[instruction, rd, rs1, ..]
    
    if tokens[0][-1]==':' :#label
        tokens = tokens[1:]
        if tokens == []:
            return ''

    instr = tokens[0]       #instruction
    
    try:
        output_line = convert(tokens[1:], instr, pc)
    except KeyError:
        raise Exception ("Invalid instruction or wrong register name")
    
    return output_line



#read and store input from file
with open("src\input.txt") as f:
    inp_lines = [i.strip('\n') for i in f]

length = len(inp_lines)
count = 0

with open("src\output.txt", "w") as f:
    for line in inp_lines:
        count+=1
        out_line = Parse(line, count)
        print(out_line)
        f.write(out_line)
        f.write("\n")