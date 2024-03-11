from instr_dicts import *
from reg_dicts import *

def twos_comp(s: str):                                                                                              #fxn calculates twos complement, by first reversing 0s to 1s and 1s to 0s
    fin = ""; fina = ""
    for i in s:                                                                                         
        if i == '0': 
            fin += '1'
        else:
            fin += '0'
    
    for i in range(len(fin)-1,0,-1):                                                                                
        if fin[i] == '1':
            fina = '0' + fina
        else:
            fina = '1' + fina
            fina = fin[:i] + fina
            break
    print (fina)
    return fina
        

def convert_R(x : list, instr : str) -> str:                                                                        #takes a list 'x' as input with R-type instructions and opcode string. returns a string
    opcode, funct3, funct7 = R_[instr][0], R_[instr][1], R_[instr][2]                                               #takes opcode, funct3, funct7 from instr_dicts.py
    rd = format(int(regs[x[0]][1:]), '05b')                                                                             
    rs1 = format(int(regs[x[1]][1:]), '05b')
    rs2 = format(int(regs[x[2]][1:]), '05b')
    print("rd = ", rd)
    print("rs1 = ", rs1)
    print("rs2 = ", rs2)
    return (funct7+rs2+rs1+funct3+rd+opcode)
# print(convert_R(['t1', 's0', 'a0'], 'sub'))

def convert_I(x : list, instr : str) -> str:
    opcode, func3 = I_[instr][0], I_[instr][1]
    if instr == 'lw':
        rd = format(int(regs[x[0]][1:]),'05b')
        rs1 = format(int(regs[x[1].split('(')[1].rstrip(')')][1:]),'05b')
        imm = format(int(x[1].split('(')[0].strip()),'012b')
        if imm[0] == '-':
            imm = '0' + imm[1:]
            imm = twos_comp(imm)
        print("rd = ", rd)
        print("rs1 = ", rs1)
        print("offset = ", imm)
        
    else:
        rd = format(int(regs[x[0]][1:]),'05b')
        rs1 = format(int(regs[x[1]][1:]),'05b')
        imm = format(int(x[2]),'012b') #this is offset for jalr instruc
        if imm[0] == '-':
            imm = '0' + imm[1:]
            imm = twos_comp(imm)
        print("rd = ", rd)
        print("rs1 = ", rs1)
        print("offset = ", imm) if instr == 'jalr' else print("imm = ", imm)
    return imm+rs1+func3+rd+opcode
#print(convert_I(['ra','2(gp)'],'lw'))
#print(convert_I(['t1', 's0', '120'], 'addi'))
def convert_S(x : list, instr : str) -> str:
    opcode, funct3 = S_[instr][0], S_[instr][1]
    rs2 = format(int(regs[x[0]][1:]), '05b')
    rs1 = format(int(regs[x[1].split('(')[1].rstrip(')')][1:]),'05b')
    imm = format(int(x[1].split('(')[0].strip()),'012b')
    if imm[0] == '-':
        imm = "0" + imm[1:]
        imm = twos_comp(imm)
    print("rs2 = ", rs2)
    print("rs1 = ", rs1)
    print("offset = ", imm) 
    return imm[0:7]+rs2+rs1+funct3+imm[7:12]+opcode
#print(convert_S(['ra', '32(sp)'], 'sw'))

def convert_J(x : list, instr : str, pc: int) -> str:
    opcode,rd = J_[instr], x[0]
    rd = format(int(regs[rd][1:]),'05b')
    imm = format(int(x[1]),'021b')
    # if int(x[1])%4 != 0:
    #     raise Exception('Invalid offset value')
    # if int(x[1]) < 0:
    #     if -int(x[1]) > pc:
    #         raise Exception("Offset outside program range")
    if imm[0] == '-':
        imm = "0" + imm[1:]
        imm = twos_comp(imm)
    imm = imm[::-1]
    #imm = imm[19] + imm[9:0:-1] + imm[0]+imm[10] + imm[18:10:-1] #further inspection needed
    imm = imm[20] + imm[10:0:-1] +imm[11] + imm[19:11:-1]
    print("rd = ", rd)
    print("offset = ", x[1])
    return imm + rd + opcode


#U-type instructions
def convert_U(x: list, instr: str, pc: int) -> str:
    opcode = U_[instr]
    rd = format(int(regs[x[0]][1:]), '05b')          #converts destination register to binary
    imm = int(x[1])                                   #immediate value
    if imm < 0:
        imm = twos_comp(format(abs(imm), '032b'))    #computes two's complement for immediate < 0
    else:
        imm = format(imm, '032b')                   
    imm = imm[:20]
    print("rd =", rd)
    print("imm =", imm)
    print("opcode =", opcode)
    machine_code = imm + rd + opcode                 # Concatenate all parts to form the machine code
    print("machine_code =", machine_code)
    return machine_code

def convert_B(x : list, instr: str, pc: int, labledict : dict) -> str:
    opcode, funct3 = B_[instr][0], B_[instr][1]
    rs1 = format(int(regs[x[0]][1:]), '05b')
    rs2 = format(int(regs[x[1]][1:]), '05b') 
    print(labledict)
    if x[2] not in labledict and x[2].isdigit():
        imm = int(x[2])

    elif x[2] in labledict:
        lable_addr = labledict[x[2]]
        imm = (lable_addr-pc)*4

    else:
        raise Exception ("Invalid lable")
    print(imm)
    if imm < 0:
        imm = twos_comp(format(abs(imm), '013b'))    #computes two's complement for immediate < 0
    else:
        imm = format(imm, '013b')
    imm = imm[::-1]

    return imm[12]+imm[10:4:-1]+rs2+rs1+funct3+imm[4:0:-1]+imm[11]+opcode