from sim_.simulatorclass import simulator
import sys

inpf = sys.argv[1]
outpf = sys.argv[2]

pc = 0

with open(inpf,'r') as f:
    instruc = f.readlines()
    instruc = [i.strip('\n') for i in instruc]

sim = simulator(instruc,pc)
sim.execute(outpf)

with open(outpf,'w') as f:
    f.write("")

