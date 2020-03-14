#!/usr/bin/env python3

import collections
import re
import numpy as np
import matplotlib.pyplot as plt


# # open files with VHH sequences
# llama_ngs = open('llama_uniques.fasta')
# original_library = open('original_library.fasta')
# high_fitness = open('high_fitness.fasta')
# low_fitness = open('low_fitness.fasta')
#
# # go through each seq, find CDR1 and append to CDR1 list
# CDR3_llamas = []
# for line in llama_ngs:
#     if re.search(r"YYC.{1,24}WGQ", str(line)):
#         CDR3 = re.search(r"YYC.{1,24}WGQ", str(line))
#         CDR3_seq = CDR3.group()
#         CDR3_llamas.append(CDR3_seq)
#
# CDR3_original_list = []
# for line in original_library:
#     if re.search(r"YYC.{1,24}WGQ", str(line)):
#         CDR3 = re.search(r"YYC.{1,24}WGQ", str(line))
#         CDR3_seq = CDR3.group()
#         CDR3_original_list.append(CDR3_seq)
#
# CDR3_high_fitness = []
# for line in high_fitness:
#     if re.search(r"YYC.{1,24}WGQ", str(line)):
#         CDR3 = re.search(r"YYC.{1,24}WGQ", str(line))
#         CDR3_seq = CDR3.group()
#         CDR3_high_fitness.append(CDR3_seq)
#
# CDR3_low_fitness = []
# for line in low_fitness:
#     if re.search(r"YYC.{1,24}WGQ", str(line)):
#         CDR3 = re.search(r"YYC.{1,24}WGQ", str(line))
#         CDR3_seq = CDR3.group()
#         CDR3_low_fitness.append(CDR3_seq)
#
# # make an array of CDR3 lengths for each library
# CDR3_llama_lengths = []
# for sequence in CDR3_llamas:
#     CDR3_llama_lengths.append(len(sequence))
# CDR3_llama_lengths_array = np.array(CDR3_llama_lengths)
#
# CDR3_original_lengths = []
# for sequence in CDR3_original_list:
#     CDR3_original_lengths.append(len(sequence))
# CDR3_original_lengths_array = np.array(CDR3_original_lengths)
#
# CDR3_high_lengths = []
# for sequence in CDR3_high_fitness:
#     CDR3_high_lengths.append(len(sequence))
# CDR3_high_lengths_array = np.array(CDR3_high_lengths)
#
# CDR3_low_lengths = []
# for sequence in CDR3_low_fitness:
#     CDR3_low_lengths.append(len(sequence))
# CDR3_low_lengths_array = np.array(CDR3_low_lengths)
#
# # plot
# nbins = np.arange(7, 30, 1)
#
# plt.hist([CDR3_llama_lengths, CDR3_original_lengths_array, CDR3_high_lengths_array, CDR3_low_lengths_array], alpha=0.5,
#          bins=nbins, normed=True)
#
# plt.title('CDR3 length distribution')
# plt.xlabel('CDR3 size')
# plt.ylabel('count')
# plt.xlim(1, 32)
# plt.legend()
#
# plt.show()


def parse_fasta_to_list(input_fasta):
    sequence_list = []
    with open(input_fasta, 'r') as f:
        for line in f:
            line = line.strip()
            if line and line[0].isalpha():
                sequence_list.append(line)
    return sequence_list


def length_counter_from_regex_search(string_list, regex_constraint):
    length_counter = collections.Counter()
    for query in string_list:
        found_strings = re.findall(regex_constraint, query)
        if len(found_strings) > 1:
            print(found_strings)
            raise (Exception, "Non unique sequence for CDR found")
        elif len(found_strings) == 0:
            print("no match found")
        else:
            length_counter[len(found_strings[0])] += 1
    return length_counter


if __name__ == '__main__':
    # parse input fasta files
    # input_fasta_files = ['llama_uniques.fasta', 'original_library.fasta', 'high_fitness.fasta', 'low_fitness.fasta']
    # input_fasta_files = ['high_fitness.fasta', 'low_fitness.fasta']
    input_fasta_files = ['llama_uniques.fasta', 'original_library.fasta']
    sequence_dicts = {}
    for input_fasta in input_fasta_files:
        key_name = (input_fasta.split('/')[-1]).split('.fasta')[0]
        sequence_list = parse_fasta_to_list(input_fasta)
        sequence_dicts[input_fasta] = sequence_list
    # set cdr boundaries
    cdr_boundaries_regex = {1: r"AASG(.*)MGWY", 2: r"KERE(.*)YADS", 3: r"YYC(.*)WGQ"}

    # what lengths do cdrs have
    for cdr_number in [3]: #cdr_boundaries_regex.keys():
        # get lengths per file
        fig = plt.figure()
        for sequence_list_name, sequence_list in sequence_dicts.items():
            length_counter = length_counter_from_regex_search(sequence_list, cdr_boundaries_regex[cdr_number])
            total_count = float(sum(length_counter.values()))
            for k in length_counter:
                length_counter[k] /= total_count
            plt.bar(length_counter.keys(), length_counter.values(), label=sequence_list_name, alpha=0.4)

        plt.legend()
        plt.savefig('length_histogram_cdr{0}.png'.format(cdr_number), dpi=300, format="png")
        plt.xlim([1,25])
        plt.close()
