#!/usr/bin/env python3

import argparse
import itertools
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""script 
    to plot spr curves and write out maximal responses from binning experiment
    """)
    required = parser.add_argument_group('required')
    required.add_argument('-s', '--sensorgram_raw_binning_data', required=True,
                          help='raw txt from Biacore T100 machine of reference subtracted sensorgram with binning data')
    # parser.add_argument()
    args = parser.parse_args()
    sensorgram_df = pd.read_csv(args.sensorgram_raw_binning_data, sep='\t', encoding='iso-8859-1', index_col=0)
    # sensorgram_df.columns = list(itertools.product(association_times, ['time', 'response']))
    sens_plot = sns.lineplot(x=sensorgram_df.index, y=sensorgram_df.iloc[:,0])
    fig = sens_plot.get_figure()
    fig.savefig('test.png')


