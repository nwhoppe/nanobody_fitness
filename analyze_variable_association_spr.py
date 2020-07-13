#!/usr/bin/env python3

import argparse
import itertools
import pandas as pd


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""script 
    align dissociation phase
    normalize max at start of dissociation
    keep zero zero
    fit single exponential with rate constant constrained across samples
    plot raw curves - # do last
    """)
    required = parser.add_argument_group('required')
    required.add_argument('-s', '--sensorgram_raw_data', required=True, nargs='*',
                          help='raw txt from Biacore T100 machine of reference subtracted sensorgram')
    parser.add_argument()
    args = parser.parse_args()

    # notes on structure of data file
    # cycle number is unfortunately the header and not time, so going to manually assign
    # columns alternate x and y; x is time and 0 starts association
    # annoying there is not just one time column
    # time columns start about 60 secs before association (-60 sec). going to max(time columns first entry)
    # check that all other times align and have index be time
    # how to handle replicates - same df? or separate?
    association_times = [5, 10, 20, 40, 60, 120, 180, 240, 300, 420, 540]

    sensorgram_df_list = []
    dissociation_df_list = []
    for raw_sensorgram_data_file in args.s:
        # keep original data in list
        sensorgram_df = pd.read_csv(raw_sensorgram_data_file, sep='\t', encoding='iso-8859-1')
        # sensorgram_df.columns = list(itertools.product(association_times, ['time', 'response']))
        sensorgram_df_list.append(sensorgram_df)

        # extract just dissociation curves
        dissociation_df = pd.DataFrame()
        column_iter = iter(sensorgram_df.columns)
        counter = 0
        for column in column_iter:
            # columns are paired with time then response
            column_x = column
            column_y = next(column_iter)
            sub_df = sensorgram_df[[column, next(column_iter)]]
            # subtract association time from time axis - make 0 point be end of association
            sub_df = sub_df.sub([association_times[counter], 0], axis='columns')
            sub_df.set_index(round(column_x, 2), inplace=True)
            counter += 1
