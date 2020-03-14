#!/usr/bin/env python3

import re
import numpy as np
from collections import OrderedDict
import pandas as pd
import colorcet as cc

cmaps = OrderedDict()

# open files with VHH sequences
original_library = open('original_library.fasta')
high_fitness = open('high_fitness.fasta')
low_fitness = open('low_fitness.fasta')

# go through each seq, find CDR1 and append to CDR1 list
CDR1_original_list = []
for line in original_library:
    if re.search(r"KERE.{12}YADS", str(line)):
        CDR1 = re.search(r"KERE.{12}YADS", str(line))
        CDR1_seq = CDR1.group()
        CDR1_original_list.append(CDR1_seq)

CDR1_high_fitness = []
for line in high_fitness:
    if re.search(r"KERE.{12}YADS", str(line)):
        CDR1 = re.search(r"KERE.{12}YADS", str(line))
        CDR1_seq = CDR1.group()
        CDR1_high_fitness.append(CDR1_seq)

CDR1_low_fitness = []
for line in low_fitness:
    if re.search(r"KERE.{12}YADS", str(line)):
        CDR1 = re.search(r"KERE.{12}YADS", str(line))
        CDR1_seq = CDR1.group()
        CDR1_low_fitness.append(CDR1_seq)


# define aa_composition table function, which takes in list of sequences and outputs aa composition table
def aa_composition_function(sequence_list):
    aa_table = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    aa_composition_table = []
    for a in range(0, 20):
        position = str()  # defines a string composed of all amino acids at given position a
        for x in range(0, len(sequence_list)):
            position = position + sequence_list[x][
                a]  # adds each amino acid at a given position into a super long string
        total_position = len(position)
        aa_composition = []
        for aa in aa_table:
            aa_percent = (position.count(str(aa)) / total_position)
            aa_composition.append(aa_percent)
        aa_composition_table.append(aa_composition)
    return aa_composition_table


CDR1_original_frequencies = np.array(aa_composition_function(CDR1_original_list))
CDR1_high_frequencies = np.array(aa_composition_function(CDR1_high_fitness))
CDR1_low_frequencies = np.array(aa_composition_function(CDR1_low_fitness))

high_array = CDR1_high_frequencies / CDR1_original_frequencies
low_array = CDR1_original_frequencies / CDR1_low_frequencies

high_list = np.array(high_array).tolist()
low_list = np.array(low_array).tolist()

print(high_list)

# workup the data to have a dictionary with keys as each amino acid and values as their amino acid compositions
enrichment_high_transposed = map(list, zip(*high_list))  # transposes list; now data for amino acid is a list
enrichment_high_transposed_data = {}
aa_table = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
for index, aa in enumerate(aa_table):
    enrichment_high_transposed_data[aa] = enrichment_high_transposed[index]
# 	

# plot
# x_axis = range(1,21)
# index = pd.Index(x_axis, name='CDR1_position')
# data = enrichment_high_transposed_data
# df = pd.DataFrame(data, index=index)
# ax = df.plot(kind='bar', stacked=True, figsize=(18.5, 10.5), colormap=cc.cm.glasbey)
# ax.set_ylabel('foo')
# plt.show()
# 
#
