#!/usr/bin/env python

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 3/26/20

import argparse
import pickle
from datetime import datetime
from decision_tree_classify_one_hot_cdrs import split_dataframes_train_test, calculate_roc_stats
from sklearn.neural_network import MLPClassifier

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""use a neural net to classify one-hot encoded cdrs""")
    required = parser.add_argument_group('required')
    required.add_argument('-d0', '--dataframe_csv0', required=True,
                          help='input dataframe csv from encode_one_hot_cdrs_from_fasta.')
    required.add_argument('-d1', '--dataframe_csv1', required=True,
                          help='input dataframe csv from encode_one_hot_cdrs_from_fasta.')
    parser.add_argument('-t', '--test_size', type=float, default=0.2)
    args = parser.parse_args()

    print('start: splitting data for training')
    df_train, df_train_class, df_test, df_test_class = split_dataframes_train_test(
        args.dataframe_csv0, args.dataframe_csv1, args.test_size)

    print('start: training nn')
    neural_net_classifier = MLPClassifier(hidden_layer_sizes=(25,), verbose=True).fit(df_train, df_train_class)

    print('start: save and calc confusion')
    date_time_string = datetime.now().strftime('%Y%m%d_%H.%M')
    output_file_name = 'neural_network_classifier_{0}'.format(date_time_string)
    pickle.dump(neural_net_classifier, open('{0}.p'.format(output_file_name), 'wb'))
    print("Model saved to: {0}".format(output_file_name))

    if args.test_size > 0:
        print('start: predict on test data')
        predicted_classes = neural_net_classifier.predict(df_test)
        calculate_roc_stats(df_test_class, predicted_classes)

