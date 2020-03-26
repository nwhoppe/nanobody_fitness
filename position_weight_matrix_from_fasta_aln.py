#!/usr/bin/env python

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 3/22/20

import argparse
import itertools
import numpy as np
import pandas as pd
from encode_one_hot_cdrs_from_fasta import parse_identifier_sequence_from_fasta, parse_cdrs_from_seq

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""""")
    required = parser.add_argument_group('required')
    required.add_argument('-f', '--fasta', required=True)
    args = parser.parse_args()
    id_seq_dict = parse_identifier_sequence_from_fasta(args.fasta, check_cdrs=False)

    # initialize dataframe
    aa_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    cdr_df_columns = []
    cdr_length_limits = {1: [7], 2: [13], 3: [25]}
    for cdr_number, cdr_length_list in cdr_length_limits.items():
        cdr_position_list = ['CDR{0}_P{1}'.format(cdr_number, x) for x in range(1, max(cdr_length_list) + 1)]
        cdr_df_columns.extend(cdr_position_list)
    cdr_count_df = pd.DataFrame(1, columns=cdr_df_columns, index=aa_list)  # psuedo count to avoid log of 0

    # populate dataframe with counts
    for identifer, sequence in id_seq_dict.items():
        cdr_dict, complete_cdrs = parse_cdrs_from_seq(sequence, cdr_length_limits={1: [7], 2: [13], 3: [25]})
        for cdr_number, cdr_sequence in cdr_dict.items():
            for i, amino_acid in enumerate(cdr_sequence):
                cdr_position = 'CDR{0}_P{1}'.format(cdr_number, i + 1)
                if amino_acid is not '-':
                    cdr_count_df.loc[amino_acid, cdr_position] += 1
    # normalize by number of sequences
    cdr_norm_df = cdr_count_df.div(len(id_seq_dict))
    cdr_norm_df.to_csv('{0}_normalized_counts.csv'.format(args.fasta.split('/')[-1].split('.')[0]))
    cdr_pwm_df = cdr_norm_df.applymap(lambda x: np.log2(x))
    cdr_pwm_df.to_csv('{0}_pwm.csv'.format(args.fasta.split('/')[-1].split('.')[0]))
