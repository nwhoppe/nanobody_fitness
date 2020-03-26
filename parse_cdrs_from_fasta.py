#!/usr/bin/env python3

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 3/17/20

import argparse
from clean_nanobody_fasta import parse_identifier_sequence_from_fasta
from encode_one_hot_cdrs_from_fasta import parse_cdrs_from_seq


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""script to write a fasta file for each CDR from fasta with 
    nanobody sequences""")
    required = parser.add_argument_group('required')
    required.add_argument('-f', '--fasta', required=True, help='input fasta file with nanobody sequences')
    args = parser.parse_args()
    id_seq_dict = parse_identifier_sequence_from_fasta(args.fasta)
    # using this on an alignment - all CDRs are same length
    cdr_length_limits = {1: [7], 2: [13], 3: [25]}

    file1 = open('{0}_cdr{1}.fasta'.format(args.fasta.split('/')[-1].split('.')[0], 1), 'w')
    file2 = open('{0}_cdr{1}.fasta'.format(args.fasta.split('/')[-1].split('.')[0], 2), 'w')
    file3 = open('{0}_cdr{1}.fasta'.format(args.fasta.split('/')[-1].split('.')[0], 3), 'w')
    file_list = [file1, file2, file3]

    for identifier, sequence in id_seq_dict.items():
        cdr_dict, complete_bool = parse_cdrs_from_seq(sequence, cdr_length_limits=cdr_length_limits)
        # since I did not do any cdr checking this would error out, but I am only running on cleaned, aligned fastas
        for cdr_num, cdr_seq in cdr_dict.items():
            file_list[cdr_num - 1].write('>{0}\n'.format(identifier))
            file_list[cdr_num - 1].write('{0}\n'.format(cdr_seq))

    for file in file_list:
        file.close()
