from instruc import *
#---------------DONT DELETE THIS FOR NOWwWWWWWWWWWWWWWWWWWWW--------------
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
            if reg_v >= 0:
                w+=prefix+format(reg_v,'032b') + ' '
                print(prefix+format(reg_v,'032b'),end = ' ')
            else:
                reg_v = 2**32 + reg_v
                w+=prefix+format(reg_v,'032b') + ' '
                print(prefix+format(reg_v,'032b'),end = ' ')
        w += '\n'
        with open('src\sim_\sim_output.txt','a') as f:
            f.write(w)
        print()
    def print_mem(self):
        prefixB, prefixH,w = '0b', '0x', ''
        for mem_k, mem_v in mem.items():
            w += prefixH+format(mem_k,'08x')+':'
            print(prefixH+format(mem_k,'08x')+':', end = '')
            if mem_v>=0: 
                w += prefixB+format(mem_v,'032b') + '\n'
                print(prefixB+format(mem_v,'032b'))

            else: 
                w += prefixB+format(mem_v+2**32,'032b') + '\n'
                print(prefixB+format(mem_v+2**32,'032b'))
        with open('src\sim_\sim_output.txt','a') as f:
            f.write(w)
        
    def execute(self):
        while self.instruc_list[self.pc//4] != '00000000000000000000000001100011':
            pointer = self.pc//4
            opcode = self.instruc_list[pointer][-7:] 
            ex = None
            if opcode == list(R_.values())[1][0]:
                ex = R_type(self.instruc_list[pointer], self.pc)
                
            elif opcode in [i[0] for i in I_.values()]:
                ex = I_type(self.instruc_list[pointer],self.pc)
            elif opcode == "0100011":
                ex = S_type(self.instruc_list[pointer], self.pc)
            elif opcode == list(B_.values())[1][0]:
                ex = B_type(self.instruc_list[pointer], self.pc)
            elif opcode in [i for i in U_.values()]:
                ex = U_type(self.instruc_list[pointer], self.pc)
            elif opcode in [i for i in J_.values()]:
                ex = J_type(self.instruc_list[pointer],self.pc) 
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
            # print(format(self.pc,'032b'))
        self.print_state()
        self.print_mem()
            
print('''0b00000000000000000000000000000100 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000100000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000'''=='''0b00000000000000000000000000000100 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000100000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000''')