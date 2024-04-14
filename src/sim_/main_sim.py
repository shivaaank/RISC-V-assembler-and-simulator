from simulator import simulator

pc = 0

with open('src\sim_\sim_input.txt','r') as f:
    instruc = f.readlines()
    instruc = [i.strip('\n') for i in instruc]

with open('src\sim_\sim_output.txt','w') as f:
    f.write('')

sim = simulator(instruc,pc)
sim.execute()
