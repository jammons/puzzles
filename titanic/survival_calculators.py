import numpy as np

class SurvivalCalculator:
    '''
    Calculate survival probability based on dead/alive counts
    '''
    def calc_survival(self, row):
        key = row[index]      
        if self.survive_table.has_key(key):
            key_data = self.survive_table[key]
            alive = key_data['alive']
            dead = key_data['dead']
            return alive/(alive+dead)

    def __init__(self, data, index):
        self.index = index
        self.survive_table = {}
        for entry in data:
            survived = int(entry[0])
            key = entry[self.index]
            if not key:
                continue
            if not survive_table.has_key(key):
                survive_table[key] = {'dead': 0, 'alive':0}
            survive_table[key][survived and 'alive' or 'dead'] += 1

    
class PClassCalculator(SurvivalCalculator):
    pass
class SexCalculator(SurvivalCalculator):
    pass
class AgeCalculator(SurvivalCalculator):
    pass
