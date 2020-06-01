#!/usr/bin/env python

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 3/22/20

import argparse
import sys
from encode_one_hot_cdrs_from_fasta import parse_cdrs_from_seq, parse_identifier_sequence_from_fasta


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""script to ensuring each sequence 
    has all 3 CDRs within a specified length. one sequence per line written to stdout""")
    required = parser.add_argument_group('required')
    required.add_argument('-f', '--fasta', required=True, help="fasta formatted file")
    parser.add_argument('-c', '--check_cdrs', action='store_true')
    parser.add_argument('-n', '--sequence_name', help='string to put after > symbol for each sequence')
    args = parser.parse_args()

    cdr_length_limits = {1: [7], 2: [13], 3: [25]}
    id_seq_dict = parse_identifier_sequence_from_fasta(args.fasta, args.check_cdrs, cdr_length_limits=cdr_length_limits)
    if args.sequence_name:
        base_name = args.sequence_name
    else:
        # base_name = args.fasta.split('/')[-1].split('.')[0] + '_'
        base_name = ''
    for identifier, seq in id_seq_dict.items():
        sys.stdout.write('>{0}{1}\n'.format(base_name, identifier))
        sys.stdout.write('{0}\n'.format(seq))
