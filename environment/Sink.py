import simpy
from config import *
from .Monitor import *


# region Sink
class Sink(object):
    def __init__(self, env, monitor):
        self.env = env
        self.name = 'Sink'
        self.monitor = monitor

        # Sink를 통해 끝마친 Part의 갯수
        self.parts_rec = 0
        # 마지막 Part가 도착한 시간
        self.last_arrival = 0.0
        # self.finished = simpy.Event()

    # put function
    def put(self, part):
        self.parts_rec += 1
        self.last_arrival = self.env.now
        monitor_by_console(CONSOLE_MODE, self.env, part, OBJECT, "Completed on")
        self.monitor.record(self.env.now, self.name, machine=None,
                            part_name=part.name, event="Completed")

        if self.parts_rec == 10:
            self.last_arrival = self.env.now
            # print(str(self.env.now))
            # print(str(self.env.now)+'\tAll Parts Finished')


# endregion