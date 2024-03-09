from instr_dicts import *
from reg_dicts import *

def twos_comp(s: str):
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
    return fina
        

def convert_R(x : list, instr : str) -> str:
    opcode, funct3, funct7 = R_[instr][0], R_[instr][1], R_[instr][2]
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
    print("rs2 = ", rs2)
    print("rs1 = ", rs1)
    print("offset = ", imm) 
    return imm[-1:-7:-1]+rs2+rs1+funct3+imm[4:-1:-1]+opcode
print(convert_S(['t5', '200(gp)'], 'sw'))