#!/usr/bin/env python3

import argparse
import pandas as pd
import seaborn as sns

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required')
    required.add_argument('-i', '--input_csvs', nargs='*', required=True)
    parser.add_argument('-xmin', type=int, default=0)
    parser.add_argument('-xmax', type=int, default=25)
    parser.add_argument('-n')
    args = parser.parse_args()
    plotting_df = pd.DataFrame()
    sns.set_context('talk')
    i = 0
    colors = ['dimgray', 'royalblue', 'firebrick', 'royalblue']
    # labels = ['GPR68-mGq', 'GPR68-mGq complex', 'KCTD12 and GPR85']
    for sec_csv in args.input_csvs:

        sec_df = pd.read_csv(sec_csv, header=1)
        # if sec_csv == args.input_csvs[1]:
        #     sec_df += 0.5
        lp = sns.lineplot(sec_df.iloc[:, 0], sec_df.iloc[:, 1], color=colors[i], linewidth=5)  # label=labels[i])
        i += 1
    sns.despine()
    lp.set(xlim=(args.xmin, args.xmax))
    # lp.set_ylim(top=50)
    # lp.set(ylim=(0, 250))
    lp.set_xlabel('Elution Volume (mL)')
    lp.set_ylabel('Absorbance at 280 nm (mAU)')

    fig = lp.get_figure()
    fig.tight_layout()
    if args.n:
        fig.savefig(args.n, format='svg')
    else:
        output_file = args.input_csvs[0].split('/')[-1].split('.')[0]
        fig.savefig('{0}.svg'.format(output_file), format='svg')

    # sns.despine()
    # lp.set_ylabel('Absorbance at 280 nm (mAU)')
    # lp.fill_between(sec_df.iloc[:, 0], sec_df.iloc[:, 1], alpha=0.5)
    # fig = lp.get_figure()
    # fig.savefig('GPR85_asec_trace.png', dpi=500)


    # input_csv = sys.argv[1]
    # # sec_df = pd.read_csv('/Users/Nick.Hoppe/google_drive/manglik_lab/ngc_fplc_nick/20191008_sec_nb80_humanized_scaffolds.csv', header=[0, 1])
    # for csv_file_name in sec_df.columns.levels[0]:
    #     legend_label = csv_file_name.split('_')[-1]
    #     if len(legend_label) == 1:
    #         legend_label = csv_file_name.split('_')[-2]
    #     volume_series = sec_df[csv_file_name, 'UV(280 nm)_volume']
    #     absorbance_series = sec_df[csv_file_name, 'UV(280 nm)_mAU']
    #     lp = sns.lineplot(volume_series, absorbance_series, label=legend_label, )


    # to fill under curve try
    # plt.fill_between(df.Date.values, df.Data.values)

