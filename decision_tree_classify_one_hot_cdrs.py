#!/usr/bin/env python3

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 3/17/20

import argparse
from datetime import datetime
import pandas as pd
import pickle
from sklearn import tree
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split


def split_dataframes_train_test(class0_dataframe_csv, class1_dataframe_csv, test_size):
    """split data for each cass independently to keep the proportions of classes equal between train and test"""
    class0 = pd.read_csv(class0_dataframe_csv, index_col=0)
    class0.loc[:, 'class'] = 0
    class1 = pd.read_csv(class1_dataframe_csv, index_col=0)
    class1.loc[:, 'class'] = 1

    if test_size > 0:
        train_class0, test_class0 = train_test_split(class0, test_size=test_size)
        train_class1, test_class1 = train_test_split(class1, test_size=test_size)
        train = pd.concat([train_class0, train_class1])
        test = pd.concat([test_class0, test_class1])
        test_true_class = test.loc[:, 'class']
        test.drop(columns=['class'], inplace=True)
    else:
        train = pd.concat([class0, class1])
        test = pd.DataFrame()
        test_true_class = pd.DataFrame()
    train_true_class = train.loc[:, 'class']
    train.drop(columns=['class'], inplace=True)

    # make sure counts equal fasta files
    print('class0 count: {0}'.format(class0.shape))
    print('class1 count: {0}'.format(class1.shape))
    print('training set size: {0}'.format(train.shape))
    print('test set size: {0}'.format(test.shape))

    return train, train_true_class, test, test_true_class


def calculate_roc_stats(true_classes, predicted_classes):
    c_matrix = confusion_matrix(true_classes, predicted_classes)
    tn, fp, fn, tp = c_matrix.ravel()
    print('Confusion matrix:')
    print(c_matrix)
    print("True positive rate = {0}".format(float(tp)/(tp + fn)))
    print("False positive rate = {0}".format(float(fp)/(fp + tn)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""use a decision tree to classify nanobody sequences as high or 
    low fitness. required input is one-hot encoded csv dataframes of CDR sequences""")
    required = parser.add_argument_group('required')
    required.add_argument('-d0', '--dataframe_csv0', required=True,
                          help='input dataframe csv from encode_one_hot_cdrs_from_fasta.')
    required.add_argument('-d1', '--dataframe_csv1', required=True,
                          help='input dataframe csv from encode_one_hot_cdrs_from_fasta.')
    parser.add_argument('-lm', '--min_samples_leaf', type=int, default=1)
    parser.add_argument('-m', '--max_depth', type=int, default=None)
    # parser.add_argument('-r', '--random_seed', type=int, default=0) # doesnt make sense to have this with random split
    parser.add_argument('-t', '--test_size', type=float, default=0.2)

    args = parser.parse_args()

    df_train, df_train_class, df_test, df_test_class = split_dataframes_train_test(
        args.dataframe_csv0, args.dataframe_csv1, args.test_size)
    # seed_int = args.random_seed
    depth = args.max_depth
    leaf_min = args.min_samples_leaf
    date_time_string = datetime.now().strftime('%Y%m%d_%H.%M.%S')
    output_file_name = 'decision_tree_model_depth{0}_leaf_min{1}_{2}'.format(depth, leaf_min, date_time_string)

    dt_classifier = tree.DecisionTreeClassifier(max_depth=depth, min_samples_leaf=leaf_min).fit(df_train, df_train_class)

    tree.export_graphviz(dt_classifier, out_file='{0}.dot'.format(output_file_name), feature_names=list(
        df_train.columns.values),
                         class_names=['Low', 'High'], rounded=True, filled=True)
    pickle.dump(dt_classifier, open('{0}.p'.format(output_file_name), 'wb'))
    print("Model saved to: {0}".format(output_file_name))

    if args.test_size > 0:
        predicted_classes = dt_classifier.predict(df_test)
        calculate_roc_stats(df_test_class, predicted_classes)

    print(dt_classifier.feature_importances_)
