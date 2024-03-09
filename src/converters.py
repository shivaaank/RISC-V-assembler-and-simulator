from instr_dicts import *
from reg_dicts import *

def sext(binnum : str, l : int):
    while len(binnum)!=l:
        binnum = "0" + binnum
    return binnum
# print(sext(bin(10)[2:], 5))

def convert_R(x : list, instr : str) -> str:
    opcode, funct3, funct7 = R_[instr][0], R_[instr][1], R_[instr][2]
    rd = sext(bin(int(regs[x[0]][1:]))[2:], 5)
    rs1 = sext(bin(int(regs[x[1]][1:]))[2:], 5)
    rs2 = sext(bin(int(regs[x[2]][1:]))[2:], 5)
    print("rd = ", rd)
    print("rs1 = ", rs1)
    print("rs2 = ", rs2)
    return (funct7+rs2+rs1+funct3+rd+opcode)
# print(convert_R(['t1', 's0', 'a0'], 'sub'))
