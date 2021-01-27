#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly
import plotly.express as px

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""plot ms data given input two column txt file and x axis bounds""")
    required = parser.add_argument_group('required')
    required.add_argument('-t', '--input_txt_file', required=True)
    parser.add_argument('-xmin', type=float)
    parser.add_argument('-xmax', type=float)

    args = parser.parse_args()

    ms_intensity_mz_df = pd.read_csv(args.input_txt_file, sep='\t', index_col=False, header=None)
    # ms_intensity_mz_df.index.name = 'Mass to charge ratio (m/z)'
    ms_intensity_mz_df.columns = ['Mass to charge ratio (m/z)', 'Intensity (AU)']
    if args.xmin and args.xmax:
        ms_intensity_mz_df = ms_intensity_mz_df[
            (ms_intensity_mz_df['Mass to charge ratio (m/z)'] >= args.xmin) &
            (ms_intensity_mz_df['Mass to charge ratio (m/z)'] <= args.xmax)
        ]
    elif args.xmin:
        ms_intensity_mz_df = ms_intensity_mz_df[ms_intensity_mz_df['Mass to charge ratio (m/z)'] >= args.xmin]
    elif args.xmax:
        ms_intensity_mz_df = ms_intensity_mz_df[ms_intensity_mz_df['Mass to charge ratio (m/z)'] <= args.xmax]

    fig = px.line(ms_intensity_mz_df, x='Mass to charge ratio (m/z)', y='Intensity (AU)')
    plotly.offline.plot(fig, filename='full_range.html')

    # lp = sns.lineplot(x='Mass to charge ratio (m/z)', y='Intensity (AU)', data=ms_intensity_mz_df)
    # lp.set_xlabel('Temperature')
    # lp.set_ylabel('Molar Ellipticity')
    # sns.set_style("white")
    # sns.set_style("ticks")
    # sns.despine()
    # fig = lp.get_figure()
    # fig.savefig('test_ms_plot.svg', format='svg')