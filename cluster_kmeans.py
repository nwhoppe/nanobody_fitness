#!/usr/bin/env python

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 3/17/20

import argparse
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""script to cluster nanobody sequences using k-means
    and assess what fraction were correctly assigned""")
    required = parser.add_argument_group('required')
    required.add_argument('-d0', '--dataframe_csv0', required=True,
                          help='input dataframe csv from encode_one_hot_cdrs_from_fasta.')
    required.add_argument('-d1', '--dataframe_csv1', required=True,
                          help='input dataframe csv from encode_one_hot_cdrs_from_fasta.')
    parser.add_argument('-r', '--random_seed', type=int, default=0)
    args = parser.parse_args()
    df_class0 = pd.read_csv(args.dataframe_csv0, index_col=0)
    df_class0.loc[:, 'class'] = 0
    df_class1 = pd.read_csv(args.dataframe_csv1, index_col=0)
    df_class1.loc[:, 'class'] = 1

    df_both_classes = pd.concat([df_class0, df_class1], ignore_index=True)
    true_classes = df_both_classes.loc[:, 'class']
    df_both_classes.drop(columns=['class'], inplace=True)

    cluster_kmeans = KMeans(n_clusters=2, random_state=args.random_seed).fit(df_both_classes)
    cluster_true_df = pd.DataFrame(cluster_kmeans.labels_, columns=['cluster_labels'])
    cluster_true_df = pd.concat([cluster_true_df, true_classes], axis='columns')
    cluster_true_df.to_csv('clusters_kmeans_true_classes_output.csv')
    c_matrix = confusion_matrix(true_classes, cluster_kmeans.labels_)
    tn, fp, fn, tp = c_matrix.ravel()
    print("Confusion matrix:")
    print(c_matrix)
    print("True positive rate = {0}".format(float(tp)/(tp + fn)))
    print("False positive rate = {0}".format(float(fp)/(fp + tn)))
