class SurvivalCalculator(object):
    '''
    Calculate survival probability based on dead/alive counts
    '''
    def calc_survival(self, row):
        key = row[self.index]      
        if self.survive_table.has_key(key):
            key_data = self.survive_table[key]
            alive = key_data['alive']
            dead = key_data['dead']
            return float(alive)/(alive+dead)


    def __init__(self, data, index):
        self.index = index
        self.survive_table = {}
        for entry in data:
            survived = int(entry[0])
            key = entry[self.index]
            if not key:
                continue
            if not self.survive_table.has_key(key):
                self.survive_table[key] = {'dead': 0, 'alive':0}
            self.survive_table[key][survived and 'alive' or 'dead'] += 1

    
class PClassCalculator(SurvivalCalculator):
    def __init__(self, data):
        super(SexCalculator, self).__init__(data, 1)


class SexCalculator(SurvivalCalculator):
    def __init__(self, data):
        super(SexCalculator, self).__init__(data, 3)

class EmbarkedCalculator(SurvivalCalculator):
    def __init__(self, data):
        super(EmbarkedCalculator, self).__init__(data, 10)



class AgeCalculator(SurvivalCalculator):
    pass
