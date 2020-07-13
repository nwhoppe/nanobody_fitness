#!/usr/bin/env python3

import argparse
import collections
import re
import sys
from encode_one_hot_cdrs_from_fasta import parse_identifier_sequence_from_fasta
from Bio import Seq
from Levenshtein import distance as levenshtein_distance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""script to write protein fasta from sanger sequencing fasta. 
    Extracts sequence based on matching 5' and 3' bases. Calculates hamming distance from expected sequence. 
    Initially made for checking colonies in M1 selections with peptide display library
    """)
    required = parser.add_argument_group('required')
    required.add_argument('-f', '--fasta', required=True, help='input fasta file with nanobody sequences')
    parser.add_argument('-p5', '--prime5', default='CAGATTGGAGGT')
    parser.add_argument('-p3', '--prime3', default='GGTGGATCTGGC')
    parser.add_argument('-e', '--expected_aa_seq', default='DYDKDDD')
    args = parser.parse_args()
    id_seq_dna_dict = parse_identifier_sequence_from_fasta(args.fasta, check_cdrs=False)

    id_seq_aa_dict = {}
    for identifier, dna_read in id_seq_dna_dict.items():
        # only works for reverse dna reads at moment
        dna_read = Seq.reverse_complement(dna_read)
        parsed_dna_seq_list = re.findall(
            r"{0}(.*?){1}".format(args.prime5, args.prime3),
            dna_read,
        )
        if len(parsed_dna_seq_list) > 1:
            sys.stderr.write("Non unique sequence found for {0}\n".format(identifier))
            sys.stderr.write('{0}\n'.format(parsed_dna_seq_list))
        elif len(parsed_dna_seq_list) == 0:
            sys.stderr.write("No match found for {0}\n".format(identifier))
        else:
            dna_seq = parsed_dna_seq_list[0]
            # test if full codons
            if len(dna_seq) % 3 != 0:
                sys.stderr.write("Matched sequence has an incomplete codon\n")
                sys.stderr.write("{0}\n{1}\n".format(identifier, dna_seq))
            else:
                aa_seq = Seq.translate(dna_seq)
                id_seq_aa_dict[identifier] = aa_seq

    aa_seq_counter = collections.Counter(id_seq_aa_dict.values())
    counter = 0
    for aa_seq, count in aa_seq_counter.most_common():
        counter += 1
        l_dist = levenshtein_distance(aa_seq, args.expected_aa_seq)
        sys.stdout.write('>{0}_count{1}_levenshtein{2}\n'.format(counter, count, l_dist))
        sys.stdout.write(aa_seq + '\n')
