#!/usr/bin/env python

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 7/21/20

import argparse
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""""")
    required = parser.add_argument_group('required')
    required.add_argument('-m', '--melt_curve_data', required=True, nargs='*')
    parser.add_argument('-w', '--molecular_weight', default=13.5, help='molecular weight in kDa')
    parser.add_argument('-c', '--concentration', default=5, help='concentration in uM')
    args = parser.parse_args()
    start_temp = 25
    end_temp = 80
    step_size = 0.1
    molar_ellipticity_df = pd.DataFrame(index=np.linspace(start_temp, end_temp,
                                                          num=int((end_temp - start_temp)/step_size + 1)))
    conversion_dict = {
        'NbCov6': [13.6, 5/1000*13.6],
        'NbCov6tri': [41.5, 5/1000*41.5],
        'hmNbCov6': [13.6, 5/1000*13.6],
        'hmNbCov6tri': [41.5, 5/1000*41.5]
    }
    path_length = 0.1

    for i, melt_curve_file in enumerate(args.melt_curve_data):
        molar_ellipticity_list = []
        sample = melt_curve_file.split('_')[1]
        with open(melt_curve_file, 'r') as f:
            for line in f:
                if line[0].isnumeric():
                    temp, millidegree, voltage = line.split()
                    # convert millidegree to molar ellipticity
                    molar_ellipticity = float(millidegree) / 1000 * conversion_dict[sample][0] / (
                        10 * conversion_dict[sample][1] * path_length
                    )
                    molar_ellipticity_list.append(molar_ellipticity)
        molar_ellipticity_df[sample] = molar_ellipticity_list
    molar_ellipticity_df.index.name = 'Temperature'
    min_max_scaler = MinMaxScaler()
    fraction_folded_df = pd.DataFrame(min_max_scaler.fit_transform(molar_ellipticity_df),
                                      columns=molar_ellipticity_df.columns, index=molar_ellipticity_df.index)
    plotting_molar_ellipticity_df = pd.melt(molar_ellipticity_df.reset_index(), id_vars='Temperature',
                                            value_name='Molar Ellipticity', var_name='Sample')
    plotting_fraction_folded_df = pd.melt(fraction_folded_df.reset_index(), id_vars='Temperature', var_name='Sample',
                                          value_name='Fraction Folded')

    lp = sns.lineplot(x='Temperature', y='Molar Ellipticity', hue='Sample', data=plotting_molar_ellipticity_df)
    # lp.set_xlabel('Temperature')
    # lp.set_ylabel('Molar Ellipticity')
    sns.set_style("white")
    sns.set_style("ticks")
    sns.despine()
    fig = lp.get_figure()
    fig.savefig('nanobody_melt_molar_ellip_denoise.svg', format='svg')

    plt.clf()

    lp = sns.lineplot(x='Temperature', y='Fraction Folded', hue='Sample', data=plotting_fraction_folded_df)
    sns.set_style("white")
    sns.set_style("ticks")
    sns.despine()
    fig = lp.get_figure()
    fig.savefig('nanobody_melt_fraction_folded_denoise.svg', format='svg')
