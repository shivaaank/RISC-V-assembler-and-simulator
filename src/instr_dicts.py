#R-type (opcode,func3,func7)
R_ = {
    "add": ("0110011","000","0000000"),
    "sub": ("0110011","000","0100000"),
    "sll": ("0110011","001","0000000"),
    "slt": ("0110011","010","0000000"),
    "sltu": ("0110011","011","0000000"),
    "xor": ("0110011","100","0000000"),
    "srl": ("0110011","101","0000000"),
    "or": ("0110011","110","0000000"),
    "and": ("0110011","111","0000000")
}

#I-type (opcode, funct3)
I_ = {
    "lw": ("0000011", "010"),
    "addi": ("0010011", "000"),
    "sltiu": ("0010011", "011"),
    "jalr": ("1100111", "000"),
}

#S-type (opcode, funct3)
S_ = {
    "sw" : ("0100011", "010"),
}

#J-type (opcode)
J_ = {
    "jal" : ('1101111')
}

#U-type (opcode)
U_ = {
    "lui": ("0110111"),
    "auipc": ("0010111"),
}

#B-type (opcode, funct3)
B_ = {
  "beq": ("1100011", "000"), 
  "bne": ("1100011", "001"),  
  "blt": ("1100011", "100"),  
  "bge": ("1100011", "101"),  
  "bltu": ("1100011", "110"), 
  "bgeu": ("1100011", "111"), 
}
