#!/usr/bin/env python3

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 3/15/20

import argparse
import itertools
import pandas as pd
import re


def parse_fasta_to_list(input_fasta):
    """each sequence in a fasta file is appended to a list without keeping track of sequence name"""
    sequence_list = []
    with open(input_fasta, 'r') as f:
        for line in f:
            line = line.strip()
            if line and line[0].isalpha():
                sequence_list.append(line)
    return sequence_list


def parse_cdrs_from_seq_list(sequence_list, cdr_length_limits=None):
    """CDRs are pulled out of sequences. if all three CDRs are not uniquely present, the sequence is skipped.
    for each sequence, a dictionary is made. Keys are 1, 2, or 3. Values are amino acid string corresponding to that
    cdr. dictionaries are appended to a list. that list is returned. also, a dictionary of the longest cdr lengths
    is returned"""
    # set cdr boundaries
    cdr_boundaries_regex = {1: r"AASG(.*?)MGWY", 2: r"KERE(.*?)YADS", 3: r"YYC(.*?)WGQ"}
    # this dictionary will be used to set dimensions for one-hot matrix
    if not cdr_length_limits:
        cdr_length_limits = {1: [7], 2: range(8, 15), 3: range(5, 31)}
    cdr_sequence_list = []

    for sequence in sequence_list:
        cdr_dict = {}
        complete_cdr_counter = 0
        for cdr_number in cdr_boundaries_regex.keys():
            found_strings = re.findall(cdr_boundaries_regex[cdr_number], sequence)
            if len(found_strings) > 1:
                print("Non unique sequence found for CDR{0}".format(cdr_number))
                print(sequence)
                print(found_strings)
                print()
            elif len(found_strings) == 0:
                print("No match found for CDR{0}".format(cdr_number))
                print(sequence)
                print()
            else:
                unique_cdr = found_strings[0]
                if len(unique_cdr) in cdr_length_limits[cdr_number]:
                    complete_cdr_counter += 1
                    cdr_dict[cdr_number] = unique_cdr
                else:
                    # cdr is either shorter or longer than expected
                    print("CDR{0} has length {1}, which is outside the expected range".format(
                        cdr_number, len(unique_cdr))
                    )
                    print(sequence)
                    print()
        if complete_cdr_counter == 3:
            cdr_sequence_list.append(cdr_dict)
    print("number of sequences: {0}".format(len(sequence_list)))
    print("number of cdr triplets: {0}".format(len(cdr_sequence_list)))

    return cdr_sequence_list


def encode_one_hot_cdrs_from_list(cdr_dictionary_list, cdr_length_limits):
    """concatenated strings of cdrs are one hot encoded to capture position and amino acid identity
    rows of matrix are individual sequence observations (ie. sequence 1 to N)
    columns are a string containing CDR, position, amino acid"""
    aa_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    cdr_df_columns = []
    #  have cdr number, position, amino acid in column labels of dataframe
    for cdr_number, cdr_length_list in cdr_length_limits.items():
        cdr_max_length = max(cdr_length_list)
        cdr_position_list = ['CDR{0}_P{1}'.format(cdr_number, x) for x in list(range(1, cdr_max_length + 1))]
        cdr_variable_tup_list = list(itertools.product(cdr_position_list, aa_list))
        cdr_df_columns.extend(cdr_variable_tup_list)
    cdr_df = pd.DataFrame(0, columns=cdr_df_columns, index=range(len(cdr_dict_list)))

    # for observed sequences, assign 1 to value in dataframe - this is large time sink - if used a lot, optimize
    # for d tree, vars could be left categorical - and could skip the one-hot stuff
    for seq_index, cdr_dict in enumerate(cdr_dict_list):
        for cdr_number, cdr_seq in cdr_dict.items():
            column_ids = [('CDR{0}_P{1}'.format(cdr_number, p + 1), aa) for p, aa in enumerate(cdr_seq)]
            cdr_df.loc[[seq_index], column_ids] = 1
    return cdr_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""script to take nanobody sequences from fasta file and create a 
    matrix of one-hot variables describing each CDR position and amino acid""")
    required = parser.add_argument_group('required')
    required.add_argument('-f', '--fasta', required=True, help='fasta file containing nanobody sequences')
    args = parser.parse_args()
    seq_list = parse_fasta_to_list(args.fasta)
    cdr_length_limits = {1: [7], 2: range(8, 15), 3: range(5, 31)}
    cdr_dict_list = parse_cdrs_from_seq_list(seq_list, cdr_length_limits)

    cdr_df_one_hot = encode_one_hot_cdrs_from_list(cdr_dict_list, cdr_length_limits)
    cdr_df_one_hot.to_csv('{0}_one_hot_encoded_cdrs.csv'.format(args.fasta.split('/')[-1].split('.')[0]))
