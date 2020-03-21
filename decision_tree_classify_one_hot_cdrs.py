#!/usr/bin/env python3

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 3/17/20

import argparse
import pandas as pd
import pickle
from sklearn import tree
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""use a decision tree to classify nanobody sequences as high or 
    low fitness. required input is one-hot encoded csv dataframes of CDR sequences""")
    required = parser.add_argument_group('required')
    required.add_argument('-d0', '--dataframe_csv0', required=True,
                          help='input dataframe csv from encode_one_hot_cdrs_from_fasta.')
    required.add_argument('-d1', '--dataframe_csv1', required=True,
                          help='input dataframe csv from encode_one_hot_cdrs_from_fasta.')
    args = parser.parse_args()
    df_class0 = pd.read_csv(args.dataframe_csv0, index_col=0)
    df_class0.loc[:, 'class'] = 0
    df_class1 = pd.read_csv(args.dataframe_csv1, index_col=0)
    df_class1.loc[:, 'class'] = 1
    # split data for each lass independently to keep the proportions of classes equal between train and test
    train_class0, test_class0 = train_test_split(df_class0, test_size=0.2)
    train_class1, test_class1 = train_test_split(df_class1, test_size=0.2)

    df_train = pd.concat([train_class0, train_class1])
    df_test = pd.concat([test_class0, test_class1])

    df_train_class = df_train.loc[:, 'class']
    df_test_class = df_test.loc[:, 'class']

    df_train.drop(columns=['class'], inplace=True)
    df_test.drop(columns=['class'], inplace=True)

    dt_classifier = tree.DecisionTreeClassifier().fit(df_train, df_train_class)
    tree.export_graphviz(dt_classifier, out_file='dt.dot', feature_names=list(df_train.columns.values),
                         class_names=['Low', 'High'], rounded=True, filled=True)
    predicted_classes = dt_classifier.predict(df_test)
    # r_squared = dt_classifier.score(df_test, df_test_class)
    # pickle.dump(dt_classifier, open('dt_classifier.p', 'wb'))
    tn, fp, fn, tp = confusion_matrix(df_test, predicted_classes).ravel()
    print("True positive rate = {0}".format(float(tp)/sum(tp + fn)))
    print("False positive rate = {0}".format(float(fp)/sum(fp + tn)))
    # print('score: {0}'.format(r_squared))
