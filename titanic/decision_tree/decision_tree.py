import math
from copy import copy
import os
import csv
import numpy as np

class DecisionTreeGen(object):

    def gen_subtree(self, data, attributes):
        # if entropy of data is = 0:
        # set value of 1 or 0 for node
        # elif attributes == []:
        # set_value of 1 or 0 for node
        # else:
        # determine next attribute
        # for each value of attribute: gen_subtree
        # return { value1: get_subtree(), value2: gen_subtree(), ... }

        '''
        { gender:
            { male: { 
                embarked: {
                    S: {...},
                    C: {...},
                    E: 1,
                }
            },
            { female: {...}
        }
        '''
        if len(data) == 0:
            return 0
        elif len(attributes) == 0:
            return self.pick_survival_val(data)
        entropy = self.calc_ent(data)
        if entropy ==  0:
            return int(data[0, self.train_column_mapping[self.target_attr]]) # they're all the same, so get the 0th

        next_attr = self.choose_next_attr(
            data,
            attributes
        )
        
        node = {}
        attr_copy = copy(attributes)
        attr_copy.remove(next_attr)
        for value in self.possible_values[next_attr]:
            data_subset = data[data[0::, self.train_column_mapping[next_attr]] == value]
            node[value] = self.gen_subtree(data_subset, attr_copy)
        return { next_attr: node }


    def choose_next_attr(self, data, attributes):
        ''' Use entropy calculation to determine the attribute with best predictive 
        value. '''
        def calc_gain(data, attribute):
            total = 0.0
            total += self.calc_ent(data)
            
            for value in self.possible_values[attribute]:
                matching_data = data[data[0::, self.train_column_mapping[attribute]] == value]
                if len(matching_data) == 0:
                    continue
                value_ent = self.calc_ent(matching_data)
                total -= ((float(len(matching_data))/len(data)) * value_ent)
            return total
        
        next_attr = (None, 0.0)
        for attribute in attributes:
            gain = calc_gain(data, attribute)
            if gain >= next_attr[1]:
                next_attr = (attribute, gain)
        return next_attr[0]


    def pick_survival_val(self, data):
        ''' Returns a 1 or 0 based on the more likely outcome for the given data set '''
        unique_vals = np.bincount(data[::, 0].astype(int))
        if len(unique_vals) == 1:
            # This must only contain [count] therefore 0 is only present
            return 0
        if unique_vals[0] > unique_vals[1]:
            return 0
        else:
            return 1


    def calc_ent(self, data):
        ''' Calculates the entropy of a set for a given target attribute. '''
        sum = 0.0
        for value in self.possible_values[self.target_attr]:
            # use numpy to figure out the number of entries matching this value
            total_count = len(data)
            val_num = len(data[data[0::, self.train_column_mapping[self.target_attr]] == value])
            prob = float(val_num)/total_count
            if prob == 0:
                continue
            sum += prob * math.log(prob, 2) # entropy definition
        return -sum

    def get_prediction(self, trained_tree, row, column_mapping):
        current_tree = trained_tree
        while True:
            attribute = current_tree.keys()[0] # should only be one
            row_value = row[column_mapping[attribute]]
            try:
                current_tree = current_tree[attribute][row_value]
            except KeyError:
                return 0 # this could be better,
                         # but if we can't categorize them, they're dead
            if current_tree in [1, 0]:
                return current_tree

    def check_vals(self, data, trained_tree):
        correct = 0
        incorrect = 0

        for row in data:
            prediction = self.get_prediction(
                trained_tree,
                row,
                self.train_column_mapping
            )
            actual = int(row[self.train_column_mapping[self.target_attr]])
            
            if prediction == actual:
                correct += 1
            else:
                incorrect += 1

        print "We predicted %s of %s correct" % (correct, (correct+incorrect))
        print "That's %s %%" % (float(correct)/(correct+incorrect))

    def write_test_csv(self, trained_tree):
        test_csv = csv.reader(
            open(os.path.join(self.project_root, 'data/test.csv'), 'rb')
        )
        # get a mapping of readable header names to column indexes
        headers = test_csv.next()
        test_column_mapping = {}
        for (header, index) in zip(headers, range(0, len(headers))):
            test_column_mapping[header] = index

        result_csv = csv.writer(
            open(os.path.join(self.project_root, 'results/decision_tree.csv'), 'wb')
        )

        for row in test_csv:
            prediction = self.get_prediction(trained_tree, row, test_column_mapping)
            row.insert(0, str(prediction))
            result_csv.writerow(row)

    def run(self):
        self.project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        train_csv = csv.reader(
            open(os.path.join(self.project_root, 'data/train.csv'), 'rb')
        )
        # get a mapping of readable header names to column indexes
        headers = train_csv.next()
        self.train_column_mapping = {}
        for (header, index) in zip(headers, range(0, len(headers))):
            self.train_column_mapping[header] = index

        data = []
        for row in train_csv:
            data.append(row)
        data = np.array(data)

        # Create a dictionary of possible values for a given attribute
        self.possible_values = {}
        for header, row_num in self.train_column_mapping.iteritems():
            self.possible_values[header] = set(data[::, row_num])

        self.target_attr = 'survived'

        trained_tree = self.gen_subtree(
            data,
            ['pclass', 'sex', 'embarked', 'sibsp', 'parch'],
        )

        self.write_test_csv(trained_tree)

if __name__ == '__main__':
    DecisionTreeGen().run()
