#!/usr/bin/env python

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 9/20/20

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def parse_luminescence_data(input_txt_file, plate_mapping_df):
    # longform dataframe with columns: condition, well, stdev, avg_lum
    luminescence_df = pd.DataFrame(columns=['Condition', 'Well', 'Receptor', 'Luminescence (RLU)'])
    with open(input_txt_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # start grabbing data from each individual reading of the well denoted by time colon

            split_line = line.rstrip().split('\t')
            if split_line[0] and split_line[0][1] == ':':
                row_number = 0
                while len(split_line) >= 12:
                    split_line = line.rstrip().split('\t')
                    # last 12 numbers in line are readings from each column
                    row_lum_values = split_line[-12:]
                    for column_number in range(0, 12):
                        luminescence_reading = float(row_lum_values[column_number])
                        well_text = plate_mapping_df.loc[row_number, column_number]
                        if '+' in well_text:
                            split_well = well_text.split('+', 1)
                            receptor = well_text.split('+', 1)[0].strip()
                            condition = well_text.split('+', 1)[1].strip()
                        else:
                            receptor, condition = [well_text, 'vehicle']
                        luminescence_df = luminescence_df.append(
                            [{'Condition': condition,
                              'Receptor': receptor,
                              'Well': (row_number, column_number),
                              'Luminescence (RLU)': luminescence_reading
                              }],
                            ignore_index=True
                        )
                    row_number += 1
                    line = next(f)
                    split_line = line.rstrip().split('\t')

                #
    return luminescence_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""highly specific script for plotting plate reader data from the 
    taunton lab""")
    required = parser.add_argument_group('required')
    required.add_argument('-p', '--plate_map_csv', required=True, help='csv corresponding to 96 well plate map')
    required.add_argument('-i', '--input_txt_file', required=True, help='txt file from plate reader')
    args = parser.parse_args()

    plate_layout = pd.read_csv(args.plate_map_csv, header=None) #, header=range(1, 13), )
    luminescence_df_longform = parse_luminescence_data(args.input_txt_file, plate_layout)

    # focus on KOR
    # KOR_df = luminescence_df_longform[
    #     # (luminescence_df_longform.Condition != '1% extract') &
    #     # (luminescence_df_longform.Condition != '1% extract + 10 uM antagonist') &
    #     (luminescence_df_longform.Condition != '0.2% extract') &
    #     (luminescence_df_longform.Condition != '0.2% extract + 10 uM antagonist') &
    #     # (luminescence_df_longform.Condition != '50 nM agonist + 10 uM antagonist') &
    #     (luminescence_df_longform.Receptor != 'Gal1R') &
    #     (luminescence_df_longform.Receptor != 'HTR4')
    # ]
    KOR_df = luminescence_df_longform[
        (luminescence_df_longform.Receptor == 'HTR4') &
        (luminescence_df_longform.Condition == '1% extract')
    ]
    # KOR_v_df = KOR_df[KOR_df.condition == 'vehicle']
    sns.set_theme(style="whitegrid")
    # sns.set(rc={'figure.figsize': (11.7, 8.27)})
    ax = sns.barplot(x="Well", y="Luminescence (RLU)", data=KOR_df,)
                     # order=['Untransfected', 'HTR4', 'KOR', 'MOR', 'GPR85', 'GPR151'])
    # ax.set_xticklabels(ax.get_xticklabels(), fontsize=7)
    # fig = ax.get_figure()
    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    # plt.setp(ax.get_legend().get_texts(), fontsize='8')
    # plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig('20200919_HTR4_extract_by_well.svg', format='svg')
