from instr_dicts import *
from converters import *

def convert(x : list, instr : str, pc: int)-> str:        #senior function checking where the opcode exists.  
    if instr in R_:                                       #Accordingly it runs functions relevant to the type of instruction, R, I, S, J, U, B etc.
        return convert_R(x, instr)
    elif instr in I_:
        return convert_I(x, instr)
    elif instr in S_:
        return convert_S(x, instr)
    elif instr in J_:
        return convert_J(x, instr, pc)
    else:
        raise Exception ('{} is an invalid instruction'.format(instr))
        

def Parse(x : str, pc : int)-> str:                                     #function takes string 'x' and program counter pc as int. 
    #check if valid:
    if (x[0] == "#" or x[0] == "\n" or x[0] == "" or x[0] == "."):      #checks whether string is a comment or empty, in which case returns empty string
        return ''

    if x=="beq zero,zero,0x00000000" or x == "beq zero,zero,0":         #checks if the string is beq instruction with zero operands
        #check if last line
        if pc==length:      
            return '00000000000000000000000001100011'                   #returns machine code for virtual halt, otherwise throws error suggesting that it is not last instruction
        else:
            raise Exception ('Virtual halt not last instruction')

    if pc==length and x!="beq zero,zero,0x00000000":                    #if program counter is equal to length of instructions, throw error for missing Virtual halt
        raise Exception ("missing virtual halt")

    #handle inline comments, replace , with space
    if "#" in x:
        pos = x.index("#")                                              #if there is a comment, sets index to position of # in str
        if pos != 0 and pos != len(x)-1:                                #if position isn't first or last, replaces ',' by ' ' from 0 to position
            x = x[0:pos].replace(',', ' ')
    else:
        x = x.replace(',', ' ') 
    

    tokens = x.split(' ')   #[instruction, rd, rs1, ..]                #splits the str into tokens, for every space
    
    if tokens[0][-1]==':' :#label           
        tokens = tokens[1:]
        if tokens == []:
            return ''

    instr = tokens[0]       #instruction                                #first element of tokens is the instruction 
    
    try:
        output_line = convert(tokens[1:], instr, pc)                    #calls for the convert function in line 4 and returns the final output line
    except KeyError:
        raise Exception ("Invalid instruction or wrong register name")
    
    return output_line



#read and store input from file                                         #classic input
with open("src\input.txt") as f:
    inp_lines = [i.strip('\n') for i in f]
inp_lines = [i for i in inp_lines if i != '']
length = len(inp_lines)
print(inp_lines)
count = 0

with open("src\output.txt", "w") as f:
    for line in inp_lines:
        #if not line=='':
            count+=1
            print(f'Instruction {count}.')
            out_line = Parse(line, count)
            print(out_line)
            print('----------')
            f.write(out_line)
            f.write("\n")