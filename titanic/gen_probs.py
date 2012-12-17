import os
import csv as csv 
import survival_calculators as prob_gens
import numpy as np


def open_data_set(name):
    ''' Opens a csv file and returns a numpy array with values from set. '''
    project_root = os.path.abspath(os.path.dirname(__file__))
    #Open up the csv file in to a Python object
    csv_file_object = csv.reader(
        open(os.path.join(project_root, 'data/' + name), 'rb')
    ) 
    csv_file_object.next()  # First line is the header
    data=[]
    for row in csv_file_object:
        data.append(row)
    data = np.array(data)
    return data

def weight_calcs(active_calcs):
    ''' Takes the list of active calculators and runs them against the training
    data to apply a more accurate weight for each calculator
    '''
    training_set = open_data_set('train.csv')
    alpha = 1 # the value to adjust the weighting on a successful/failed attempt

    # Go through for each data row and see if a given calculator is correct.
    # If it's not, decriment its weight by the distance it's off * alpha
    for passenger in training_set:
        survived = int(passenger[0])
 
        for calc in active_calcs:
            prob = calc.calc_survival(passenger)
            if not prob:
                continue # there's no value for this row, so skip it
            prediction = round(prob)
            
            # Adjust weight
            distance = np.abs(.5-prob)
            adjustment = alpha * distance
            # Determine direction of adjustment
            if prediction == survived:
                # increase weight
                calc.weight += adjustment
            else:
                calc.weight -= adjustment

def calc_passenger_survival(active_calcs, data_row):
    ''' Takes a row and returns a survival boolean value '''
    predicted_survival = [] # List of values from each calculator
    for gen in active_calcs:
        # Calculate probabilities for each calculator
        predicted_val = gen.calc_survival(data_row)
        if predicted_val is None:
            continue
        predicted_survival.append(predicted_val)

    # Average the values from all calculators
    averaged_survival = np.average(predicted_survival)

    # Convert the survival float into a 0 or 1 value
    survival_bool = bool(round(averaged_survival))
    return survival_bool

def test_against_training_sample(active_calcs):
    ''' Runs all the active_calcs against each passenger and determines what %
    we predicted correctly. '''
    data = open_data_set('train.csv') # yes, this is redundant, but I like
                                      # refreshing this value here.
    correct = 0
    for passenger_row in data:
        # See if we predict the correct value
        survival_bool = calc_passenger_survival(active_calcs, passenger_row)

        if bool(int(passenger_row[0])) == survival_bool:
            correct += 1

    print "We predicted %s/%s correct. This is %s%%" % (
        correct, len(data), float(correct)/len(data)
    )


def calc_test_data(active_calcs):
    data = open_data_set('test.csv')
    write_file = csv.writer(open('./survivors.csv', 'wb'))

    results = []
    for passenger_row in data:
        survival_bool = calc_passenger_survival(active_calcs, passenger_row)
        results.append(survival_bool)

    project_root = os.path.abspath(os.path.dirname(__file__))
    #Open up the csv file in to a Python object
    csv_file_object = csv.reader(
        open(os.path.join(project_root, 'data/' + 'test.csv'), 'rb')
    ) 
    row_counter = 0
    csv_file_object.next()
    for row in csv_file_object:
        row.insert(0, int(results[row_counter]))
        write_file.writerow(row)
        row_counter += 1



def main():
    training_data = open_data_set('train.csv')

    # String names of active probability generators
    active_gen_names = ['SexCalculator', 'PClassCalculator', 'EmbarkedCalculator']
    # class instances of generators
    active_calcs = []

    # Calculate probabilities for calculators
    for gen in active_gen_names:
        ''' Instantiate generators and run against training data set '''
        prob_gen_instance = getattr(prob_gens, gen)(training_data)
        active_calcs.append(prob_gen_instance)

    weight_calcs(active_calcs)
    
    weights = [calc.weight for calc in active_calcs]
    print weights

    # Test our results against actual training set values
    test_against_training_sample(active_calcs)

    # Calculate against test.csv data
    #calc_test_data(active_calcs)


if __name__ == '__main__':
    main()
