from Adams.abz9.abz9 import Dataset
# from FT.ft10.ft10 import Dataset
import matplotlib.pyplot as plt
import numpy as np

dataset = Dataset()
op_data = np.array(dataset.op_data)

machines = [[] for _ in range(dataset.n_machine)]
machines_pt = [[] for _ in range(dataset.n_machine)]

for i in range(len(op_data)):
    for j in range(len(op_data[i])):
        # op_data[i][j][0] : machine
        m = op_data[i][j][0]
        machines[m].append(np.where(op_data[i,:,0]==m)) # 자신의 위치
        machines_pt[m].append(op_data[i][j][1])


plt.figure(figsize=(4,3))
for i in range(dataset.n_machine):
    for j in range(dataset.n_job):
        plt.scatter(i, machines[i][j], color='black', alpha = 0.2, s=(machines_pt[i][j]/8.))

plt.title(dataset.name+' Data Distribution')
plt.savefig('..\\'+dataset.path + dataset.name+'_Data_Distribution.png')
plt.show()
