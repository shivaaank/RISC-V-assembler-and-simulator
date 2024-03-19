from instr_dicts import *
from converters import *
import sys

# print(sys.argv)
inp_file = sys.argv[1]
out_file = sys.argv[2]
label_ = {}
virtual_hlt = ("beq zero,zero,0x00000000", "beq zero,zero,0", "beq,zero,zero,0")

def convert(x : list, instr : str, pc: int)-> str:        #senior function checking where the opcode exists.  
    if instr in R_:                                       #Accordingly it runs functions relevant to the type of instruction, R, I, S, J, U, B etc.
        return convert_R(x, instr)
    elif instr in I_:
        return convert_I(x, instr)
    elif instr in S_:
        return convert_S(x, instr)
    elif instr in J_:
        return convert_J(x, instr, label_, pc)
    elif instr in U_:
        return convert_U(x, instr, pc)
    elif instr in B_:
        return convert_B(x, instr, pc, label_)
    else:
        raise Exception ('{} is an invalid instruction'.format(instr))
        

def Parse(x : str, pc : int)-> str:                                     #function takes string 'x' and program counter pc as int. 
    #check if valid:
    # x = x.lstrip()
    #handle inline comments, replace , with space
    if "#" in x:
        pos = x.index("#")                                              #if there is a comment, sets index to position of # in str
        if pos != 0:                                #if position isn't first or last, replaces ',' by ' ' from 0 to position
            x = x[0:pos]
            print(x)
    
    # print(x)
    if (x[0] == "\n" or x[0] == "" or x[0] == "."):      #checks whether string is a comment or empty, in which case returns empty string
        return ''

    if x=="beq zero,zero,0x00000000" or x=="beq zero,zero,0" or x=="beq,zero,zero,0":         #checks if instruction is virtual halt
        #check if last line

            
        if pc==length-1:      
            return '00000000000000000000000001100011'                   #returns machine code for virtual halt, otherwise throws error suggesting that it is not last instruction
        else:
            raise Exception ('Virtual halt not last instruction')

    if pc==length-1 and (x!="beq zero,zero,0x00000000" or x!="beq,zero,zero,0" or x!="beq zero,zero,0"):                    #if program counter is equal to length of instructions, throw error for missing Virtual halt
        raise Exception ("missing virtual halt")

    
    x = x.replace(',', ' ')
    tokens = x.split(' ')   #[instruction, rd, rs1, ..]                #splits the str into tokens, for every space
    tokens = [i for i in tokens if i!='']
    instr = tokens[0]       #instruction                                #first element of tokens is the instruction 
    
    try:
        # print(len(tokens))
        output_line = convert(tokens[1:], instr, pc)                    #calls for the convert function in line 4 and returns the final output line
    except KeyError:
        raise Exception ("Invalid instruction or wrong register name")
    
    return output_line



#read and store input from file                                         #classic input
with open(inp_file) as f:
    inp_lines = [i.strip('\n').strip() for i in f]
inp_lines = [i for i in inp_lines if i != ''] #remove empty lines
inp_lines = [i for i in inp_lines if i.strip()[0]!="#"] #remove commented lines

#print(inp_lines)
count = 0

#first pass
for line in inp_lines:
    temp = line.replace(',', ' ')
    temp = temp.split(' ')
    if ':' in temp[0]:#label
        temp2 = temp[0].split(':')
        temp2 = [i for i in temp2 if i!='']
        temp = temp2 + temp[1:]           
        label_[temp[0]] = count 
        if temp[1:]==[] or (temp[1:][0].lstrip()[0]=="#"):
            inp_lines.pop(count)
                  
        else:
            inp_lines[count] = ','.join(temp[1:]).lstrip(',')
    count += 1
            
count = 0
print(inp_lines)
#print(label_)
#print(inp_lines)
length = len(inp_lines)
#second pass
with open(out_file, "w") as f:
    for line in inp_lines:
        #if not line=='':
            out_line = Parse(line, count)
            if out_line!='':
                print(f'Instruction {count+1}.')
                print(out_line)
                print('----------')
                f.write(out_line)
                f.write("\n")
                count+=1