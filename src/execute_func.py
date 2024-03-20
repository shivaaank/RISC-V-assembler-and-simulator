from instr_dicts import *
from reg_dicts import *

def execute_I(token):
    print('h')
    imm,rs1,rd = token[0],token[1],token[3]
    print(reg_vals[rd])
    if (token[4],token[2]) == I_['addi']:
        imm = format(int(imm),'032b')
        imm = list(imm)
        imm = [int(i) for i in imm]
        
        rs1 = reg_vals[rs1]
        reg_vals[rd] = [i+j for i,j in zip(imm,rs1)]
        print(reg_vals[rd])

        
