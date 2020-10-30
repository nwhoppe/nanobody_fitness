#!/usr/bin/env python3

import argparse
import itertools
import pandas as pd
import seaborn as sns


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""script 
    to plot spr curves and write out maximal responses from binning experiment
    """)
    required = parser.add_argument_group('required')
    required.add_argument('-s', '--sensorgram_raw_binning_data', required=True, nargs='*',
                          help='raw txt from Biacore T100 machine of reference subtracted sensorgram with binning data')
    # parser.add_argument()
    args = parser.parse_args()
    composite_df = pd.DataFrame()
    class_one = ['Nb6', 'Nb11']
    class_two = ['Nb3', 'Nb17', 'Nb18']
    for raw_response_text_file in args.sensorgram_raw_binning_data:
        sensorgram_df = pd.read_csv(raw_response_text_file, sep='\t', encoding='iso-8859-1')
        sensorgram_df.columns = ['time', 'response']
        post_loading_df = sensorgram_df.loc[sensorgram_df['time'] > 225]
        association_df = post_loading_df.loc[post_loading_df['time'] < 400]
        #baseline subtract
        association_df = association_df.subtract([0, association_df.loc[association_df.index[0], 'response']],
                                                 axis='columns')

        first_injection, second_injection = raw_response_text_file.split('.')[0].split('_')[1:]
        association_df['first_injection'] = first_injection
        association_df['second_injection'] = second_injection

        if first_injection in class_one and second_injection in class_one:
            association_df['class'] = 'I'
        elif first_injection in class_two and second_injection in class_two:
            association_df['class'] = 'II'
        else:
            association_df['class'] = 'I and II'
        composite_df = composite_df.append(association_df)

    g = sns.FacetGrid(composite_df, row="first_injection", col="second_injection", hue='class',
                      margin_titles=True,)
    g.map(sns.lineplot, "time", "response",)

    # sensorgram_df.columns = list(itertools.product(association_times, ['time', 'response']))
    # sns.set()

    # line_plot = sns.lineplot(x=association_df.index, y=association_df.iloc[:, 0])
    # line_plot = sns.lineplot(data=association_df)
    # line_plot.set(xlabel='Time (s)', ylabel='Response (RU)')
    # sns.set_style("white")
    # sns.set_style("ticks")
    # sns.despine()
    # fig = g.get_figure()
    g.add_legend()
    g.savefig('20200720_binning_Nb3_Nb6_Nb11_Nb17_Nb18.svg', format='svg')
    # sns_plot.show()



