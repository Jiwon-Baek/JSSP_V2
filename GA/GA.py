from environment.Source import Source
from environment.Sink import Sink
from environment.Part import Job, Operation
from environment.Process import Process
from environment.Resource import Machine
from environment.Monitor import Monitor
from postprocessing.PostProcessing import *
from data import *
from visualization.Gantt import *
from visualization.GUI import GUI

import simpy



class Individual():
    def __init__(self, seq):
        self.seq = seq
        self.job_seq = self.get_repeatable()
        self.feasible_seq = self.get_feasible()
        self.machine_seq = self.get_machine_order()
        self.makespan = self.get_makespan(self.machine_seq)

    def get_repeatable(self):
        cumul = 0
        sequence_ = np.array(self.seq)
        for i in range(NUM_MACHINE):
            for j in range(NUM_OP):
                sequence_ = np.where((sequence_ >= cumul) &
                                     (sequence_ < cumul + NUM_MACHINE), i, sequence_)
            cumul += NUM_MACHINE
        sequence_ = sequence_.tolist()
        return sequence_

    def get_feasible(self):
        temp = 0
        cumul = 0
        sequence_ = np.array(self.seq)
        for i in range(NUM_MACHINE):
            idx = np.where((sequence_ >= cumul) & (sequence_ < cumul + NUM_MACHINE))[0]
            for j in range(NUM_OP):
                sequence_[idx[j]] = temp
                temp += 1
            cumul += NUM_MACHINE
        return sequence_

    def get_machine_order(self):
        m_list = []
        for num in self.feasible_seq:
            idx_i = num % NUM_OP
            idx_j = num // NUM_MACHINE
            m_list.append(op_data[idx_j][idx_i][0])
        m_list = np.array(m_list)

        m_order = []
        for num in range(NUM_MACHINE):
            idx = np.where((m_list == num))[0]
            job_order = [self.job_seq[o]for o in idx]
            m_order.append(job_order)
        return m_order

    def get_makespan(self, machine_order):
        env = simpy.Environment()
        monitor = Monitor(filepath)
        model = dict()
        for i in range(NUM_MACHINE):
            model['Source' + str(i)] = Source(env, 'Source' + str(i), model, monitor,
                                              part_type=i, IAT=IAT, num_parts=float('inf'))
            model['Process' + str(i)] = Process(env, 'Process' + str(i), model, monitor, machine_order[i],
                                                capacity=1, in_buffer=12, out_buffer=12)
            model['M' + str(i)] = Machine(env, i)
        model['Sink'] = Sink(env, monitor)

        # In case of the situation where termination of the simulation greatly affects the machine utilization time,
        # it is necessary to terminate all the process at (SIMUL_TIME -1) and add up the process time to all machines
        env.run(SIMUL_TIME)
        # monitor.save_event_tracer()
        # machine_log_ = machine_log(filepath)
        # gantt = Gantt(machine_log_, len(machine_log_), printmode=True, writemode=True)
        # gui = GUI(gantt)

        return model['Sink'].last_arrival




if __name__ == "__main__":
    NUM_ITERATION = 100
    # machine_order = [[] for i in range(NUM_ITERATION)]
    makespan = [0 for i in range(NUM_ITERATION)]
    # for i in range(NUM_ITERATION):
    #     for j in range(10):
    #         temp = np.random.permutation(10)
    #         machine_order[i].append(temp.tolist())
    popul = []
    for i in range(NUM_ITERATION):
        seq = np.random.permutation(100)
        individual = Individual(seq)
        # print(individual.machine_seq)
        popul.append(individual)

    for i in range(NUM_ITERATION):
        # popul[i].makespan = get_makespan(popul[i].machine_seq)
        # if i%10 == 0:
        #     print(str(i/NUM_ITERATION)+'% Completed')
        print(popul[i].makespan)
        makespan[i] = popul[i].makespan

    optimized_machine_order = np.argsort(makespan)[-50:].tolist()
    # optimized_machine_order = np.argsort(makespan)[-5:].tolist()
    optimized_makespan = []
    for i in optimized_machine_order:
        optimized_makespan.append(makespan[i])
    print("optimized makespan :", optimized_makespan)







