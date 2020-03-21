#!/usr/bin/env python3

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 3/17/20

import argparse
from encode_one_hot_cdrs_from_fasta import parse_fasta_to_list, parse_cdrs_from_seq_list
import re


# def parse_cdrs_from_seq_list(sequence_list, cdr_length_limits=None):
#     """CDRs are pulled out of sequences according to regex and length constraints.
#     if all three CDRs are not uniquely present, the sequence is skipped.
#     dictionary with keys 1, 2, 3 and values are lists of cdr sequence strings"""
#
#     # set cdr boundaries
#     cdr_boundaries_regex = {1: r"AASG(.*?)MGWY", 2: r"KERE(.*?)YADS", 3: r"VYY(.*?)WGQG"}
#     # this dictionary will be used to set dimensions for one-hot matrix
#     if not cdr_length_limits:
#         cdr_length_limits = {1: [7], 2: range(8, 15), 3: range(15, 30)}
#     output_cdr_dict = {1: [], 2: [], 3: []}
#
#     for sequence in sequence_list:
#         current_cdr_dict = {}
#         complete_cdr_counter = 0
#         for cdr_number in cdr_boundaries_regex.keys():
#             found_strings = re.findall(cdr_boundaries_regex[cdr_number], sequence)
#             if len(found_strings) == 1:
#                 unique_cdr = found_strings[0]
#                 if len(unique_cdr) in cdr_length_limits[cdr_number]:
#                     complete_cdr_counter += 1
#                     current_cdr_dict[cdr_number] = unique_cdr
#         if complete_cdr_counter == 3:
#             for cdr_number, cdr_seq in current_cdr_dict.items():
#                 output_cdr_dict[cdr_number].append(cdr_seq)
#
#     return output_cdr_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""script to write a fasta file for each CDR from fasta with 
    nanobody sequences""")
    required = parser.add_argument_group('required')
    required.add_argument('-f', '--fasta', required=True, help='input fasta file with nanobody sequences')
    args = parser.parse_args()
    seq_list = parse_fasta_to_list(args.fasta)
    # cdr_list_dict = parse_cdrs_from_seq_list(seq_list)
    #
    # for cdr_number, cdr_seq_list in cdr_list_dict.items():
    #     file_name = '{0}_cdr{1}.fasta'.format(args.fasta.split('/')[-1].split('.')[0], cdr_number)
    #     with open(file_name, 'w') as o:
    #         for i, cdr_seq in enumerate(cdr_seq_list):
    #             o.write('>{0}\n'.format(i))
    #             o.write(cdr_seq)
    #             o.write('\n')

    # THIS GIVES ME DIFFERENT seqs than encode_one_hot script - need to figure out why
    # not obvious
    cdr_dict_list = parse_cdrs_from_seq_list(seq_list)
    file1 = open('{0}_cdr{1}.fasta'.format(args.fasta.split('/')[-1].split('.')[0], 1), 'w')
    file2 = open('{0}_cdr{1}.fasta'.format(args.fasta.split('/')[-1].split('.')[0], 2), 'w')
    file3 = open('{0}_cdr{1}.fasta'.format(args.fasta.split('/')[-1].split('.')[0], 3), 'w')
    file_list = [file1, file2, file3]

    for i, cdr_dict in enumerate(cdr_dict_list):
        for file in file_list:
            file.write('>{0}\n'.format(i))
        for cdr_number, cdr_seq in cdr_dict.items():
            file_list[cdr_number - 1].write('{0}\n'.format(cdr_seq))
    for file in file_list:
        file.close()
