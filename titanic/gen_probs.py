import os
import csv as csv 
import probability_generators as prob_gens
import numpy as np


def test_against_training_sample(active_gens):
    ''' Runs all the active_gens against each passenger and determines what %
    we predicted correctly. '''
    data = open_data_set('train.csv') # yes, this is redundant, but I like
                                      # refreshing this value here.
    correct = 0
    for passenger_row in data:
        # See if we predict the correct value
        predicted_survival = []
        for gen in active_gens:
            predicted_survival.append(gen.calc_survival(passenger_row))
        averaged_survival = np.average(predicted_survival)
        survival_bool = bool(round(averaged_survival))

        if bool(passenger_row[0]) == survival_bool:
            correct += 1

    print "We predicted %s/%s correct. This is %s%" % (
        correct, len(data), float(correct)/len(data)
    )


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


def main():
    training_data = open_data_set('train.csv')

    active_gen_names = [] # String names of active probability generators
    active_gens = [] # class instances of generators

    for gen in active_gen_names:
        ''' Instantiate generators and run against training data set '''
        prob_gen_instance = getattr(prob_gens, gen)(training_data)
        active_gens.append(prob_gen_instance)

    # Test our results against actual training set values
    test_against_training_sample(active_gens)

    # Later: Calculate against test.csv data

if __name__ == '__main__':
    main()
