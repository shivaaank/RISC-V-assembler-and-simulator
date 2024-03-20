from instr_dicts import *
from execute_func import *

def read(instruc):
    opcode = instruc[-1:-8:-1]
    
    opcode = opcode[::-1]
    if opcode == list(R_.values())[1][0]:
        x =parse(instruc,[7,12,17,20,25,32])
    elif opcode in [i[0] for i in I_.values()]:
        x =parse(instruc,[12,17,20,25,32])
        execute_I(x)
    elif opcode in [i for i in S_.values()]:
        x =parse(instruc,[7,12,17,20,25,32])
    elif opcode == list(B_.values())[1][0]:
        x=parse(instruc,[7,12,17,20,25,32])
    elif opcode in [i for i in U_.values()]:
        x=parse(instruc,[20,25,32])
    elif opcode in [i for i in J_.values()]:
        x=parse(instruc,[20,25,32])
    elif opcode in [i for i in bonus_.values()]:
        pass
    else:
        raise Exception (f"{opcode} is an invalid opcode")   
    

def parse(i, y):
    x = [i[y[j]:y[j+1]] for j in range(len(y)-1)]
    j = [i[:y[0]]]
    j.extend(x)
    return j
    

read('00000000001000011000000100010011')



