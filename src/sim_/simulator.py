from instruc import *

# def read(instruc):
#     opcode = instruc[-1:-8:-1]
    
#     opcode = opcode[::-1]
#     if opcode == list(R_.values())[1][0]:
#         x =parse(instruc,[7,12,17,20,25,32])
#     elif opcode in [i[0] for i in I_.values()]:
#         x =parse(instruc,[12,17,20,25,32])
#         execute_I(x)
#     elif opcode in [i for i in S_.values()]:
#         x =parse(instruc,[7,12,17,20,25,32])
#     elif opcode == list(B_.values())[1][0]:
#         x=parse(instruc,[7,12,17,20,25,32])
#     elif opcode in [i for i in U_.values()]:
#         x=parse(instruc,[20,25,32])
#     elif opcode in [i for i in J_.values()]:
#         x=parse(instruc,[20,25,32])
#     elif opcode in [i for i in bonus_.values()]:
#         pass
#     else:
#         raise Exception (f"{opcode} is an invalid opcode")   
    

# def parse(i, y):
#     x = [i[y[j]:y[j+1]] for j in range(len(y)-1)]
#     j = [i[:y[0]]]
#     j.extend(x)
#     return j
    

# read('00000000001000011000000100010011')


class simulator:
    def __init__(self,instruc:list,pc:int):
        self.instruc_list = instruc
        self.pc = pc
        #opcode diff for same type instruc asw
    # def pc_incr(self): #either pc increment b4 instr execution OR start pc = 4
    #     self.pc += 4
    def print_state(self):
        prefix = '0b'
        w = ''
        w+= prefix+format(self.pc,'032b')+' '
        print(prefix+format(self.pc,'032b'),end = ' ')
        for reg_v in list(reg_vals.values()):
            w+=prefix+format(reg_v,'032b') + ' '
            print(prefix+format(reg_v,'032b'),end = ' ')
        w += '\n'
        with open('src\sim_output.txt','a') as f:
            f.write(w)
        print()
    def execute(self):
        while self.instruc_list[self.pc//4] != '00000000000000000000000001100011':
            pointer = self.pc//4
            opcode = self.instruc_list[pointer][-7:-1] + self.instruc_list[pointer][-1]
            ex = 0
            if opcode == list(R_.values())[1][0]:
                ex = R_type(self.instruc_list[pointer], self.pc)
                ex.execute()
                self.pc = ex.pc
                self.print_state()
            elif opcode in [i[0] for i in I_.values()]:
                ex = I_type(self.instruc_list[pointer],self.pc)
            elif opcode in [i for i in S_.values()]:
                pass
            elif opcode == list(B_.values())[1][0]:
                pass
            elif opcode in [i for i in U_.values()]:
                pass
            elif opcode in [i for i in J_.values()]:
                pass
            elif opcode in [i for i in bonus_.values()]:
                pass
            else:
                raise Exception (f"{opcode} is an invalid opcode")
            ex.execute()
            self.pc = ex.pc
            if self.pc < 0:
                self.pc = 2**32 + self.pc
                self.print_state()
                break
            self.print_state()
        self.print_state()
            
