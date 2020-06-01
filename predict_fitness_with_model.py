#!/usr/bin/env python

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 4/28/20

import argparse
import pandas as pd
import pickle

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""script to predict fitness class with a prebuilt model input as a 
    binary pickle file. model must have a .predict method""")
    required = parser.add_argument_group('required')
    required.add_argument('-d', '--data_csv', required=True,
                          help='csv file containing one-hot encoded CDRs for which fitness will be predict. '
                               'This data must not have been used to train the model')
    required.add_argument('-m', '--model_pickle_file', required=True,
                          help='pickle file containing trained model. This model must not have been trained on input '
                               'data')
    args = parser.parse_args()

    df = pd.read_csv(args.data_csv, index_col=0)
    # print(df)
    model = pickle.load(open(args.model_pickle_file, 'rb'))
    predicted_classes = model.predict(df)
    print(predicted_classes)
