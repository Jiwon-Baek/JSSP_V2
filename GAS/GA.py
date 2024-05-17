# TODO
class GAEngine:
    def __init__(self, cfg, op_data, crossover=None, mutation=None, selection=None):
        self.cfg = cfg
        self.op_data = op_data
        self.crossover = crossover
        self.mutation = mutation
        self.selection = selection

    def evolve(self):
        pass


if "__main__" == __name__:
    from GAS.Crossover.PMX import PMXCrossover
    from GAS.Crossover.OX import OXCrossover
    from Config.Run_Config import Run_Config
    from Data.Dataset.Dataset import Dataset

    dataset = Dataset('test_1515.txt')
    cfg = Run_Config()

    ga1 = GAEngine(cfg, dataset.op_data, crossover="PMX", selection='Roulette')
    ga2 = GAEngine(cfg, dataset.op_data, crossover="OX", selection='Seed')
    ga3 = GAEngine(cfg, dataset.op_data, crossover="PMX", selection='Tournament')
    ga4 = GAEngine(cfg, dataset.op_data, crossover="OX", selection='Roulette')
