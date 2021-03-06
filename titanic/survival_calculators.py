'''
Base class for calculators for data columns
Column indices:
0-survival,1-pclass,2-name,3-sex,4-age,5-sibsp,6-parch,7-ticket,8-fare,9-cabin,10-embarked
'''
class SurvivalCalculator(object):
    '''
    Calculate survival probability based on dead/alive counts
    '''
    def calc_survival(self, row):
        #key = row[self.index-1]                 # Decrement index for test set
        key = row[self.index]      
        if self.survive_table.has_key(key):
            key_data = self.survive_table[key]
            alive = key_data['alive']
            dead = key_data['dead']
            return float(alive)/(alive+dead)

    '''
    Default __init__ method builds a hash based on keys and survival counts
    A useful starting point for any SurvivalCalculator
    '''
    def __init__(self, data, index):
        self.weight = 1.0
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

    def gen_weighted_prob(self, row):
        ''' Returns a weighed value for probability of survival '''
        calc_val = self.calc_survival(row)
        if calc_val is None:
            return None
        return self.weight * calc_val

    def __str__(self):
        return self.__class__.__name__

'''
Passenger class is a proxy for socio-economic status
There are only three possible values, so not much needs to be done here.
'''
class PClassCalculator(SurvivalCalculator):
    def __init__(self, data):
        super(PClassCalculator, self).__init__(data, 1)

'''
Passenger name might be an interesting area to research...later
'''
class NameCalculator(SurvivalCalculator):
    def __init__(self, data):
        super(NameCalculator, self).__init__(data, 2)

'''
Straightforward probability calculator based on sex
'''
class SexCalculator(SurvivalCalculator):
    def __init__(self, data):
        super(SexCalculator, self).__init__(data, 3)

'''
Probability based on age. Not all ages will be covered, so 
a function is in order.
'''
class AgeCalculator(SurvivalCalculator):
    
    def createBrackets(self):
        # We want the computer to determine the bracket boundaries for us

        
    def __init__(self, data):
        super(AgeCalculator, self).__init__(data, 4)


class SibSpCalculator(SurvivalCalculator):
    def __init__(self, data):
        super(SipSpCalculator, self).__init__(data, 5)


class ParChCalculator(SurvivalCalculator):
    def __init__(self, data):
        super(ParChCalculator, self).__init__(data, 6)


class TicketCalculator(SurvivalCalculator):
    def __init__(self, data):
        super(TicketCalculator, self).__init__(data, 7)


class FareCalculator(SurvivalCalculator):
    def __init__(self, data):
        super(FareCalculator, self).__init__(data, 8)


class CabinCalculator(SurvivalCalculator):
    def __init__(self, data):
        super(CabinCalculator, self).__init__(data, 9)


class EmbarkedCalculator(SurvivalCalculator):
    def __init__(self, data):
        super(EmbarkedCalculator, self).__init__(data, 10)


