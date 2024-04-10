from simulator import simulator

pc = 0

with open('sim_input.txt','r') as f:
    instruc = f.readlines()
    instruc = [i.strip('\n') for i in instruc]

with open('sim_output.txt','w') as f:
    f.write('')

sim = simulator(instruc,pc)
sim.execute()
