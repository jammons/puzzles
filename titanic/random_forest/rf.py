#!/usr/bin/env python

import os
import pandas as pd
import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def clean_data(data):
    # Clean training data
    data.ix[data['sex']=='male', 'sex'] = 1
    data.ix[data['sex']=='female', 'sex'] = 0

    data.ix[data['age'].isnull(), 'age'] = data['age'].median()
     
    data.ix[data['embarked']=='S', 'embarked'] = 0
    data.ix[data['embarked']=='C', 'embarked'] = 1
    data.ix[data['embarked']=='Q', 'embarked'] = 2
    data.ix[data['embarked'].isnull(), 'embarked'] = data['embarked'].median()
    
def main():
    # Set the project dir
    project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    #read in the training file
    train_data = pd.read_csv(os.path.join(project_root, "data/train.csv"))
   
    # Create training and target arrays
    target = train_data['survived']
    train = train_data[['pclass', 'sex', 'age', 'sibsp', 'parch', 'embarked']]
   
    # Clean training data
    clean_data(train)

    #read in the test file
    realtest = pd.read_csv(os.path.join(project_root, "data/test.csv"))
    realtest = realtest[['pclass', 'sex', 'age', 'sibsp', 'parch', 'embarked']]
    clean_data(realtest)

    # random forest code
    rf = RandomForestClassifier(n_estimators=150, min_samples_split=2, n_jobs=-1)

    # fit the training data
    print('fitting the model')
    rf.fit(train, target)
    # run model against test data
    prediction = rf.predict(realtest)
        
    open_file_object = csv.writer(open(os.path.join(project_root,"results/rf.csv"), "wb"))
    test_file_object = csv.reader(open(os.path.join(project_root, "data/test.csv"), 'rb')) #Load in the csv file

    test_file_object.next()
    i = 0
    for row in test_file_object:
        row.insert(0,prediction[i].astype(np.uint8))
        open_file_object.writerow(row)
        i += 1

    print ('Random Forest Complete! You Rock! Submit random_forest_solution.csv to Kaggle')

if __name__=="__main__":
    main()
