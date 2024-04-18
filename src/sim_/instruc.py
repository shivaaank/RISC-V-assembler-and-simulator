from instr_dicts import *
from reg_dicts import reg_vals
from mem_location import mem
class Instr:
    def __init__(self,ins: str,pc:int) -> None:
        self.instr = ins
        #self.opcode = ins[-7:-1] + ins[-1]
        self.opcode=ins[-7:]
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
    @staticmethod
    def twoscomp(val:int, length:int = 32):
        final = 2**length  - val
        return format(final,f'0{length}b')
    

    
class I_type(Instr):
    def __init__(self,ins:str,pc:int) -> None:
        super().__init__(ins,pc)
        self.instr = self.parse(self.instr,[12,17,20,25,32])
        self.imm = self.instr[0] #signed or unsigned check
        self.rs1 = self.instr[1]
        self.rd = self.instr[3]
        self.comp = (self.opcode,self.instr[2],)
    def execute(self):
        print("i type")
        if self.comp == I_['lw']:
            print('lw')
            if self.imm[0] == '0': reg_vals[self.rd] = mem[int(self.imm,2) + reg_vals[self.rs1]]
            else: reg_vals[self.rd] = mem[-int(self.twoscomp(int(self.imm,2),12),2)+ reg_vals[self.rs1]]
            self.pc += 4

        elif self.comp == I_['addi']:
            print('addi')
            print('rd = ', self.rd)
            # print('rs = ', self.rs)
            sextimm = int(self.imm,2) if self.imm[0]=='0' else -int(self.twoscomp(int(self.imm,2),12),2)
            print('imm = ', sextimm)
            if self.imm[0] == '0': reg_vals[self.rd] = int(self.imm,2) + reg_vals[self.rs1]
            else: reg_vals[self.rd] = -int(self.twoscomp(int(self.imm,2),12),2) + reg_vals[self.rs1]
            self.pc += 4

        elif self.comp == I_['sltiu']:
            print('sltiu')
            reg_vals[self.rd] = 1 if int(self.imm,2) > reg_vals[self.rs1] else 0
            self.pc += 4

        elif self.comp == I_['jalr']:
            print('jalr')
            print('rd = ', self.rd)
            reg_vals[self.rd] = self.pc + 4
            # self.pc=(self.pc>>1)<<1
            if self.imm[0] == '0': self.pc = (reg_vals[self.rs1] + int(self.imm,2))& ~1
            else: self.pc = (reg_vals[self.rs1] - int(self.twoscomp(int(self.imm,2),12),2))& ~1
            if self.pc%2 != 0: self.pc -= 1
            if self.pc<0: 
                self.pc = 2**32 + self.pc
        # self.print_state() 

class R_type(Instr):
    def __init__(self,ins:str,pc:int) -> None:
        super().__init__(ins,pc)
        self.instr = self.parse(self.instr,[7,12,17,20,25,32])
        self.rs2 = self.instr[1] #signed or unsigned check
        self.rs1 = self.instr[2]
        self.rd = self.instr[4]
        self.comp = (self.opcode,self.instr[3],self.instr[0])
        #print(self.comp)
    def execute(self):
        if self.comp == R_['add']:
            print('add')
            print('rs1 = ', self.rs1)
            print('rs2 = ',self.rs2)
            print('rd = ',self.rd)
            reg_vals[self.rd] = reg_vals[self.rs1] + reg_vals[self.rs2]

        elif self.comp == R_['sub']:
            print('sub')
            print('rs1 = ', self.rs1)
            print('rs2 = ',self.rs2)
            print('rd = ',self.rd)
            # if self.rs1 == "00000": reg_vals[self.rd] = -reg_vals[self.rs2]
            reg_vals[self.rd] = reg_vals[self.rs1] - reg_vals[self.rs2]

        elif self.comp == R_['slt']:
            print('slt')
            print('rs1 = ', self.rs1)
            print('rs2 = ', self.rs2)
            reg_vals[self.rd] = 1 if reg_vals[self.rs1] < reg_vals[self.rs2] else 0

        elif self.comp == R_['sltu']:
            print('sltu')
            unsignedrs1 = 2**32 + reg_vals[self.rs1] if reg_vals[self.rs1] <0 else reg_vals[self.rs1]
            unsignedrs2 = 2**32 + reg_vals[self.rs2] if reg_vals[self.rs2] <0 else reg_vals[self.rs2]
            reg_vals[self.rd] = 1 if unsignedrs1 < unsignedrs2 else 0

        elif self.comp == R_['xor']:
            print('xor')
            reg_vals[self.rd] = reg_vals[self.rs1] ^ reg_vals[self.rs2]

        elif self.comp == R_['sll']:
            print('sll')
            unsignedrs1 = 2**32 + reg_vals[self.rs1] if reg_vals[self.rs1] <0 else reg_vals[self.rs1]
            reg_vals[self.rd] = unsignedrs1 << int('{:032b}'.format(reg_vals[self.rs2])[-5:],2)
            # reg_vals[self.rd] = reg_vals[self.rs1]

        elif self.comp == R_['srl']:
            print('srl')
            print('rs1 = ', reg_vals[self.rs1])
            unsignedrs1 = 2**32 + reg_vals[self.rs1] if reg_vals[self.rs1] <0 else reg_vals[self.rs1]
            print(int('{:032b}'.format(reg_vals[self.rs2])[-5:],2) )
            reg_vals[self.rd] = unsignedrs1 >> int('{:032b}'.format(reg_vals[self.rs2])[-5:],2) 
            # reg_vals[self.rd] = reg_vals[self.rs1]

        elif self.comp == R_['or']:
            print('or')
            reg_vals[self.rd] = reg_vals[self.rs1] | reg_vals[self.rs2]

        elif self.comp == R_['and']:
            print('and')
            reg_vals[self.rd] = reg_vals[self.rs1] & reg_vals[self.rs2]
        self.pc += 4


class S_type(Instr):
    def __init__(self,ins:str,pc:int) -> None:
        super().__init__(ins,pc)
        self.instr = self.parse(self.instr, [7,12,17,20,25,32])
        self.imm = self.instr[0]+self.instr[4]
        self.rs2 = self.instr[1]
        self.rs1 = self.instr[2]
    def execute(self):
        print('s type')
        sextimm = int(self.imm,2) if self.imm[0]=='0' else -int(self.twoscomp(int(self.imm,2),12),2) 
        mem[reg_vals[self.rs1]+sextimm] = reg_vals[self.rs2]
        self.pc+=4

class J_type(Instr):
    def __init__(self,ins:str,pc:int) -> None:
        super().__init__(ins,pc)
        self.instr=self.parse(self.instr,[20,25,32])
        self.imm = self.instr[0]
        self.rd=self.instr[1]
        #self.comp=(self.opcode,)
    def execute(self):
        print("j type")
        #a = (a >> 4) << 4 
        reg_vals[self.rd]=self.pc+4
        print('rd = ', self.rd, ' value at rd = ', reg_vals[self.rd])
        #self.rd=self.pc+4
        #imm = imm[::-1]
        #imm = imm[20] + imm[10:0:-1] +imm[11] + imm[19:11:-1]
        print('unscrambled imm = ', self.imm)
        self.imm = self.imm[10:0:-1] + self.imm[11] + self.imm[19:11:-1] + self.imm[0]
        self.imm=self.imm[::-1] + '0'
        # self.imm = self.imm[0] + self.imm[13::] + self.imm[12] + self.imm[1:12]
        # self.imm=self.imm[20]+self.imm[10:0:-1]+self.imm[11]+self.imm[19:11:-1]
        # self.imm[::-1]
        print('imm binary = ', self.imm)
        if self.imm[0] == '0':
            self.pc=self.pc+int(self.imm,2)
            print('imm = ', int(self.imm,2))
        else:
            self.pc=self.pc-int(self.twoscomp(int(self.imm,2),20),2)
            print('imm = ', -int(self.twoscomp(int(self.imm,2),20),2))
        # self.pc=(self.pc>>1)<<1

class U_type(Instr):
    def __init__(self,ins:str,pc:int) -> None:
        super().__init__(ins,pc)
        self.instr = self.parse(self.instr, [20,25,32])
        self.imm = self.instr[0]
        self.rd = self.instr[1]
        self.op = self.instr[2]
        print(self.instr)
        imm = self.imm + 12*'0'
        self.sextimm = int(imm,2) if imm[0]=='0' else -int(self.twoscomp(int(self.imm,2),32),2)
    def execute(self):
        print('u type')
        if self.op=='0110111': #lui
            reg_vals[self.rd] = self.sextimm
        else:
            reg_vals[self.rd] = self.pc+ self.sextimm
        self.pc+=4

class B_type(Instr):
    def __init__(self,ins:str,pc:int) -> None:
        super().__init__(ins,pc)
        self.instr = self.parse(self.instr, [7,12,17,20,25,32])
        self.funct3 = self.instr[3]
        self.rs1 = self.instr[2]
        self.rs2 = self.instr[1]
        print('unscrambled imm = ', self.instr[0]+self.instr[4])
        self.imm = self.instr[0]+self.instr[4]
        self.imm = self.imm[0]+self.imm[-1]+self.imm[1:11]
        # self.imm = self.imm[::-1]
        # self.imm = self.instr[0][0] + self.instr[4][-1] + self.instr[0][1:] + self.instr[4][0:5]
        self.imm += "0"
        print(len(self.imm))
        print('imm binary = ', self.imm)
        self.sextimm = int(self.imm,2) if self.imm[0]=='0' else -int(self.twoscomp(int(self.imm,2),13),2) 

    def execute(self):
        print('b type')
        print('sextimm = ', self.sextimm)
        if(self.funct3=='000'):
            if(reg_vals[self.rs1]==reg_vals[self.rs2]):
                self.pc = self.pc + self.sextimm
            else:
                self.pc+=4
        elif(self.funct3=='001'):
            print('bne')
            if(reg_vals[self.rs1]!=reg_vals[self.rs2]):
                self.pc = self.pc + self.sextimm 
            else:
                self.pc+=4
        elif(self.funct3=='100'):
            if(reg_vals[self.rs1]<reg_vals[self.rs2]):
               self.pc = self.pc + self.sextimm
            else:
                self.pc+=4
        elif(self.funct3=='101'):
            if(reg_vals[self.rs1]>=reg_vals[self.rs2]):
               self.pc = self.pc + self.sextimm
            else:
                self.pc+=4
        elif(self.funct3=='110'):
            unsignedrs1 = 2**32 + reg_vals[self.rs1] if reg_vals[self.rs1] <0 else reg_vals[self.rs1]
            unsignedrs2 = 2**32 + reg_vals[self.rs2] if reg_vals[self.rs2] <0 else reg_vals[self.rs2] 
            if(unsignedrs1<unsignedrs2):
               self.pc = self.pc + self.sextimm 
            else:
                self.pc+=4
        elif(self.funct3=='111'):
            unsignedrs1 = 2**32 + reg_vals[self.rs1] if reg_vals[self.rs1] <0 else reg_vals[self.rs1]
            unsignedrs2 = 2**32 + reg_vals[self.rs2] if reg_vals[self.rs2] <0 else reg_vals[self.rs2] 
            if(unsignedrs1>unsignedrs2):
               self.pc = self.pc + self.sextimm
            else:
                self.pc+=4

def twoscomp(val:int, length:int = 32):
        final = 2**length  - val
        return format(final,f'0{length}b') 

print(int(twoscomp(int('00000000000000010000'+12*'0',2),13),2))
# u = J_type('00000000000000000000100100110011', 1)
# print(len(u.imm))
# print(format(2**32 - int(Instr.twoscomp(int('111111111001',2),12),2),'032b'))
# # print(Instr.parse('11111111100101111000000011100111',[12,17,20,25,32]))
# a = I_type('00000000011101111000000011100111',0)
# a.execute()
# print(a.pc)