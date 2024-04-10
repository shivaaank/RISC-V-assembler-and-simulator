from instr_dicts import *
from reg_dicts import reg_vals
class Instr:
    def __init__(self,ins: str,pc:int) -> None:
        self.instr = ins
        self.opcode = ins[-7:-1] + ins[-1]
        self.pc = pc

    @staticmethod
    def parse(i:str, y:list):
        x = [i[y[j]:y[j+1]] for j in range(len(y)-1)]
        j = [i[:y[0]]]
        j.extend(x)
        return j
    # def print_state(self): #remove function later(only for debugging)
    #     prefix = '0b'
    #     print(prefix+format(self.pc,'032b'),end = ' ')
    #     for reg_v in list(reg_vals.values()):
    #         print(prefix+format(reg_v,'032b'),end = ' ')
    #     print()
class I_type(Instr):
    def __init__(self,ins:str,pc:int) -> None:
        super().__init__(ins,pc)
        self.instr = self.parse(self.instr,[12,17,20,25,32])
        self.imm = self.instr[0] #signed or unsigned check
        self.rs1 = self.instr[1]
        self.rd = self.instr[3]
        self.comp = (self.opcode,self.instr[2],)
    def execute(self):
        if self.comp == I_['lw']:
            self.pc += 4
            pass #memory
        elif self.comp == I_['addi']:
            reg_vals[self.rd] += int(self.imm,2)
            self.pc += 4
        elif self.comp == I_['sltiu']:
            reg_vals[self.rd] = 1 if int(self.imm,2) > reg_vals[self.rs1] else 0
            self.pc += 4
        elif self.comp == I_['jalr']:
            reg_vals[self.rd] = self.pc + 4
            self.pc = reg_vals[self.rs1] + int(self.imm,2)
            if self.pc%2 != 0: self.pc -= 1
        # self.print_state() 

class R_type(Instr):
    def __init__(self,ins:str,pc:int) -> None:
        super().__init__(ins,pc)

class S_type(Instr):
    def __init__(self,ins:str,pc:int) -> None:
        super().__init__(ins,pc)

class J_type(Instr):
    def __init__(self,ins:str,pc:int) -> None:
        super().__init__(ins,pc)

class U_type(Instr):
    def __init__(self,ins:str,pc:int) -> None:
        super().__init__(ins,pc)

class B_type(Instr):
    def __init__(self,ins:str,pc:int) -> None:
        super().__init__(ins,pc)



