#!/usr/bin/env python3

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 3/15/20

import argparse
import itertools
import pandas as pd
import re


def parse_identifier_sequence_from_fasta(fasta_file, check_cdrs=True, cdr_length_limits=None):
    id_seq_dict = {}
    with open(fasta_file, 'r') as f:
        line = f.readline()
        while line:
            if line.startswith('>'):
                identifier = line.strip().split('>')[-1]
                line = f.readline()
                seq = ''
                while line and (line[0].isalpha() or line[0] == '-'):
                    seq += line.strip()
                    line = f.readline()
                if check_cdrs:
                    cdr_dict, complete_cdrs = parse_cdrs_from_seq(seq, cdr_length_limits=cdr_length_limits)
                    if complete_cdrs:
                        id_seq_dict[identifier] = seq
                else:
                    id_seq_dict[identifier] = seq
            else:
                line = f.readline()
    return id_seq_dict


def parse_cdrs_from_seq(sequence_string, cdr_length_limits=None, verbose=True):
    """CDRs are parsed from from a string of amino acids and returned as a dict. a boolean is returned to indicate if
    all three CDRs were present according to length constraints
    """
    # set cdr boundaries
    # TODO: add flexibility for alignments - ie do not hard code dashes
    cdr_boundaries_regex = {1: r"AASG(.*?)MGWY", 2: r"KERE(.*?)YADS", 3: r"YYC(.*?)WGQ"}
    # this dictionary will be used to set dimensions for one-hot matrix
    if not cdr_length_limits:
        cdr_length_limits = {1: [7], 2: range(12, 14), 3: range(10, 23)}
    cdr_dict = {}
    complete_cdr_counter = 0
    for cdr_number in cdr_boundaries_regex.keys():
        found_strings = re.findall(cdr_boundaries_regex[cdr_number], sequence_string)
        if len(found_strings) > 1:
            if verbose:
                print("Non unique sequence found for CDR{0}".format(cdr_number), sequence_string, found_strings, sep='\n')
        elif len(found_strings) == 0:
            if verbose:
                print("No match found for CDR{0}".format(cdr_number), sequence_string, sep='\n')
        else:
            unique_cdr = found_strings[0]
            if len(unique_cdr) in cdr_length_limits[cdr_number]:
                complete_cdr_counter += 1
                cdr_dict[cdr_number] = unique_cdr
            else:
                # cdr is either shorter or longer than expected
                if verbose:
                    print("CDR{0} has length {1}, which is outside the expected range".format(
                        cdr_number, len(unique_cdr)), sequence_string, sep='\n')
    if complete_cdr_counter == 3:
        complete_cdrs = True
    else:
        complete_cdrs = False

    return cdr_dict, complete_cdrs


def encode_one_hot_cdrs_from_seq_dict(identifier_sequence_dict, cdr_length_limits):
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
    cdr_df = pd.DataFrame(0, columns=cdr_df_columns, index=identifier_sequence_dict.keys())
    # cdr_df = pd.DataFrame(0, columns=cdr_df_columns)

    # for observed sequences, assign 1 to value in dataframe - this is large time sink - if used a lot, optimize
    # for d tree, vars could be left categorical - and could skip the one-hot stuff
    for identifier, nanobody_sequence in identifier_sequence_dict.items():
        # should see nothing to stdout from this line - if so, there is a problem
        cdr_dict, complete_cdrs = parse_cdrs_from_seq(nanobody_sequence, cdr_length_limits, verbose=True)
        if complete_cdrs:
            for cdr_number, cdr_seq in cdr_dict.items():
                # get column positions that should be made hot and
                # remove positions that are gaps - they will have no - hot amino acids at that position
                column_ids = [('CDR{0}_P{1}'.format(cdr_number, p + 1), aa) for p, aa in enumerate(cdr_seq) if aa != '-']
                cdr_df.loc[[identifier], column_ids] = 1
        else:
            raise Exception('Sequence did not have all three cdrs\n{0}\n'.format(nanobody_sequence))
    return cdr_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""script to take nanobody sequences from fasta file and create a 
    matrix of one-hot variables describing each CDR position and amino acid""")
    required = parser.add_argument_group('required')
    required.add_argument('-f', '--fasta', required=True, help='fasta file containing nanobody sequences')
    args = parser.parse_args()

    # using aligned sequences so CDRs are all one length
    cdr_length_limits = {1: [7], 2: [13], 3: [25]}
    id_seq_dict = parse_identifier_sequence_from_fasta(args.fasta, check_cdrs=True, cdr_length_limits=cdr_length_limits)

    cdr_df_one_hot = encode_one_hot_cdrs_from_seq_dict(id_seq_dict, cdr_length_limits)
    cdr_df_one_hot.to_csv('{0}_one_hot_encoded_cdrs.csv'.format(args.fasta.split('/')[-1].split('.')[0]))
