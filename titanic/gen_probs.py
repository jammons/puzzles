import os
import csv as csv 
import survival_calculators as prob_gens
import numpy as np


def calc_passenger_survival(active_gens, data_row):
    ''' Takes a row and returns a survival boolean value '''
    predicted_survival = []
    for gen in active_gens:
        predicted_val = gen.calc_survival(data_row)
        if predicted_val is None:
            continue
        predicted_survival.append(predicted_val)
    averaged_survival = np.average(predicted_survival)
    survival_bool = bool(round(averaged_survival))
    return survival_bool

def test_against_training_sample(active_gens):
    ''' Runs all the active_gens against each passenger and determines what %
    we predicted correctly. '''
    (file, data) = open_data_set('train.csv') # yes, this is redundant, but I like
                                      # refreshing this value here.
    correct = 0
    for passenger_row in data:
        # See if we predict the correct value
        survival_bool = calc_passenger_survival(active_gens, passenger_row)

        if bool(int(passenger_row[0])) == survival_bool:
            correct += 1

    print "We predicted %s/%s correct. This is %s%%" % (
        correct, len(data), float(correct)/len(data)
    )


def calc_test_data(active_gens):
    (readfile, data) = open_data_set('test.csv')
    write_file = csv.writer(open('./survivors.csv', 'wb'))

    results = []
    for passenger_row in data:
        survival_bool = calc_passenger_survival(active_gens, passenger_row)
        results.append(survival_bool)

    project_root = os.path.abspath(os.path.dirname(__file__))
    #Open up the csv file in to a Python object
    csv_file_object = csv.reader(
        open(os.path.join(project_root, 'data/' + 'test.csv'), 'rb')
    ) 
    row_counter = 1
    csv_file_object.next()
    for row in csv_file_object:
        row.insert(0, int(results[row_counter]))
        write_file.writerow(row)
        row_counter += 1

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
    return (csv_file_object, data)


def main():
    (file, training_data) = open_data_set('train.csv')

    # String names of active probability generators
    active_gen_names = ['SexCalculator', 'PClassCalculator', 'EmbarkedCalculator']
    # class instances of generators
    active_gens = []

    for gen in active_gen_names:
        ''' Instantiate generators and run against training data set '''
        prob_gen_instance = getattr(prob_gens, gen)(training_data)
        active_gens.append(prob_gen_instance)

    # Test our results against actual training set values
    #test_against_training_sample(active_gens)

    # Calculate against test.csv data
    calc_test_data(active_gens)


if __name__ == '__main__':
    main()
